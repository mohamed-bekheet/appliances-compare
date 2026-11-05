"""Scrape Egyptian appliance stores and merge prices into data.json (keeps price history).

usage:
  python3 tools/scrape/run.py                       # all stores
  python3 tools/scrape/run.py --stores btech,jumia  # some stores
  python3 tools/scrape/run.py --limit 20 --dry-run  # quick test, don't touch data.json

Writes scraped/<store>.json (normalised listings) and scraped/report.md (summary + cheapest shop per model).
"""
import argparse, collections, datetime, json, logging, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from common import Fetcher                      # noqa: E402
from normalize import build                      # noqa: E402
from stores import STORES                        # noqa: E402
from pricebook import load, save                 # noqa: E402
from upsert import upsert_items                  # noqa: E402

log = logging.getLogger("scrape")


def dedupe(items):
    """One listing per shop+model (colour variants): keep the cheapest in-stock one."""
    best = {}
    for p in items:
        k = (p["shop"], p.get("product_key") or p.get("url") or p["name"])
        cur = best.get(k)
        rank = (not p["in_stock"], p["price_after"])
        if cur is None or rank < (not cur["in_stock"], cur["price_after"]):
            best[k] = p
    return list(best.values())


def cheapest_table(products, date):
    groups = collections.defaultdict(list)
    for p in products:
        if p.get("product_key") and p.get("price_after") and p.get("in_stock", True) and p.get("last_seen") == date:
            groups[p["product_key"]].append(p)
    rows = []
    for k, g in groups.items():
        shops = {x["shop"] for x in g}
        if len(shops) < 2:
            continue
        g.sort(key=lambda x: x["price_after"])
        rows.append((g[-1]["price_after"] - g[0]["price_after"], g))
    rows.sort(key=lambda r: -r[0])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stores", default="all")
    ap.add_argument("--data", default="data.json")
    ap.add_argument("--out", default="scraped")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--limit", type=int, default=0, help="max listings per store (testing)")
    ap.add_argument("--delay", type=float, default=2.0, help="seconds between requests to the same site")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    names = list(STORES) if a.stores == "all" else [s.strip() for s in a.stores.split(",")]
    d = load(a.data)
    ctx = {"known_urls": [p["url"] for p in d["products"] if p.get("url")], "limit": a.limit}
    f = Fetcher(delay=a.delay)
    os.makedirs(a.out, exist_ok=True)
    summary, all_items = {}, []
    for name in names:
        t0 = time.time()
        try:
            raws = STORES[name](f, ctx)
        except Exception as e:                       # one broken store must not stop the others
            log.exception("%s failed", name)
            summary[name] = {"error": repr(e)[:300]}
            continue
        built, skips = [], collections.Counter()
        for r in raws:
            p = build(r)
            if p:
                built.append(p)
            else:
                skips[r.get("_skip", "?")] += 1
        built = dedupe(built)
        json.dump(built, open(os.path.join(a.out, f"{name}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        cats = collections.Counter(p["category"] for p in built)
        summary[name] = {"raw": len(raws), "kept": len(built), "skipped": dict(skips),
                         "with_model": sum(1 for p in built if p.get("product_key")),
                         "categories": dict(cats), "minutes": round((time.time() - t0) / 60, 1)}
        log.info("%s: %s", name, summary[name])
        all_items += built

    summary["_http"] = f.stats
    summary["_date"] = a.date
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return
    stats = upsert_items(d, all_items, a.date, verbose=False)
    save(d, a.data)
    write_report(d, summary, stats, names, a.date, a.out)


def write_report(d, summary, stats, names, date, out):
    summary["_upsert"] = {k: v for k, v in stats.items() if k != "changes"}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = [f"# Scrape report {date}", "", "| store | listings | kept | with model | minutes | note |",
         "|---|---|---|---|---|---|"]
    for n in names:
        s = summary.get(n, {})
        L.append(f"| {n} | {s.get('raw','-')} | {s.get('kept','-')} | {s.get('with_model','-')} | {s.get('minutes','-')} | "
                 f"{s.get('error','')} |")
    L += ["", f"New listings: {stats['new']}, price changes: {stats['changed']}, unchanged: {stats['same']}", "",
          "## Price changes", ""]
    for i, b, m, shop, old, new in sorted([c for c in stats["changes"] if c[4] != c[5]], key=lambda c: c[5] - c[4])[:80]:
        L.append(f"- {b} {m or ''} @ {shop}: {old:,} → {new:,} ({new - old:+,})")
    L += ["", "## Same model, different shops (biggest gaps)", ""]
    for gap, g in cheapest_table(d["products"], date)[:60]:
        L.append(f"- **{g[0]['brand']} {g[0].get('model','')}** ({g[0]['category']}): cheapest {g[0]['shop']} "
                 f"{g[0]['price_after']:,} — " + ", ".join(f"{x['shop']} {x['price_after']:,}" for x in g[1:]) +
                 f" (save {gap:,})")
    open(os.path.join(out, "report.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    main()
