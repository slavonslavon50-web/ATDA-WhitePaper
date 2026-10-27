# Contributing to ATDA research

ATDA welcomes **critical review**, not unsubstantiated endorsements. Contributions should help falsify assumptions, reproduce reference results or strengthen privacy safeguards for distributed sensor deployments.

## High-value contributions

- Report concrete privacy counterexamples (especially threshold leakage, sparse-site correlation, multi-epoch composition and input spoofing).
- Reproduce Python reference tests using synthetic inputs and identify failing cases with exact steps, environment and expected/actual output.
- Review hardware HW-01 trust-boundary and prohibited-connection checks: isolate payment/access hardware from all sensor analytics interfaces.
- Compare proposed cryptographic procurement requirements against vendor documentation and applicable standards. Do **not** submit bespoke cryptographic implementations or claims of unsupported certification.
- Critique cost assumptions, false alarm models, environmental interferents and use limitations.

## Before opening an issue

Check the [readme](README.md), [privacy limitations](docs/PRIVACY_PROOF.md), [threat model](docs/THREAT_MODEL.md) and [security policy](SECURITY.md). Describe the problem, relevant file and line, a minimal synthetic reproduction and how you would measure success. Keep issue titles descriptive, e.g., `Path B: checkpoint timing after 49 -> 50 transitions`.

**Never submit** real payment/card data, biometric samples, identifiable observation logs, detailed operational protection bypasses, real malicious chemical recipes, source-code signing keys, deployed device addresses or unknown third-party proprietary materials. For potentially sensitive vulnerabilities follow [SECURITY.md](SECURITY.md) instead of filing a public issue.

## Review standards

The current code is a reconstructed research reference from 27 October 2026. A merged pull request should have a scoped explanation, appropriate regression tests, revised privacy claims where necessary, and no invented evidence of certification. No peer review or compliance approval is implied by GitHub CI.

## Licensing

The original architecture is publicly disclosed, but the repository **does not currently provide an explicit code licence**. Contributors should not assume a right to redistribute or commercially reuse the reference implementation. The maintainer should decide an appropriate licence and clarify contribution terms before accepting substantive third-party code contributions.
