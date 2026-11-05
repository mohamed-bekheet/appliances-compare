"""Merge per-store results (from parallel GitHub Actions jobs) into data.json and write scraped/report.md.

usage: python3 tools/scrape/merge.py artifacts_dir [--dry-run] [--date YYYY-MM-DD]
"""
import argparse, datetime, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from pricebook import load, save          # noqa: E402
from upsert import upsert_items           # noqa: E402
from run import write_report              # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("artifacts"); ap.add_argument("--data", default="data.json")
ap.add_argument("--date", default=datetime.date.today().isoformat()); ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

items, summary, names = [], {}, []
for sfile in sorted(glob.glob(os.path.join(a.artifacts, "**", "summary.json"), recursive=True)):
    folder = os.path.dirname(sfile)
    s = json.load(open(sfile, encoding="utf-8"))
    for name, v in s.items():
        if name.startswith("_"):
            continue
        names.append(name); summary[name] = v
        f = os.path.join(folder, f"{name}.json")
        if os.path.exists(f) and "error" not in v:
            items += json.load(open(f, encoding="utf-8"))
print(f"stores: {names}; listings to merge: {len(items)}")
d = load(a.data)
stats = upsert_items(d, items, a.date, verbose=False)
print({k: v for k, v in stats.items() if k != "changes"})
if not a.dry_run:
    save(d, a.data)
    os.makedirs("scraped", exist_ok=True)
    write_report(d, summary, stats, names, a.date, "scraped")
