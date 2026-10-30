"""Auditable regression tests; no real-world sensor or live identity data."""
import random
import statistics
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from atda_pathb_fortress import (
    AggregateRelease, CapacityExceeded, ClockFault,
    FortressBuffer, Policy, SanitizedPassage, two_sided_geometric,
)


def passage(i: int, bucket: str = 'NARCOTICS') -> SanitizedPassage:
    return SanitizedPassage(token=i.to_bytes(16, 'big'), bucket=bucket)


class ZeroNoise:
    """Every geometric variate is 0 (testing only)."""
    def randrange(self, stop: int) -> int:
        return stop - 1


class TestConfig(unittest.TestCase):
    def test_policy_fixed_normative_k(self):
        self.assertRaises(ValueError, Policy, k_min=49)
        self.assertRaises(ValueError, Policy, epoch_total_max=49)
        self.assertRaises(ValueError, Policy, window_steps_min=(15, 30, 120))

    def test_single_category_per_passage_schema(self):
        with self.assertRaises(TypeError):
            SanitizedPassage(token=b'x'*16, bucket='NARCOTICS', payment_id='NEVER')
        with self.assertRaises(ValueError):
            FortressBuffer('UNSAFE:INDIVIDUAL')

    def test_noise_epsilon(self):
        self.assertAlmostEqual(Policy().epsilon_query, 0.6931471805599453, places=12)


class TestGating(unittest.TestCase):
    def setUp(self):
        self.b = FortressBuffer('ZONE_A', rng=ZeroNoise())

    def test_no_release_under_50_then_30min_release(self):
        for i in range(49):
            self.assertTrue(self.b.ingest(passage(i), 1))
        self.assertIsNone(self.b.checkpoint(15))
        self.assertEqual(self.b.active_window_minutes, 30)
        self.b.ingest(passage(49), 16)
        result = self.b.checkpoint(30)
        self.assertIsInstance(result, AggregateRelease)
        self.assertEqual(result.noisy_counts['NARCOTICS'], 50)
        self.assertEqual(result.window_minutes, 30)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_release_exactly_at_50_after_15min(self):
        for i in range(50):
            self.b.ingest(passage(i, 'BIOHAZARD' if i < 17 else 'OTHER'), 3)
        self.assertIsNone(self.b.checkpoint(14))
        result = self.b.checkpoint(15)
        self.assertEqual(result.noisy_counts, {'NARCOTICS':0,'BIOHAZARD':17,'OTHER':33})
        self.assertEqual(result.window_start_utc_min, 0)
        self.assertNotIn('token', repr(result))

    def test_duplicate_does_not_increase_count(self):
        for i in range(49):
            self.b.ingest(passage(i), 3)
        self.assertFalse(self.b.ingest(passage(1), 3))
        self.assertEqual(self.b.buffered_interactions, 49)
        self.assertIsNone(self.b.checkpoint(15))

    def test_discard_at_24h_under_k(self):
        self.b.ingest(passage(1), 1)
        for deadline in (15,30,60,120,240,480,960,1440):
            self.assertIsNone(self.b.checkpoint(deadline))
        self.assertEqual(self.b.buffered_interactions, 0)
        self.assertIsNone(self.b.active_window_minutes)

    def test_overflow_fails_closed(self):
        b = FortressBuffer('ZONE_A', Policy(epoch_total_max=50, bucket_max=50, dedup_capacity=50), ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 1)
        with self.assertRaises(CapacityExceeded):
            b.ingest(passage(51), 2)
        self.assertEqual(b.buffered_interactions, 0)  # overflow erases counts
        with self.assertRaises(RuntimeError):
            b.checkpoint(15)  # quarantine blocks any partial export

    def test_fails_closed_on_late_checkpoint(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        with self.assertRaises(ClockFault):
            self.b.checkpoint(19)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_fails_closed_on_missing_checkpoint(self):
        self.b.ingest(passage(1), 0)
        with self.assertRaises(ClockFault):
            self.b.ingest(passage(2), 15)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_clock_rollback_clears_local_buffer(self):
        self.b.ingest(passage(1), 6)
        with self.assertRaises(ClockFault):
            self.b.ingest(passage(2), 5)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_no_schema_or_token_leak_in_release(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        r = self.b.checkpoint(15)
        self.assertEqual(set(r.__dict__),
            {'zone','window_start_utc_min','window_minutes','noisy_counts','policy_version'})
        self.assertFalse(any('payment' in x.lower() for x in r.__dict__))

    def test_reset_is_nonoverlapping(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        self.assertIsNotNone(self.b.checkpoint(15))
        self.assertIsNone(self.b.checkpoint(15))
        self.b.ingest(passage(1111), 16)
        self.assertEqual(self.b.buffered_interactions, 1)

    def test_refuses_unknown_bucket(self):
        with self.assertRaises(ValueError):
            self.b.ingest(passage(1,'UNKNOWN'), 1)


class TestDistribution(unittest.TestCase):
    def test_two_sided_geometric_unbiased(self):
        rng = random.Random(1701)  # deterministic for test ONLY, never production
        draws = [two_sided_geometric(1,2,rng) for _ in range(30000)]
        self.assertLess(abs(statistics.mean(draws)), 0.055)
        self.assertAlmostEqual(statistics.pvariance(draws), 4.0, delta=0.30)
        self.assertLess(abs(draws.count(0) / len(draws) - 1/3), 0.014)
        self.assertTrue(min(draws) <= -8 and max(draws) >= 8)

    def test_invalid_q(self):
        with self.assertRaises(ValueError):
            two_sided_geometric(1, 1, ZeroNoise())


if __name__ == '__main__':
    unittest.main()
