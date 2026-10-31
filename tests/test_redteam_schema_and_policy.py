"""Red-team regression: published reference profiles and export schema must be fixed."""
import sys
import unittest
import time
import threading
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from atda_pathb_fortress import Policy, AggregateRelease, FortressBuffer, SanitizedPassage

class FixedProfileTests(unittest.TestCase):
    def test_mutable_window_schedule_rejected(self):
        with self.assertRaises(ValueError):
            Policy(window_steps_min=list(Policy.window_steps_min))

    def test_non_normative_window_schedule_rejected(self):
        with self.assertRaises(ValueError):
            Policy(window_steps_min=(15, 1440))

    def test_mutable_category_names_rejected(self):
        with self.assertRaises(ValueError):
            Policy(categories=list(Policy.categories))

    def test_custom_categories_rejected(self):
        with self.assertRaises(ValueError):
            Policy(categories=('CARD_12345',))

    def test_float_schedule_cannot_pass_integer_equality(self):
        with self.assertRaises(ValueError):
            Policy(window_steps_min=tuple(float(x) for x in Policy.window_steps_min))

    def test_fractional_config_parameters_rejected(self):
        for field, value in [('epoch_total_max', 10000.0), ('q_den', 2.0),
                             ('max_checkpoint_lag_min', 2.0)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                Policy(**{field: value})

class ConcurrencyTests(unittest.TestCase):
    def test_two_checkpoint_calls_produce_exactly_one_release(self):
        class SlowRng:
            def randrange(self, stop):
                time.sleep(0.002)
                return stop - 1
        b = FortressBuffer('ZONE', rng=SlowRng())
        for i in range(50):
            b.ingest(SanitizedPassage(i.to_bytes(16, 'big'), 'NARCOTICS'), 1)
        barrier = threading.Barrier(3)
        outputs = []
        outputs_lock = threading.Lock()
        def worker():
            barrier.wait()
            try:
                value = b.checkpoint(15)
                state = 'RELEASE' if value is not None else 'NONE'
            except Exception as exc:
                state = type(exc).__name__
            with outputs_lock:
                outputs.append(state)
        threads = [threading.Thread(target=worker) for _ in range(2)]
        for t in threads: t.start()
        barrier.wait()
        for t in threads: t.join(timeout=3)
        self.assertFalse(any(t.is_alive() for t in threads), 'deadlocked checkpoint')
        self.assertEqual(sorted(outputs), ['NONE', 'RELEASE'])

    def test_concurrent_duplicate_cannot_increase_category_count_twice(self):
        class SlowSet(set):
            def __contains__(self, x):
                present = super().__contains__(x)
                time.sleep(0.01)  # deterministic instrumentation at read/write gap
                return present
        b = FortressBuffer('ZONE')
        b._seen = SlowSet()  # fault-injection fixture, not production API
        barrier = threading.Barrier(3)
        status = []
        def worker():
            barrier.wait()
            status.append(b.ingest(SanitizedPassage(b'Z'*16, 'NARCOTICS'), 1))
        threads = [threading.Thread(target=worker) for _ in range(2)]
        for t in threads: t.start()
        barrier.wait()
        for t in threads: t.join(timeout=3)
        self.assertFalse(any(t.is_alive() for t in threads), 'deadlocked ingest')
        self.assertEqual(sorted(status), [False, True])
        self.assertEqual(b._counts['NARCOTICS'], 1)
        self.assertEqual(b.buffered_interactions, 1)


class ExportSchemaTests(unittest.TestCase):
    @staticmethod
    def valid_release(**overrides):
        args=dict(zone='ZONE', window_start_utc_min=0,window_minutes=15,
                  noisy_counts={'NARCOTICS':40,'BIOHAZARD':12,'OTHER':0},
                  policy_version='ATDA-PathB-Fortress-1.2-reference')
        args.update(overrides)
        return AggregateRelease(**args)

    def test_disallow_identity_like_bucket(self):
        with self.assertRaises(ValueError):
            self.valid_release(noisy_counts={'NARCOTICS':40,'BIOHAZARD':12,
                                             'CARD_1234567890123456':1})

    def test_disallow_missing_bucket(self):
        with self.assertRaises(ValueError):
            self.valid_release(noisy_counts={'NARCOTICS':40,'BIOHAZARD':12})

    def test_disallow_unrecognised_policy_version(self):
        with self.assertRaises(ValueError):
            self.valid_release(policy_version='UNTRUSTED')

    def test_disallow_invalid_window(self):
        with self.assertRaises(ValueError):
            self.valid_release(window_minutes=1)

    def test_disallow_unaligned_start(self):
        with self.assertRaises(ValueError):
            self.valid_release(window_start_utc_min=1)

    def test_disallow_zone_embedded_data(self):
        with self.assertRaises(ValueError):
            self.valid_release(zone='CARD:1234567890123456')

    def test_valid_release_output_is_detached(self):
        v=self.valid_release()
        p=v.to_public_payload()
        self.assertEqual(set(p['noisy_counts']),set(Policy.categories))
        p['noisy_counts']['NARCOTICS']=999
        self.assertEqual(v.noisy_counts['NARCOTICS'],40)

if __name__ == '__main__': unittest.main()
