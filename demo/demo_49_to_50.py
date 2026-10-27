"""Public ATDA Path B demonstration using the actual research reference kernel.

Run from repository root: python3 demo/demo_49_to_50.py
No personal data, real sensors, or transport are accessed. The printed trace is
an explanatory view of local state; the model has no network transport.
"""
from __future__ import annotations

import sys
from dataclasses import fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.atda_pathb_fortress import AggregateRelease, FortressBuffer, SanitizedPassage

PUBLIC_RELEASE_FIELDS = frozenset(
    {"zone", "window_start_utc_min", "window_minutes", "noisy_counts", "policy_version"}
)


def run_scenario() -> tuple[tuple[str, ...], AggregateRelease]:
    """Exercise 49 at t=15, then 50 at t=16 and release at t=30.

    Tokens are sequential *test fixtures* and must not be used in production.
    The output's noise is nondeterministic; the publish/no-publish behavior is not.
    """
    buffer = FortressBuffer("DEMO_ZONE")

    for index in range(49):
        buffer.ingest(SanitizedPassage(index.to_bytes(16, "big"), "NARCOTICS"), 1)

    if buffer.buffered_interactions != 49:
        raise AssertionError("initial test fixture count incorrect")
    before = buffer.checkpoint(15)
    if before is not None or buffer.active_window_minutes != 30:
        raise AssertionError("49 interactions must withhold the aggregate")

    buffer.ingest(SanitizedPassage((49).to_bytes(16, "big"), "NARCOTICS"), 16)
    if buffer.buffered_interactions != 50 or buffer.checkpoint(29) is not None:
        raise AssertionError("reaching 50 must not immediately publish")

    published = buffer.checkpoint(30)
    if not isinstance(published, AggregateRelease):
        raise AssertionError("a matured window with 50 events should release")
    if published.window_minutes != 30 or published.zone != "DEMO_ZONE":
        raise AssertionError("unexpected aggregate metadata")
    if {field.name for field in fields(published)} != PUBLIC_RELEASE_FIELDS:
        raise AssertionError("public release schema changed; review before demo")

    trace = (
        "00:01  49 synthetic interaction events locally buffered; no aggregate released",
        "00:15  CHECKPOINT: 49 < 50 -> NO AGGREGATE RELEASE; window extends to 30 min",
        "00:16  50th synthetic interaction accepted -> still NO RELEASE before checkpoint",
        "00:29  Not yet due -> NO AGGREGATE RELEASE",
        "00:30  CHECKPOINT: 50 >= 50 -> AGGREGATE RELEASE ELIGIBLE (30-min window)",
        "Export schema: zone, window_start_utc_min, window_minutes, noisy_counts, policy_version",
        "Counts are RANDOMIZED; no per-interaction tokens, payments or exact event times in release",
    )
    return trace, published


def main() -> None:
    trace, _ = run_scenario()
    print("ATDA Path B | public 49 -> 50 synthetic-data demonstration")
    for message in trace:
        print(message)
    print("Limits: 50 interactions are not 50 distinct people; hardware PII isolation is NOT tested.")
    print("Limits: hard threshold publication leaks threshold state; NO end-to-end pure epsilon-DP claim.")


if __name__ == "__main__":
    main()
