#!/usr/bin/env python3
"""List listings whose price can be re-checked online (they have a product page URL).

Usage: python3 tools/to_check.py [--data data.json] [--json]
Prints id, shop, brand, model, current price, last_seen and url, oldest last_seen first.
Brand/category pages (url_note set) are listed separately: they need a search for the product.
"""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument('--data', default='data.json')
ap.add_argument('--json', action='store_true')
a = ap.parse_args()

P = json.load(open(a.data, encoding='utf-8'))['products']
rows = [p for p in P if p.get('url')]
rows.sort(key=lambda p: (p.get('last_seen') or '', p['id']))
direct = [p for p in rows if not p.get('url_note') and '/c/' not in p['url'] and '/manufacturer/' not in p['url']]
search = [p for p in rows if p not in direct]

if a.json:
    pick = lambda p: {k: p.get(k) for k in ('id', 'shop', 'brand', 'model', 'price_after', 'price_before', 'in_stock', 'last_seen', 'url')}
    print(json.dumps({'direct': [pick(p) for p in direct], 'needs_search': [pick(p) for p in search]}, ensure_ascii=False, indent=1))
else:
    for title, L in (('product pages', direct), ('needs search (brand/category page only)', search)):
        print(f'## {title}: {len(L)}')
        for p in L:
            print(f"{p['id']:>4} | {p['shop']:<26} | {p['brand']} {p.get('model') or ''} | {p['price_after']:,} | {p.get('last_seen','-')} | {p['url']}")
