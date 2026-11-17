"""Scrape health: compare each store's result with its recent history and raise alerts.

history file (scraped/health.json): {store: [{"date":..., "kept":..., "error":...}, ...]} (last 8 runs)
alerts: store failed, or kept < 70% of the median of the previous 4 runs, or it returned 0 listings.
"""
import json, os, statistics

DROP = 0.7


def check(summary, path, date):
    hist = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    alerts = []
    for store, s in summary.items():
        if store.startswith("_"):
            continue
        h = hist.setdefault(store, [])
        if "error" in s:
            alerts.append(f"{store}: scrape failed - {s['error'][:120]}")
            h.append({"date": date, "kept": 0, "error": True})
            continue
        kept = s.get("kept", 0)
        prev = [x["kept"] for x in h if not x.get("error") and x["kept"] > 0][-4:]
        if kept == 0:
            alerts.append(f"{store}: returned 0 listings (selector or site change?)")
        elif prev and kept < DROP * statistics.median(prev):
            alerts.append(f"{store}: {kept} listings vs ~{round(statistics.median(prev))} usually "
                          f"({round(100 * kept / statistics.median(prev))}%) - adapter may be broken")
        if not any(x["date"] == date for x in h):
            h.append({"date": date, "kept": kept})
        else:
            for x in h:
                if x["date"] == date: x["kept"] = kept
        del h[:-8]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    json.dump(hist, open(path, "w", encoding="utf-8"), indent=1)
    return alerts
