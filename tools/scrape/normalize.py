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
    ("مجفف",        r"(?<!hair )\b(?:tumble )?dryer\b|مجفف(?!\s*(?:ال)?شعر)|نشافة"),
    ("ديب فريزر",   r"deep[\s-]?freezer|chest[\s-]?freezer|upright[\s-]?freezer|ديب ?فريزر|فريزر رأسي|فريزر أفقي"),
    ("ثلاجة",       r"refrigerat|refrigrator|fridge|ثلاج[ةه]|ثلاجات|mini\s?-?bar|ميني ?بار|\bfreezer\b"),
    ("شفاط",        r"\bhood\b|chimney|cooker hood|شفاط"),
    ("مسطح كهرباء", r"hot\s?plate|flat cooker|electric (?:stove|cooker)|موقد كهربائي|بوتاجاز كهربائي|سخان طهي|(?:induction|ceramic|electric|vitro)[\w\s-]{0,12}(?:hob|cook\s?top)|مسطح (?:كهرب|سيراميك|انداكشن)"),
    ("مسطح غاز",    r"\bhob\b|cook\s?top|built[\s-]?in gas|مسطح"),
    ("بوتاجاز",     r"cooker|\brange\b|gas stove|بوتاجاز|بوتجاز|موقد"),
    ("فرن",         r"\boven\b|فرن"),
]
CATS = [(c, re.compile(r, re.I)) for c, r in CATS]


# not home appliances even though they share words with them
NOT_APPLIANCE = re.compile(r"hair\s?dryer|مجفف\s*(?:ال)?شعر|سشوار|exhaust fan|ventilat|شفاط (?:هواء|حمام)|للحمام|للجبسيون|"
                           r"clothes dryer rack|foldable clothes|منشر", re.I)
# lowest believable price per category (EGP); below that it's an accessory, a spare part or a broken price
MIN_PRICE = {"غسالة": 1000, "ثلاجة": 2500, "ديب فريزر": 3000, "غسالة أطباق": 3000, "مجفف": 2000, "بوتاجاز": 1500,
             "باكدج": 3000}


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
    ("نصف أوتوماتيك", r"ES-T[A-Z0-9]|half[\s-]?auto|semi[\s-]?auto|twin[\s-]?tub|نصف"),
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



# ── washer loading type: "أمامي" (front) / "علوي" (top) ───────────────────────
_FRONT = re.compile(r"front[\s-]?load|فرونت|أمامي|امامي|امامى|أمامى|washer[\s&-]*dryer|combo|\d\s*(?:kg\s*)?dryer|\bFL\b|ES-F[A-Z0-9]|TWV-?FN|مجفف \d|BWD\d|غسالة مجفف|مع مجفف|بمجفف|بالمجفف|\bWD\d", re.I)
_TOP = re.compile(r"top[\s-]?load|توب ?لود|علوي|علوى|فوق ?(?:ال)?(?:اتوماتيك|أتوماتيك|أوتوماتيك|اوتوماتيك)|2 ?موتور|حلة عصر|half[\s-]?auto|semi[\s-]?auto|twin[\s-]?tub|نصف ?اتوماتيك|نصف ?أوتوماتيك|single[\s-]?tub|double[\s-]?tub|تانك واحد|حوض", re.I)
# model-code families whose loading type is fixed by the maker's naming scheme
_MODEL_RULES = [
    (r"^WW\d", "front"), (r"^WA\d", "top"), (r"^WD\d", "front"),             # Samsung
    (r"^F\d|^FH|^FV|^FC", "front"), (r"^T\d|^TD\d", "top"),                      # LG (F4V.., T2108..)
    (r"^ZWF|^ZWD|^ZWY", "front"), (r"^ZWT", "top"), (r"^EWF|^EWW", "front"), (r"^EWT", "top"),  # Zanussi / Electrolux
    (r"^TWD|^TWF|^TWL|^TW-?BL", "front"), (r"^TW-?B[JK]|^AW-?[JKU]|^AW-?DJ", "top"),       # Toshiba
    (r"^B\d?WF|^WTE|^WUE|^WMB|^WMY|^B3WF|^B5WF", "front"),                      # Beko
    (r"^HW\d{3}-?B|^HWD|^HW\d{2,3}-?BP|^HW\d{2,3}-?B\d", "front"), (r"^HWT|^HWM", "top"),  # Haier
    (r"^FWD|^FWM|^FFB|^FFT|^FF\d", "front"),                                      # Whirlpool/Fresh-like
    (r"^WG[A-Z]\d|^WA[NJTU]\d|^WU[ZQ]?\d|^WM\d|^WL[GK]", "front"),            # Bosch / Siemens (no top-loaders sold)
    (r"^NL[MS]|^NM\d|^NS\d|^AQ\d|^RPD|^RSG", "front"), (r"^H[3-9]W", "front"),   # Ariston / Hoover
    (r"^MFN|^MF\d{2,3}[A-Z]|^MFK", "front"), (r"^MA\d|^MAS", "top"),            # Midea
    (r"^BWD|^WFS|^WTX|^WTV|^WCV|^WDV|^WY", "front"),                            # Beko
    (r"^GVS|^CS\d|^CSS|^CO\d", "front"),                                         # Candy
]


def loading_type(name, model="", features=(), category="غسالة"):
    """Return 'أمامي' / 'علوي' / None for a washer. None = could not tell (never guess)."""
    if category != "غسالة":
        return None
    t = " ".join([name or "", " ".join(features or [])])
    f, tp = bool(_FRONT.search(t)), bool(_TOP.search(t))
    if f and not tp:
        return "أمامي"
    if tp and not f:
        return "علوي"
    if f and tp:   # e.g. "washer dryer" next to a stray "حوض" — dryers combos are always front
        return "أمامي" if re.search(r"dryer|combo|مجفف", t, re.I) else None
    if re.search(r"مجفف ملابس|(?<!washer )\b(?:tumble )?dryer\b|^\s*مجفف", name or "", re.I) and not re.search(r"غسالة|washing|washer", name or "", re.I):
        return None   # a drier that landed in the washer tab
    cands = [re.sub(r"[^A-Z0-9-]", "", (model or "").upper())]
    cands += [re.sub(r"[^A-Z0-9-]", "", w.upper()) for w in re.findall(r"[A-Za-z][A-Za-z0-9/-]{4,}", name or "")]
    for m in cands:
        for rx, kind in _MODEL_RULES:
            if m and re.search(rx, m):
                return "أمامي" if kind == "front" else "علوي"
    return None


# ── specs written in free text (B.TECH "Key: Value" descriptions, Woo descriptions, Arabic titles) ──
_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
_YR = r"(?:years?|yrs?|سنين|سنوات|سنه|سنة)"


def specs_from_text(desc, cat=None):
    """Pull warranty / motor / programs / dimensions / energy class out of a product description.
    Only fields that are actually written there are returned; nothing is guessed."""
    t = re.sub(r"<[^>]+>", " ", desc or "").translate(_AR_DIGITS)
    t = re.sub(r"&nbsp;|\s+", " ", t)
    if not t.strip():
        return {}
    out = {}
    m = re.search(r"(\d{1,2})\s*" + _YR + r"[^.;|\d]{0,25}?(?:on|for)\s+(?:the\s+)?(?:compressor|motor)", t, re.I) \
        or re.search(r"(?:motor|compressor|الموتور|موتور|الكومبريسور|كمبروسر)[^.;|\d]{0,30}?(\d{1,2})\s*" + _YR, t, re.I) \
        or re.search(r"(\d{1,2})\s*" + _YR + r"\s*(?:على|ضمان)\s*(?:ال)?(?:موتور|كومبريسور|كمبروسر)", t, re.I)
    if m:
        out["motor_warranty_years"] = int(m.group(1))
    # general warranty = first "N years" next to the word warranty that is not the motor/compressor one
    for m in re.finditer(r"(?:warranty|ضمان)[^0-9.;|]{0,12}(\d{1,2})\s*" + _YR + r"|(\d{1,2})\s*" + _YR + r"\s*(?:warranty|ضمان)", t, re.I):
        n = int(m.group(1) or m.group(2))
        if re.search(r"motor|compressor|موتور|كومبر|كمبر", t[max(0, m.start() - 14):m.end()], re.I):
            continue   # that number is the motor/compressor warranty
        if 1 <= n <= 15:
            out["warranty_years"] = n
            break
    m = re.search(r"(?:number of programs|programs|عدد البرامج)\s*[:：-]?\s*(\d{1,2})\b|\b(\d{1,2})\s*(?:programs|برنامج)", t, re.I)
    if m:
        n = int(m.group(1) or m.group(2))
        if 2 <= n <= 60:
            out["programs"] = n
    m = re.search(r"(?:dimensions?|الأبعاد|الابعاد)[^0-9]{0,25}(\d{2,3}(?:\.\d)?\s*[x×*]\s*\d{2,3}(?:\.\d)?(?:\s*[x×*]\s*\d{2,3}(?:\.\d)?)?)\s*(cm|سم|mm|مم)?", t, re.I)
    if m:
        out["dimensions"] = re.sub(r"\s*[x×*]\s*", "x", m.group(1)) + (" " + ("cm" if (m.group(2) or "cm").lower() in ("cm", "سم") else "mm"))
    m = re.search(r"energy\s*(?:class|rating|efficiency)\s*[:：-]?\s*(A\+{0,3}|[B-E])(?![\w+])|فئة الطاقة\s*[:：-]?\s*(A\+{0,3})", t, re.I)
    if m:
        out["energy_class"] = (m.group(1) or m.group(2)).upper()
    if cat in ("غسالة", "مجفف", None):
        if re.search(r"direct[\s-]?drive|دفع مباشر|DD\s*motor", t, re.I):
            out["motor_type"] = "Direct Drive Inverter" if re.search(r"inverter|انفرتر", t, re.I) else "Direct Drive"
            out["motor_class"] = "dd"
        elif re.search(r"inverter[\s-]*(?:motor|drive)|(?:motor|محرك|موتور)[^.;|]{0,15}inverter|انفرتر", t, re.I):
            out["motor_type"] = "Inverter"
            out["motor_class"] = "inverter"
    return out


BUNDLE = re.compile(
    r"\b(?:with|and|\+)\b[\w\s,-]{0,60}?\b(?:hood|oven|hob|cooker|microwave|air[\s-]?fryer|fryer|mini[\s-]?bar|dishwasher|"
    r"refrigerator|fridge|freezer|washing machine|kettle|blender|iron|vacuum|tv|screen)\b|"
    r"\bbundle\b|\bpackage\b|\bcombo set\b|\s\+\s|باكدج|باقة|عرض \d|مع (?:شفاط|فرن|مسطح|ثلاجة|ميكرويف|مايكروويف|قلاية)", re.I)


def is_bundle(name, url=""):
    slug = (url or "").rstrip("/").rsplit("/", 1)[-1].replace("-", " ")
    t = name + " " + slug
    return bool(BUNDLE.search(t)) and not re.search(r"washer[\s&-]*dryer|with dryer|مع مجفف|بمجفف|with grill|بالشواية|with fan", t, re.I) \
        or bool(re.search(r"\s\+\s|باكدج|bundle|package", t, re.I))


def build(raw):
    """raw: name, price, old, url, shop, source, in_stock, brand_hint, cat_hint, model_hint, extra.
    Returns a data.json product dict or None (with reason in raw['_skip'])."""
    name = re.sub(r"\s+", " ", raw.get("name") or "").strip()
    text = " ".join(x for x in (name, raw.get("extra") or "") if x)
    price = int(raw.get("price") or 0)
    if not name or price <= 0:
        raw["_skip"] = "no name/price"; return None
    if NOT_APPLIANCE.search(name):
        raw["_skip"] = "not an appliance"; return None
    if ACCESSORY.search(name) and (not re.search(r"washing machine|refrigerator|cooker|oven", name, re.I)
                                   or re.search(r"\bfor\b|compatible|متوافق|\bلـ", name, re.I)):
        raw["_skip"] = "accessory"; return None
    cat = guess_category(raw.get("cat_hint"), name) if raw.get("cat_hint") else guess_category(name)
    if raw.get("cat_hint") and not cat:
        cat = guess_category(name)
    if not cat:
        raw["_skip"] = "not an appliance"; return None
    bundle = is_bundle(name, raw.get("url"))
    if bundle:
        cat = "باكدج"
    if price < MIN_PRICE.get(cat, 250):
        raw["_skip"] = "implausible price"; return None
    brand = brand_from(name, raw.get("brand_hint"))
    if not brand:
        raw["_skip"] = "no brand"; return None
    title_model = extract_model(name, raw.get("extra"))
    hint = (raw.get("model_hint") or "").strip().upper()
    # a store-supplied model (SKU / "Model Number") is trusted only if the title has no model of its own
    # or the two agree; B.TECH sometimes carries another product's model in the description
    model = title_model if (title_model and hint and model_key(brand, hint) != model_key(brand, title_model)
                             and raw.get("source") == "btech.com") else (hint or title_model)
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
    if raw.get("image"):
        p["image"] = raw["image"]
    if raw.get("seller"):
        p["seller"] = raw["seller"]
    p.update(capacities(text, cat))
    sp = specs_from_text(raw.get("desc"), cat)
    for k, v in sp.items():
        if k in ("motor_class", "motor_type") and cat not in ("غسالة", "مجفف"):
            continue
        p[k] = v
    if cat == "غسالة" and raw.get("desc"):
        mt = re.search(r"loading\s*type\s*[:：-]?\s*(front|top)", raw["desc"], re.I)
        if mt:
            p["loading"] = "أمامي" if mt.group(1).lower() == "front" else "علوي"
    if p.get("motor_class"):
        pass   # already read from the description (e.g. direct drive)
    elif "انفرتر" in p["features"]:
        p["motor_class"] = "inverter"
    elif cat == "غسالة":
        p["motor_class"] = "unknown"
    if cat == "غسالة":
        lt = loading_type(name, model, p["features"], cat)
        if lt:
            p["loading"] = lt
    k = None if bundle else model_key(brand, model)
    if k:
        p["product_key"] = k
    return p
