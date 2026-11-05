"""One-time: add product_key + history to every listing in data.json."""
import sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pricebook import product_key, snapshot, load, save
path = sys.argv[1] if len(sys.argv) > 1 else 'data.json'
d = load(path); date = d['meta']['last_updated']
for p in d['products']:
    k = product_key(p)
    if k: p['product_key'] = k
    if not p.get('history'):
        p['history'] = [snapshot(p, date)]
    p.setdefault('first_seen', p['history'][0]['date'])
    p.setdefault('last_seen', p['history'][-1]['date'])
save(d, path)
from collections import Counter
c = Counter(p.get('product_key') for p in d['products'] if p.get('product_key'))
print('keyed:', sum(c.values()), '/', len(d['products']), '| multi-shop products:', {k:v for k,v in c.items() if v > 1})
