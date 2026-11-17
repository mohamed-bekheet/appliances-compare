"""Derived price signals + data-quality report, computed from data.json (never invents data).

signals(p) is stored in data.json only when something is worth showing (keeps the file small):
  low   True when the current price equals the lowest in-stock price in our history AND history has >=3 distinct dates
  vs    (price - market median) / market median * 100, where the median is over the same product in the OTHER shops
        (needs >=2 other shops)
  med   that market median
  inf   True when price_before is >30% above the market median and the advertised discount is >=10%
"""
import collections, datetime, statistics


def _days(a, b):
    return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days


def compute_signals(products):
    by_key = collections.defaultdict(list)
    for p in products:
        if p.get("product_key") and p.get("price_after", 0) > 0 and p.get("in_stock", True):
            by_key[(p["product_key"], p["category"])].append(p)
    n = 0
    for p in products:
        h = [x for x in p.get("history", []) if x.get("price", 0) > 0 and x.get("in_stock", True)]
        s = {}
        if h:
            dates = {x["date"] for x in h}
            if len(dates) >= 3 and p.get("price_after") == min(x["price"] for x in h) and any(x["price"] > p["price_after"] for x in h):
                s["low"] = True
        grp = by_key.get((p.get("product_key"), p["category"]), [])
        others = {}
        for o in grp:
            if o["shop"] != p["shop"]:
                others[o["shop"]] = min(others.get(o["shop"], 10**12), o["price_after"])
        if len(others) >= 2 and p.get("price_after", 0) > 0:
            med = statistics.median(others.values())
            s["med"] = round(med)
            s["vs"] = round((p["price_after"] - med) / med * 100, 1)
            if p.get("price_before", 0) > 1.3 * med and p.get("discount_pct", 0) >= 10:
                s["inf"] = True
        if s:
            p["signals"] = s
            n += 1
        else:
            p.pop("signals", None)
    return n


def quality_report(products, today=None):
    latest = max((p.get("last_seen", "") for p in products), default="")
    today = today or latest
    per = collections.defaultdict(lambda: collections.Counter())
    outliers = []
    med = {}
    g = collections.defaultdict(list)
    for p in products:
        if p.get("product_key") and p.get("price_after", 0) > 0:
            g[(p["product_key"], p["category"])].append(p["price_after"])
    for k, v in g.items():
        if len(v) >= 3:
            med[k] = statistics.median(v)
    for p in products:
        c = per[p["shop"]]
        c["listings"] += 1
        if not p.get("image"): c["no_image"] += 1
        if not p.get("url"): c["no_url"] += 1
        if not (p.get("warranty_years") or p.get("energy_class") or p.get("dimensions")): c["no_specs"] += 1
        if not p.get("product_key"): c["no_model"] += 1
        if p.get("last_seen") and today and _days(p["last_seen"], today) > 14: c["stale_14d"] += 1
        m = med.get((p.get("product_key"), p["category"]))
        if m and p.get("price_after", 0) > 0 and (p["price_after"] < 0.4 * m or p["price_after"] > 2.5 * m):
            c["price_outlier"] += 1
            outliers.append({"id": p["id"], "shop": p["shop"], "name": p["name"][:80], "price": p["price_after"], "median": round(m)})
    return {"date": today, "total": len(products), "per_shop": {k: dict(v) for k, v in sorted(per.items())},
            "outliers": sorted(outliers, key=lambda o: -abs(o["price"] / o["median"] - 1))[:100]}
