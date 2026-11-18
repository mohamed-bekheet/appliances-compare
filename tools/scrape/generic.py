"""Config-driven adapters so a new store is one JSON entry (generic_stores.json) instead of new code.

platforms
  shopify : /products.json (same as Al Reyada)
  jsonld  : sitemap(s) -> product URLs (config "include" regex + appliance keywords in the URL) -> each page's JSON-LD Product
Only stores with "enabled": true are registered in STORES. A store becomes enabled after tools/scrape/probe.py shows that
robots.txt allows the paths and the pages carry usable data. Everything goes through the polite Fetcher (robots.txt, delay).
"""
import json, logging, os, re
from bs4 import BeautifulSoup
from common import to_num

log = logging.getLogger("scrape")
HERE = os.path.dirname(os.path.abspath(__file__))
WANT_URL = re.compile(r"wash|laundry|refrig|fridge|freez|cook|oven|microw|hood|hob|dish|heater|dryer|built-in|range|stove|"
                      r"غسال|ثلاج|بوتاجاز|فرن|مايكروويف|شفاط|سخان|فريزر|ديب", re.I)


def load_config(path=None):
    return json.load(open(path or os.path.join(HERE, "generic_stores.json"), encoding="utf-8"))


def sitemap_urls(f, base, limit_maps=30):
    """All <loc> URLs from the sitemaps listed in robots.txt (or /sitemap.xml), following sitemap indexes."""
    robots = f.get(base + "/robots.txt") or ""
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots) or [base + "/sitemap.xml"]
    urls, seen = [], set()
    while maps and len(seen) < limit_maps:
        m = maps.pop(0)
        if m in seen:
            continue
        seen.add(m)
        x = f.get(m)
        if not x:
            continue
        locs = re.findall(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)", x)
        for u in locs:
            (maps if re.search(r"\.xml(\.gz)?$|sitemap", u, re.I) and "<sitemapindex" in x else urls).append(u)
    return urls


def _ld_product(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    best, crumbs = None, []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(s.string or s.get_text() or "")
        except (ValueError, TypeError):
            continue
        for x in (j if isinstance(j, list) else j.get("@graph", [j])):
            if not isinstance(x, dict):
                continue
            t = x.get("@type")
            t = t if isinstance(t, list) else [t]
            if "Product" in t and best is None:
                best = x
            if "BreadcrumbList" in t:
                crumbs = [str((i.get("item") or {}).get("name") if isinstance(i.get("item"), dict) else i.get("name") or "")
                          for i in x.get("itemListElement", []) if isinstance(i, dict)]
    return best, crumbs


def raw_from_jsonld(html_text, url, cfg):
    p, crumbs = _ld_product(html_text)
    if not p:
        return None
    offers = p.get("offers")
    offers = offers if isinstance(offers, list) else [offers] if isinstance(offers, dict) else []
    prices = []
    for o in offers:
        price = to_num(o.get("price") or o.get("lowPrice"))
        if price:
            prices.append((price, str(o.get("availability", "")).lower().endswith("instock")))
    if not prices:
        return None
    price, in_stock = min(prices, key=lambda t: (not t[1], t[0]))
    brand = p.get("brand")
    brand = brand.get("name") if isinstance(brand, dict) else brand
    img = p.get("image")
    img = img[0] if isinstance(img, list) and img else img
    img = img.get("url") if isinstance(img, dict) else img
    return dict(name=str(p.get("name") or "").strip(), price=price, old=0, url=url, in_stock=in_stock, shop=cfg["shop"],
                source=cfg["base"].split("//")[1], brand_hint=brand if isinstance(brand, str) else None,
                cat_hint=" ".join(crumbs) + " " + url, model_hint=p.get("mpn") or p.get("sku"), extra=None,
                desc=BeautifulSoup(str(p.get("description") or ""), "lxml").get_text("\n", strip=True),
                image=img if isinstance(img, str) and img.startswith("http") else None)


def jsonld_adapter(f, ctx, cfg):
    inc = re.compile(cfg.get("include") or ".")
    urls = [u for u in sitemap_urls(f, cfg["base"]) if inc.search(u) and WANT_URL.search(u)]
    cap = ctx.get("limit") or cfg.get("max_pages", 1500)
    out = []
    for u in urls[:cap]:
        h = f.get(u)
        r = raw_from_jsonld(h, u, cfg) if h else None
        if r and r["name"]:
            out.append(r)
    log.info("%s: %d product URLs in sitemap, %d listings", cfg["key"], len(urls), len(out))
    return out


def shopify_adapter(f, ctx, cfg):
    out = []
    for page in range(1, 40):
        j = f.get(f"{cfg['base']}/products.json?limit=250&page={page}", as_json=True)
        if not j or not j.get("products"):
            break
        for p in j["products"]:
            v = (p.get("variants") or [{}])[0]
            out.append(dict(name=p.get("title"), price=to_num(v.get("price")), old=to_num(v.get("compare_at_price")),
                            url=f"{cfg['base']}/products/{p.get('handle')}", in_stock=bool(v.get("available")), shop=cfg["shop"],
                            source=cfg["base"].split("//")[1], brand_hint=p.get("vendor"),
                            cat_hint=(p.get("product_type") or "") + " " + " ".join(p.get("tags") or []), model_hint=None, extra=None,
                            desc=BeautifulSoup(p.get("body_html") or "", "lxml").get_text("\n", strip=True),
                            image=((p.get("images") or [{}])[0].get("src") or "") or None))
        if ctx.get("limit") and len(out) >= ctx["limit"]:
            break
    return out[: ctx["limit"]] if ctx.get("limit") else out


ADAPTERS = {"jsonld": jsonld_adapter, "shopify": shopify_adapter}


def register(stores):
    for cfg in load_config():
        if cfg.get("enabled") and cfg["platform"] in ADAPTERS:
            stores[cfg["key"]] = (lambda c: lambda f, ctx: ADAPTERS[c["platform"]](f, ctx, c))(cfg)
