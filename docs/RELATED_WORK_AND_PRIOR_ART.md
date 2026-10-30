# ATDA — Related Work and Prior Art

**Review date:** 30 October 2026  
**Status:** preliminary, source-linked engineering comparison; **not** an exhaustive novelty search, patent freedom-to-operate (FTO) opinion, plagiarism certification, product certification, or official GitHub Release.

## Executive assessment

ATDA integrates established mathematical, hardware-security and sensing concepts into a documented two-path **research architecture**. The public October 2026 reference is a new reconstruction of the 2025 architectural requirements, **not** recovered original 2025 software. A novel combination, non-infringement, legal anonymisation and actual hardware privacy have **not** been demonstrated. The present review identifies technical overlap and concrete distinctions to test, without claiming originality by absence of search hits.

The distinction between **known mechanisms**, **ATDA-specific design choices** and **unverified assurance claims** must accompany any public or procurement material.

## Source-to-claim comparison

| Topic | Prior work | ATDA use and evidence | Boundary of defensible claim |
|---|---|---|---|
| k-anonymity | Sweeney (2002) formalises protection for **persons** in released data [R1]. | The [reference kernel](../src/atda_pathb_fortress.py) gates on 50 distinct **interaction events** per local epoch. | 50 interactions are **not 50 distinct people**; this is not person-level k-anonymity or certified GDPR anonymisation. |
| Geometric mechanism | Ghosh, Roughgarden & Sundararajan's 2008 preprint/2009 work [R2] and Dwork & Roth (2014) [R3]. | `two_sided_geometric` implements the difference of two geometric draws. Under ideal fixed-query assumptions, q=1/2 yields ε=ln2 for one-passage add/remove adjacency. | The mechanism is known prior art; the deterministic 49/50 publish/no-publish event prevents a **whole-protocol pure ε-DP** guarantee. See [proof](PRIVACY_PROOF.md). |
| Streaming adaptive windows | PeGaSus (2017) [R4], Re-ADP (2018) [R5], and adaptive DP trajectory stream work (2018) [R6]. | Local checkpoints at 15, 30, 60, 120, 240, 480, 960 and 1440 minutes; no statistical release below k=50; expiry if under threshold after 24 h. | Edge aggregation and adaptive windows were known. Prior work's privacy theorems **do not transfer** to our hard gate. |
| Stream anonymisation / dynamic k | US20180131740A1 (2018) [P2], and *Dynamic K-Anonymity* technical disclosure dated 29 June 2026 [R7]. | ATDA extends the window but holds the minimum interaction count at k=50. | Thresholded time-aware aggregation alone is not demonstrably unique. R7 is later than the dated 2025 ATDA concept but earlier than the October 2026 reconstructed code. |
| Transit chemical sensing | US20090072024A1, *Transit security detection system* (2009 publication; reported 2005 priority) [P1]. | ATDA proposes physically isolated payment/sensing domains, separate independently verified threat alerts (Path A), and coarse Path B aggregates without payment IDs. | Sensors at transit gates are prior art. An architecture distinction from particular P1 disclosures does **not** prove novelty or freedom from its claims. |
| Data diodes | NIST defines a hardware-enforced unidirectional data flow [S1-S2]. | Proposed [HW-01](../hardware/HW01_ARCHITECTURE.md) isolates sensors and calls for unidirectional aggregate egress. The [four-byte lab frame](../src/hw01_boundary_contract.py) is only a software schema test. | Neither data diodes nor isolation are ATDA inventions; physical PII exclusion and one-way electrical transmission are **not built/tested**. |
| Post-quantum standards | NIST FIPS 203/204/205 (13 August **2024**); hybrid TLS RFC 10024 (August **2026**) [S3-S6]. | [PQC migration plan](PQC_MIGRATION.md) specifies candidate algorithms and procurement/anti-downgrade checks. | Algorithms were developed externally; no ML-KEM/ML-DSA transport, secure-boot implementation, CMVP validation or quantum-resistance of a deployed ATDA system is established. |
| OT governance | NIST SP 800-53, SP 800-82, IEC 62443, ISO/IEC 27001 [S1,S7-S8]. | Threat/requirements crosswalk for future procurement and validation. | References are **not certifications or endorsements**. |

## Patent publications (focused, non-exhaustive)

**[P1] US20090072024A1 — Transit security detection system.** Google Patents reports earliest priority **8 March 2005**, filing **11 August 2008**, and publication **19 March 2009**, with transit hazard sensors, portal action and fare-media information. A potential ATDA design difference is the *prohibition* on payment-identity ingress into Path B and its statistical-only purpose. This does not show that every claim is avoided or that other patents lack similar isolation concepts. A lawyer must inspect the granted claims, prosecution and national family members for the actual proposed device.

**[P2] US20180131740A1 — Anonymizing streaming data.** General Motors LLC, priority/filing **4 November 2016**, published **10 May 2018**. It discusses anonymised data representations and time-constrained stream processing. It is evidence of a pre-existing field, **not** evidence that ATDA copied its source or necessarily implements its patent claims. A reported US abandoned status must not be extrapolated to other jurisdictions or patent families. [P2](https://patents.google.com/patent/US20180131740A1/en)

Patent applications, grants, priority dates, published claim wording, expiration and national rights are distinct questions. **A published patent is evidence of disclosure, not automatic proof of enforceable rights or infringement.** Google Patents' legal status is informational, not legal advice. No FTO clearance is claimed for the USA, EU or UK.

## ATDA chronology and provenance constraints

| Date | Evidence | Limitation |
|---|---|---|
| **5 December 2025** | Author-dated original `WhitePaper_ATDA_Privacy_Preserving_Detection_2025_v5.pdf`; repository creation documented in [provenance](PROVENANCE.md). | A repository creation date or PDF file date does not alone prove that every detailed algorithm was publicly disclosed that day. |
| **30 January 2026** | GitHub root commit [a754b3f](https://github.com/slavonslavon50-web/ATDA-WhitePaper/commit/a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1) preserves one actual text artifact, despite a broader commit message. | No recovered full implementation in that commit. |
| **29 June 2026** | *Dynamic K-Anonymity* technical disclosure [R7]. | After the original author-dated white paper; before new reference code. |
| **27 October 2026** | Reconstructed Python, tests, privacy correction and security plan committed. | New software work; not retrospectively original 2025 code. |
| **30 October 2026** | This targeted literature/patent review. | Not comprehensive or independently certified. |

**Chronology correction:** FIPS 203, 204 and 205 were published in **August 2024**, before the dated ATDA architecture. The **August 2026** RFC 10024 hybrid TLS document came after it. No ATDA influence on either is claimed.

**Attribution:** V. Panov's 2025 white paper documents the ATDA concept. The 2026 Python reference is a **new AI-assisted reconstruction** under the project's direction, using established public mathematics. This is not proof of uniqueness; independent implementation and reuse of known methods are compatible.

## Evidence and verification gaps

| Engineering claim | Current evidence | Missing evidence |
|---|---|---|
| 50-event checkpoint gate | Python tests and synthetic demo | Authentic sensor interaction origin, replay resistance, real clock and board-level tests |
| PII removed before buffering | Proposed HW-01 schema and 16 planned verification cases | Isolated circuit schematic/netlist, actual electrical, DMA/debug, timing and fault-injection tests |
| Safety/cleaner anti-false-alarm logic | Requirements and threat analysis | Representative lab detection sensitivity/specificity, false-alarm and interferent tests |
| Real PQC protection | NIST standards and proposed migration roadmap | Supported hardware and TLS library, keys/certificates, anti-downgrade trials, FIPS module evidence |
| Privacy assurance | Conditional mathematical analysis with explicit threshold counterexample | Whole-system linkability and composition assessment, DPIA and independent review |
| Originality and licensing | This targeted source comparison and recorded Git history | Broader code similarity audit, licenses review, professional prior-art novelty and jurisdictional FTO review |

## Recommended gates before official v1.2 Release

1. Maintain this source ledger with dates, scope, exact overlapping function and direct source URLs; invite reviewers to challenge each row.
2. Map the actual proposed hardware/software product feature-by-feature against relevant **granted claims and families** in USA, UK and EU using professional patent counsel before procurement.
3. Independently check source-level similarity and licence obligations. A matching mathematical formula, short name or known protocol does not alone establish copyright infringement.
4. Preserve original dated PDF bytes, metadata and preferably SHA-256, without rewriting Git history or asserting public 2025 disclosure of later code.
5. Complete hardware privacy and sensor tests; distinguish the 50-*event* gate from person k-anonymity, whole-protocol DP and GDPR certification.
6. Select an explicit code licence and release governance; **no official v1.2 Release has been created**.

## References

### Research and technical disclosures
- **[R1]** L. Sweeney (2002), *k-Anonymity: A Model for Protecting Privacy*: https://doi.org/10.1142/S0218488502001648
- **[R2]** A. Ghosh, T. Roughgarden, M. Sundararajan, *Universally Utility-Maximizing Privacy Mechanisms*, arXiv preprint (2008): https://arxiv.org/abs/0811.2841
- **[R3]** C. Dwork, A. Roth (2014), *The Algorithmic Foundations of Differential Privacy*: https://doi.org/10.1561/0400000042
- **[R4]** Y. Chen et al. (2017), *PeGaSus: Data-Adaptive Differentially Private Stream Processing*: https://doi.org/10.1145/3133956.3134102
- **[R5]** *Re-ADP: Real-Time Data Aggregation with Adaptive ω-Event Differential Privacy for Fog Computing* (2018): https://doi.org/10.1155/2018/6285719
- **[R6]** *An Adaptive Window Size Selection Method for Differentially Private Data Publishing over Infinite Trajectory Stream* (2018): https://doi.org/10.1155/2018/8297678
- **[R7]** *Dynamic K-Anonymity*, Technical Disclosure Commons (29 June 2026), a technical disclosure, **not claimed to be peer reviewed**: https://www.tdcommons.org/dpubs_series/10641/

### Patent publications
- **[P1]** US20090072024A1, *Transit security detection system*: https://patents.google.com/patent/US20090072024A1/en
- **[P2]** US20180131740A1, *Anonymizing streaming data*: https://patents.google.com/patent/US20180131740A1/en

### Standards and legal guidance
- **[S1]** NIST SP 800-82 Rev.3 (2023), *Guide to OT Security*: https://csrc.nist.gov/pubs/sp/800/82/r3/final
- **[S2]** NIST CSRC, *Data Diode* definition: https://csrc.nist.gov/glossary/term/data_diode
- **[S3]** NIST FIPS 203 (13 August 2024): https://csrc.nist.gov/pubs/fips/203/final
- **[S4]** NIST FIPS 204 (13 August 2024): https://csrc.nist.gov/pubs/fips/204/final
- **[S5]** NIST FIPS 205 (13 August 2024): https://csrc.nist.gov/pubs/fips/205/final
- **[S6]** IETF RFC 10024 (August 2026): https://www.rfc-editor.org/rfc/rfc10024.html
- **[S7]** NIST SP 800-53 Rev.5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- **[S8]** ISA/IEC 62443 series: https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- **[L1]** Irish Data Protection Commission, anonymisation and pseudonymisation guidance: https://www.dataprotection.ie/en/dpc-guidance/anonymisation-pseudonymisation

**Author and scope note:** This document attributes the original ATDA architectural concept to V. Panov's dated 2025 white paper and the new 2026 reference implementation to its actual development period. None of the cited third-party works is presented as ATDA-owned IP. This review is non-exhaustive and is not legal advice.
