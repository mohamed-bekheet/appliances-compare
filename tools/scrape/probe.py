"""Check candidate stores (generic_stores.json) from a machine that can reach them (run it in GitHub Actions).
Writes scraped/probe.md: robots.txt verdict for product paths, sitemap size, JSON-LD on a sample page, Shopify/Woo detection.
usage: python3 tools/scrape/probe.py [--out scraped/probe.md]"""
import argparse, collections, json, os, re, sys
from bs4 import BeautifulSoup
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import Fetcher            # noqa: E402
import generic                        # noqa: E402


def structured_types(h):
    """What a page offers for price extraction: JSON-LD @types, og/product meta price, microdata itemprop price."""
    soup = BeautifulSoup(h, "lxml")
    types = []
    for s_ in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(s_.string or s_.get_text() or "")
        except (ValueError, TypeError):
            continue
        for x in (j if isinstance(j, list) else j.get("@graph", [j])):
            if isinstance(x, dict):
                t = x.get("@type"); types += t if isinstance(t, list) else [str(t)]
    meta = [m.get("property") or m.get("name") for m in soup.find_all("meta") if re.search(r"price|amount|availability", (m.get("property") or m.get("name") or ""), re.I)]
    micro = bool(soup.select('[itemprop="price"]'))
    nd = bool(soup.find("script", id="__NEXT_DATA__"))
    return {"jsonld_types": sorted(set(types)), "price_meta": meta[:4], "microdata_price": micro, "next_data": nd, "title": (soup.title.string or "").strip()[:80] if soup.title else ""}


def probe(f, cfg):
    bases = cfg.get("bases") or [cfg["base"]]
    for b in bases:                                    # first domain that answers
        cfg = {**cfg, "base": b}
        robots = f.get(b + "/robots.txt")
        if robots is not None:
            break
    r = {"key": cfg["key"], "base": cfg["base"], "tried": bases}
    r["robots"] = "reachable" if robots is not None else f"unreachable (HTTP {f.last_status or 'no response'})"
    r["shopify"] = bool(f.get(cfg["base"] + "/products.json?limit=1", as_json=True))
    r["woo"] = bool(f.get(cfg["base"] + "/wp-json/wc/store/v1/products?per_page=1", as_json=True))
    home = f.get(cfg["base"] + "/")
    r["home_status"] = f.last_status
    r["home_title"] = (BeautifulSoup(home, "lxml").title.string or "").strip()[:100] if home and BeautifulSoup(home, "lxml").title else ""
    inc = re.compile(cfg.get("include") or ".")
    urls = generic.sitemap_urls(f, cfg["base"]) if robots is not None else []
    prod = [u for u in urls if inc.search(u) and generic.WANT_URL.search(u)]
    r["sitemap_urls"], r["appliance_product_urls"] = len(urls), len(prod)
    # where the URLs live: first path segment histogram, plus samples
    seg = collections.Counter(re.sub(r"^https?://[^/]+/?([^/?#]*).*$", r"\1", u) or "/" for u in urls)
    r["path_prefixes"] = seg.most_common(8)
    r["sample_urls"] = prod[:5]
    r["pages"] = []
    r["jsonld"], r["sample"] = False, None
    for u in prod[:4]:
        h = f.get(u)
        entry = {"url": u, "status": f.last_status}
        if h:
            entry.update(structured_types(h))
            raw = generic.raw_from_jsonld(h, u, cfg)
            if raw and not r["sample"]:
                r["sample"] = {k: raw[k] for k in ("name", "price", "in_stock", "url")}; r["jsonld"] = True
        r["pages"].append(entry)
    r["verdict"] = ("shopify: set platform=shopify" if r["shopify"] else "woo: set platform=woo_all" if r["woo"] else
                    "jsonld OK: set platform=jsonld, enabled=true" if r["jsonld"] else
                    "blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass" if r["robots"].startswith("unreachable") else
                    "reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible")
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="scraped/probe.md"); a = ap.parse_args()
    f = Fetcher(delay=2.0)
    res = [probe(f, c) for c in generic.load_config()]
    skipped = [c for c in generic.load_config(include_skipped=True) if c.get("skip")]
    L = ["# Store probe", ""]
    for r in res:
        L += [f"## {r['key']} ({r['base']})", f"- domains tried: {r['tried']} -> using {r['base']}", f"- home title: {r.get('home_title') or '-'} (check it is the right shop)", f"- robots.txt: {r['robots']}", f"- Shopify products.json: {r['shopify']} | WooCommerce API: {r['woo']}",
              f"- home page HTTP: {r['home_status']}",
              f"- sitemap URLs: {r['sitemap_urls']} (appliance-looking product URLs: {r['appliance_product_urls']})",
              f"- URL prefixes in sitemap: {r['path_prefixes']}", f"- sample URLs: {r['sample_urls']}",
              *[f"- page {p['url']} -> HTTP {p['status']} {json.dumps({k: v for k, v in p.items() if k not in ('url','status')}, ensure_ascii=False)}" for p in r['pages']],
              f"- JSON-LD sample: {json.dumps(r['sample'], ensure_ascii=False) if r['sample'] else 'none'}", f"- **{r['verdict']}**", ""]
    L += ["## Skipped on purpose", ""] + [f"- {c['shop']}: {c['skip']}" for c in skipped]
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))
