"""Turn a raw store listing into a data.json product (Arabic category, brand, model, capacity, features)."""
import re

# ── categories (Arabic names used by the site's tabs) ────────────────────────
ACCESSORY = re.compile(
    r"\b(cover|stand|base|hose|filter|spare|part|accessor|bracket|cleaner|descal|kit|pipe|valve|"
    r"remote|tray|shelf|rack|knob|gasket|seal|bag|cable|adapter|protector|stabili[sz]er)\b|"
    r"غطاء|قاعدة|خرطوم|فلتر|قطع غيار|منظف|حامل|مثبت|كابل|واقي", re.I)
CATS = [  # (category, regex) — order matters
    ("غسالة أطباق", r"dish\s?washer|غسالة (?:ال)?[أا]طباق|غسالات (?:ال)?[أا]طباق"),
    ("سخان",        r"water[\s-]?heater|gas[\s-]heater|electric[\s-]heater|instant[\s-]water|سخان"),
    ("مايكروويف",   r"micro\s?wave|مايكرو?ويف|ميكرو?ويف"),
    ("غسالة",       r"washer[\s&-]*dryer|washer[\s-]dryer|combo|غسالة.{0,25}مجفف|washing machine|"
                    r"\bwasher\b|front[\s-]?load|top[\s-]?load|twin tub|غسال[ةه]|غسالات"),
    ("مجفف",        r"(?<!hair )\b(?:tumble )?dryer\b|مجفف(?! شعر)|نشافة"),
    ("ديب فريزر",   r"deep[\s-]?freezer|chest[\s-]?freezer|upright[\s-]?freezer|ديب ?فريزر|فريزر رأسي|فريزر أفقي"),
    ("ثلاجة",       r"refrigerat|refrigrator|fridge|ثلاج[ةه]|ثلاجات|mini\s?-?bar|ميني ?بار|\bfreezer\b"),
    ("شفاط",        r"\bhood\b|chimney|cooker hood|شفاط"),
    ("مسطح كهرباء", r"(?:induction|ceramic|electric|vitro)[\w\s-]{0,12}(?:hob|cook\s?top)|مسطح (?:كهرب|سيراميك|انداكشن)"),
    ("مسطح غاز",    r"\bhob\b|cook\s?top|built[\s-]?in gas|مسطح"),
    ("بوتاجاز",     r"cooker|\brange\b|gas stove|بوتاجاز|بوتجاز|موقد"),
    ("فرن",         r"\boven\b|فرن"),
]
CATS = [(c, re.compile(r, re.I)) for c, r in CATS]


def guess_category(*texts):
    t = " ".join(x for x in texts if x)
    for cat, rx in CATS:
        if rx.search(t):
            return cat
    return None


# ── brands ────────────────────────────────────────────────────────────────────
BRANDS = {
    "lg": "LG", "zanussi": "Zanussi", "toshiba": "Toshiba", "samsung": "Samsung", "sharp": "Sharp",
    "fresh": "Fresh", "beko": "Beko", "hoover": "Hoover", "unionaire": "Unionaire", "kiriazi": "Kiriazi",
    "white point": "White Point", "whitepoint": "White Point", "white whale": "White Whale",
    "midea": "Midea", "haier": "Haier", "bosch": "Bosch", "ariston": "Ariston", "indesit": "Indesit",
    "tornado": "Tornado", "gorenje": "Gorenje", "candy": "Candy", "alaska": "Alaska", "w.alaska": "Alaska",
    "ideal": "Ideal", "hisense": "Hisense", "hitachi": "Hitachi", "panasonic": "Panasonic",
    "whirlpool": "Whirlpool", "electrolux": "Electrolux", "siemens": "Siemens", "miele": "Miele",
    "electrostar": "Electrostar", "passap": "Passap", "kenwood": "Kenwood", "purity": "Purity",
    "premium": "Premium", "la germania": "La Germania", "teka": "Teka", "elba": "Elba",
    "glem gas": "Glem Gas", "glemgas": "Glem Gas", "techno gas": "Techno Gas", "universal": "Universal",
    "olympic electric": "Olympic Electric", "olympic": "Olympic Electric", "black & decker": "Black & Decker",
    "tefal": "Tefal", "moulinex": "Moulinex", "castle": "Castle", "ocean": "Ocean", "armadillo": "Armadillo",
    "siltal": "Siltal", "penguin": "Penguin", "hamburg": "Hamburg", "pluto": "Pluto", "jac": "Jac",
    "argosta": "Argosta", "sonai": "Sonai", "prifix": "Prifix", "daewoo": "Daewoo", "caloriphere": "Caloriphere",
    "deluxe": "Deluxe", "fagor": "Fagor", "smeg": "Smeg", "franke": "Franke", "cata": "Cata",
    "zahran": "Zahran", "hans": "Hans", "simfer": "Simfer", "ecomatic": "Ecomatic",
    "kitchen line": "Kitchen Line", "valerio": "Valerio", "folger": "Folger", "ata": "ATA", "carrier": "Carrier", "mienta": "Mienta", "kumtel": "Kumtel", "aftron": "Aftron", "media": "Midea",
}
AR_BRANDS = {
    "زانوسي": "Zanussi", "توشيبا": "Toshiba", "ال جي": "LG", "إل جي": "LG", "سامسونج": "Samsung",
    "شارب": "Sharp", "فريش": "Fresh", "بيكو": "Beko", "هوفر": "Hoover", "يونيون اير": "Unionaire",
    "كريازي": "Kiriazi", "وايت بوينت": "White Point", "وايت ويل": "White Whale", "ميديا": "Midea",
    "هاير": "Haier", "بوش": "Bosch", "اريستون": "Ariston", "أريستون": "Ariston", "اندست": "Indesit",
    "تورنيدو": "Tornado", "جورينيه": "Gorenje", "كاندي": "Candy", "الاسكا": "Alaska", "ايديال": "Ideal",
    "هايسنس": "Hisense", "هيتاشي": "Hitachi", "ويرلبول": "Whirlpool", "يونيفرسال": "Universal",
    "جليم جاز": "Glem Gas", "لاجرمانيا": "La Germania", "تكنو جاز": "Techno Gas", "هانز": "Hans",
    "بيورتي": "Purity", "كومتيل": "Kumtel", "إلبا": "Elba", "ألبا": "Elba", "البا": "Elba", "جورينيا": "Gorenje",
    "تيكا": "Teka", "تيڤا": "Teka", "سيمفر": "Simfer", "أوشن": "Ocean", "اوشن": "Ocean", "إيكوماتيك": "Ecomatic",
    "ايكوماتيك": "Ecomatic", "كيتشن لاين": "Kitchen Line", "فيماش": "Fimash", "فاليريو": "Valerio",
    "منيجيتي": "Minigetti", "فولجر": "Folger", "إل جى": "LG", "ال جى": "LG", "يونيون إير": "Unionaire",
    "اونيون اير": "Unionaire", "سامسونح": "Samsung", "فريش ": "Fresh", "تورنادو": "Tornado", "شارب ": "Sharp",
    "بيكو ": "Beko", "كاريير": "Carrier", "اليكتروستار": "Electrostar", "إليكتروستار": "Electrostar",
}
NOT_BRANDS = {"generic", "no brand", "other", "others", "unbranded", ""}


def canon_brand(b):
    if not b:
        return None
    k = re.sub(r"\s+", " ", b.strip().lower().replace("‏", ""))
    if k in NOT_BRANDS:
        return None
    if k in BRANDS:
        return BRANDS[k]
    if b.strip() in AR_BRANDS:
        return AR_BRANDS[b.strip()]
    return b.strip().title() if (b.isupper() or b.islower()) else b.strip()


def brand_from(text, hint=None):
    b = canon_brand(hint)
    if b:
        return b
    low = " " + (text or "").lower() + " "
    for k, v in sorted(BRANDS.items(), key=lambda kv: -len(kv[0])):
        if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", low):
            return v
    for k, v in AR_BRANDS.items():
        if k in (text or ""):
            return v
    return None


# ── model numbers ─────────────────────────────────────────────────────────────
UNIT = re.compile(r"^\d+(?:[.,]\d+)?(?:KG|KGS|RPM|L|LT|LTR|LITERS?|LITRES?|CM|MM|W|KW|FT|FEET|HP|K|GB|TB|INCH|V|H|MIN|PCS?|X\d+)?$")
NOT_MODEL = {"WI-FI", "WIFI", "MP3", "A+++", "TC2", "T21", "T15", "T25", "T06", "K-PRO", "X7", "AI"}


def extract_model(*texts):
    cands = []
    for t in texts:
        if not t:
            continue
        m = re.search(r"(?:model(?: number| no\.?)?\s*[:\-]|موديل\s*[:\-]?)\s*([A-Za-z0-9][A-Za-z0-9\-/.()]+)", t, re.I)
        if m:
            return m.group(1).upper().strip(".-/")
        cands += re.findall(r"[A-Za-z0-9][A-Za-z0-9\-/.()]{2,}[A-Za-z0-9)]", t)
    good = []
    for c in cands:
        u = c.upper().strip(".-/(")
        if u.count("(") != u.count(")"):
            u = u.split("(")[0]
        letters, digits = re.sub(r"[^A-Z]", "", u), re.sub(r"[^0-9]", "", u)
        if not letters or not digits or u in NOT_MODEL:
            continue
        if UNIT.match(u) or re.match(r"^\d+(?:[.,]\d+)?(?:KG|RPM|L|CM|W|LITER)", u):
            continue
        if len(letters + digits) < 5 or re.match(r"^\d{4,}$", u):
            continue
        good.append(u)
    return good[-1] if good else None


import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pricebook import model_key  # noqa: E402  (shared with upsert so all listings group the same way)


# ── capacities & features ────────────────────────────────────────────────────
def num(x):
    x = x.replace(",", ".")
    f = float(x)
    return int(f) if f == int(f) else f


def capacities(text, cat):
    t = (text or "").translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    out = {}
    if cat in ("غسالة", "مجفف"):
        m = re.search(r"(\d{1,2}(?:[.,]\d)?)(?:\s*/\s*\d{1,2})?\s*(?:kg|kgs|كجم|كيلو|ك\.?ج)", t, re.I)
        if m and 2 <= float(m.group(1).replace(",", ".")) <= 30:
            out["capacity_kg"] = num(m.group(1))
    if cat in ("ثلاجة", "ديب فريزر", "سخان", "فرن", "مايكروويف"):
        m = re.search(r"(\d{2,4})\s*(?:liters?|litres?|ltrs?|lt\b|l\b|لتر)", t, re.I)
        if m:
            out["capacity_liters"] = int(m.group(1))
        elif cat in ("ثلاجة", "ديب فريزر"):
            m = re.search(r"(\d{1,2})\s*(?:ft|feet|قدم)", t, re.I)
            if m:
                out["capacity_feet"] = int(m.group(1))
    if cat in ("بوتاجاز", "مسطح غاز", "مسطح كهرباء", "شفاط", "فرن"):
        m = re.search(r"(\d{2,3})\s*(?:cm|سم|سنتي)", t, re.I)
        if m and 30 <= int(m.group(1)) <= 120:
            out["width_cm"] = int(m.group(1))
        m = re.search(r"(\d)\s*(?:burners?|عيون|عين|شعلات|شعلة)", t, re.I)
        if m:
            out["burners"] = int(m.group(1))
    m = re.search(r"(\d{3,4})\s*(?:rpm|لفة|دورة)", t, re.I)
    if m and cat in ("غسالة",):
        out["spin_rpm"] = int(m.group(1))
    return out


FEATS = [
    ("انفرتر", r"inverter|انفرتر|إنفرتر|عاكس"),
    ("Front Load", r"front[\s-]?load|أمامي|امامي|front loader"),
    ("Top Load", r"top[\s-]?load|علوي|تحميل علوي"),
    ("نصف أوتوماتيك", r"half[\s-]?auto|semi[\s-]?auto|twin[\s-]?tub|نصف"),
    ("غسالة مجفف", r"washer[\s&-]*dryer|combo|مع مجفف|بمجفف"),
    ("بخار", r"steam|بخار"),
    ("Wi-Fi", r"wi-?fi|smart|thinq|واي فاي"),
    ("نوفروست", r"no[\s-]?frost|نو ?فروست|نوفروست"),
    ("ديفروست", r"(?<!no )(?<!no-)\bdefrost|ديفروست"),
    ("فريزر سفلي", r"bottom[\s-]?freezer|combi"),
    ("سايد باي سايد", r"side[\s-]?by[\s-]?side"),
    ("ميني بار", r"mini\s?-?bar|ميني ?بار"),
    ("بلت إن", r"built[\s-]?in|بلت ?ان|مدمج"),
    ("أمان كامل", r"full safety|أمان كامل|امان كامل"),
    ("مروحة", r"\bfan\b|turbo|مروحة"),
]
FEATS = [(f, re.compile(r, re.I)) for f, r in FEATS]


def build(raw):
    """raw: name, price, old, url, shop, source, in_stock, brand_hint, cat_hint, model_hint, extra.
    Returns a data.json product dict or None (with reason in raw['_skip'])."""
    name = re.sub(r"\s+", " ", raw.get("name") or "").strip()
    text = " ".join(x for x in (name, raw.get("extra") or "") if x)
    price = int(raw.get("price") or 0)
    if not name or price <= 0:
        raw["_skip"] = "no name/price"; return None
    if ACCESSORY.search(name) and not re.search(r"washing machine|refrigerator|cooker|oven", name, re.I):
        raw["_skip"] = "accessory"; return None
    cat = guess_category(raw.get("cat_hint"), name) if raw.get("cat_hint") else guess_category(name)
    if raw.get("cat_hint") and not cat:
        cat = guess_category(name)
    if not cat:
        raw["_skip"] = "not an appliance"; return None
    brand = brand_from(name, raw.get("brand_hint"))
    if not brand:
        raw["_skip"] = "no brand"; return None
    model = (raw.get("model_hint") or "").strip().upper() or extract_model(name, raw.get("extra"))
    if model and not re.search(r"\d", model):
        model = extract_model(name, raw.get("extra"))
    old = int(raw.get("old") or 0)
    p = {
        "name": name, "brand": brand, "category": cat, "model": model,
        "price_after": price, "price_before": old if old > price else 0,
        "discount_pct": round((old - price) * 100 / old) if old > price else 0,
        "shop": raw["shop"], "source": raw["source"], "url": raw.get("url"),
        "in_stock": bool(raw.get("in_stock", True)),
        "features": [f for f, rx in FEATS if rx.search(text)],
        "scraped": True,
    }
    if raw.get("seller"):
        p["seller"] = raw["seller"]
    p.update(capacities(text, cat))
    if "انفرتر" in p["features"]:
        p["motor_class"] = "inverter"
    elif cat == "غسالة":
        p["motor_class"] = "unknown"
    k = model_key(brand, model)
    if k:
        p["product_key"] = k
    return p
