"""Run: python -m unittest discover -s tests -v   (no network needed)"""
import os, sys, unittest
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "tools", "scrape")]
import pricebook, match, analysis, health, normalize   # noqa: E402


def prod(i, shop, key, price, **kw):
    p = {"id": i, "name": kw.pop("name", "x"), "brand": kw.pop("brand", key.split(":")[0].title()), "category": "ثلاجة", "shop": shop,
         "product_key": key, "price_after": price, "price_before": kw.pop("before", 0), "in_stock": True,
         "history": kw.pop("history", [{"date": "2026-11-05", "price": price}]), "first_seen": "2026-11-05",
         "last_seen": "2026-11-18"}
    p.update(kw)
    return p


class ModelKey(unittest.TestCase):
    def test_region_tail_samsung(self):
        self.assertEqual(pricebook.model_key("Samsung", "RS70F65QATMR"), pricebook.model_key("Samsung", "RS70F65QAT"))

    def test_colour_letter_not_merged(self):
        self.assertNotEqual(pricebook.model_key("Fresh", "FDF220S"), pricebook.model_key("Fresh", "FDF220"))

    def test_bracket_colour_dropped(self):
        self.assertEqual(pricebook.model_key("LG", "GN-B422SQCL (Silver)"), pricebook.model_key("LG", "GN-B422SQCL"))

    def test_junk_rejected(self):
        self.assertIsNone(pricebook.model_key("LG", "WHITE"))


class Match(unittest.TestCase):
    def test_link_by_name_unique_token(self):
        d = {"products": [prod(1, "A", "FRESH:FWS300NA", 2400),
                          prod(2, "B", "x", 2500, brand="Fresh", name="Fresh Baby Top Load FWS300NA White")]}
        d["products"][1].pop("product_key")
        self.assertEqual(match.link_unkeyed(d), 1)
        self.assertEqual(d["products"][1]["product_key"], "FRESH:FWS300NA")

    def test_no_link_when_ambiguous(self):
        d = {"products": [prod(1, "A", "FRESH:FWS300NA", 1), prod(2, "A", "FRESH:FWS400NB", 1)]}
        u = prod(3, "B", "x", 1, brand="Fresh", name="FWS300NA vs FWS400NB"); u.pop("product_key")
        d["products"].append(u)
        self.assertEqual(match.link_unkeyed(d), 0)

    def test_colour_suggestion_listed_not_merged(self):
        d = {"products": [prod(1, "A", "FRESH:FDF220", 1), prod(2, "B", "FRESH:FDF220S", 1)]}
        self.assertEqual(len(match.colour_suggestions(d)), 1)
        self.assertNotEqual(d["products"][0]["product_key"], d["products"][1]["product_key"])


class Signals(unittest.TestCase):
    def test_market_and_inflated(self):
        P = [prod(1, "A", "LG:GNB422", 10000, before=15000, **{"history": [{"date": "2026-11-05", "price": 10000}]}),
             prod(2, "B", "LG:GNB422", 10000), prod(3, "C", "LG:GNB422", 10200)]
        P[0]["discount_pct"] = 33
        analysis.compute_signals(P)
        self.assertEqual(P[0]["signals"]["med"], 10100)
        self.assertTrue(P[0]["signals"]["inf"])

    def test_needs_two_other_shops(self):
        P = [prod(1, "A", "LG:GNB422", 10000), prod(2, "B", "LG:GNB422", 9000)]
        analysis.compute_signals(P)
        self.assertNotIn("vs", P[0].get("signals", {}))

    def test_lowest_needs_history(self):
        h = [{"date": "2026-11-05", "price": 12000}, {"date": "2026-11-10", "price": 11000}, {"date": "2026-11-17", "price": 10000}]
        P = [prod(1, "A", "LG:GNB422", 10000, history=h)]
        analysis.compute_signals(P)
        self.assertTrue(P[0]["signals"]["low"])
        P2 = [prod(1, "A", "LG:GNB422", 10000)]
        analysis.compute_signals(P2)
        self.assertNotIn("signals", P2[0])

    def test_quality_outlier(self):
        P = [prod(i, s, "LG:GNB422", p) for i, (s, p) in enumerate([("A", 10000), ("B", 10100), ("C", 10200), ("D", 1000)], 1)]
        q = analysis.quality_report(P)
        self.assertEqual(len(q["outliers"]), 1)


class Health(unittest.TestCase):
    def test_drop_alert(self):
        import tempfile
        path = os.path.join(tempfile.mkdtemp(), "h.json")
        for i, n in enumerate([100, 102, 99, 101], 1):
            health.check({"shop": {"kept": n}}, path, f"2026-11-0{i}")
        self.assertEqual(health.check({"shop": {"kept": 40}}, path, "2026-11-09")[0][:4], "shop")
        self.assertEqual(health.check({"shop": {"kept": 99}}, path, "2026-11-10"), [])
        self.assertTrue(health.check({"shop": {"error": "boom"}}, path, "2026-11-11"))


if __name__ == "__main__":
    unittest.main()


class Upsert(unittest.TestCase):
    def setUp(self):
        import upsert
        self.u = upsert

    def _d(self, **kw):
        p = prod(1, "A", "LG:GNB422", 10000, url="http://a/1", scraped=True, **kw)
        return {"meta": {"last_updated": "2026-11-05"}, "products": [p]}

    def _item(self, price):
        return {"name": "x", "brand": "Lg", "category": "ثلاجة", "shop": "A", "url": "http://a/1", "product_key": "LG:GNB422",
                "price_after": price, "in_stock": True, "scraped": True}

    def test_big_jump_held_then_confirmed(self):
        d = self._d()
        st = self.u.upsert_items(d, [self._item(4000)], "2026-11-12", verbose=False)
        self.assertEqual((st["held"], d["products"][0]["price_after"]), (1, 10000))
        st = self.u.upsert_items(d, [self._item(4000)], "2026-11-19", verbose=False)
        self.assertEqual((st["held"], d["products"][0]["price_after"]), (0, 4000))
        self.assertNotIn("pending_price", d["products"][0])

    def test_small_move_accepted_at_once(self):
        d = self._d()
        self.u.upsert_items(d, [self._item(9000)], "2026-11-12", verbose=False)
        self.assertEqual(d["products"][0]["price_after"], 9000)

    def test_missing_becomes_out_of_stock_after_two_runs(self):
        d = self._d()
        self.assertEqual(self.u.mark_missing(d, {"A"}, "2026-11-25"), 0)
        self.assertEqual(self.u.mark_missing(d, {"A"}, "2026-12-02"), 1)
        self.assertFalse(d["products"][0]["in_stock"])
        self.assertFalse(d["products"][0]["history"][-1]["in_stock"])

    def test_missing_ignores_unhealthy_shop_and_handentered(self):
        d = self._d()
        self.u.mark_missing(d, set(), "2026-11-25"); self.u.mark_missing(d, set(), "2026-12-02")
        self.assertTrue(d["products"][0]["in_stock"])
        d = self._d(); d["products"][0].pop("scraped")
        self.u.mark_missing(d, {"A"}, "2026-11-25"); self.u.mark_missing(d, {"A"}, "2026-12-02")
        self.assertTrue(d["products"][0]["in_stock"])

    def test_same_run_counted_once(self):
        d = self._d()
        for _ in range(3):
            self.u.mark_missing(d, {"A": "2026-11-25"}, "2026-12-30")
        self.assertEqual(d["products"][0]["missed_runs"], 1)
        self.assertTrue(d["products"][0]["in_stock"])
