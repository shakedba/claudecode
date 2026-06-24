"""Offline tests — no network. Run with:  python -m pytest  (or python -m unittest)."""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dealfinder.extract import extract, matches_product
from dealfinder.landed_cost import compute_landed
from dealfinder.models import Offer
from dealfinder.finder import run, load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "sample_product.html")


class TestExtract(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE, encoding="utf-8") as f:
            self.html = f.read()

    def test_jsonld_price_and_stock(self):
        data = extract(self.html)
        self.assertEqual(data["price"], 155.0)
        self.assertEqual(data["currency"], "USD")
        self.assertTrue(data["in_stock"])

    def test_match_keywords(self):
        cfg = load_config(os.path.join(ROOT, "config.json"))
        model, width = matches_product(
            "Brooks Adrenaline GTS 25 Extra Wide (4E)", cfg["product"]
        )
        self.assertTrue(model)
        self.assertTrue(width)


class TestLandedCost(unittest.TestCase):
    def setUp(self):
        self.dest = {
            "vat_rate": 0.18,
            "customs_duty_rate": 0.12,
            "clearance_fee_usd": 0,
            "import_tiers_usd": [
                {"max": 75, "apply_vat": False, "apply_customs": False},
                {"max": 500, "apply_vat": True, "apply_customs": False},
                {"max": None, "apply_vat": True, "apply_customs": True},
            ],
        }
        self.fx = {"USD": 1.0, "GBP": 1.27}

    def _offer(self, price, currency="USD", ship=0.0):
        return Offer("r", "R", "http://x", "t", price, currency, True, True, ship,
                     matched_size=True, matched_width=True)

    def test_mid_tier_vat_only(self):
        # $155 item + $20 ship = $175 -> VAT only, no customs
        q = compute_landed(self._offer(155.0, ship=20.0), self.dest, self.fx)
        self.assertEqual(q.customs_usd, 0.0)
        self.assertAlmostEqual(q.vat_usd, 175 * 0.18, places=2)
        self.assertAlmostEqual(q.total_usd, 175 + 175 * 0.18, places=2)

    def test_under_deminimis_no_tax(self):
        q = compute_landed(self._offer(50.0), self.dest, self.fx)
        self.assertEqual(q.vat_usd, 0.0)
        self.assertEqual(q.customs_usd, 0.0)
        self.assertEqual(q.total_usd, 50.0)

    def test_high_tier_has_customs(self):
        q = compute_landed(self._offer(600.0), self.dest, self.fx)
        self.assertGreater(q.customs_usd, 0.0)

    def test_currency_conversion(self):
        q = compute_landed(self._offer(100.0, "GBP"), self.dest, self.fx)
        self.assertAlmostEqual(q.item_usd, 127.0, places=2)

    def test_no_price_is_unreachable_infinite(self):
        q = compute_landed(self._offer(None), self.dest, self.fx)
        self.assertEqual(q.total_usd, float("inf"))
        self.assertFalse(q.reachable)


class TestRunOffline(unittest.TestCase):
    def test_full_run_ranks_reachable_first(self):
        cfg = load_config(os.path.join(ROOT, "config.json"))
        with open(FIXTURE, encoding="utf-8") as f:
            html = f.read()
        offline = {r["id"]: html for r in cfg["retailers"]}
        quotes = run(cfg, store=None, offline=offline)
        self.assertEqual(len(quotes), len(cfg["retailers"]))
        # Reachable retailers must sort ahead of non-reachable ones.
        reach_flags = [q.reachable for q in quotes]
        self.assertEqual(reach_flags, sorted(reach_flags, reverse=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
