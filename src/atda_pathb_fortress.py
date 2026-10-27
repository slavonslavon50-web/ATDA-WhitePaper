"""ATDA Path B Fortress: AUDITABLE REFERENCE ONLY; not field-deployable.

Threat model and privacy limitations in docs/PRIVACY_PROOF.md.
Hardware PII stripping and secure passage token issuance are external prerequisites.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log
from random import SystemRandom
from typing import Protocol


class UniformRng(Protocol):
    def randrange(self, stop: int) -> int: ...


class CapacityExceeded(RuntimeError):
    """Local protected buffer is full; stop rather than silently undercount."""


class ClockFault(RuntimeError):
    """A missed checkpoint or out-of-order clock invalidated the window."""


@dataclass(frozen=True)
class Policy:
    """Static public parameters; no remote runtime override is allowed."""

    k_min: int = 50
    window_steps_min: tuple[int, ...] = (15, 30, 60, 120, 240, 480, 960, 1440)
    categories: tuple[str, ...] = ("NARCOTICS", "BIOHAZARD", "OTHER")
    epoch_total_max: int = 10000
    bucket_max: int = 10000
    dedup_capacity: int = 10000
    q_num: int = 1
    q_den: int = 2
    max_checkpoint_lag_min: int = 2

    def __post_init__(self) -> None:
        if self.k_min < 50:
            raise ValueError("normative k_min must be at least 50")
        if (not self.window_steps_min or self.window_steps_min[0] != 15
                or self.window_steps_min[-1] != 1440
                or any(b <= a for a, b in zip(self.window_steps_min, self.window_steps_min[1:]))):
            raise ValueError("windows must increase 15 -> ... -> 1440")
        if any(step % 15 for step in self.window_steps_min):
            raise ValueError("window steps must align to 15-minute epochs")
        if not self.categories or len(set(self.categories)) != len(self.categories):
            raise ValueError("category schema must be fixed and unique")
        if any(not s.isupper() or not s.isascii() for s in self.categories):
            raise ValueError("category names must be uppercase ASCII")
        if min(self.epoch_total_max, self.bucket_max, self.dedup_capacity) < self.k_min:
            raise ValueError("capacity must support k_min")
        if self.bucket_max > self.epoch_total_max or self.dedup_capacity < self.epoch_total_max:
            raise ValueError("inconsistent capacity bounds")
        if not (0 < self.q_num < self.q_den) or self.q_den > 256:
            raise ValueError("noise q must be rational in (0,1), denominator <= 256")
        if self.q_num / self.q_den > 0.9:
            raise ValueError("reference sampler rejects q > 0.9 for availability")
        if self.max_checkpoint_lag_min < 0 or self.max_checkpoint_lag_min >= 15:
            raise ValueError("bad checkpoint tolerance")

    @property
    def epsilon_query(self) -> float:
        """Ideal *fixed-schedule count-vector* epsilon, not end-to-end epsilon."""
        return log(self.q_den / self.q_num)


@dataclass(frozen=True)
class SanitizedPassage:
    """MUST originate downstream of a physical PII-stripping boundary.

    token: 128-bit random one-interaction token generated on the sensor side;
           never derived from payments, persons, biometrics, or network IDs.
    bucket: exactly one category for L1 sensitivity = 1.
    """

    token: bytes
    bucket: str


@dataclass(frozen=True)
class AggregateRelease:
    """Only aggregate values. Never expose tokens or true raw counts."""

    zone: str
    window_start_utc_min: int
    window_minutes: int
    noisy_counts: dict[str, int]
    policy_version: str = "ATDA-PathB-Fortress-1.2-reference"


def _geometric_failures(q_num: int, q_den: int, rng: UniformRng) -> int:
    """Unbounded-support geometric distribution, P(G=n)=(1-q)*q**n.

    Uses integer-uniform draws; NO clipping or rounding of the noise tails.
    Unbounded runtime is intentionally unsuitable for hard real-time systems.
    """
    n = 0
    while rng.randrange(q_den) < q_num:
        n += 1
    return n


def two_sided_geometric(q_num: int, q_den: int, rng: UniformRng) -> int:
    """Z=G1-G2, P(Z=z)=(1-q)/(1+q) * q**abs(z).

    For one passage assigned to one of fixed buckets, vector L1 sensitivity 1.
    Ideal independent uniform draws yield epsilon=ln(1/q) for fixed output.
    """
    if not 0 < q_num < q_den:
        raise ValueError("q must lie in (0,1)")
    return _geometric_failures(q_num, q_den, rng) - _geometric_failures(q_num, q_den, rng)


class FortressBuffer:
    """Fail-closed, exact-set, single-site, non-overlapping epoch aggregator.

    NOT an anonymisation certification. Publication event itself depends on
    the nonprivate k-gate and is NOT covered by pure epsilon-DP.
    """

    def __init__(self, zone: str, policy: Policy | None = None, rng: UniformRng | None = None):
        if not zone or not zone.isascii() or len(zone) > 32 or any(
            c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in zone
        ):
            raise ValueError("zone must be coarse public ASCII deployment code")
        self.zone = zone
        self.policy = policy if policy is not None else Policy()
        self._rng = rng if rng is not None else SystemRandom()
        self._start: int | None = None
        self._step_idx = 0
        self._seen: set[bytes] = set()
        self._counts: dict[str, int] = {b: 0 for b in self.policy.categories}
        self._last_clock: int | None = None

    @property
    def buffered_interactions(self) -> int:
        """LOCAL diagnostic only; do not export or expose via Path B."""
        return len(self._seen)

    @property
    def active_window_minutes(self) -> int | None:
        return self.policy.window_steps_min[self._step_idx] if self._start is not None else None

    def _clear(self) -> None:
        self._seen.clear()
        self._counts = {b: 0 for b in self.policy.categories}
        self._start = None
        self._step_idx = 0
        self._last_clock = None

    def ingest(self, event: SanitizedPassage, now_utc_min: int) -> bool:
        if type(event) is not SanitizedPassage:
            raise TypeError("only strict sanitized passage schema is accepted")
        if type(event.token) is not bytes or len(event.token) != 16:
            raise ValueError("token must be exactly 128 random bits")
        if event.bucket not in self._counts:
            raise ValueError("unknown category")
        if type(now_utc_min) is not int or now_utc_min < 0:
            raise ValueError("time must be nonnegative integer UTC minutes")
        if self._start is None:
            self._start = (now_utc_min // 15) * 15
        if self._last_clock is not None and now_utc_min < self._last_clock:
            self._clear()
            raise ClockFault("monotonic UTC minute sequence required")
        self._last_clock = now_utc_min
        if now_utc_min >= self._start + self.policy.window_steps_min[self._step_idx]:
            self._clear()
            raise ClockFault("checkpoint missed: discarded buffer before ingest")
        if event.token in self._seen:
            return False
        if len(self._seen) >= self.policy.dedup_capacity or len(self._seen) >= self.policy.epoch_total_max:
            raise CapacityExceeded("no silent overflow or approximate dedup")
        if self._counts[event.bucket] >= self.policy.bucket_max:
            raise CapacityExceeded("bucket capacity reached")
        self._seen.add(event.token)
        self._counts[event.bucket] += 1
        return True

    def checkpoint(self, now_utc_min: int) -> AggregateRelease | None:
        """Call at every active deadline. Suppress until k; discard at 24h.

        A release is possible only once per local epoch. The randomized
        aggregate is a *conditional/fixed-query* DP mechanism; the decision
        to publish is deterministic and leaks the k threshold boundary.
        """
        if type(now_utc_min) is not int or now_utc_min < 0:
            raise ValueError("time must be nonnegative integer UTC minutes")
        if self._start is None:
            return None
        if self._last_clock is not None and now_utc_min < self._last_clock:
            self._clear()
            raise ClockFault("backward clock: discarded")
        due = self._start + self.policy.window_steps_min[self._step_idx]
        if now_utc_min < due:
            return None
        if now_utc_min - due > self.policy.max_checkpoint_lag_min:
            self._clear()
            raise ClockFault("late checkpoint: discarded instead of stale release")
        if len(self._seen) >= self.policy.k_min:
            noisy = {
                bucket: max(
                    0,
                    value + two_sided_geometric(self.policy.q_num, self.policy.q_den, self._rng),
                )
                for bucket, value in self._counts.items()
            }
            release = AggregateRelease(
                zone=self.zone,
                window_start_utc_min=self._start,
                window_minutes=self.policy.window_steps_min[self._step_idx],
                noisy_counts=noisy,
            )
            self._clear()
            return release
        if self._step_idx == len(self.policy.window_steps_min) - 1:
            self._clear()  # hard expiry; never release under-k counts
        else:
            self._step_idx += 1
        return None
