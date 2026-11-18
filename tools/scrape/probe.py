"""Check candidate stores (generic_stores.json) from a machine that can reach them (run it in GitHub Actions).
Writes scraped/probe.md: robots.txt verdict for product paths, sitemap size, JSON-LD on a sample page, Shopify/Woo detection.
usage: python3 tools/scrape/probe.py [--out scraped/probe.md]"""
import argparse, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import Fetcher            # noqa: E402
import generic                        # noqa: E402


def probe(f, cfg):
    r = {"key": cfg["key"], "base": cfg["base"]}
    robots = f.get(cfg["base"] + "/robots.txt")
    r["robots"] = "reachable" if robots is not None else "unreachable/blocked"
    r["shopify"] = bool(f.get(cfg["base"] + "/products.json?limit=1", as_json=True))
    r["woo"] = bool(f.get(cfg["base"] + "/wp-json/wc/store/v1/products?per_page=1", as_json=True))
    inc = re.compile(cfg.get("include") or ".")
    urls = generic.sitemap_urls(f, cfg["base"]) if robots is not None else []
    prod = [u for u in urls if inc.search(u) and generic.WANT_URL.search(u)]
    r["sitemap_urls"], r["appliance_product_urls"] = len(urls), len(prod)
    r["sample"] = None
    for u in prod[:3]:
        h = f.get(u)
        raw = generic.raw_from_jsonld(h, u, cfg) if h else None
        if raw:
            r["sample"] = {k: raw[k] for k in ("name", "price", "in_stock", "url")}
            r["jsonld"] = True
            break
    r.setdefault("jsonld", False)
    r["verdict"] = ("shopify: use platform=shopify" if r["shopify"] else "woo: use the existing woo adapter" if r["woo"] else
                    "jsonld OK: set enabled=true" if r["jsonld"] else "no usable data found: needs a custom adapter or skip")
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="scraped/probe.md"); a = ap.parse_args()
    f = Fetcher(delay=2.0)
    res = [probe(f, c) for c in generic.load_config()]
    L = ["# Store probe", ""]
    for r in res:
        L += [f"## {r['key']} ({r['base']})", f"- robots.txt: {r['robots']}", f"- Shopify products.json: {r['shopify']} | WooCommerce API: {r['woo']}",
              f"- sitemap URLs: {r['sitemap_urls']} (appliance-looking product URLs: {r['appliance_product_urls']})",
              f"- JSON-LD sample: {json.dumps(r['sample'], ensure_ascii=False) if r['sample'] else 'none'}", f"- **{r['verdict']}**", ""]
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))
