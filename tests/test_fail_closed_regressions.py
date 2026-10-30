"""ATDA review regressions: ensure a faulty epoch cannot export analytics."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from atda_pathb_fortress import (  # noqa: E402
    AggregateRelease, CapacityExceeded, ClockFault, FortressBuffer,
    Policy, SanitizedPassage,
)


class ZeroNoise:
    def randrange(self, stop: int) -> int:
        return stop - 1


def passage(number: int, category: str = 'NARCOTICS') -> SanitizedPassage:
    return SanitizedPassage(number.to_bytes(16, 'big'), category)


class TestFailClosedAfterFault(unittest.TestCase):
    def test_overflow_quarantines_epoch_and_never_releases_partial_counts(self):
        b = FortressBuffer('ZONE', Policy(epoch_total_max=50, bucket_max=50,
                                          dedup_capacity=50), ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 1)
        with self.assertRaises(CapacityExceeded):
            b.ingest(passage(50), 2)
        self.assertEqual(b.buffered_interactions, 0)
        self.assertIsNone(b.active_window_minutes)
        with self.assertRaises(RuntimeError):
            b.checkpoint(15)
        with self.assertRaises(RuntimeError):
            b.ingest(passage(51), 16)

    def test_category_overflow_quarantines_whole_window(self):
        p = Policy(k_min=50, epoch_total_max=120, bucket_max=50, dedup_capacity=120)
        b = FortressBuffer('ZONE', p, ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 2)
        with self.assertRaises(CapacityExceeded):
            b.ingest(passage(51), 3)
        self.assertEqual(b.buffered_interactions, 0)
        with self.assertRaises(RuntimeError):
            b.checkpoint(15)

    def test_randomness_failure_quarantines_window(self):
        class FailedRng:
            def randrange(self, stop):
                raise OSError('synthetic RNG failure')
        b = FortressBuffer('ZONE', rng=FailedRng())
        for i in range(50):
            b.ingest(passage(i), 1)
        with self.assertRaisesRegex(RuntimeError, 'noise generation failed'):
            b.checkpoint(15)
        self.assertEqual(b.buffered_interactions, 0)
        with self.assertRaises(RuntimeError):
            b.checkpoint(16)

    def test_checkpoint_advances_time_floor_for_future_ingest(self):
        b = FortressBuffer('ZONE', rng=ZeroNoise())
        b.ingest(passage(0), 1)
        b.checkpoint(15)
        with self.assertRaises(ClockFault):
            b.ingest(passage(1), 2)
        self.assertEqual(b.buffered_interactions, 0)
        with self.assertRaises(RuntimeError):
            b.checkpoint(30)

    def test_early_checkpoint_advances_time_floor(self):
        b = FortressBuffer('ZONE', rng=ZeroNoise())
        b.ingest(passage(0), 1)
        b.checkpoint(11)
        with self.assertRaises(ClockFault):
            b.ingest(passage(1), 10)

    def test_completed_epoch_does_not_reset_monotonic_clock(self):
        b = FortressBuffer('ZONE', rng=ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 1)
        self.assertIsNotNone(b.checkpoint(15))
        with self.assertRaises(ClockFault):
            b.ingest(passage(100), 1)

    def test_faulted_buffer_does_not_restart_after_late_checkpoint(self):
        b = FortressBuffer('ZONE', rng=ZeroNoise())
        b.ingest(passage(0), 1)
        with self.assertRaises(ClockFault):
            b.checkpoint(20)
        self.assertEqual(b.buffered_interactions, 0)
        with self.assertRaises(RuntimeError):
            b.ingest(passage(1), 21)


class TestImmutableRelease(unittest.TestCase):
    def test_no_nested_mutability(self):
        b = FortressBuffer('ZONE', rng=ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 1)
        output = b.checkpoint(15)
        self.assertIsInstance(output, AggregateRelease)
        with self.assertRaises(TypeError):
            output.noisy_counts['NARCOTICS'] = 99
        with self.assertRaises(FrozenInstanceError):
            output.window_minutes = 60
        self.assertEqual(output.noisy_counts['NARCOTICS'], 50)

    def test_reject_nested_mutable_count_values(self):
        with self.assertRaises(ValueError):
            AggregateRelease('ZONE', 0, 15, {'NARCOTICS': [1]})

    def test_source_mapping_cannot_mutate_release_and_wire_payload_is_detached(self):
        source = {'NARCOTICS': 3, 'BIOHAZARD': 0}
        release = AggregateRelease('ZONE', 0, 15, source)
        source['NARCOTICS'] = 999
        self.assertEqual(release.noisy_counts['NARCOTICS'], 3)
        payload = release.to_public_payload()
        self.assertEqual(json.loads(json.dumps(payload))['noisy_counts']['NARCOTICS'], 3)
        payload['noisy_counts']['NARCOTICS'] = 999
        self.assertEqual(release.noisy_counts['NARCOTICS'], 3)
        self.assertEqual(set(payload), {'zone', 'window_start_utc_min',
                                        'window_minutes', 'noisy_counts', 'policy_version'})


class TestManifestOptimizedMode(unittest.TestCase):
    def test_optimized_python_still_rejects_bad_manifest(self):
        original = (ROOT / 'manifest' / 'ATDA_Privacy_Safety_Manifest_v1_2.json').read_text()
        wrong = original.replace('"k_min": 50', '"k_min": 1', 1)
        self.assertNotEqual(wrong, original)
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td, 'invalid.json')
            path.write_text(wrong)
            for mode in ([], ['-O']):
                script = (
                    'import sys, pathlib; '
                    f'sys.path.insert(0, {str(ROOT / "manifest")!r}); '
                    'from validate_manifest import validate; '
                    f'validate(pathlib.Path({str(path)!r}))'
                )
                result = subprocess.run([sys.executable, *mode, '-c', script],
                                        text=True, capture_output=True, check=False)
                self.assertNotEqual(result.returncode, 0, (mode, result.stdout, result.stderr))
                self.assertIn('ManifestValidationError', result.stderr)


if __name__ == '__main__':
    unittest.main()
