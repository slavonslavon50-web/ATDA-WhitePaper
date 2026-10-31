"""Reproducible synthetic-only Red Team state-machine invariants (not formal proof)."""
import random
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from atda_pathb_fortress import FortressBuffer, Policy, SanitizedPassage

class ZeroNoise:
    def randrange(self, stop: int) -> int:
        return stop - 1

class StateMachineInvariants(unittest.TestCase):
    def test_seeded_interaction_streams_respect_k_and_exact_accounting(self):
        rng = random.Random(20261031)
        for trial in range(600):
            b = FortressBuffer('TEST_ZONE', rng=ZeroNoise())
            seen = set()
            expected = {name: 0 for name in Policy.categories}
            first = SanitizedPassage((0).to_bytes(16, 'big'), 'NARCOTICS')
            self.assertTrue(b.ingest(first, 1))
            seen.add(first.token)
            expected[first.bucket] += 1
            next_token = 1
            released = False
            for deadline in Policy.window_steps_min:
                # Apply only records that arrive strictly before the public
                # checkpoint, ensuring the test does not rely on clock faults.
                current_time = deadline - 1 if deadline > 15 else 1
                for _ in range(rng.randrange(0, 44)):
                    is_duplicate = rng.randrange(6) == 0
                    if is_duplicate:
                        token = rng.choice(tuple(seen))
                    else:
                        token = next_token.to_bytes(16, 'big')
                        next_token += 1
                    category = rng.choice(Policy.categories)
                    accepted = b.ingest(SanitizedPassage(token, category), current_time)
                    self.assertEqual(accepted, token not in seen, trial)
                    if accepted:
                        seen.add(token)
                        expected[category] += 1
                self.assertEqual(b.buffered_interactions, len(seen), trial)
                before = len(seen)
                output = b.checkpoint(deadline)
                if before < 50:
                    self.assertIsNone(output, trial)
                else:
                    self.assertIsNotNone(output, trial)
                    self.assertEqual(dict(output.noisy_counts), expected, trial)
                    self.assertEqual(set(output.to_public_payload()['noisy_counts']), set(Policy.categories))
                    self.assertEqual(output.window_minutes, deadline, trial)
                    self.assertEqual(b.buffered_interactions, 0)
                    released = True
                    break
            if not released:
                self.assertEqual(b.buffered_interactions, 0, trial)  # 24h expiry

if __name__ == '__main__':
    unittest.main()
