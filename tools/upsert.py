"""Add or update listings while keeping price history.

usage: python3 tools/upsert.py new_items.json [--date YYYY-MM-DD] [--data data.json]

new_items.json = list of listings (same schema as data.json products, no id needed).
Matching (same shop only):
  1. same product URL                                       -> update that listing
  2. same product_key (brand + model number)                -> update that listing
  3. no model number: same brand + category + name          -> update that listing
  otherwise -> new listing.
On update, a history point is appended only when price / old price / stock changed;
last_seen is always refreshed. Hand-entered listings (no "scraped" flag) keep their own
name/specs: a scraped update only changes price, stock and a missing URL.
"""
import sys, argparse, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pricebook import product_key, snapshot, load, save

KEEP = {'id', 'history', 'first_seen'}
TRACK = ('price', 'price_before', 'in_stock')
FILL_IF_MISSING = ('url', 'image', 'loading', 'warranty_years', 'motor_warranty_years', 'motor_type', 'motor_class',
                   'programs', 'dimensions', 'energy_class', 'spec_seen')
PRICE_FIELDS = ('price_after', 'price_before', 'discount_pct', 'in_stock', 'seller')
SUSPECT = 0.5          # a price move bigger than this needs a second sighting (two-strike) before it is believed
MISSED_LIMIT = 2       # consecutive healthy runs without seeing a listing before it is marked out of stock


def find(products, item, key, by_url=None):
    if by_url is not None and item.get('url'):
        p = by_url.get((item['shop'], item['url']))
        if p:
            return p
    for p in products:
        if p['shop'] != item['shop']:
            continue
        if key and p.get('product_key') == key:
            return p
        if not key and not p.get('product_key') and all(
                p.get(f) == item.get(f) for f in ('brand', 'category', 'name')):
            return p
    return None


def _suspicious(old, last, it):
    """True when the new price jumps by more than SUSPECT vs the last known one and this is the first time we see it.
    Guards against scraping glitches (installment price, wrong variant). A second run with the same price confirms it."""
    a, b = last.get('price') or 0, it.get('price_after') or 0
    if not a or not b or abs(b - a) / a <= SUSPECT:
        return False
    return old.get('pending_price') != b


def mark_missing(d, shops, date):
    """Listings of fully-scraped, healthy shops that were not seen in that shop's latest run: after MISSED_LIMIT
    consecutive runs they become out of stock (history point added) instead of staying as a stale 'cheapest'.
    `shops` is a set of shop names (run date = `date`) or {shop: run date}; one run is counted once (missed_on)."""
    ref = shops if isinstance(shops, dict) else {s: date for s in shops}
    n = 0
    for p in d['products']:
        when = ref.get(p['shop'])
        if not when or not p.get('scraped') or p.get('last_seen', when) >= when or p.get('missed_on') == when:
            continue
        p['missed_on'] = when
        p['missed_runs'] = p.get('missed_runs', 0) + 1
        if p['missed_runs'] >= MISSED_LIMIT and p.get('in_stock') is not False:
            p['in_stock'] = False
            last = p['history'][-1]
            p['history'].append({'date': when, 'price': last['price'], 'price_before': last.get('price_before', 0), 'in_stock': False})
            n += 1
    return n


def upsert_items(d, items, date, verbose=True):
    P = d['products']
    nid = max((p['id'] for p in P), default=0)
    by_url = {(p['shop'], p['url']): p for p in P if p.get('url')}
    stats = {'new': 0, 'changed': 0, 'same': 0, 'held': 0, 'changes': []}
    for it in items:
        it.setdefault('price_before', 0); it.setdefault('discount_pct', 0)
        key = product_key(it)
        old = find(P, it, key, by_url)
        snap = snapshot(it, date)
        if old:
            last = old['history'][-1]
            if _suspicious(old, last, it):
                old['pending_price'] = it['price_after']
                old['last_seen'] = date
                old['missed_runs'] = 0
                stats['held'] += 1
                continue
            old.pop('pending_price', None)
            changed = any(last.get(f) != snap.get(f) for f in TRACK if f in snap or f in last)
            curated = it.get('scraped') and not old.get('scraped')
            for k, v in it.items():
                if k in KEEP or v in (None, '', []):
                    continue
                if curated and k not in PRICE_FIELDS and not (k in FILL_IF_MISSING and (not old.get(k) or old.get(k) == 'unknown')):
                    continue
                old[k] = v
            if key and not curated:
                old['product_key'] = key
            if changed:
                old['history'].append(snap)
                stats['changed'] += 1
                stats['changes'].append((old['id'], old['brand'], old.get('model'), old['shop'], last['price'], snap['price']))
                if verbose:
                    print(f"↻ #{old['id']} {old['brand']} {old.get('model','')} @ {old['shop']}: "
                          f"{last['price']:,} → {snap['price']:,}")
            else:
                stats['same'] += 1
            old['last_seen'] = date
            old['missed_runs'] = 0
        else:
            nid += 1
            target = {'id': nid, **it, 'history': [snap], 'first_seen': date, 'last_seen': date}
            if key:
                target['product_key'] = key
            P.append(target)
            if it.get('url'):
                by_url[(it['shop'], it['url'])] = target
            stats['new'] += 1
            if verbose:
                print(f"+ #{nid} {it['brand']} {it.get('model','')} @ {it['shop']}: {snap['price']:,}")
    d['meta']['last_updated'] = max(d['meta']['last_updated'], date)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('items'); ap.add_argument('--data', default='data.json')
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    d, items = load(a.data), load(a.items)
    items = items if isinstance(items, list) else [items]
    upsert_items(d, items, a.date)
    save(d, a.data)


if __name__ == '__main__':
    main()
