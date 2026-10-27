# ATDA HW-01 — Hardware identity boundary and dual-path sensor node
**Status:** proposed laboratory design, 27 October 2026. **NOT wired, measured, certified, or production deployable.** This document expands rather than replaces the 2026-10-27 v1.2 research release. Original 2025 architecture and original 2026 Git commit remain unchanged.

## 0. Priority and decision
Start with a **physically identity-disconnected sensor acquisition domain**, not a complicated FPGA PII scrubber. If a payment ID enters the sensor subsystem, the hardware privacy goal has already failed. The default build has **no card interface, payment bus, camera, microphone, biometrics, MAC/Bluetooth scans, payment-clock feed or access-controller network connection**. A sealed, minimal sensor MCU receives simulated chemical-class data and issues separate, constrained Path A/B decisions. This is maximum privacy improvement for minimum complexity. A serial directionality claim is **not** proof of a complete data diode or of anonymisation.

## 1. Data-flow and trust domains
```text
TD-P PAYMENTS / ACCESS (out of scope)    X NO PCB/net/radio/clock/data connection
                                            |
TD-S SYNTHETIC SENSOR ---> TD-ACQ signed-boot acquisition MCU
                                      |                 |
                                PATH A branch      PATH B branch
                                  distinct             local
                                alert firmware      fixed-schema-only
                                      |                 |
                                authenticated       k >= 50 exact
                                alert gateway       interaction events
                                      |             / adapt 15m -> 24h
                                  SOC endpoint          |
                                            TD-B EXPORT ENFORCEMENT
                                            fixed coarse statistics
                                                    |
                                       single-direction physical link
                                                    |
                                         analytics-side collector
```
The illustrated 'X' means *physically absent connection*, not a software authorization rule. Both A and B lack payment PII by construction. The laboratory test must not use live chemical threats or personal data.

### 1.1 Electrical partitions and negative connectivity requirements
- **HW-01.01:** TD-P is never connected to TD-S/TD-ACQ at board, cable, connector, wireless, shared peripheral, DMA, test-header or maintenance level; confirm by schematic/netlist inspection and measurements on the assembled prototype. A common enclosure is NOT proof of isolation.
- **HW-01.02:** Use an independent regulated supply for the laboratory sensor board; where co-located in a field enclosure, assess shared power, ground, emissions and side-channels. A separate power supply mitigates but does not mathematically eliminate electromagnetic correlation.
- **HW-01.03:** No bus bridge to the payment/access controller, even through 'trusted' software. Optical isolated one-way egress for B is recommended; transmitter opto/isolator LED -> receiver with no populated reverse path. Audit actual PCB, pin assignment, debug access, maintenance connector and bootloader.
- **HW-01.04:** Hardcoded outgoing schema: the exporter cannot serialize arbitrary bytes, strings, transaction IDs, exact per-interaction timestamps, location coordinates, BLE IDs or arbitrary diagnostics. Reject/disable unknown field types. Timing metadata of release still exists and is a privacy risk.
- **HW-01.05:** Fuse/lock debug interfaces after measured tests; secure boot with authenticated rollback-protected updates; physical seals are tamper evidence, not prevention. Control firmware signing keys off-board.
- **HW-01.06:** Path A shall be a separate classified decision process and authenticated transport; Path B outage/under-k/overflow shall not suppress validated Path A alerts. Chemical-cleaner interferents alone trigger MAINTENANCE not security alarm. Combined signals require separately verified threat evidence and human-governed escalation.
- **HW-01.07:** If data integrity, clock integrity, firmware integrity, buffer capacity, classification validity, or diagnostics fail: Path B export FAILS CLOSED, yields an internal privacy/maintenance fault, never emits partial statistics. Path A fault policy must independently preserve alerting for verified threats and identify untrusted sensors to responders.

### 1.2 One-way communication: where and why
The **only external Path B connection** is from the aggregation/export device to a receiving collector. It is inactive for statistics until the local privacy gate is satisfied (>=50 validated distinct interactions). Do not build a wire for incoming analytics commands: changes must use a separately authenticated, maintenance-governed, physical service procedure and change control. An isolated TX-only physical interface does not prevent a malicious local device from encoding PII in packet timing or malicious aggregates: control payload schema, rate, release cadence and firmware provenance too.

### 1.3 Sensor-edge fixed-format simulator frame
A lab-only **four-byte** internal frame, sent solely from a mock sensor to acquisition firmware: [version=1, class=0..3, quality=0..1, CRC8]. Class: 0=environment/maintenance, 1=narcotics, 2=biohazard, 3=other. **No real CBRN classifier** in this frame; real Path A requires an independently validated high-consequence sensing path and is not simulated as a positive security alarm. CRC8 is for accidental error detection ONLY and provides NO authenticity, freshness, replay protection, or tamper evidence. The strict decoder in `src/hw01_boundary_contract.py` is a unit-testable *software contract*, NOT proof of hardware stripping. All interaction distinctness is established by independent local hardware interaction verification, not by the class frame itself. No unique-person claim may be inferred.

## 2. Architecture options and trades
| Option | Extra complexity | Security advantage | Residual defect | Decision |
|---|---|---|---|---|
| Independent MCU / no payment connectivity | Low | Prevents direct receipt of payment PII | Timing/location inference; local compromise | **HW-01 laboratory baseline** |
| MCU + physical one-way isolated B aggregate egress | Low–medium | No analytics return-channel via that physical link | Covert timing channel and maintenance port remain | Add in laboratory gate 2 |
| FPGA schema gate receiving payment traffic | High | Filter potentially untrusted ingress | Insufficient proof of no leakage, complex verification | **Rejected** unless a true integration constraint emerges |
| Shared CPU software filter | Low | No meaningful physical trust boundary | Kernel/DMA/debug/driver bypass | **Rejected** for normative PII barrier |

## 3. Trust, crypto, and root-of-trust
- Prototype stage 0 can test isolation without a TPM. The *production requirement* is a vendor-evidenced Root of Trust, secure measured boot, rollback protection, signed updates and an attestable identity with lifecycle support (TPM 2.0 or an appropriate embedded secure element). TPM chip presence alone does not validate the chain of trust.
- Do not generate custom ML-KEM/ML-DSA code. Secure transport is later provided by supported, properly validated cryptographic libraries and components. Consult NIST SP 800-193 for protection, detection and recovery of firmware; SP 800-53 SC-7/SC-13/SI-7; IEC 62443-3-3 SR 3.4/SR 5.1 and IEC 62443-4-2 restricted data flow; ISO/IEC 27001:2022 Annex A controls 8.9/8.20/8.22/8.24.
- Laboratory-only debug and firmware access is recorded and signed off; no default passwords, unprotected OTA or private signing keys in this repository.
- Treat secure boot/attestation as **unverified until tested on an actual candidate module**; a chip marketing sheet is not evidence.

## 4. Privacy gates, accounting and timing
- Source data lacks all PII **before first storage**. A local hardware-validated interaction signal generates ephemeral per-epoch dedup tokens, and no sender ID, person ID or payment timestamp is retained.
- Reference Path B code enforces a minimum count of 50 validated **interactions, not people**. An adversary can stimulate 50 interactions. Adaptive windows start at 15 min and extend up to 24 h; at expiry, under-k local counts expire with no statistics output.
- Pre-k aggregate traffic must be absent; independent health telemetry MUST NOT carry customer-correlated information and should be separated from Path B statistics at the physical and logical level. Packet timing/site sparsity is still linkable and requires DPIA.
- Hard deterministic k=50 publication/no-publication is incompatible with global pure epsilon-DP at the 49/50 boundary. A two-sided geometric mechanism can have a limited fixed-query DP guarantee but not full-protocol, human-level privacy. See `docs/PRIVACY_PROOF.md`.
- A 'valid interaction' is NOT proven merely by a digitally generated token. The lab test must measure event-counter spoofing, replay, clock faults, buffer exhaustion and restart behavior.

## 5. Safety / abuse-case priorities
1. Payment host compromise -> attempt injection through nonexistent interface: prove physically absent paths, including service and RF.
2. Insider changes firmware -> attempts output covert channel: signed changes, isolated keys, firmware attestations, strict output parser, independent review, egress limits.
3. Maintenance cleaner interference -> nuisance alarms: maintenance-only for isolated cleaning signature, never suppress independent validated threat evidence.
4. Stolen/sabotaged edge node -> fabricated background analytics: attested provenance, anomaly checks, local quarantine, audit.
5. Fault injection -> reboots and dedup reset: under-k export denied during resets/uncertain state, wipe and conservative recovery.

## 6. What HW-01 deliberately cannot claim
No chemical sensitivity/specificity, false alarm rate, cryptographic certification, electrical isolation rating, electromagnetic assurance, legally sufficient anonymisation, person-level DP, firmware attestation, FIPS 140-3 module approval, IEC 62443 conformity, NIS2 compliance or readiness for an actual ATM connection is established by this paper design.

## 7. Gate outcome
The concept graduates from Gate 0 (paper and software) to Gate 1 (bench) ONLY after a documented schematic, purchase provenance, witness-reviewed prohibited-interface netlist, representative negative tests and a signed engineering test log. The system is never connected to live payment hardware in Gate 1.
