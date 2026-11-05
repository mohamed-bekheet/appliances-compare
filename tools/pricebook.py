"""Shared helpers for price history (used by migrate + upsert)."""
import re, json

REAL_MODEL = re.compile(r'^[A-Z0-9][A-Z0-9\-/().]*$')

def product_key(p):
    """Same key = same product regardless of shop. Explicit product_key wins."""
    if p.get('product_key'):
        return p['product_key']
    m = (p.get('model') or '').strip()
    if not m or not REAL_MODEL.match(m) or not re.search(r'\d', m):
        return None                      # no reliable model number -> not grouped
    norm = re.sub(r'[\s\-/().]', '', m.upper())
    return f"{p['brand'].upper().replace(' ', '')}:{norm}"

def snapshot(p, date):
    return {"date": date, "price": p.get('price_after', 0),
            "price_before": p.get('price_before', 0),
            **({"in_stock": p['in_stock']} if 'in_stock' in p else {})}

def load(path):  return json.load(open(path, encoding='utf-8'))
def save(d, path): json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
