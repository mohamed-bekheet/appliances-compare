"""Cross-shop matching helpers.

link_unkeyed(d): a listing with no model field but whose title contains exactly one known model of the
  same brand and category gets that product_key (key_src="name"). Safe because the model must appear as
  a whole token (or two adjacent tokens) in the title.
colour_suggestions(d): keys that differ from another key of the same brand only by 1-2 trailing letters
  (colour/finish variants such as FDF220 vs FDF220S). They are NOT merged automatically - different SKUs -
  but are listed for review in scraped/match_suggestions.md.
"""
import collections, re


def _tokens(name):
    return re.findall(r"[A-Z0-9]+", (name or "").upper())


def _model_of(key):
    return key.split(":", 1)[1]


def _index(products):
    idx = collections.defaultdict(dict)            # (brand, category) -> {model: key}
    for p in products:
        k = p.get("product_key")
        if k:
            b = k.split(":", 1)[0]
            m = _model_of(k)
            if len(m) >= 6 and re.search(r"\d", m) and re.search(r"[A-Z]", m):
                idx[(b, p["category"])][m] = k
    return idx


def link_unkeyed(d):
    P = d["products"]
    idx = _index(P)
    linked = 0
    for p in P:
        if p.get("product_key"):
            continue
        b = p["brand"].upper().replace(" ", "")
        models = idx.get((b, p["category"]))
        if not models:
            continue
        toks = _tokens(p["name"])
        grams = set(toks) | {a + c for a, c in zip(toks, toks[1:])}
        hits = {models[m] for m in grams if m in models}
        if len(hits) == 1:
            p["product_key"] = hits.pop()
            p["key_src"] = "name"
            linked += 1
    return linked


def colour_suggestions(d, max_diff=2):
    shops = collections.defaultdict(set)
    cat = {}
    for p in d["products"]:
        k = p.get("product_key")
        if k:
            shops[k].add(p["shop"]); cat[k] = p["category"]
    byb = collections.defaultdict(list)
    for k in shops:
        byb[(k.split(":", 1)[0], cat[k])].append(_model_of(k))
    out = []
    for (b, c), ms in byb.items():
        ms.sort()
        for i, a in enumerate(ms):
            if len(a) < 6:
                continue
            for x in ms[i + 1:]:
                if not x.startswith(a):
                    break
                if 1 <= len(x) - len(a) <= max_diff:
                    ka, kx = f"{b}:{a}", f"{b}:{x}"
                    out.append({"brand": b, "category": c, "a": a, "b": x,
                                "shops_a": sorted(shops[ka]), "shops_b": sorted(shops[kx]),
                                "cross_shop_if_merged": len(shops[ka] | shops[kx]) > max(len(shops[ka]), len(shops[kx]))})
    return out


def write_suggestions(d, path):
    S = [s for s in colour_suggestions(d) if s["cross_shop_if_merged"]]
    L = ["# Possible same-product pairs (colour/finish suffix) - review, not merged", "",
         "Add a rule to REGION_TAILS in tools/pricebook.py only when the suffix is a market code, not a colour.", ""]
    for s in S[:300]:
        L.append(f"- {s['brand']} ({s['category']}): `{s['a']}` [{', '.join(s['shops_a'])}] ~ `{s['b']}` [{', '.join(s['shops_b'])}]")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return len(S)
