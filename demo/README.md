# Public demo: 49 interactions -> no statistical output; 50 -> eligible at checkpoint

This **synthetic-data-only** walkthrough runs the repository's real `FortressBuffer` research implementation. It demonstrates the local decision to construct an `AggregateRelease` object; there is **no network stack, sensor, payment interface or production hardware** in the demo.

## Run it

From the repository root, with Python 3.10 or newer:

```bash
python3 demo/demo_49_to_50.py
python3 -m unittest discover -s tests -v
```

The script prints the decision trace (not randomized numerical counts, which vary on each run):

```text
00:01  49 synthetic interaction events locally buffered; no aggregate released
00:15  CHECKPOINT: 49 < 50 -> NO AGGREGATE RELEASE; window extends to 30 min
00:16  50th synthetic interaction accepted -> still NO RELEASE before checkpoint
00:29  Not yet due -> NO AGGREGATE RELEASE
00:30  CHECKPOINT: 50 >= 50 -> AGGREGATE RELEASE ELIGIBLE (30-min window)
Export schema: zone, window_start_utc_min, window_minutes, noisy_counts, policy_version
Counts are RANDOMIZED; no per-interaction tokens, payments or exact event times in release
Limits: 50 interactions are not 50 distinct people; hardware PII isolation is NOT tested.
Limits: hard threshold publication leaks threshold state; NO end-to-end pure epsilon-DP claim.
```

**Why 30 minutes, not 16?** The first 15-minute checkpoint sees 49 validated events and extends the aggregation window. The 50th event at minute 16 crosses the hard minimum but publication can occur only at the next checkpoint, minute 30.

`SanitizedPassage` tokens here are **sequential fixtures for an isolated test only**; never use these tokens in a real deployment. The real proposal requires locally generated, cryptographically random ephemeral tokens *after* demonstrated hardware PII exclusion. The lab-only local event count is not an external Path B field.

## Read it / show it

- [Illustration SVG](threshold.svg) — displays inside GitHub README.
- [Offline HTML storyboard](../docs/index.html) — interactive four-step explanation; download and open locally, or serve via GitHub Pages after enabling Pages in repository settings. The storyboard is **not** the executable privacy kernel and uses no network APIs.
- [Actual reference kernel](../src/atda_pathb_fortress.py) and [integration tests](../tests/test_public_demo.py).

## Strict limitations

- A validated **interaction event** is not a distinct person. The demo cannot verify independence from users or payments.
- The simulated physical sensor and interface do not exist; no electrical PII isolation, cryptographic transport, attestation, secure-boot or CBRN detector is implemented here.
- The published/non-published event leaks k-threshold information, so hard k=50 is incompatible with claiming pure **end-to-end** epsilon-DP for this protocol. The geometric-noise proof applies only to a fixed always-executed count query under its stated assumptions.
- Zone and time-window metadata and rare-location aggregates may remain identifying when joined with external sources; GDPR anonymisation is **not** established.
