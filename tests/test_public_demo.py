"""Regression tests for published 49 -> 50 synthetic-only CLI demonstration."""
import sys
import unittest
from dataclasses import fields
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo.demo_49_to_50 import PUBLIC_RELEASE_FIELDS, run_scenario
from src.atda_pathb_fortress import AggregateRelease


class PublicDemoTests(unittest.TestCase):
    def test_actual_reference_kernel_drives_explanation(self):
        trace, released = run_scenario()
        self.assertIsInstance(released, AggregateRelease)
        self.assertEqual(released.window_minutes, 30)
        self.assertEqual(released.zone, "DEMO_ZONE")
        self.assertIn("49 < 50 -> NO AGGREGATE RELEASE", trace[1])
        self.assertIn("still NO RELEASE", trace[2])
        self.assertIn("50 >= 50 -> AGGREGATE RELEASE ELIGIBLE", trace[4])
        self.assertEqual({field.name for field in fields(released)}, PUBLIC_RELEASE_FIELDS)
        self.assertTrue(all(cat in released.noisy_counts for cat in ("NARCOTICS", "BIOHAZARD", "OTHER")))

    def test_release_has_no_payment_or_person_schema(self):
        _, release = run_scenario()
        names = set(release.__dict__)
        self.assertFalse({"payment_id", "card_number", "person_id", "token"} & names)
        self.assertEqual(set(release.noisy_counts), {"NARCOTICS", "BIOHAZARD", "OTHER"})


if __name__ == "__main__":
    unittest.main()
