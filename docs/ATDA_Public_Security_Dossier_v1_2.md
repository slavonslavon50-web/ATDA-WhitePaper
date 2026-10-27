---
title: "ATDA | Technical Security & Privacy Specification"
subtitle: "Public Sanitised Reference - Reconstruction v1.2.0"
author: "V. Panov | Original architectural concept (2025)"
date: "27 October 2026"
lang: en-GB
colorlinks: true
links-as-notes: false
abstract: |
  This specification preserves provenance of the 2025 ATDA white paper,
  identifies the hard k=50 versus pure epsilon-DP incompatibility, documents
  independent Path A/B governance, and proposes a post-quantum migration path.
  The included source is synthetic-data reference code only; no production,
  GDPR anonymisation, FIPS 140-3 or sensor detection certification is claimed.
---

# Document control and limitations

**Edition:** ATDA v1.2.0, 27 October 2026. **Readiness:** research reference, NOT field-deployable. The original authored white paper was dated 5 December 2025; the code in this package was reconstructed in October 2026. An earlier GitHub commit misleadingly lists artifacts that are absent from its Git tree. Historical evidence remains unchanged.

**Decision:** Preserve strict local k>=50 no-output policy; do not claim end-to-end pure differential privacy for the combined adaptive-window release protocol. Formal noise guarantee applies only to fixed bucket-vector query under idealized assumptions; read the proof appendix.

**NOT included:** hardware payment-data stripping, TPM PQC attestation, validated sensor classification, incident escalation logic, actual cryptographic KEM implementations, field performance results, DPIA or certification.


\clearpage

# Part 1: Consolidated technical specification

**Public Sanitised Reference / 27 October 2026**

**Originator:** V. Panov (ATDA architectural concept, 05 December 2025)  
**Implementation status:** independently reconstructed Python research reference, **NOT field/production ready**.  
**Scope:** dual-path data processing, privacy, assurance, crypto agility, procurement and controls for distributed chemical-trace sensing in soft targets (2025-2040 programme).

> **Normative distinction.** `SHALL` means a proposed mandatory system requirement subject to deployment contract and audit; `SHOULD` means a recommended engineering control; `MAY` means optional. This public document is not a government-issued standard or certification.

## 1. Executive safety case and priorities

ATDA addresses two specific infrastructure problems. First, high-consequence chemical threats may need urgent escalation, but incidental environmental contamination must not trigger unsustainable emergency traffic. Second, background narcotics or biohazard observations can inform public health and infrastructure planning only if data are structurally unable to reconstruct a person's payments, travel or access history. A purely software-based deletion of payment IDs after ingest is insufficient: identity isolation must occur before Path B memory is exposed to untrusted processing.

The **highest-value/lowest-complexity starting control** is an explicit, fail-closed hardware-verified schema boundary and a demonstrable independent data path. Purchase no bespoke cryptography until these fundamental trust conditions, device updateability and governance are documented. Modern crypto protects the channel but cannot anonymise data that should never have entered it. Conversely, the absence of payment IDs alone does not anonymise site/time aggregates if they can be joined against external observations.

The reference release includes no sensor detection model, no payment interface, no operational threat thresholds, no CBRN attack signatures, no live deployment topology and no secret key. The reference Python only illustrates an independently auditable Path B counting mechanism. A field deployment requires materially more work and evidence.

### 1.1 System goals

- `G-1` Permit real-time, verified high-confidence explosives/CBRN alerts with independent safety governance.
- `G-2` Keep Path B limited to coarse, purpose-specific statistics; no identification or person-level enforcement.
- `G-3` Enforce hardware PII removal before buffering; prohibit joins back to payment or access transactions.
- `G-4` Withhold Path B publication until at least 50 **distinct validated interaction events**, expand windows adaptively up to 24 h, then expire under-k data.
- `G-5` Guarantee that isolated household-cleaning interferents produce maintenance, not security alert, while independently validated high-consequence threats retain their own evidence workflow.
- `G-6` Provide cryptographic agility and a migration path to modern post-quantum transport and software signatures without claiming untested platform capabilities.
- `G-7` Preserve auditability, source provenance, legal transparency and independent third-party validation.

### 1.2 Exclusions

No automatic individual criminal suspicion, low-level drug interdiction, hidden per-user biometrics, payment-card identifiers in Path B, backdoors from analytics to incident logic, unconstrained sensor log retention, unsupported anonymisation guarantees, unfounded FIPS/ISO/IEC certification assertions or unauthorised direct law-enforcement access to Path B are permissible under the reference policy.

## 2. Reference system contexts

The architecture is sensor-agnostic. Physical embodiments may include bank ATM surfaces, ticketing kiosks, transit turnstiles or controlled gateway devices. These are example form factors; no universal claim is made that current low-cost sensors can perform reliable walk-through discrimination for all target analytes under all field conditions. The original research explores near-field active air sampling, spectroscopy and e-nose arrays with limitations including air flow, laser safety, drift, measurement time and interferents. Deployment requires laboratory characterization on representative units and rigorous false alarm budgets.

### 2.1 Context boundary

```
[payment/access CPU, sensitive PII] -- physically isolated; no Path B link --> [FORBIDDEN]
                                              [sensor observation]
                                                        |
                                              [trusted acquisition]
                                                        |
                                            [hardware-classification]
                                                      /   \
                                             Path A      Path B
                                       validated threat  PII strip before buffer
                                              |                 |
                                        signed alert        exact-set local k gate
                                              |                 |
                                     incident gateway       coarse noisy aggregate
                                              |                 |
                                       authorised SOC       analytics gateway
```

The diagram is conceptual. Physical separation must be evidenced via bus-level diagrams, isolation analysis, boot chain coverage and adversarial testing of debugging/DMA paths. A logical `if` statement in Python is **not** a data diode.

### 2.2 Physical trust domains

**TD0 untrusted environment:** public space, users, cleaning products, environmental turbulence, electromagnetic noise. **TD1 sensor-acquisition:** sensing hardware/driver and health diagnostics; may observe chemically sensitive but not payment-identifying signals. **TD2 PII firewall:** hardware-enforced one-way schema/traffic constraint between payment/access and protected aggregation; ideally no direct data path from payments to chemical subsystem. **TD3 Path A:** high-confidence threat rules, restricted incident schema and signed operations channels. **TD4 Path B:** isolated memory containing only aggregate counts and short-lived random interaction tokens. **TD5 fleet trust:** signed firmware, attestation, gateway policy, certificate life cycle, independent audit. Crossing TD2/TD3/TD4 is prohibited without separately validated interfaces.

### 2.3 Threat assumptions

Attackers can trigger repeated benign interactions, spill cleaning agents, block airflow, interfere with sensing, replay network packets, compromise a supplier or attempt to correlate releases with external observations. A state-level adversary may record encrypted traffic for later quantum decryption. None of these should be modeled as merely random noise. Insider analysts may correlate small geographic/time outputs to payment/transport logs even if Path B never receives those identifiers. The DPIA must test these linkability hypotheses explicitly.

## 3. Path A: high-consequence interdiction

Path A is restricted to independently calibrated, above-high-confidence detections for explosives/CBRN threats. Events SHALL be structured to the minimum necessary for response: bounded coarse source identifier or designated site code, UTC event time, threat classification, confidence/evidence indicator, hardware health/quality, event sequence/nonce, signed integrity state and a reference to a restricted incident workflow. No payment identifier, customer account, access-card number, biometric or raw card payload belongs in the event. Exact security thresholds and sensor signatures are outside the public baseline and MUST be governed by secured validation profiles.

### 3.1 Interferent logic

A cleaning/disinfectant/bleach/peroxide indicator by itself SHALL map to `MAINTENANCE_FLAG`, not `SECURITY_ALERT`. The decision SHALL be confirmed by multi-channel evidence and calibration appropriate to the sensor technology. A cleaning signal must not be an unrestricted suppression switch that masks an independently validated high-consequence threat. When signatures are ambiguous, the system SHALL report diagnostics and abstain rather than fabricate confidence. The optimal safety policy depends on sensor confusion-matrix evidence from controlled research.

### 3.2 Alert transport

The verified alert path SHOULD maintain a mutually authenticated session, enforce sequence/nonce freshness, reject replay and validate gateway/recipient authorisation. Cryptography SHALL be selected from a documented accredited suite (FIPS 140-3 validated modules where contractually mandated) and SHOULD follow the migration guidance in the PQC annex. Network downtime SHALL be raised as a health fault, not silently interpreted as clean sensor evidence. Incident workflow and access are a different administrative domain from Path B.

### 3.3 Path A acceptance

`A-01` A cleaner-only test must not emit a security alert. `A-02` Independently verified threat samples under documented test conditions must meet agreed sensitivity/specificity/latency targets. `A-03` Tampered signatures, stale timestamps, revoked certificates and replayed IDs must be rejected or quarantined. `A-04` There must be no permission edge from the analytics role to the alert/threshold controller. `A-05` Laboratory interference cases shall include simultaneous benign interferent and actual certified test threat under authorised safe handling.

## 4. Path B: permitted analytical purpose

Path B is for background traces, long-term baselines and strategic risk/public-health statistics. It SHALL NOT be used for individual identity matching, low-level enforcement, probable-cause triggers or linkage with payment-card/access event logs. Only approved coarse zone IDs and fixed, low-dimensional category labels may appear in aggregate output. The classification set is defined in signed policy rather than supplied by arbitrary clients; any change resets the privacy analysis.

### 4.1 Local schema and identity isolation

Only `SanitizedPassage(token: bytes[16], bucket: public fixed category)` crosses into the reference buffer. In a real device, this object must be created **only after hardware-level stripping of all identity fields**, including payment IDs, device payment session IDs, network correlators and per-transaction timestamp fields. The 128-bit token is independent random material representing one validated passage. It must not be a hash or reversible transform of person-related data. This reference cannot verify token origin or hardware enforcement; the manifest reports `hardware_strip_pii_verified: false`.

### 4.2 Distinctness meaning

Distinct **interactions** are not necessarily distinct natural persons. One person can legitimately pass 50 times; a saboteur can generate 50 sensor triggers. Therefore `k>=50` is a density/aggregation threshold, not a strong individual-anonymity theorem. Tokens need replay resistance, uniqueness under sensor clock reboot and rolling key epochs; all such guarantees require trusted capture/attestation equipment and operational validation.

### 4.3 Buffer rules

The buffer SHALL be in protected local memory, not raw transaction logs. It retains only an exact set of interaction tokens and bounded counts per fixed category, with total and per-bucket capacity guards. On duplicate token, input is rejected without increment. On capacity overflow, fail closed and flag local maintenance/security diagnostics, not silent record replacement or Bloom dedup approximation. On clock rollback, missed checkpoint or untrusted startup state, zeroise logical state, prohibit release and log only an authorised non-identity health indication. The reference uses `clear()` on Python objects, not a certified RAM zeroisation procedure.

### 4.4 Adaptive aggregation

Window sequence: `15, 30, 60, 120, 240, 480, 960, 1440` minutes. The first window is aligned to a 15-minute UTC boundary; checkpoint execution is a local timer obligation. If <50 distinct interactions have been counted, the next window begins without releasing. If >=50, the epoch may publish one noisy aggregate at its checkpoint and is immediately reset. At 24h with <50, discard without publication. Output includes coarse zone, window start, aggregate duration and fixed category counts after independently sampled noise and nonnegative post-processing. It MUST NOT include true n, raw interaction tokens or data-dependent per-passsage timestamps.

There can be no guarantee that adaptive output timing is itself differentially private; see privacy appendix. Repeated fixed-window releases across adjacent sites remain linkable without separate risk controls. The backend SHALL NOT permit arbitrary analyst-driven drill-down or threshold changes.

## 5. Formal privacy analysis and proof obligations

Fix a public bucket vector of dimension three. Every passage maps to exactly one category; add/remove one passage has L1 count-vector sensitivity 1. Under ideal independent randomness and pre-fixed always-release schedule, two-sided geometric noise `P(Z=z)=((1-q)/(1+q))*q^abs(z)` with `q=1/2` yields epsilon=`ln 2`. Integer draws implement the reference distribution; no data-dependent clamping occurs prior to sampling. Post-processing `max(0, noisy_count)` is permitted for a **fixed-query** DP mechanism, but clamps should be reflected in analytic bias estimates when counts are near zero.

### 5.1 Critical counterexample

No payload is permitted when true n<50. A 49-passage database yields zero probability of a statistical release at its checkpoint. A neighbouring 50-passage database has positive probability of releasing. For the event 'a release occurred', the pure DP likelihood inequality cannot hold with any finite epsilon. Therefore neither the historical phrase 'DP-clean k-gate' nor the code's correct noise sampling justifies claiming end-to-end pure differential privacy. This limitation is explicitly surfaced in README, JSON manifest, privacy proof and release notes; suppressing it would be misleading to integrators and regulators.

### 5.2 Scope that remains useful

The hard k boundary still enforces a clear system policy, and released counts have randomisation useful against some inference attacks. The combined system is an **engineering privacy control set** with mathematically bounded noise on fixed queries, **not a certified pure-DP channel**. The regulator's anonymisation assessment requires independent review of reasonably likely re-identification through site/time auxiliary information. A site with low traffic and an identifiable queue can reveal presence from timing even if each count has two-sided geometric noise. Fixed windows and coarser geography improve resilience but cannot automatically convert the hard-gated mechanism to pure DP.

### 5.3 Protection measures beyond k

The controller SHALL document a site-level DPIA and retention schedule. Operator analysts SHOULD receive coarse region aggregates under least privilege, with query-rate controls, anti-differencing audit and published data minimisation rules. No analyst-supplied new dimensions may be added to an already collected cohort. Auxiliary join experiments using synthetic payment/transport traces and CCTV timestamps SHALL measure residual membership-inference risk before operational deployment.

## 6. System health, maintenance and sabotage resilience

The sensor health model shall distinguish environmental interference, hardware malfunction, denied transmission, tamper evidence and verified high-consequence classification. An interferent event is not a security event merely due to oxidising chemistry. A dedicated maintenance queue can request calibration/cleaning and notify authorised technicians without exposing Path B per-interaction histories. Direct public security escalation from an ordinary cleaning signature is prohibited. However a genuine independently confirmed threat requires its own evidence decision; implementers must avoid an 'always suppress all alarms when bleach present' failure mode.

Threat-actors can deliberately inject many passage tokens or cause sensor resets. Rate limiting, exact dedup within the local epoch, proof of trusted token creation, capacity monitoring and fault-state quarantine reduce sabotage-induced distortions but do not make physical sensing tamper-proof. Tests need real sensor hardware, benign interference, environmental drift and authenticated maintenance workflows. No operational threshold values are provided in this public specification.

## 7. Device identity, trust anchor and remote attestation

Each deployed module SHALL have an inventory identity bound to a hardware key/measurement root with verified boot policy, signed updates, anti-rollback, firmware measurement and a controlled rotation process. TPM 2.0 is one possible building block but is **not** a declaration of PQC support. Each firmware generation shall be independently qualified for signature verification in early boot. A revoked or failed-attestation endpoint shall not inject network observations into Path A or receive an unrestricted analytics certificate. The attestation result must not become a covert Path B per-person tracking field.

The gateway SHALL apply certificate expiry, revocation, nonce freshness and configuration signature checks before trusting device output. Device/service keys for Path A and Path B SHALL be separate; permissions and telemetry schemas must not be inherited across boundaries. Establish support for reporting crypto inventory per fleet segment without publishing secrets, private site topology or raw certificates on the public internet.

## 8. Post-quantum migration and cryptographic lifecycle

The system SHALL support crypto agility, meaning it can replace primitives and certificates with signed policy controls without redesigning the full sensor assembly when the hardware permits. Candidates are ML-KEM-768 (FIPS 203) for key establishment and ML-DSA-65 (FIPS 204) for signatures, with SLH-DSA (FIPS 205) evaluated for niche fallback. RFC 10024 defines TLS 1.3 hybrid supported groups `X25519MLKEM768` and `SecP256r1MLKEM768` among others. Deployment shall select a complete, vendor-supported TLS/PKI stack, not a handwritten KEM. A cryptographic module must have a matching FIPS 140-3 certificate to be called validated where required.

### 8.1 Protecting latency

Path A alert dispatch should use an established authenticated connection and be measured at p50/p95/p99 under realistic bandwidth, loss and CPU load. Never lower the confidence threshold to 'compensate' for cryptographic overhead. TLS 0-RTT is not a safe default for replay-sensitive incident commands. PQC handshake and certificate size influence memory and timing and need measured procurement evidence. The UK NCSC recommends preparation by 2028, priority migrations by 2031 and migration completion by 2035 as planning targets; legal applicability depends on customer and sector.

### 8.2 Secure firmware transition

A dual or hybrid signature transition must be defined at the bootloader/hardware root, not merely in a Python application. Preserve an authenticated recovery chain during update interruptions, verify anti-rollback and enforce minimum accepted crypto policy versions. The update signing keys need managed cryptoperiods and protected HSM-backed operation. Incident recovery for a compromised post-quantum signer should include revocation, containment, new trusted root enrollment and forensic chain preservation, with no silent restoration of a vulnerable signature path.

## 9. Authentication, authorisation and operational partition

Roles: sensor/platform integrator, site operator, central SOC, public-health analyst, maintenance technician, independent privacy auditor, certificate authority, legal controller and contract processor. Each role SHALL receive only the data fields necessary for its purpose. An SOC can action verified Path A incidents but not reconstruct Path B passage histories. An analyst can consume coarse aggregates but not alter the hard k rule, retrieve token sets or dispatch alerts. Maintenance can obtain sensor health and run signed diagnostics; maintenance keys may not sign emergency incidents or override data privacy settings.

All critical policy and firmware changes SHALL require dual control and signed audit evidence with immutable version identifiers. Logs must store only minimal system health and independent signed cryptographic events; they must not quietly reintroduce a payment-to-sensor join path. Production connectors and incident system interfaces require explicit network zoning and separate key stores.

## 10. Reliability, availability and unsafe degraded modes

The design SHOULD be fault-tolerant to power failure, clock rollback, memory exhaustion, network outage, local sensor drift and certificate expiration. At trust uncertainty, fail closed for Path B publication and unverified Path A alerts while raising a local service-fault state. 'Fail closed' does NOT mean pretending no threat: a safety controller and operator should see a health failure. The reference buffer discards an epoch on missed checkpoints; this is deliberately strict to prevent stale-window mislabelling. Production designs must test that expected watchdog timing can meet such service constraints without operational over-suppression.

For constrained endpoints, a watchdog, protected nonvolatile monotonic counters and validated output envelopes may be needed. Logs may include event-class diagnostic counters only when they cannot reconstruct an interaction history. Sensor safety is not established by the Python runtime because actual detection/classification happens in firmware/hardware not included here.

## 11. Attack assessment methods

Threat modeling includes STRIDE per trust boundary and a documented ordinal DREAD workshop to focus engineering attention. The principal threats are output timing membership inference, chemical interference and drift, supply-chain firmware compromise, high-rate denial of service, cross-path metadata correlation, compromised roots of trust, side-channel extraction and downgrade during PQC transition. DREAD values in the annex are indicative not probabilities. A funded red team shall test direct/indirect data paths, time inference, cold boot, debug interfaces, physical tampering, endpoint cloning and signing-key recovery paths.

### 11.1 Test ethics and disclosure

All tests on controlled synthetic inputs must avoid live personal data and dangerous chemical handling in unaccredited settings. Laboratory interference experiments shall use approved procedures and facilities. Public documentation shall not contain operational alert thresholds, chemical signatures or site maps that aid circumvention; detailed test protocols are restricted to authorised safety and security reviewers.

## 12. Data governance and international deployment

ATDA is not a legal shortcut around GDPR, UK GDPR or US privacy regimes. Controller, processor and operator responsibilities differ among payment operators, municipal transit authorities and public safety agencies; establish them in written contracts. Data protection by design under GDPR Article 25 and a DPIA under Article 35 may be necessary because distributed sensing in public space can carry high re-identification and civil-liberties risks even without payment IDs inside a sensor. Data minimisation and purpose limitation are binding governance constraints, not optional risk labels.

The blanket claim 'k=50 plus noise makes the data anonymous' is specifically excluded. Each deployment must assess the possibility of identification using reasonably available external data, how outputs are combined, and retention/linkage risk. EDPB anonymisation guidance (July 2026 consultation) is relevant, but not a substitute for case-specific legal advice and regulator engagement.

The baseline use-purpose is strategic public-health/operations statistics; Path B shall not independently trigger criminal investigation or be used as individualised probable-cause evidence. A change of purpose needs legal and architectural re-approval, not simply a checkbox in a settings file.

## 13. Cryptographic key domains and data retention

A recommended minimum design includes separate issuers or policy domains for device enrollment, Path A incident transport, Path B analytics transport and firmware/update signing. Device certificates shall be short enough for realistic revocation operation and independently attested. Archived event signatures should be subject to key lifetime and re-sign strategy; cryptographic rollover must not leak Path B local tokens. Documentation of secure deletion shall distinguish logical data structure clearing, protected memory erasure and nonvolatile physical destruction where applicable.

Never transmit or buffer card IDs as 'pseudonymised' by ordinary hashing: low-entropy IDs can be reversed or linked, and even high-entropy persistent identifiers permit tracking. For the reference, locally generated tokens expire with the epoch and are not reported. Production issuance should be tied to trusted sensor event confirmation rather than any payment credential.

## 14. Data formats and immutable manifest

The normative Path B output schema is a fixed aggregate object with: `zone` (coarse public zone code), `window_start_utc_min` (coarse time boundary), `window_minutes` (15 through 1440), `noisy_counts` (all fixed public categories), and `policy_version`. No `user`, `card`, `payment`, `device serial`, `token`, transaction ID, raw event timestamp, raw count or named person field is allowed. Actual fleet delivery must add authenticated transport metadata outside the published statistics payload, under a separate validated threat model. Randomness is generated locally. Signed policy changes are non-interactive and must be independently approved.

The machine manifest `manifest/ATDA_Privacy_Safety_Manifest_v1_2.json` is authoritative for the *claims this code makes*; it contains explicit `false` for production validation, physical PII verification, end-to-end pure DP and GDPR anonymisation. The original historical fake-JSON file remains unchanged, and no parser should treat that historical file as a configuration source.

## 15. Test framework and acceptance gates

The reference's built-in unit suite covers k=49/50, delayed adaptive release, 24h hard expiry, duplicate rejection, strict input schema, capacity overflow, clock rollback and late checkpoints, payload fields, non-overlap and distribution moments for geometric noise. These are deterministic simulation tests on a software logic kernel and cannot demonstrate physical PII stripping, true entropy source validity, threat-classifier accuracy, FIPS/IEC qualification, regulatory compliance or worst-case endpoint timing. CI deliberately uses Python standard library only and a pinned checkout action with least-privilege repository permissions.

### 15.1 Additional pre-production tests

- Hardware fault injection at all identity and DMA interfaces; inspect memory/flash and crash dumps for any personal data after 50/49/24h sequences.
- Signed/unsigned OTA, invalid firmware measurements, certificate revocation, boot rollback, brown-out and power-cut endurance, under strict independent logging.
- Network message fuzzing and replay to Path A and Path B, including multi-gateway buffering, connection loss and TLS hybrid negotiation failures.
- Controlled cleaning-agent interference with independent safety evidence, remote tampering and sensor health drift over environmental cycles.
- Privacy red-team inference with synthetic site operations, repeated group queries and external CCTV/payment join datasets.
- PQC timing, memory, power and side-channel measurements on selected production bill of materials; path A p99 alert latency under degraded network.
- Legally approved DPIA and site permissions before real-world data acquisition.

## 16. Procurement and economic decision

An equipment contract shall not pass solely because an algorithm appears in a marketing datasheet. Request module-specific cryptographic evidence, signed boot recovery, trust root rotation, firmware provenance, 15-year support and objective side-channel/latency benchmarks. The separate TCO annex illustrates seven-year incremental crypto migration costs and shows why agile design can be economically favourable for a 1000-device fleet under stated assumptions. These numbers are hypotheses for procurement discovery, not market quotations. Actual sensing hardware and legal operations dominate full-system TCO and remain unestimated in this public reference.

Vendor RFP evaluation should weight trust-boundary assurance and viable secure updates before algorithm fashion or sensor sensitivity claims. For minimum complexity begin with field-upgradeable secure boot, accurate component inventory and isolated Path B memory; only then decide whether a discrete PQC accelerator, software implementation, HSM proxy or replacement platform is economically justified.

## 17. Implementation roadmap and release control

Stage M0: preserve original evidence, identify missing source artifacts and publish a reconstructed, clearly dated public reference. Stage M1: privacy formalisation and a scoped DPIA with explicit hard-k versus full-DP decision. Stage M2: hardware isolation proof and sensor-issued token validity. Stage M3: authorised classifier/maintenance experiments. Stage M4: CBOM/PQC lab integration and security assurance of firmware update. Stage M5: limited live pilot with independent re-identification testing. Stage M6: procurement qualification and sector/legal approvals. Stage M7: fleet lifecycle and PQC sustainment through 2040. Every stage has a stop condition and an independent approval artifact. Phase advancement without acceptance evidence is prohibited.

## 18. Open research questions

1. Can a physical event token be validated as one legitimate passage under deliberate replay, multi-person overlap and denial-of-service without observing identity?
2. How should strict k publication suppression be reconciled with an actual full-mechanism DP claim under visible output timing?
3. What is the right adaptive window strategy across dense metro and sparse suburban ATM deployments without producing revealing geography/time schedules?
4. How robust are non-contact chemical sensors under cold, humid, dirty and cleaning-intensive environments, and what is the measured calibration burden?
5. Which hardware roots allow migration of remote attestation and very early boot signatures to PQC, rather than only upgrading TLS software?
6. How can operators prove lack of a payment–sensor side channel when both systems share an enclosure, power supply or service technician?
7. What procurement metrics can independently validate anti-bleach sabotage resistance without publication of operationally sensitive threat thresholds?
8. How can an external auditor prove firmware and privacy policy enforcement while preserving security-sensitive deployment topology?
9. Can an independent privacy committee assess source code and legal risk without indefinite access to site-level personal inference evidence?
10. What are the public-risk and civil-rights consequences of deploying invisible sensing at soft targets, and which transparency policies are adequate?

## 19. Standards crosswalk

| Engineering control | Reference | Relevant mapping and caution |
|---|---|---|
| Approved key management / cryptography | NIST SP 800-53 Rev. 5, SC-12/SC-13 | Control family selection, not evidence of FIPS compliance |
| Firmware and software integrity | NIST SP 800-53 SI-7; SR-11 | Supplier validation and provenance required |
| Access and device identity | NIST SP 800-53 IA-3, SC-7 | Zero Trust requires policy enforcement and monitoring, not only TPM label |
| Encryption governance | ISO/IEC 27001:2022 Annex A 8.24 | Normative control applied via ISO/IEC 27002 guidance; certification separate |
| Device integrity and cryptography | IEC 62443-3-3 SR 3.4 / SR 4.3 | Industrial-control integration requires security-level specification |
| ML-KEM and signatures | NIST FIPS 203/204/205 | Standardised algorithms; no claim of implementation in Python reference |
| Hybrid transport | RFC 10024 TLS 1.3 | Group negotiation must be supported end-to-end |
| Crypto agility | NIST CSWP 39upd1 | Vendor patchability and policy governs migration |
| GDPR privacy-by-design | GDPR Art.5/25/35 | Compliance review remains contextual; k+DP are not legal magic |
| Anonymisation | EDPB Guidelines 02/2026 consultation draft | Watch final guidance; no blanket 'anonymous' claim |

## 20. Release acceptance record (current)

| Control / artifact | State at 2026-10-27 | Basis |
|---|---|---|
| 2025 architectural white paper | RECOVERED (Drive text and metadata) | Original dated 5 Dec 2025 |
| Jan 2026 GitHub root commit | VERIFIED (one-file tree) | SHA preserved; commit message does not equal uploaded content |
| Full original v4.35/v5.0 kernel | MISSING / NOT IDENTICAL | Reconstructed version explicitly marked |
| Python synthetic reference | PASS (local unittest) | Stdlib tests; not hardware assurance |
| Strict Path B 50-event gate | PASS (reference logic) | Local tests, trusted-input assumption |
| Pure end-to-end ε-DP | **NOT SATISFIED / NOT CLAIMED** | Formal k-boundary contradiction |
| Real hardware PII strip | NOT TESTED | Hardware needed |
| Path A chemical threat detection | NOT IMPLEMENTED | Lab methods not included |
| PQC handshake/signing | DESIGN ONLY | Vendor and platform validation pending |
| FIPS 140-3 validation | NOT CLAIMED | Certified module evidence unavailable |
| GDPR legal anonymisation | NOT CLAIMED | DPIA, threat model and counsel needed |
| Operational production | NO-GO | Missing external evidence |

## 21. External references

- Original ATDA white paper, V. Panov, 5 December 2025: https://drive.google.com/file/d/1lEXMtkPDWbe5ruQFORrCpHwERX4Ba9fw/view
- NIST FIPS 203: https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204: https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205: https://csrc.nist.gov/pubs/fips/205/final
- NIST IR 8547 initial public draft: https://csrc.nist.gov/pubs/ir/8547/ipd
- NIST CSWP 39upd1: https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- NIST SP 800-53 Rev.5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- RFC 10024: https://www.rfc-editor.org/rfc/rfc10024.html
- IEC 62443-3-3; ISO/IEC 27001:2022 (licensed standards, reference only)
- EDPB Anonymisation Guidelines 02/2026 consultation: https://www.edpb.europa.eu/documents/guideline/guidelines-022026-on-anonymisation_en
- UK NCSC migration guidance: https://www.ncsc.gov.uk/guidance/pqc-migration-timelines
- GDPR Regulation 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj

**End of public sanitised technical specification.**

\clearpage

# Part 2: Privacy proof and limitations

**27 October 2026 / engineering research analysis / NOT a legal-anonymisation certification.**

## 1. Privacy unit and adjacency

The intended unit is a **PASSAGE/interaction within one local epoch**, not a human being. Let `D` be a multiset of validated, PII-stripped passages in a fixed epoch, each contributing to exactly ONE bucket of a public fixed set `S`. Neighbouring datasets `D` and `D'` differ by adding or removing exactly one passage. Cross-epoch actions of one person are explicitly out of scope. Tokens are local, random, ephemeral and must be issued after hardware identity isolation; tests cannot confirm this property.

For the vector of per-bucket true counts `f(D) in N^{|S|}`, adding/removing one passage affects exactly one coordinate by one, hence `||f(D)-f(D')||_1 <= 1`. This upper bound is conditional on a one-category-per-passage rule and on fixed, non-adaptive buckets. If multi-label classification is allowed, sensitivity increases and needs a new privacy proof.

## 2. Two-sided geometric discrete noise

Choose rational `q` in `(0,1)`, default `q=1/2`. Draw two IID geometric failure counts `G1`, `G2` with `Pr[G=n] = (1-q) q^n` and form `Z=G1-G2`. Then:

`Pr[Z=z] = ((1-q)/(1+q)) q^{|z|}` for every integer `z`.

Release each fixed bucket count `f_s(D)+Z_s` with IID noise. For any two neighbours, the ratio of output probabilities for any count vector is bounded by `q^(-||f(D)-f(D')||_1)`; with sensitivity 1, `epsilon = ln(1/q) = ln 2 ~= 0.693147`. This statement assumes ideal independent randomness and a **fixed, always-performed query**. `max(0, y)` on the noisy count is post-processing and cannot worsen this fixed-query guarantee.

Default noise moments: `E[Z]=0`, `Var(Z)=2q/(1-q)^2 = 4`, `SD(Z)=2`. The exact tail for `m>=1` is `Pr[|Z|>=m]=2 q^m/(1+q)`; for `m=5`, probability is `1/48 ~= 2.083%` per bucket. Adding three independent buckets does NOT multiply epsilon when L1 sensitivity remains 1: the joint likelihood ratio is controlled by the same epsilon. Composition is, however, required if the same records are queried repeatedly or across overlapping epochs.

These are analytic results under stated hypotheses, not cryptographic certifications. The reference's integer RNG uses `secrets`-backed `SystemRandom` with finite-state implementation and unbounded sampling runtime; use a formally reviewed, availability-appropriate library for actual hardware.

## 3. Formal conflict: strict k-gate versus pure end-to-end DP

Normative ATDA rule: **no Path B transmission until the local buffer has at least `k=50` distinct validated interactions.** Let `O` denote the event that any statistical Path B message is published at a fixed checkpoint. For a database with 49 passages, `Pr[M(D_49) in O] = 0` by the hard-gate requirement. For a neighbouring database with 50 passages, if the protocol can publish, `Pr[M(D_50) in O] > 0`. Finite pure epsilon-DP would require:

`Pr[M(D_50) in O] <= exp(epsilon) * Pr[M(D_49) in O] = 0`.

Contradiction. **Therefore no nontrivial hard-k release/no-release protocol of this form is end-to-end pure epsilon-DP.** The contradiction remains if noise is added only AFTER a true-count hard gate or if a noisy gate is subordinated to a mandatory hard gate. If the gate uses only noisy counts, it may release at n<50, violating the hard normative minimum. The existing historical text claiming a "DP-clean k-gate" is not a valid proof of the combined guarantee.

For approximate `(epsilon,delta)`-DP, the publishing probability at the 49/50 boundary creates a lower bound on permissible `delta`; such a claim needs a complete mechanism-level analysis and operational policy. This repository makes **no such claim**. A constant-size, fixed-schedule non-content heartbeat can reduce traffic-analysis leakage but may conflict with the rule prohibiting Path B transmission prior to k; it is NOT implemented.

## 4. Dynamic windows

The algorithm starts at 15 minutes and, if it has fewer than k valid interactions, increases the window to 30, 60, 120, 240, 480, 960, then 1440 minutes. At a checkpoint with >=k interactions, one noisy aggregate may be published. Under-k records are discarded at 24 hours. A missed checkpoint or clock rollback invalidates the epoch rather than producing stale or mislabeled output. Each epoch is released at most once; a new local epoch begins at the first subsequent passage.

This guarantees the *code-level* k-gate and bounds buffer lifetime **provided its clock and trusted-call assumptions hold**. It cannot prove users are distinct, unique token origin, hardware PII removal, time-linkability resistance, group anonymity, or real-world deployment compliance.

## 5. Sparse geography and aggregate inference

A site-level aggregate can become identifying when site traffic is sparse or when external CCTV/payment records allow join attacks even when the sensor never ingests payment identifiers. Publish only coarse regions, fixed categories, and no interactive drill-down; restrict differences between successive releases, cross-site joins, and per-gate high-resolution heatmaps. Apply red-team membership-inference tests and revisit the legal basis and risk of re-identification in each jurisdiction.

## 6. Required proof obligations and acceptance tests

1. Hardware evidence: prove PII is stripped **before** Path B memory and before debug/DMA/peripheral sinks; document physical fault-injection results.
2. Event unit evidence: independently establish why one token means one valid interaction, including replay/sabotage handling; make NO unique-person claim.
3. Sensitivity evidence: one fixed public category per passage; no hidden multi-label effects or adaptive feature selection.
4. Output evidence: one aggregate per disjoint epoch; no true count, tokens or per-passage timestamps in payload; disable debugging dumps.
5. Composition evidence: quantify privacy impact across time, sites, baselines and external queries, not only one row of noise.
6. Legal evidence: DPIA, DPO sign-off, purpose limitation and documented re-identification threat model. GDPR anonymisation cannot be inferred from use of `k` or `epsilon` alone.
7. Release-decision evidence: explicitly state that the gate timing is NOT covered by a pure epsilon-DP guarantee. Confirm no marketing/security-claim copy contradicts this.

## 7. Reference sources

- Dwork and Roth, *The Algorithmic Foundations of Differential Privacy*, 2014 (standard DP definition).
- NIST SP 800-53 Rev.5: privacy and access-control protections; not a proof of DP.
- EDPB, *Guidelines 02/2026 on Anonymisation* (public consultation draft, 08 July 2026): https://www.edpb.europa.eu/documents/guideline/guidelines-022026-on-anonymisation_en
- GDPR Art. 5(1)(b)-(c), Art.25 and Art.35: https://eur-lex.europa.eu/eli/reg/2016/679/oj

\clearpage

# Part 3: PQC migration and assurance

**27 October 2026 | Design and procurement controls only.** Nothing in this repository performs ML-KEM/ML-DSA or claims hardware/PKI conformity.

## First control: crypto agility, maximum security impact at minimum complexity

The first acquisition requirement is not a new cryptographic accelerator; it is upgradeable, inventoried, centrally governed cryptography across edge devices and gateways. Fix key/credential lifecycle and authenticated update pathways before enabling a new algorithm. NIST CSWP 39upd1 emphasises crypto agility across protocols, software, hardware and firmware.

### Asset inventory

| Asset | Current exposure to verify | Target | Acceptance evidence |
|---|---|---|---|
| PATH A sensor to gateway | ECDH/RSA transport, certificate chain | Mutually authenticated TLS 1.3 with policy-appropriate PQ/T hybrid or approved ML-KEM | Captured negotiated group, certificate chain, no downgrade, timed alert latency |
| PATH B collector to analytics gateway | TLS, transport metadata, site correlation | Comparable hybrid transport with fixed egress constraints | Packet capture; no payload under 50; transport separation |
| Firmware update/secure boot | RSA/ECDSA/EdDSA signatures; rollback | Platform-supported ML-DSA-65 migration (or vetted multi-signature bridge) | Hardware-verifiable test vectors, dual-root update, rollback block |
| Device identity/TPM 2.0 | Existing endorsement/attestation algorithms may be ECC/RSA | TPM/HSM vendor-specific migration roadmap | Vendor attestation evidence, cert path, lifecycle support through 2040 |
| PKI, CRLs, certificate tooling | Intermediates/root capability and revocation | Algorithm-agile profile, smaller trust domains | Automated chain tests, revoked cert quarantine, rotation procedure |
| Logs, audit and archives | Signatures, key retention, long-lived metadata | Defined cryptoperiod and re-sign strategy | Tamper-proof audit trail + retention schedule |

## Algorithm choices and standards

- **FIPS 203 (2024)**: ML-KEM-768 is the reference key-establishment target for balanced security/performance; ML-KEM does NOT sign firmware.
- **FIPS 204 (2024)**: ML-DSA-65 is a candidate signature level for firmware/attestation where implementations support it; signatures do NOT establish session secrets.
- **FIPS 205 (2024)**: SLH-DSA is an alternative hash-based signature family; evaluate memory, bandwidth and verification latency before selecting.
- **RFC 10024 (August 2026)**: specifies `X25519MLKEM768`, `SecP256r1MLKEM768`, `SecP384r1MLKEM1024` TLS 1.3 hybrid groups. Select based on the *entire certified module, key derivation, host stack and national accreditation*, not brand labels alone.
- **NIST IR 8547**: transition roadmap identified by NIST. The official publication version/date and deprecation schedules shall be verified from the live NIST index during contractual baselining; this document avoids claiming a deadline is binding on every private ATDA deployment.
- **NIST SP 800-227**: guidance on KEMs, including hybrid construction principles; no bespoke key combiner.
- **NIST CSWP 39upd1 (updated 29 June 2026)**: cryptographic agility.

### Procurement controls

Do not confuse FIPS algorithms with **FIPS 140-3 validated cryptographic modules**. Require an exact security policy/certificate mapping to device model, firmware/library version and approved mode. Test key lifecycle, boot chain, rollback protection and side-channel resistance. Do not generate ML-KEM parameters locally and do not implement custom KEM code in ATDA.

### Anti-downgrade

1. Signed device policy enumerates accepted cipher suites/versions and minimum cryptographic profile.
2. Once a supported fleet cohort enables PQ/T hybrid, refuse unauthorised downgrade to classical-only key exchange.
3. On invalid/revoked device credentials, quarantine the relevant remote source and purge derived data; do not silently accept an unsigned recovery profile.
4. Maintain an authorised emergency recovery path with documented break-glass controls that do not weaken Path B privacy or Path A signature validation.
5. Distinct key roots for Path A and Path B; security/event messages from one path never acquire permissions in the other.

## PATH A latency and system safety

PQC handshake size increases (RFC 10024 client share for X25519MLKEM768 is 1216 bytes). Avoid a new handshake for each alert: maintain an already authenticated connection, queue only verified high-consequence alerts, measure p50/p95/p99 and loss, and reject replayed incident messages. TLS 0-RTT must not be used for non-idempotent alerts because replay is a protocol consideration. Document safe behavior during revocation checks, link outage or power loss; non-availability is NOT proof of no threat.

## Hardware root of trust constraints

TPM 2.0 presence provides secure-key capabilities but does not by itself guarantee post-quantum signature verification, remote attestation or secure upgrade of all roots. Demand concrete vendor claims for: algorithm capability, measured boot coverage, ability to rotate identity roots, anti-rollback fuses, recovery signature chain, lifespan, inventory reporting and physical tamper response. Treat unsigned maintenance interfaces as critical attack surfaces.

## Migration milestones

| By date | Work product | Evidence / go-no-go |
|---|---|---|
| 2027 Q2 | Cryptographic bill of materials (CBOM), algorithm dependency map | 100% of proposed devices/gateways inventoried; unsupported crypto blocked in procurement |
| 2028 Q2 | Reference hybrid TLS/ML-KEM integration in lab | Mutual-auth traffic capture, downgrade rejection, p99 PATH A proof with chosen hardware |
| 2029 Q4 | Tested firmware signature/attestation migration | Recovery after power failure, revoked credentials, key rotation and rollback tests |
| 2031 Q1 | First production-fitness vendor qualification | Independent validation and regulatory review; no unproven FIPS assertions |
| 2035 | Fleet-wide supported transition target | Document exceptions and hardware replacement plan aligned with UK NCSC guidance |
| 2040 | Ongoing maintenance | Cryptoperiod and cryptographic algorithm refresh, key compromise playbooks |

## Reference links

- https://csrc.nist.gov/pubs/fips/203/final
- https://csrc.nist.gov/pubs/fips/204/final
- https://csrc.nist.gov/pubs/fips/205/final
- https://www.rfc-editor.org/rfc/rfc10024.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://csrc.nist.gov/pubs/sp/800/227/final
- https://csrc.nist.gov/pubs/ir/8547/ipd
- https://www.ncsc.gov.uk/guidance/pqc-migration-timelines

\clearpage

# Part 4: STRIDE/DREAD threat assessment

**27 October 2026.** Research architecture, not accredited OT or CBRN system. Scope: adversaries include criminal saboteur, malicious insider, supply-chain operator, state-level APT, passive quantum-era recorder and low-resource nuisance actor. These risks are not proven addressed by an unintegrated Python prototype.

## Trust boundaries

`public environment -> sensor measurement` (untrusted), `sensor isolation / hardware PII-strip boundary -> Path B protected memory`, `verified threat decision -> Path A signed event gateway`, `device TPM/secure boot -> remotely attested gateway`, `Path B counted epoch -> anonymised coarse-zone export`, `vendor firmware -> signed OTA verification`, `operator access -> auditable governance`. Trust shall not flow back from analytics into device interdiction. No payment ID shall be accessible to Path B even transiently via trace logs, crash dumps or debug buses.

## STRIDE by data flow

| Threat | Surface | Example failure | Architectural countermeasure | Verification |
|---|---|---|---|---|
| Spoofing | Sensor / attestation | Cloned device inserts fabricated counts or alerts | Unique roots of trust, signed enrollment, nonce/freshness, quarantine | Cloned cert/attestation test |
| Tampering | OTA / configuration | Malicious classifier changes threat threshold or privacy k | Signed release manifest, separate approval, anti-rollback, dual control | Tampered OTA rejected, signed settings measured |
| Repudiation | Event/logging | Operator claims false security alert was never dispatched | Signed secure Path A audit, monotonic event sequence | Incident reconstruction drill |
| Information disclosure | Path B memory, egress | Payment ID enters analytics or re-identification via site timing | Hardware identity isolation, explicit schema, coarse geography, k threshold, DPIA | DMA/debug fault injection, external join attacks |
| Denial of service | Cleaning-agent interference | Bleach causes false CBRN alarms and overwhelms SOC | Maintenance flag only for cleaning signatures, independent threat confirmation | Benign chemical interference lab test |
| Elevation of privilege | Admin / update path | Analytics credential obtains Path A actuator access | Distinct trust domains, least privilege and isolation | Permission escalation negative tests |

## DREAD prioritisation (expert hypothesis; NOT incident statistics)

DREAD columns: Damage, Reproducibility, Exploitability, Affected users, Discoverability on an ordinal 1-10 scale. `Mean` is a workshop prioritisation aid, not a probability or NIST-defined risk score.

| Scenario | D | R | E | A | D | Mean | Owner |
|---|---:|---:|---:|---:|---:|---:|---|
| PATH B window-gate timing inference | 7 | 9 | 8 | 8 | 9 | **8.2** | Privacy lead |
| Sensor drift / adversarial interference | 7 | 9 | 8 | 8 | 8 | **8.0** | Sensor engineering |
| Signed firmware supply-chain compromise | 9 | 8 | 7 | 8 | 7 | **7.8** | Platform security |
| Deliberate event-rate / buffer DoS | 7 | 9 | 8 | 7 | 8 | **7.8** | Operations |
| Path A bleach/oxidiser misclassification | 9 | 8 | 6 | 7 | 8 | **7.6** | Detection verification |
| Cross-path metadata correlation | 9 | 7 | 6 | 9 | 7 | **7.6** | Privacy/security |
| Root-of-trust cloning / compromised attestation | 9 | 6 | 7 | 8 | 6 | **7.2** | Hardware security |
| Endpoint PQC downgrade / stale TLS | 8 | 7 | 6 | 7 | 7 | **7.0** | PKI lead |
| Insider captures protected buffer memory | 8 | 7 | 6 | 8 | 6 | **7.0** | SOC/security |

## Attack trees (defensive)

### Tree A: attacker tries to force a false emergency alert

```
ROOT: cause unauthorised Path A alert
  OR spoof high-confidence sensor data
       -> signed sensor identity + attestation + independent sensor verification
  OR inject oxidiser/cleaner interference
       -> chaotic-oxidiser classification; MAINTENANCE flag; alarm abstention
  OR compromise threshold/configuration
       -> signed, independently reviewed configuration and anti-rollback
  OR replay a previously genuine incident
       -> signed sequence/nonce, bounded time, downstream deduplication
```

A true, independently validated explosive/CBRN signature must not be hidden merely because a cleaner interferent coexists; evidence fusion and abstention rules require lab validation. Specific analyte identification thresholds and bypass instructions are deliberately absent from this public document.

### Tree B: attacker tries to identify a Path B interaction

```
ROOT: infer whether a passage/person was present
  OR extract local pre-aggregation artefacts
       -> hardware PII stripping; protected RAM; disabled debug; short retention
  OR exploit output/no-output timing at k=50
       -> no end-to-end pure DP claim; coarse windows; publication policy audit
  OR join sparse aggregate with CCTV/payment metadata
       -> coarsen zone; prohibit row-level joins; access controls; DPIA
  OR send repeated differencing queries
       -> fixed schema; no ad-hoc queries; one release per disjoint epoch
  OR impersonate an authorised analytics sink
       -> independent PKI; authenticated egress; trust-domain separation
```

### Tree C: advanced persistent compromise / supply chain

```
ROOT: covert persistent endpoint control
  OR corrupt build/update artefact
       -> reproducible builds, signed provenance/SBOM/CBOM, SLSA-inspired gates
  OR steal/replay attestation credentials
       -> TPM policy binding + challenge freshness + revocation + quarantine
  OR downgrade migration to classical-only crypto
       -> authenticated algorithm policy; monitored migration cohorts
  OR side-channel key extraction
       -> side-channel-rated crypto modules; physical threat model; lab tests
  OR insider override
       -> dual approvals, least-privileged maintenance, immutable audit
```

## Mandatory acceptance gates

- **GATE-SEC-01:** reject a synthetic payment/identity field at the public Path B API and demonstrate hardware enforcement separately.
- **GATE-SEC-02:** under 49 verified interactions, NEVER transmit a statistical Path B payload (including true counts).
- **GATE-SEC-03:** cleaner-only interferent yields MAINTENANCE, not security escalation.
- **GATE-SEC-04:** stale/revoked firmware or attestation identity cannot authorise a secure alert session.
- **GATE-SEC-05:** simulated power loss cannot undo signed update rollback protection.
- **GATE-SEC-06:** no privileged route from analytics side into Path A incident engine.
- **GATE-SEC-07:** release geometry, clock checks, payload schema and test coverage independently audited.
- **GATE-SEC-08:** no production claim until integrated hardware tests, privacy DPIA and sector assessment.

## Framework mapping (subject to control tailoring)

- NIST SP 800-53 Rev.5: IA-3 device identification/authentication; SC-7 boundary protection; SC-12/13 cryptographic key establishment/protection; SI-7 software/firmware integrity; AU-9 audit protection; SR-11 component authenticity.
- ISO/IEC 27001:2022 Annex A 5.19 supplier relationships, 8.24 cryptography, 8.9 configuration management, 8.15 logging.
- IEC 62443-3-3 SR 1.1 identification/authentication, SR 3.4 software/information integrity, SR 4.3 use of cryptography; allocation to security levels requires integrator assessment.
- UK NCSC secure design and supply-chain lifecycle controls; GDPR Art.25/35.

\clearpage

# Part 5: TCO procurement model and milestones

**27 October 2026.** Values are *engineering scenario assumptions*, NOT vendor quotations, field measurements or a procurement commitment. Costs in **EUR 2026, excluding VAT**. Model compares only incremental **cryptographic migration**, not complete chemical-sensor deployment.

## 1. Cost question

For a large 2025-2040 fleet, is it cheaper to pay for cryptographic agility during design or to replace devices later when algorithms and root-of-trust hardware change? The answer depends mainly on whether the chosen hardware can securely accept future PQC firmware and whether its TPM supports the necessary trust chain.

### Illustrative 7-year incremental model

Let `N` be installed endpoints (assumed to include networking and software update support). Scenario A: crypto-agile firmware and gateway design: EUR 140,000 engineering + EUR 80,000 independent validation + EUR 20,000/year operations for seven years = **EUR 360,000**. Scenario B: legacy fleet replacement once: EUR 420 replacement hardware + EUR 180 field visit per endpoint + EUR 120,000 project engineering + the same EUR 20,000/year operations = **EUR (260,000 + 600*N)**. Both are illustrative assumptions and ignore discount rates, security events, regulatory cost and uncertain supply-chain prices.

| N endpoints | Agility scenario A | Replacement B | A versus B |
|---:|---:|---:|---:|
| 100 | EUR 360,000 | EUR 320,000 | A costs EUR 40,000 more |
| 500 | EUR 360,000 | EUR 560,000 | A saves EUR 200,000 |
| 1,000 | EUR 360,000 | EUR 860,000 | A saves EUR 500,000 |
| 10,000 | EUR 360,000 | EUR 6,260,000 | A saves EUR 5,900,000 |

Breakeven: `360000 = 260000 + 600*N`, hence **N ~= 167 endpoints**. This is NOT a technology-neutral business case: agility costs and scaling could grow, and the scenario is impossible if an initially selected TPM/boot ROM cannot support future security profiles.

### Procurement gates / what must be priced

1. Per-device secure boot, trust-anchor rotation and FIPS validation status (including security policy and approved operation mode).
2. RAM, flash, handshake bandwidth and power margin for ML-KEM/ML-DSA and dual-signature transition.
3. Field replacement cost including transit safety restrictions, after-hours labour and operator clearance.
4. 15-year cryptographic maintenance, spare modules, software bill of materials, failure / RMA rates.
5. Independent test costs: side-channel, tamper, NIST crypto and physical PII isolation.
6. Country/sector legal review, controller/processor contract design, DPIA and retention management.
7. Procurement scoring must separate sensor detection performance from cryptographic conformity.

## 2. Milestone roadmap and stop conditions

| Milestone | Target | Evidence | Stop / accept |
|---|---|---|---|
| M0 provenance recovery | 2026 Q4 | Original 2025 white paper preserved, GitHub baseline immutable, reconstruction clearly labelled | No fabricated original source/date |
| M1 privacy formalisation | 2027 Q1 | Attack-surface map, strict k test, gate/no-DP contradiction documented, DPIA draft | Never market hard k protocol as end-to-end pure epsilon-DP |
| M2 isolate identity data | 2027 Q2 | Hardware data-flow traces from payment ID boundary to buffer, debug/DMA analysis | Zero PII ingress across all tested modes |
| M3 lab sensor validation | 2027 Q4 | Baseline/cleaning interference tests, health flags, confidence-calibration dataset | No maintenance-only incident escalations |
| M4 crypto agility | 2028 Q2 | Complete CBOM, TLS hybrid and signature proof-of-concept on chosen MCU/TPM | Authenticated no-downgrade channel and p99 link KPI |
| M5 limited gateway pilot | 2029 Q4 | Verified site-level output suppression, external re-identification red team, rollback and revocation drills | Privacy counsel and safety authority sign-off |
| M6 procurement qualification | 2031 Q1 | Vendor secure update lifecycle, independently assessed security case | No mass rollout without validated BOM |
| M7 migration / sustainment | 2035-2040 | Key-algorithm replacement programme, patches, repeated DPIAs | Every lifecycle extension evaluated |

Target dates are programme planning hypotheses and should be rescheduled as technology, assurance results and jurisdictional obligations evolve.

## 3. Open research and development

**Privacy:** How to reconcile hard k=50 publication suppression with formal mechanism-level DP without leaking presence/absence? What sensitivity model reflects repeated passages of one individual? What is the minimal safe geography/time granularity under hostile side-information? How can noisy adaptive stopping avoid release-time inference?

**Sensor validity:** What is the actual false-positive/false-negative impact of bleach, peroxide and other benign oxidisers in a validated environment? Can multi-sensor evidence discriminate maintenance interferents while not concealing a genuine co-occurring high-consequence threat? How do drift and cleaning schedules impact calibration? These require regulated lab testing; the reference implementation has no chemical signature database.

**PQC:** Which affordable TPM/HSM can maintain attestation, chain of trust, signed boot and lifetime management for 15 years? How large is real p99 hybrid TLS latency on low-power MCU plus constrained networking? Is firmware verification possible with ML-DSA-65 in a hardware boot ROM? Which exact module version is FIPS 140-3 validated?

**Operations:** Who is the data controller and processor for multinational deployments? How are incident overrides constrained and logged? How can operators demonstrate real, not merely software-proclaimed, PII stripping to an EU supervisory authority? What is the legal basis for operating a site-level non-contact sensing system in public spaces?

## 4. Optional moonshots (NOT in reference implementation)

| Approach | Approximate TRL (hypothesis) | Production horizon | Incremental versus breakthrough |
|---|---|---|---|
| Multiparty secure aggregation for cross-operator regions | TRL 3-5 | 3-6 years after funded pilot | Incremental for privacy if system compatibility proven |
| ZK proof of bounded-bucket aggregation without exposing counts | TRL 2-4 | 5-8 years | Potential breakthrough in external verifiability; high compute and trusted hardware assumptions |
| Fully homomorphic encryption for site-level analysis | TRL 3-5 | 5-10 years for constrained deployment | Research-grade; not minimum-complexity for this problem |

These TRLs are subjective estimates, not vendor assessments. None supersedes hardware PII stripping or guarantees GDPR anonymisation.

\clearpage

# Part 6: Provenance and recovered originals

**Audit date: 2026-10-27.**

## Confirmed original publication evidence

- **2025-12-05**: `WhitePaper_ATDA_Privacy_Preserving_Detection_2025_v5.pdf`, author V. Panov, original source document recovered through the owner's connected Google Drive. It introduces the dual Path A/B architecture, baseline contamination safeguards, legal limits, non-contact sensing horizon and public defensive-publication intent. Source: https://drive.google.com/file/d/1lEXMtkPDWbe5ruQFORrCpHwERX4Ba9fw/view (access may require owner permission).
- **2025-12-05 04:40 UTC**: Public GitHub repository creation date (GitHub repository metadata).
- **2026-01-30 10:47 UTC**: Historical GitHub root commit `a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1` by `V.Panov`; tree SHA `d1a09b765e74311688408741443b18a993d87890`. GitHub independently reports **a single actual blob** `ATDA_Privacy_Safety_Manifest_v1.json`. Although the commit message names PDFs, Python code, README and CI, none of these files appears in the commit tree. Link: https://github.com/slavonslavon50-web/ATDA-WhitePaper/commit/a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1
- The historical `.json` is **Markdown-like narrative, not parseable JSON**. It is intentionally preserved unchanged as a primary historical exhibit.
- Owner discussions in January 2026 referred to v4.32/v4.35 and v5.0 Fortress Python sources and appendix files, but those original bytes have NOT been recovered from the GitHub tree, and no copy was found in currently accessible Drive search results. Thus exact byte-for-byte recovery is **not** claimed.

## What is NEW and must not be backdated

The 27 October 2026 implementation in `src/` and associated tests are **new independent reconstructions** of the public architectural rules, not originals from 2025 or 2026-01. The privacy proof corrects an unsupported full-mechanism pure ε-DP claim. The PQC annex cites algorithm standards published after the original concept and does not rewrite the historical artifact. The documentation does not establish that NIST was influenced by this repository; a claim would require specific provenance evidence beyond chronological proximity.

## Rules for future release/academic citation

1. Cite the 2025 white paper as an architectural publication with its original date and author.
2. Cite this repository's 2026 v1.2 source code as an audited **reference reconstruction**, specifying the actual GitHub commit.
3. Do NOT backdate generated files, retroactively alter the root commit, or assert unpublished PDFs were part of that commit.
4. Maintain the root historical file and the original white paper in an immutable evidence archive; optional SHA-256 should be computed from bytes with preserved metadata when accessible.
5. Keep government-only submission documents and sensitive detection thresholds OUT of the public repository.
6. Publish each revision with changed algorithms, test results and known limitations in the changelog.

\clearpage

# Part 7: Source-code appendix (auditable reference)

The following implementation is newly reconstructed, not an original archived 2025/January 2026 file. Production hardware boundaries are external. No field use is approved.

```python
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

```

\clearpage

# Part 8: JSON assurance manifest

```json
{
  "manifest_version": "1.2.0",
  "release_date_utc": "2026-10-27",
  "project": "ATDA - Anonymous Trace-Detection Analytics",
  "status": "PUBLIC_REFERENCE_NOT_PRODUCTION_CERTIFIED",
  "provenance": {
    "historical_repository": "slavonslavon50-web/ATDA-WhitePaper",
    "historical_commit_sha": "a754b3fe1c2bb4dcc132febb3f1e1e35059a99f1",
    "architectural_whitepaper_date": "2025-12-05",
    "reconstructed_reference_implementation": true,
    "reconstruction_is_not_original_2025_code": true
  },
  "data_paths": {
    "A": {
      "scope": ["EXPLOSIVES", "CBRN"],
      "high_confidence_only": true,
      "interference_cleaners_outcome": "MAINTENANCE_ONLY",
      "isolated_crypto_key_domain": true,
      "runtime_implemented_in_this_repository": false
    },
    "B": {
      "purpose": "AGGREGATE_STATISTICAL_ANALYTICS_ONLY",
      "hardware_strip_pii_before_buffer": true,
      "hardware_strip_pii_verified": false,
      "interaction_not_person": true,
      "k_min": 50,
      "dynamic_window_minutes": [15, 30, 60, 120, 240, 480, 960, 1440],
      "max_window_minutes": 1440,
      "exact_dedup_only": true,
      "persistent_identity_tokens": false,
      "fixed_categories": ["NARCOTICS", "BIOHAZARD", "OTHER"],
      "cross_epoch_tracking": false,
      "max_interactions_per_epoch": 10000,
      "no_release_when_true_count_under_k": true,
      "dp_query_mechanism": "TWO_SIDED_GEOMETRIC",
      "noise_q_numerator": 1,
      "noise_q_denominator": 2,
      "ideal_fixed_query_epsilon": 0.6931471805599453,
      "l1_vector_sensitivity": 1,
      "end_to_end_pure_dp_claim": false,
      "person_level_dp_claim": false,
      "gdpr_anonymisation_certified": false,
      "no_enforcement_use": true,
      "reference_kernel": "src/atda_pathb_fortress.py"
    }
  },
  "post_quantum_migration": {
    "transition_design_only": true,
    "target_key_establishment": "ML-KEM-768 / TLS hybrid RFC 10024",
    "target_signature": "ML-DSA-65",
    "nist_fips": [203, 204, 205],
    "nist_transition_reference": "NIST IR 8547 (verify final publication record)",
    "fips_140_3_module_validation_confirmed": false,
    "tpm_pqc_attestation_available": "NOT_VERIFIED"
  },
  "assurance": {
    "readiness": "RESEARCH_REFERENCE_ONLY",
    "sensor_accuracy_field_verified": false,
    "privacy_impact_assessment_complete": false,
    "data_protection_officer_approval": false,
    "third_party_security_audit_complete": false,
    "production_authorisation": false
  }
}

```

\clearpage

# Part 9: Test catalogue

These tests represent reference logic only; there is no live sensor test or certification.

```python
"""Auditable regression tests; no real-world sensor or live identity data."""
import random
import statistics
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from atda_pathb_fortress import (
    AggregateRelease, CapacityExceeded, ClockFault,
    FortressBuffer, Policy, SanitizedPassage, two_sided_geometric,
)


def passage(i: int, bucket: str = 'NARCOTICS') -> SanitizedPassage:
    return SanitizedPassage(token=i.to_bytes(16, 'big'), bucket=bucket)


class ZeroNoise:
    """Every geometric variate is 0 (testing only)."""
    def randrange(self, stop: int) -> int:
        return stop - 1


class TestConfig(unittest.TestCase):
    def test_policy_fixed_normative_k(self):
        self.assertRaises(ValueError, Policy, k_min=49)
        self.assertRaises(ValueError, Policy, epoch_total_max=49)
        self.assertRaises(ValueError, Policy, window_steps_min=(15, 30, 120))

    def test_single_category_per_passage_schema(self):
        with self.assertRaises(TypeError):
            SanitizedPassage(token=b'x'*16, bucket='NARCOTICS', payment_id='NEVER')
        with self.assertRaises(ValueError):
            FortressBuffer('UNSAFE:INDIVIDUAL')

    def test_noise_epsilon(self):
        self.assertAlmostEqual(Policy().epsilon_query, 0.6931471805599453, places=12)


class TestGating(unittest.TestCase):
    def setUp(self):
        self.b = FortressBuffer('ZONE_A', rng=ZeroNoise())

    def test_no_release_under_50_then_30min_release(self):
        for i in range(49):
            self.assertTrue(self.b.ingest(passage(i), 1))
        self.assertIsNone(self.b.checkpoint(15))
        self.assertEqual(self.b.active_window_minutes, 30)
        self.b.ingest(passage(49), 16)
        result = self.b.checkpoint(30)
        self.assertIsInstance(result, AggregateRelease)
        self.assertEqual(result.noisy_counts['NARCOTICS'], 50)
        self.assertEqual(result.window_minutes, 30)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_release_exactly_at_50_after_15min(self):
        for i in range(50):
            self.b.ingest(passage(i, 'BIOHAZARD' if i < 17 else 'OTHER'), 3)
        self.assertIsNone(self.b.checkpoint(14))
        result = self.b.checkpoint(15)
        self.assertEqual(result.noisy_counts, {'NARCOTICS':0,'BIOHAZARD':17,'OTHER':33})
        self.assertEqual(result.window_start_utc_min, 0)
        self.assertNotIn('token', repr(result))

    def test_duplicate_does_not_increase_count(self):
        for i in range(49):
            self.b.ingest(passage(i), 3)
        self.assertFalse(self.b.ingest(passage(1), 3))
        self.assertEqual(self.b.buffered_interactions, 49)
        self.assertIsNone(self.b.checkpoint(15))

    def test_discard_at_24h_under_k(self):
        self.b.ingest(passage(1), 1)
        for deadline in (15,30,60,120,240,480,960,1440):
            self.assertIsNone(self.b.checkpoint(deadline))
        self.assertEqual(self.b.buffered_interactions, 0)
        self.assertIsNone(self.b.active_window_minutes)

    def test_overflow_fails_closed(self):
        b = FortressBuffer('ZONE_A', Policy(epoch_total_max=50, bucket_max=50, dedup_capacity=50), ZeroNoise())
        for i in range(50):
            b.ingest(passage(i), 1)
        with self.assertRaises(CapacityExceeded):
            b.ingest(passage(51), 2)
        self.assertEqual(b.buffered_interactions, 50)

    def test_fails_closed_on_late_checkpoint(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        with self.assertRaises(ClockFault):
            self.b.checkpoint(19)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_fails_closed_on_missing_checkpoint(self):
        self.b.ingest(passage(1), 0)
        with self.assertRaises(ClockFault):
            self.b.ingest(passage(2), 15)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_clock_rollback_clears_local_buffer(self):
        self.b.ingest(passage(1), 6)
        with self.assertRaises(ClockFault):
            self.b.ingest(passage(2), 5)
        self.assertEqual(self.b.buffered_interactions, 0)

    def test_no_schema_or_token_leak_in_release(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        r = self.b.checkpoint(15)
        self.assertEqual(set(r.__dict__),
            {'zone','window_start_utc_min','window_minutes','noisy_counts','policy_version'})
        self.assertFalse(any('payment' in x.lower() for x in r.__dict__))

    def test_reset_is_nonoverlapping(self):
        for i in range(50):
            self.b.ingest(passage(i), 1)
        self.assertIsNotNone(self.b.checkpoint(15))
        self.assertIsNone(self.b.checkpoint(15))
        self.b.ingest(passage(1111), 16)
        self.assertEqual(self.b.buffered_interactions, 1)

    def test_refuses_unknown_bucket(self):
        with self.assertRaises(ValueError):
            self.b.ingest(passage(1,'UNKNOWN'), 1)


class TestDistribution(unittest.TestCase):
    def test_two_sided_geometric_unbiased(self):
        rng = random.Random(1701)  # deterministic for test ONLY, never production
        draws = [two_sided_geometric(1,2,rng) for _ in range(30000)]
        self.assertLess(abs(statistics.mean(draws)), 0.055)
        self.assertAlmostEqual(statistics.pvariance(draws), 4.0, delta=0.30)
        self.assertLess(abs(draws.count(0) / len(draws) - 1/3), 0.014)
        self.assertTrue(min(draws) <= -8 and max(draws) >= 8)

    def test_invalid_q(self):
        with self.assertRaises(ValueError):
            two_sided_geometric(1, 1, ZeroNoise())


if __name__ == '__main__':
    unittest.main()

```
