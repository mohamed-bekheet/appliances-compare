"""Shared helpers for price history (used by migrate + upsert)."""
import re, json

REAL_MODEL = re.compile(r'^[A-Z0-9][A-Z0-9\-/(). ]*$')

# Market/region suffixes that do not change the product itself (the same fridge sold as RS70F65QAT and
# RS70F65QATMR). Colour letters (S/W/B/BK...) are NOT here: those are different SKUs, only suggested in match.py.
REGION_TAILS = {'SAMSUNG': ('MR', 'AS'), 'BEKO': ('EGB',), 'TOSHIBA': ('EGMK',)}


def model_key(brand, model):
    """Same key = same product in any shop. Drops colour codes in brackets and EGY/ELA/EG region tails."""
    if not brand or not model:
        return None
    m = model.upper()
    m = re.sub(r"\([^)]*\)\s*$", "", m)
    m = re.sub(r"[\s\-]*(EGY|ELA|EG)$", "", m) if len(m) > 8 else m
    m = re.sub(r"[^A-Z0-9]", "", m)
    for t in REGION_TAILS.get((brand or '').upper().replace(' ', ''), ()):
        if m.endswith(t) and len(m) - len(t) >= 6:
            m = m[:-len(t)]
            break
    if len(m) < 4 or not re.search(r"\d", m) or not re.search(r"[A-Z]", m):
        return None
    return brand.upper().replace(" ", "") + ":" + m


def product_key(p):
    """Same key = same product regardless of shop. Explicit product_key wins."""
    if p.get('product_key'):
        return p['product_key']
    m = (p.get('model') or '').strip()
    if not m or not REAL_MODEL.match(m.upper()):
        return None
    return model_key(p['brand'], m)

def snapshot(p, date):
    return {"date": date, "price": p.get('price_after', 0),
            "price_before": p.get('price_before', 0),
            **({"in_stock": p['in_stock']} if 'in_stock' in p else {})}

def load(path):  return json.load(open(path, encoding='utf-8'))
def save(d, path): json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
