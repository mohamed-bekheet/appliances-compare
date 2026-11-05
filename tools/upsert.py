"""Add or update listings while keeping price history.

usage: python3 tools/upsert.py new_items.json [--date YYYY-MM-DD] [--data data.json]

new_items.json = list of listings (same schema as data.json products, no id needed).
Matching:
  1. same product_key (brand + model number) AND same shop  -> update that listing
  2. no model number: same shop + brand + category + name    -> update that listing
  otherwise -> new listing.
On update, a history point is appended only when price / old price / stock changed;
last_seen is always refreshed.
"""
import sys, argparse, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pricebook import product_key, snapshot, load, save

KEEP = {'id', 'history', 'first_seen'}
TRACK = ('price', 'price_before', 'in_stock')

def find(products, item, key):
    for p in products:
        if p['shop'] != item['shop']:
            continue
        if key and p.get('product_key') == key:
            return p
        if not key and not p.get('product_key') and all(
                p.get(f) == item.get(f) for f in ('brand', 'category', 'name')):
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('items'); ap.add_argument('--data', default='data.json')
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    d, items = load(a.data), load(a.items)
    items = items if isinstance(items, list) else [items]
    P = d['products']; nid = max(p['id'] for p in P)
    for it in items:
        it.setdefault('price_before', 0); it.setdefault('discount_pct', 0)
        key = product_key(it)
        old = find(P, it, key)
        snap = snapshot(it, a.date)
        if old:
            last = old['history'][-1]
            changed = any(last.get(f) != snap.get(f) for f in TRACK if f in snap or f in last)
            for k, v in it.items():
                if k not in KEEP and v not in (None, '', []):
                    old[k] = v
            if key: old['product_key'] = key
            if changed:
                old['history'].append(snap)
                print(f"↻ #{old['id']} {old['brand']} {old.get('model','')} @ {old['shop']}: "
                      f"{last['price']:,} → {snap['price']:,}")
            else:
                print(f"= #{old['id']} {old['brand']} {old.get('model','')} @ {old['shop']}: no change")
            old['last_seen'] = a.date
            target = old
        else:
            nid += 1
            target = {'id': nid, **it, 'history': [snap], 'first_seen': a.date, 'last_seen': a.date}
            if key: target['product_key'] = key
            P.append(target)
            print(f"+ #{nid} {it['brand']} {it.get('model','')} @ {it['shop']}: {snap['price']:,}")
        if key:
            others = [p for p in P if p.get('product_key') == key and p is not target]
            if others:
                print('   also at: ' + ', '.join(f"{p['shop']} {p['price_after']:,}" for p in others))
    d['meta']['last_updated'] = max(d['meta']['last_updated'], a.date)
    save(d, a.data)

if __name__ == '__main__':
    main()
