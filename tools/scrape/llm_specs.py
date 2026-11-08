"""Optional LLM fallback for spec extraction. Used only when ANTHROPIC_API_KEY is set (GitHub secret) and the
regex extractor (normalize.specs_from_text) found little in a description. The model may only copy facts that the text
states; every value is validated here, and regex results always win."""
import json, logging, os, re, urllib.request

log = logging.getLogger("scrape")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")
MAX_CALLS = int(os.environ.get("LLM_MAX_CALLS", "300"))
_calls = 0

PROMPT = """You extract appliance specs from an Egyptian store product description (Arabic and/or English).
Return ONLY a JSON object with exactly these keys. Use null for anything the text does not explicitly state - never guess,
never use outside knowledge.
- warranty_years: integer, the general product warranty in years
- motor_warranty_years: integer, motor or compressor warranty in years
- motor_type: short string (e.g. "Direct Drive Inverter", "Inverter", "Universal") exactly as the text implies
- programs: integer number of wash/cooking programs
- dimensions: "WxHxD cm" style string
- energy_class: e.g. "A+++", "A", "B"
- loading: "front" or "top" (washing machines only)
- made_in: country name in Arabic if stated
- drum_material: string if stated
Category: {cat}
Product: {name}
Description:
{desc}"""


def enabled():
    return bool(os.environ.get("ANTHROPIC_API_KEY")) and _calls < MAX_CALLS


def _clean(j, cat):
    out = {}
    def num(k, lo, hi):
        v = j.get(k)
        if isinstance(v, (int, float)) and lo <= v <= hi:
            out[k] = int(v)
    num("warranty_years", 1, 15); num("motor_warranty_years", 1, 20); num("programs", 2, 60)
    d = j.get("dimensions")
    if isinstance(d, str) and re.search(r"\d+\s*[x×]\s*\d+", d):
        out["dimensions"] = re.sub(r"\s*[x×]\s*", "x", d.strip())[:40]
    e = j.get("energy_class")
    if isinstance(e, str) and re.fullmatch(r"A\+{0,3}|[B-G]", e.strip().upper()):
        out["energy_class"] = e.strip().upper()
    if cat in ("غسالة", "مجفف"):
        mt = j.get("motor_type")
        if isinstance(mt, str) and 2 < len(mt) < 40:
            out["motor_type"] = mt.strip()
            out["motor_class"] = "dd" if re.search(r"direct|دفع", mt, re.I) else "inverter" if re.search(r"inverter|انفرتر", mt, re.I) else "universal" if re.search(r"universal|عادي", mt, re.I) else None
            if not out["motor_class"]:
                del out["motor_class"]
    if cat == "غسالة" and j.get("loading") in ("front", "top"):
        out["loading"] = "أمامي" if j["loading"] == "front" else "علوي"
    for k in ("made_in", "drum_material"):
        v = j.get(k)
        if isinstance(v, str) and 1 < len(v) < 40:
            out[k] = v.strip()
    return out


def ask(name, cat, desc):
    """Return validated spec fields or {}. Never raises."""
    global _calls
    if not enabled() or not desc or len(desc) < 40:
        return {}
    _calls += 1
    try:
        body = json.dumps({"model": MODEL, "max_tokens": 400,
                           "messages": [{"role": "user", "content": PROMPT.format(cat=cat, name=name, desc=desc[:6000])}]}).encode()
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", body, {
            "content-type": "application/json", "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"})
        txt = json.load(urllib.request.urlopen(req, timeout=60))["content"][0]["text"]
        m = re.search(r"\{.*\}", txt, re.S)
        return _clean(json.loads(m.group(0)), cat) if m else {}
    except Exception as e:     # a failed call just means "no extra info"
        log.warning("llm specs failed: %s", repr(e)[:150])
        return {}
