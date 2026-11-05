"""One-off: recompute product_key for every listing with the shared model_key(), and drop colour
duplicates that the 2026-11-05 bulk import created at the same shop (keeps hand-entered ones)."""
import collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pricebook import REAL_MODEL, model_key, load, save

d = load("data.json")
P = d["products"]
for p in P:
    p.pop("product_key", None)
    m = (p.get("model") or "").strip().upper()
    k = model_key(p["brand"], m) if m and REAL_MODEL.match(m) else None
    if k:
        p["product_key"] = k
groups = collections.defaultdict(list)
for p in P:
    if p.get("product_key"):
        groups[(p["shop"], p["product_key"])].append(p)
drop = set()
for g in groups.values():
    if len(g) < 2:
        continue
    curated = [x for x in g if x["id"] <= 120]
    keep = curated[0] if curated else min(g, key=lambda x: (x.get("in_stock") is False, x["price_after"]))
    for x in g:
        if x is not keep and x["id"] > 120 and len(x.get("history", [])) <= 2:
            drop.add(x["id"])
d["products"] = [p for p in P if p["id"] not in drop]
save(d, "data.json")
print(f"keys: {sum(1 for p in d['products'] if p.get('product_key'))}, dropped duplicates: {len(drop)}, "
      f"listings now: {len(d['products'])}")
