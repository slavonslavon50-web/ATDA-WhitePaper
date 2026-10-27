# ATDA HW-01 — Low-cost laboratory prototype procurement and milestones
**Date:** 2026-10-27 | Proposal only; supplier pricing, parts availability and suitability NOT verified.
Currency in EUR; arithmetic is an illustrative planning budget, **not a vendor quotation**.

## Design-for-test BOM options
| Item | Qty | Illustrative unit budget (EUR) | Extended |
|---|---:|---:|---:|
| Small MCU development boards for acquisition, A simulation and B aggregation | 3 | 30 | 90 |
| TX-only optical isolation module / separate receiver and test fixtures | 2 | 20 | 40 |
| Separate regulated supplies, protected wiring and connectors | 1 lot | 65 | 65 |
| GPIO/microcontroller synthetic interaction simulator | 1 | 30 | 30 |
| Basic secure element evaluation module (optional Gate 2) | 1 | 45 | 45 |
| Logic-analysis / USB test adapter or rented access | 1 | 55 | 55 |
| Cable labelling, tamper tags, enclosure, passive components | 1 lot | 60 | 60 |
| **Illustrative subtotal** | | | **385** |
| 25% contingency rounded | | | **96.25** |
| **Illustrative budget envelope** | | | **481.25** |

No lab time, tax, shipping, outsourced PCB design, high-grade ESD/EMC testing, accredited certification, actual chemical sensor, air-flow hardware, PII legal review or production TPM is included. No claim that the example secure element supports post-quantum signatures or FIPS 140-3. Avoid buying specific components until a requirements-to-part matrix is signed.

## Prototype baseline
- **Gate 0 / paper and software:** schema, negative-connectivity netlist requirements, privacy proofs/limits, Python simulator contract and unit tests.
- **Gate 1 / bench electrical:** 3 low-cost independent boards, simulated counts and classes, test fixtures, blocked payment interfaces, physical one-way Path B aggregate output, measurement harness.
- **Gate 2 / trust:** verified secure boot and reproducible signed update on chosen silicon, controlled rollback, physical debug lockdown, attestation design backed by vendor capabilities.
- **Gate 3 / security and privacy verification:** independent red team, bounded covert-channel study, evidence-led DPIA, sensor failure modes; no live payment data.
- **Gate 4 / optional field feasibility:** reviewed customer-specific integration only after protection objectives, safety case, procurement certification and independent legal approval.

## Procurement questions — hard stop
1. Can the supplier provide device/board schematics, data-sheet revisions, pinout and lifecycle through project horizon?
2. Is unidirectional isolation actually electrically implemented and measurable? What are isolator common-mode and power side-channel ratings?
3. Is there a verified boot root, monotonic version/anti-rollback storage, immutable recovery and tested secure debug state?
4. How will signer keys be protected? Does the cryptographic module carry an exact applicable FIPS 140-3 certificate and approved configuration, if contractually required?
5. Can sensor-only ingress and Path A independent service be demonstrated under a compromised/failed Path B?
6. What is the supplier's security advisory, SBOM, vulnerability support, secure repair and end-of-life process?
7. Are all outgoing fields and maintenance interfaces deterministic, finite and independently documented?

## Cost-benefit logic
The first €481.25 **illustrative** lab envelope buys a way to falsify the claim 'PII cannot enter Path B.' It does NOT buy a chemically reliable detector or certified infrastructure device. A rushed monolithic sensor-plus-payment prototype would cost more and make the privacy assurance weaker. Spend on measurement and published evidence before polishing sensor algorithms.

## Open R&D questions
- Can a realistic interaction sensor assert distinct passage events while being resistant to replay and customer-specific identity inference?
- How to constrain/quantify covert timing leakage at the physical aggregate-only diode?
- Will an independent A/B architecture maintain common sensor health signals without introducing a feedback covert channel?
- Does the chosen Root of Trust support a credible and upgradable ML-DSA chain over 2026–2040?
- How can low-volume sites produce useful analytics under k=50/24-hour expiry without a surveillance incentive to merge identity-bearing contexts?
