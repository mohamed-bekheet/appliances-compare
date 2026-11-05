"""Merge per-store results (from parallel GitHub Actions jobs) into data.json and write scraped/report.md.

usage: python3 tools/scrape/merge.py DIR [DIR ...] [--dry-run] [--date YYYY-MM-DD] [--max-age-days 8]
(results from the laptop run live in scraped/local/ and are merged too while they are fresh)
"""
import argparse, datetime, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from pricebook import load, save          # noqa: E402
from upsert import upsert_items           # noqa: E402
from run import write_report              # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("dirs", nargs="+"); ap.add_argument("--max-age-days", type=int, default=8); ap.add_argument("--data", default="data.json")
ap.add_argument("--date", default=datetime.date.today().isoformat()); ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

import collections
by_date, summary, names = collections.defaultdict(list), {}, []
files = [f for d_ in a.dirs for f in glob.glob(os.path.join(d_, "**", "summary.json"), recursive=True)]
today = datetime.date.fromisoformat(a.date)
for sfile in sorted(files):
    folder = os.path.dirname(sfile)
    s = json.load(open(sfile, encoding="utf-8"))
    when = s.get("_date")
    if when and (today - datetime.date.fromisoformat(when)).days > a.max_age_days:
        print(f"skip stale results {sfile} ({when})")
        continue
    for name, v in s.items():
        if name.startswith("_"):
            continue
        names.append(name); summary[name] = v
        f = os.path.join(folder, f"{name}.json")
        if os.path.exists(f) and "error" not in v:
            by_date[when or a.date] += json.load(open(f, encoding="utf-8"))
print(f"stores: {names}; listings to merge: {sum(map(len, by_date.values()))}")
d = load(a.data)
stats = {"new": 0, "changed": 0, "same": 0, "changes": []}
for when in sorted(by_date):            # each result is stamped with the day it was scraped
    st = upsert_items(d, by_date[when], when, verbose=False)
    for k in stats:
        stats[k] += st[k]
print({k: v for k, v in stats.items() if k != "changes"})
if not a.dry_run:
    save(d, a.data)
    os.makedirs("scraped", exist_ok=True)
    write_report(d, summary, stats, names, a.date, "scraped")
