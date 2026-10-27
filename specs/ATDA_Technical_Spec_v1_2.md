# ATDA - Technical Architecture and Assurance Specification v1.2

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
