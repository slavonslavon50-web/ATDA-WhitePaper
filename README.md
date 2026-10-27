# ATDA - Privacy-Preserving Distributed Trace Detection

**Public research / defensive architecture publication.** 27 October 2026.

**Status: RECONSTRUCTED REFERENCE PACKAGE - NOT CERTIFIED, NOT FIELD-DEPLOYABLE.**

ATDA is a sensor-agnostic architecture for distributed chemical-trace awareness around soft targets (transit gates, kiosks and ATMs). It separates immediate high-confidence explosives/CBRN interdiction from anonymous background analytics. It is not a person-tracking or policing platform.

## Provenance matters

- Architectural origin: V. Panov, original white paper dated **2025-12-05** (see `docs/PROVENANCE.md`).
- GitHub repository existed from 2025-12-05. The preserved original commit, dated **2026-01-30**, contains **one textual Markdown-like file misnamed `.json`**, despite claiming further attachments in its commit message.
- This **2026-10-27 v1.2** package is newly reconstructed and tested from the public architecture and available design notes. **Do not misattribute this source code to 2025.**
- Original file `ATDA_Privacy_Safety_Manifest_v1.json` is retained UNMODIFIED as historical evidence; it is invalid JSON.

## Two independent data paths

| Path | Purpose | Gate | Privacy / safety invariant |
|---|---|---|---|
| **A** | Verified high-consequence explosives/CBRN threats | Independently validated high-confidence decision | No PII, constrained incident schema, authenticated authorised recipients; cleaning agents mean MAINTENANCE ONLY |
| **B** | Narcotics/biohazard background aggregate statistics | Hardware PII stripping **before buffering**, then local **>=50 distinct interaction events**, adaptive windows 15 min to 24 h | No payment identifiers, no record-level exports, no cross-epoch linkage, no person-level enforcement |

The repository **does not implement** Path A's detection/classification stack, hardware data diode, tamper-resistant PII stripping, secure boot, TPM attestation, or an actual network transport. It contains an independent, **synthetic-data-only Path B reference**.

## Privacy limits (read before deployment)

A hard deterministic `k>=50` no-output boundary and a non-zero probability of a published aggregate at 50 interactions **cannot together provide end-to-end pure epsilon-DP** with respect to add/remove passage adjacency. The output/no-output indicator itself reveals information. The included two-sided geometric noise **can provide epsilon = ln(2) ~= 0.693 per FIXED noninteractive bucket-vector query** under the ideal randomness and fixed schema assumptions. It **cannot** make the entire adaptive-window release protocol pure epsilon-DP. The code therefore makes NO end-to-end, user-level or legal-anonymisation claim. See [`docs/PRIVACY_PROOF.md`](docs/PRIVACY_PROOF.md).

`k` counts validated interactions, not unique humans. An attacker can cause 50 interactions themselves. Risk of differencing, temporal leakage, sparse geography and auxiliary data must be assessed in a DPIA and red-team tests.

## Files and navigation

- [`src/atda_pathb_fortress.py`](src/atda_pathb_fortress.py) - stdlib-only reference code for locally buffered interaction totals, exact-set deduplication and geometric noise.
- [`tests/`](tests/) - deterministic unit, failure, distribution and manifest tests.
- [`manifest/ATDA_Privacy_Safety_Manifest_v1_2.json`](manifest/ATDA_Privacy_Safety_Manifest_v1_2.json) - valid machine-readable release claims (including explicit negative assurances).
- [`specs/ATDA_Technical_Spec_v1_2.md`](specs/ATDA_Technical_Spec_v1_2.md) - consolidated normative/proposed architecture specification.
- [`docs/PRIVACY_PROOF.md`](docs/PRIVACY_PROOF.md) - k-gate impossibility and DP mechanism assumptions.
- [`docs/PQC_MIGRATION.md`](docs/PQC_MIGRATION.md) - NIST FIPS 203/204/205, RFC 10024 and migration guidance.
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) - STRIDE/DREAD, risk owners, attack paths and controls.
- [`docs/TCO_AND_ROADMAP.md`](docs/TCO_AND_ROADMAP.md) - hypothetical 7-year TCO comparison, milestones and open R&D.
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) - what was genuinely recovered versus reconstructed.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) - pinned checkout and standard-library test run.
- [`SECURITY.md`](SECURITY.md) - reporting restrictions and red lines.

## Run the reference tests

Python **3.10+**, no external packages:

```bash
python3 -m unittest discover -s tests -v
python3 manifest/validate_manifest.py
```

The unit tests do not prove a cryptographic primitive is FIPS validated, do not replace an independent privacy audit, and do not establish laboratory sensor false-positive rates.

## Reference usage (synthetic interactions ONLY)

```python
from src.atda_pathb_fortress import FortressBuffer, SanitizedPassage

buf = FortressBuffer('ZONE_A')
for i in range(50):
    buf.ingest(SanitizedPassage(i.to_bytes(16, 'big'), 'NARCOTICS'), now_utc_min=1)
aggregate = buf.checkpoint(now_utc_min=15)
assert aggregate is not None   # values are randomised, not the true counts
```

Synthetic tokens above are demonstration-only: production sensors MUST mint cryptographically random tokens behind a tested hardware PII boundary; sequential tokens are never acceptable in deployment.

## PQC: design baseline, not an implementation claim

- Key establishment: implement approved, mutually authenticated transport with **ML-KEM-768** (NIST FIPS 203) or applicable hybrid TLS 1.3 supported groups in **RFC 10024**.
- Digital signatures: plan **ML-DSA-65** (NIST FIPS 204) for software/firmware signatures subject to platform and ecosystem support; keep rollback-safe, signed upgrade chains.
- Do **not** claim `TPM 2.0` alone is quantum-safe or that merely using an approved algorithm creates FIPS 140-3 validation.
- Select an independently validated FIPS module/configuration when required by contracts and review supplier evidence before procurement.

See [`docs/PQC_MIGRATION.md`](docs/PQC_MIGRATION.md) for procurement tests, crypto agility and alternatives.

## Standards and legal posture

Architecture mapped (NOT certified) to NIST SP 800-53 Rev. 5: SC-12/SC-13, SI-7, IA-3, AU-9; ISO/IEC 27001:2022 Annex A 8.24 (cryptography); IEC 62443-3-3 SR 1.1/3.4/4.3; GDPR Articles 5, 25 and 35. **k-anonymity and DP are not self-executing GDPR exemption certificates.** External legal and data protection assessment required.

## Distribution and IP

The original 2025 architectural white paper describes itself as an open defensive publication. A distinct licence grant for new reference **code** has not been verified. This release intentionally makes no new licensing promise; obtain legal guidance and select a licence before encouraging third-party code reuse. Publication preserves chronological evidence; it does **not** prove novelty, priority of invention, usage by NIST, or patent rights.

## Next engineering blockers

1. Verify a real hardware PII stripping chain (including observability channels and DMA), sensor-issued 128-bit passage tokens, and measured physical distinctness.
2. Decide with the controller/DPO whether strict `k>=50` or formal **end-to-end** pure DP is required. Both cannot be asserted for this hard-gate protocol as written.
3. Validate sensing classifier performance and anti-bleach maintenance-only response using authorised laboratory studies.
4. Verify secure boot, firmware signatures, TPM/HSM hardware paths and timing on a selected bill of materials.
5. Run privacy attack simulations, penetration testing and DPIA before claiming anonymisation.
