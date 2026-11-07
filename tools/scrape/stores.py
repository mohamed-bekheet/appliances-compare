"""One function per store. Each returns raw listings: dict(name, price, old, url, in_stock, shop, source,
brand_hint, cat_hint, model_hint, extra, seller). Only public pages/feeds that robots.txt allows are used."""
import re, json, html, logging
from bs4 import BeautifulSoup
from common import to_num

log = logging.getLogger("scrape")
WANT = re.compile(r"wash|laundry|refrig|fridge|freez|cook|oven|microw|hood|hob|dish|heater|dryer|built-in|"
                  r"range|stove", re.I)


def _enough(items, ctx):
    return bool(ctx.get("limit")) and len(items) >= ctx["limit"]


def _cap(items, ctx):
    return items[: ctx["limit"]] if ctx.get("limit") else items


def _img(el):
    """First real image URL in a tile/page element (handles lazy-loading attributes)."""
    if el is None:
        return None
    for im in ([el] if el.name == "img" else el.select("img")):
        for a in ("data-src", "data-lazysrc", "data-original", "data-lazy-src", "src"):
            u = im.get(a) or ""
            if u.startswith("http") and not re.search(r"placeholder|loader|blank|\.svg|data:image", u, re.I):
                return u
    return None


def _ld_image(prod):
    im = prod.get("image")
    if isinstance(im, list):
        im = im[0] if im else None
    if isinstance(im, dict):
        im = im.get("url") or im.get("contentUrl")
    return im if isinstance(im, str) and im.startswith("http") else None


def _ld_blocks(soup):
    out = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(s.string or s.get_text() or "")
        except (ValueError, TypeError):
            continue
        for x in (j if isinstance(j, list) else j.get("@graph", [j])):
            if isinstance(x, dict):
                out.append(x)
    return out


# ── B.TECH: category pages (server-rendered, 20 per sort) + product-page JSON-LD ─────────────
def btech(f, ctx):
    B = "https://btech.com"
    seen_c, queue, slugs = set(), ["/en/c/large-home-appliances"], set()
    while queue and len(seen_c) < 60:
        c = queue.pop(0)
        if c in seen_c:
            continue
        seen_c.add(c)
        for sort in ("", "?sort=price_asc", "?sort=price_desc"):
            h = f.get(B + c + sort)
            if not h:
                continue
            slugs |= set(re.findall(r"/en/p/([a-z0-9\-]+)", h))
            if not sort:
                for sub in set(re.findall(r'href="(/en/c/large-home-appliances/[a-z0-9\-/]+)"', h)):
                    if sub not in seen_c and WANT.search(sub):
                        queue.append(sub)
    found = len(slugs)
    slugs |= {u.split("/en/p/")[1].split("?")[0] for u in ctx["known_urls"] if "btech.com/en/p/" in u}
    log.info("btech: %d category pages, %d products from listings, %d incl. known URLs", len(seen_c), found, len(slugs))
    out = []
    for slug in _cap(sorted(slugs), ctx):
        url = f"{B}/en/p/{slug}"
        h = f.get(url)
        if not h:
            continue
        soup = BeautifulSoup(h, "lxml")
        lds = _ld_blocks(soup)
        prod = next((x for x in lds if x.get("@type") == "Product"), None)
        if not prod:
            continue
        crumbs = next((x for x in lds if x.get("@type") == "BreadcrumbList"), {})
        cat = " ".join(i.get("name", "") for i in crumbs.get("itemListElement", [])[1:-1])
        off = prod.get("offers") or {}
        off = off[0] if isinstance(off, list) else off
        desc = prod.get("description") or ""
        mm = re.search(r"Model Number:\s*([^\n]+)", desc)
        out.append(dict(name=prod.get("name"), price=to_num(off.get("price")), old=0, url=url,
                        in_stock="InStock" in str(off.get("availability", "InStock")),
                        shop="B.TECH", source="btech.com", brand_hint=(prod.get("brand") or {}).get("name"),
                        cat_hint=cat, model_hint=mm.group(1).strip() if mm else None, extra=None,
                        image=_ld_image(prod)))
    return out


ELARABY_CATS = ["washing-machines", "tumble-dryer", "refrigerators", "deep-freezer", "freestanding-cookers",
                "built-in-hobs-cookers", "built-in-ovens", "cookers-hoods", "dishwashers", "water-heaters"]


# ── El Araby: sitemap (listed in robots.txt) + product pages (Magento meta tags) ──────────────
def elaraby(f, ctx):
    B = "https://www.elarabygroup.com"
    urls = []
    for smu in ("/pub/media/sitemap/en.xml", "/media/sitemap/en.xml", "/sitemap.xml"):
        sm = f.get(B + smu) or ""
        urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", sm) if "/en/" in u and not u.endswith(".xml")]
        if urls:
            break
    if not urls:   # fallback: first page of each category (robots.txt disallows ?p= paging)
        for c in ELARABY_CATS:
            h = f.get(f"{B}/en/electric-home-appliances/large-home-appliances/{c}")
            if h:
                urls += [a["href"] for a in BeautifulSoup(h, "lxml").select("a.product-item-link")]
        urls = list(dict.fromkeys(urls))
        log.info("elaraby: sitemap unavailable, %d products from category first pages", len(urls))
    kw = re.compile(r"washing-machine|washer|refrigerator|fridge|freezer|cooker|oven|microwave|hood|-hob|"
                    r"dishwasher|water-heater|heater|dryer|mini-bar|stove", re.I)
    urls = [u for u in urls if kw.search(u.rsplit("/", 1)[-1])]
    log.info("elaraby: %d appliance URLs in sitemap", len(urls))
    out = []
    for url in _cap(urls, ctx):
        h = f.get(url)
        if not h:
            continue
        soup = BeautifulSoup(h, "lxml")
        meta = lambda p: (soup.find("meta", property=p) or {}).get("content")
        price = to_num(meta("product:price:amount"))
        if not price:
            continue
        t = soup.select_one("h1 .base") or soup.find("h1")
        old = soup.select_one('[data-price-type="oldPrice"]')
        prod = next((x for x in _ld_blocks(soup) if x.get("@type") == "Product"), {})
        name = t.get_text(" ", strip=True) if t else prod.get("name")
        out.append(dict(name=name, price=price, old=to_num(old.get("data-price-amount")) if old else 0, url=url,
                        in_stock="out" not in (meta("product:availability") or "in stock").lower(),
                        shop="El Araby", source="elarabygroup.com", brand_hint=(name or "").split(" ")[0],
                        cat_hint=None, model_hint=prod.get("sku"), extra=None,
                        image=meta("og:image") or _ld_image(prod)))
    return out


def magento_prices(it):
    """(final, old) from a Magento product tile: data-price-amount if present, else the visible price text."""
    fp = it.select_one('[data-price-type="finalPrice"]')
    op = it.select_one('[data-price-type="oldPrice"]')
    if fp and fp.get("data-price-amount"):
        return to_num(fp.get("data-price-amount")), to_num(op.get("data-price-amount")) if op else 0
    box = it.select_one(".price-box")
    if not box:
        return 0, 0
    sp = box.select_one(".special-price .price") or box.select_one(".price")
    ol = box.select_one(".old-price .price")
    return to_num(sp.get_text() if sp else 0), to_num(ol.get_text()) if ol else 0


# ── Zanussi Egypt (official store, Magento; robots.txt is empty) ──────────────────────────────
ZANUSSI_CATS = ["laundry/washing-machines", "laundry/washer-dryers", "laundry/dryers", "cooking/range-cookers",
                "cooking/built-in-gas-hobs", "cooking/ovens", "cooking/microwaves", "cooking/hoods",
                "cooling/fridge-and-freezers", "heating/water-heaters", "dish-washers/freestanding-dishwashers",
                "dish-washers/built-in-dishwashers"]


def zanussi(f, ctx):
    B, listing = "https://www.zanussi.com.eg/en/", {}
    for c in ZANUSSI_CATS:
        for page in range(1, 15):
            h = f.get(f"{B}{c}.html" + (f"?p={page}" if page > 1 else ""))
            if not h:
                break
            soup, new = BeautifulSoup(h, "lxml"), 0
            for it in soup.select(".product-item"):
                a = it.select_one("a.product-item-link")
                price, old = magento_prices(it)
                if not a or not price or a["href"] in listing:
                    continue
                listing[a["href"]] = dict(name=a.get_text(" ", strip=True), price=price, old=old, cat_hint=c, image=_img(it),
                                          in_stock=not it.select_one(".stock.unavailable"))
                new += 1
            if not new:
                break
    log.info("zanussi: %d products in listings", len(listing))
    out = []
    for url, d in _cap(list(listing.items()), ctx):
        h = f.get(url)
        sku = None
        if h:
            s = BeautifulSoup(h, "lxml").select_one('.product.attribute.sku .value, [itemprop="sku"]')
            sku = s.get_text(strip=True) if s else None
        out.append(dict(d, url=url, shop="Zanussi Official", source="zanussi.com.eg", brand_hint="Zanussi",
                        model_hint=sku, extra=None))
    return out


# ── Jumia (robots.txt allows identified bots < 200 req/min; Arabic listing pages) ────────────
JUMIA_CATS = ["washers-dryers-washers", "appliances-fridges-freezers", "freezers", "cooking-appliances",
              "small-appliances-microwave", "range-hoods", "dishwashers", "water-heaters"]


def jumia(f, ctx):
    B, out, seen = "https://www.jumia.com.eg", [], set()
    for c in JUMIA_CATS:
        last = 1
        page = 1
        while page <= min(last, 40):
            if _enough(out, ctx):
                return _cap(out, ctx)
            h = f.get(f"{B}/ar/{c}/" + (f"?page={page}" if page > 1 else ""))
            if not h:
                break
            soup = BeautifulSoup(h, "lxml")
            if page == 1:
                nums = [int(m) for m in re.findall(r"\?page=(\d+)", " ".join(a.get("href", "") for a in soup.select("a.pg")))]
                last = max(nums or [1])
            for art in soup.select("article.prd"):
                a = art.select_one("a.core")
                if not a or a["href"] in seen:
                    continue
                seen.add(a["href"])
                g = art.select_one("[data-ga4-item_brand]") or a
                cat = " ".join(g.get(f"data-ga4-item_category{i}", "") for i in (3, 4, 5, 6))
                nm, pr, od = art.select_one(".name"), art.select_one(".prc"), art.select_one(".old")
                out.append(dict(name=nm.get_text(" ", strip=True) if nm else None, price=to_num(pr.get_text() if pr else 0),
                                old=to_num(od.get_text()) if od else 0, url=B + a["href"], in_stock=True,
                                shop="Jumia", source="jumia.com.eg", brand_hint=g.get("data-ga4-item_brand"),
                                cat_hint=cat + " " + c.replace("-", " "), model_hint=None, extra=None,
                                image=_img(art) or g.get("data-moengage-product_image")))
            page += 1
    log.info("jumia: %d listings", len(out))
    return _cap(out, ctx)


# ── WooCommerce public Store API (Ehab Center, Berty Center; no login) ─────────────────────────
def woo(f, ctx, base, cats, shop, source, per_page=100):
    out, seen = [], set()
    for c in cats:
        for page in range(1, 60):
            if _enough(out, ctx):
                return _cap(out, ctx)
            q = f"?category={c}&page={page}" + (f"&per_page={per_page}" if per_page else "")
            j = f.get(f"{base}/wp-json/wc/store/v1/products{q}", as_json=True)
            if not j:
                break
            for x in j:
                if x["id"] in seen:
                    continue
                seen.add(x["id"])
                pr = x.get("prices") or {}
                div = 10 ** int(pr.get("currency_minor_unit") or 0)
                name = html.unescape(x.get("name") or "")
                out.append(dict(name=name, price=to_num(pr.get("price")) // div, old=to_num(pr.get("regular_price")) // div,
                                url=x.get("permalink"), in_stock=bool(x.get("is_in_stock")), shop=shop, source=source,
                                brand_hint=(x.get("brands") or [{}])[0].get("name"),
                                cat_hint=" ".join(k.get("slug", "").replace("-", " ") for k in x.get("categories", [])) + " " + c,
                                model_hint=None, extra=html.unescape(x.get("slug") or "").replace("-", " "),
                                image=((x.get("images") or [{}])[0].get("thumbnail") or (x.get("images") or [{}])[0].get("src"))))
            if len(j) < (per_page or 10):
                break
    log.info("%s: %d listings", shop, len(out))
    return _cap(out, ctx)


EHAB_CATS = ["washing-machines", "washer-dryers", "tumble-dryers", "refrigerators", "deep-freezers", "cookers",
             "built-in-ovens", "built-in-hobs", "built-in-hood", "microwaves", "built-in-microwaves", "ovens",
             "dishwashers", "electric-heaters", "gas-heaters", "instant-water-heater"]
BERTY_CATS = ["washing-machines", "dryer", "refrigerators", "deep-freezer", "gas-stove", "built-in-stove",
              "built-in-oven", "cooker-hoods", "microwave", "dishwashers", "water-heater", "electric-oven"]


def ehab(f, ctx):
    return woo(f, ctx, "https://ehabcenter.com", EHAB_CATS, "Ehab Center", "ehabcenter.com")


WAZEN_CATS = ["washing-machine", "refrigerators", "freezers", "cookers", "dishwashers", "built-in", "water-heater",
              "microwaves"]


def wazen(f, ctx):
    return woo(f, ctx, "https://wazen.eg", WAZEN_CATS, "Wazen", "wazen.eg")


def berty(f, ctx):
    # robots.txt disallows "?per_page=" on this site, so use the default page size (10)
    return woo(f, ctx, "https://berty-center.com", BERTY_CATS, "Berty Center", "berty-center.com", per_page=None)


# ── Raneen (Magento listing pages; ?p= allowed, Crawl-delay 10 honoured) ──────────────────────
RANEEN_CATS = ["washers-and-dryers", "dish-washers", "refrigerators-and-freezers", "cookers", "built-in-appliances",
               "water-heaters"]


def raneen(f, ctx):
    B, out, seen = "https://www.raneen.com/ar/appliances/", [], set()
    cats = [f"{B}large-appliances/{c}" for c in RANEEN_CATS] + [f"{B}kitchen-appliances/microwaves-ovens"]
    for c in cats:
        for page in range(1, 80):
            if _enough(out, ctx):
                return _cap(out, ctx)
            h = f.get(c + (f"?p={page}" if page > 1 else ""))
            if not h:
                break
            soup, new = BeautifulSoup(h, "lxml"), 0
            for it in soup.select(".product-item"):
                a = it.select_one("a.product-item-link")
                price, old = magento_prices(it)
                if not a or not price or a["href"] in seen:
                    continue
                seen.add(a["href"])
                new += 1
                out.append(dict(name=a.get_text(" ", strip=True), price=price, old=old, url=a["href"],
                                in_stock=not it.select_one(".stock.unavailable"), shop="Raneen", source="raneen.com",
                                brand_hint=None, cat_hint=c.rsplit("/", 1)[-1].replace("-", " "), model_hint=None,
                                extra=a["href"].rsplit("/", 1)[-1].replace("-", " "), image=_img(it)))
            if not new:
                break
    log.info("raneen: %d listings", len(out))
    return _cap(out, ctx)


# ── Azmy (own site; category pages paged with ?start=; no robots.txt) ─────────────────────────
AZMY_CATS = ["Washing-Machines", "Washers-Dryers", "Refrigerators", "Refrigeration", "Cookers", "Dishwashers",
             "Built-In", "Ovens", "Hobs", "Hoods", "Microwaves", "Water-Heaters"]


def azmy(f, ctx):
    B, out, seen = "https://azmyco.com/ar/products/", [], set()
    for c in AZMY_CATS:
        for start in range(0, 2000, 12):
            if _enough(out, ctx):
                return _cap(out, ctx)
            h = f.get(f"{B}{c}/" + (f"?start={start}" if start else ""))
            if not h:
                break
            soup, new = BeautifulSoup(h, "lxml"), 0
            for col in soup.select("[data-product-id]"):
                pid = col["data-product-id"]
                a = col.select_one("a[href]")
                cur = col.select_one(".current-price")
                if pid in seen or not a or not cur:
                    continue
                seen.add(pid)
                new += 1
                img, old = col.select_one("img[alt]"), col.select_one(".old-price")
                slug = a["href"].rstrip("/").rsplit("/", 1)[-1]
                out.append(dict(name=img["alt"] if img else slug, price=to_num(cur.get_text()),
                                old=to_num(old.get_text()) if old else 0, url=a["href"], in_stock=True, shop="Azmy",
                                source="azmyco.com", brand_hint=None, cat_hint=c.replace("-", " "), model_hint=None,
                                extra=re.sub(r"-\d+$", "", slug).replace("-", " "), image=_img(img)))
            if not new:
                break
    log.info("azmy: %d listings", len(out))
    return _cap(out, ctx)


# ── Al Reyada (Shopify public /products.json) ─────────────────────────────────────────────────
def alreyada(f, ctx):
    out = []
    for page in range(1, 40):
        j = f.get(f"https://alreyadastore.com/products.json?limit=250&page={page}", as_json=True)
        if not j or not j.get("products"):
            break
        for p in j["products"]:
            v = (p.get("variants") or [{}])[0]
            out.append(dict(name=p.get("title"), price=to_num(v.get("price")), old=to_num(v.get("compare_at_price")),
                            url=f"https://alreyadastore.com/products/{p.get('handle')}", in_stock=bool(v.get("available")),
                            shop="Al Reyada", source="alreyadastore.com", brand_hint=p.get("vendor"),
                            cat_hint=(p.get("product_type") or "") + " " + " ".join(p.get("tags") or []),
                            model_hint=None, extra=None,
                            image=((p.get("images") or [{}])[0].get("src") or "").split("?")[0] + "?width=300" if p.get("images") else None))
    log.info("alreyada: %d listings", len(out))
    return _cap(out, ctx)


# ── Carrefour (first page of each category only: robots.txt disallows ?currentPage=) ─────────
CARREFOUR_CATS = ["NFEGY4100701", "fridges-freezers"]


def carrefour(f, ctx):
    B, out, seen = "https://www.carrefouregypt.com/mafegy/en/c/", [], set()
    cats, i = list(CARREFOUR_CATS), 0
    while i < len(cats) and i < 30:
        h = f.get(B + cats[i])
        i += 1
        if not h:
            continue
        if i <= len(CARREFOUR_CATS):   # discover sibling large-appliance categories (NFEGY41xxxxx)
            for c in re.findall(r'href="/mafegy/en/c/(NFEGY41\d{5})"', h):
                if c not in cats:
                    cats.append(c)
        u = h.replace('\\"', '"')
        for m in re.finditer(r'"productId":"(\d+)","productName":"((?:[^"\\]|\\.)*)"', u):
            pid, name = m.group(1), m.group(2)
            if pid in seen:
                continue
            win, back = u[m.end(): m.end() + 1500], u[max(0, m.start() - 900): m.start()]
            sp = re.search(r'"sellingPrice":([\d.]+)', win)
            if not sp:
                continue
            seen.add(pid)
            mp = re.search(r'"markedPrice":([\d.]+)', win)
            shop = re.search(r'"shopName":"([^"]*)"', win)
            stock = re.search(r'"stockLevelStatus":"(\w+)"', back)
            href = re.search(r'href="(/mafegy/en/[^"?]*/p/' + pid + r')', h)
            im = re.search(r'"imageUrl":"(https://[^"]+)"', back[-700:] + win[:300])
            out.append(dict(name=name.encode().decode("unicode_escape", "ignore") if "\\u" in name else name,
                            price=to_num(float(sp.group(1))), old=to_num(float(mp.group(1))) if mp else 0,
                            url="https://www.carrefouregypt.com" + (href.group(1) if href else f"/mafegy/en/p/{pid}"),
                            in_stock=(stock.group(1) != "outOfStock") if stock else True, shop="Carrefour",
                            source="carrefouregypt.com", seller=(shop.group(1) if shop and shop.group(1) != "Carrefour" else None),
                            brand_hint=None, cat_hint=None, model_hint=None, extra=None,
                            image=im.group(1) if im else None))
    log.info("carrefour: %d categories, %d listings", i, len(out))
    return _cap(out, ctx)


STORES = {"btech": btech, "elaraby": elaraby, "zanussi": zanussi, "jumia": jumia, "ehab": ehab, "wazen": wazen, "berty": berty,
          "raneen": raneen, "azmy": azmy, "alreyada": alreyada, "carrefour": carrefour}
