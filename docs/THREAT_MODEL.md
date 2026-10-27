# ATDA threat model v1.2 - STRIDE, DREAD, attacks and controls

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
