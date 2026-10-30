# Change log

## Unreleased documentation update - 2026-10-30

- Created [`docs/RELATED_WORK_AND_PRIOR_ART.md`](docs/RELATED_WORK_AND_PRIOR_ART.md): a source-linked prior-art comparison of known DP methods, adaptive streaming, data diodes, hazard sensing and related patent publications, with claim boundaries and gaps.
- Added a [GitHub Pages prior-art overview](https://slavonslavon50-web.github.io/ATDA-WhitePaper/related-work.html) and linked it from README and the demo home page.
- Cross-referenced the comparison in technical specification, mathematical privacy proof, PQC plan and provenance history.
- Corrected the chronological claim: NIST FIPS 203/204/205 published **August 2024**, before the dated 2025 ATDA concept; IETF RFC 10024 appeared in **August 2026**.
- No privacy gate, executable algorithm, hardware claim or deployment changed. **Official GitHub Release v1.2 not created.**

## 1.2.0 - 2026-10-27 (new reconstruction, not a claim of prior authorship date)

- Restored provenance links to the original 2025 architectural white paper and preserved the 2026-01-30 GitHub commit/file.
- Added a strict valid JSON privacy/safety manifest with negative assurance fields.
- Built a Python 3.10+ no-dependency synthetic Path B reference with a 50-interaction hard gate, exact-set dedup, 15-to-1440-minute adaptive windows, one category per passage, non-overlapping epochs, checked capacity and fail-closed time.
- Added a rational-parameter two-sided geometric sampler and independent tests.
- Added a mathematical counterexample explaining why deterministic hard k gating is not compatible with end-to-end pure epsilon-DP when release timing is observed.
- Added PQC migration design for FIPS 203/204/205 and RFC 10024 without pretending to implement PQC primitives or certified attestation.
- Added STRIDE/DREAD, hypothetical procurement TCO, acceptance roadmap, security disclosure policy and GitHub CI.

### Compatibility

This new package is a research reference. It is NOT byte-for-byte recovery of missing January 2026 source artifacts; there is no claim of production certification, GDPR anonymisation, field chemical performance, or NIST influence.
