# ATDA post-quantum cryptography migration plan

**27 October 2026 | Design and procurement controls only.** Nothing in this repository performs ML-KEM/ML-DSA or claims hardware/PKI conformity.

**Research attribution (30 October 2026):** NIST FIPS 203, 204 and 205 were published in **August 2024**, before the dated ATDA 2025 concept; IETF hybrid TLS RFC 10024 was published in **August 2026**. These are pre-existing external standards, not ATDA inventions, and the current repository has no implemented PQC primitives or validated module. See [Related work and prior art](RELATED_WORK_AND_PRIOR_ART.md).

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
