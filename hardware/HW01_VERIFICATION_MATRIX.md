# ATDA HW-01 — Bench verification and evidence matrix
**Date:** 2026-10-27. **Status:** planned acceptance tests, NOT performed on hardware.

## Entry gate: evidence chain
Before powering any board: approve schematic revision and BOM; board photos front/back; electrical connectivity table including external enclosure/metalwork; list of populated and unpopulated connectors; firmware image hash and signing-policy record; physical test setup; clock source assumptions; all equipment calibration IDs; controlled synthetic test data. A pass requires witnesses and a reproducible test record. Unit tests alone never satisfy hardware gates.

| ID | Verification | Procedure (synthetic inputs only) | PASS criterion | Evidence / owner | Current |
|---|---|---|---|---|---|
| HW-T01 | Payment isolation | Compare schematics/netlists for all cable, copper, RF and debug connections; physical continuity and oscilloscope tests after build | No permissible TD-P -> TD-S/TD-ACQ interface, including shared test ports; side-channel review recorded | Electrical engineer, signed netlist and measurements | NOT TESTED |
| HW-T02 | Fixed-format ingress | Fuzz versions, class, flags, lengths and CRC of lab frame | Every malformed frame rejected; no arbitrary string channel | Firmware QA; fuzz corpus, counters | Software unit test only |
| HW-T03 | Path B egress diode | Inject back-channel stimuli / reverse TX attempts at collector-side pins; inspect populated parts | No electrically available reverse data path; no undocumented maintenance bypass | Hardware security; schematic/photo/scope | NOT TESTED |
| HW-T04 | Under-k silence | 0, 1, 49 synthetic verified interactions with observation of physical TX | Zero statistical frames; reset/clock/buffer faults likewise zero | Independent tester; packet trace and logic analyser | NOT TESTED |
| HW-T05 | Exactly 50 interactions | 50 synthetic distinct validated interactions; include repeated events, injected duplicates | Release only on permitted matured window; counter cannot use injected duplicate labels | Firmware + QA; trace | Software Path B test only |
| HW-T06 | Time boundary | Advance synthetic monotonic clock 15 min to 24 h, with wall-clock rollback and power interruption | Release policy as documented; no early publish; under-k expires, not silently retained | Firmware QA; trace | Software Path B test only |
| HW-T07 | Memory forensics | Pause lab board after <50; inspect RAM/NVM, dump through permitted developer channels | No PII, payment trace, exact customer timestamps, or recoverable cross-epoch ID | Privacy tester; inventory and dump report | NOT TESTED |
| HW-T08 | Path A independence | Force Path B CPU/link/storage unavailable while lab Path A channel runs approved dummy-alert event | Path B failure does not block independent Path A alerting; no real threat sample required | Safety engineer; latency histogram | NOT TESTED |
| HW-T09 | Cleaner interference | Synthetic maintenance-class signal only; then independent benign test of combined classifications | Cleaner alone cannot issue security alert; independent verified threat evidence not masked by maintenance | Safety/test leads | NOT TESTED |
| HW-T10 | Secure boot / rollback | Boot signed image; mutate image; attempt older signed image; request recovery | Mutated/rolled-back firmware not accepted; recovery authenticated; failure signal observed | Firmware security + vendor | NOT TESTED |
| HW-T11 | Debug/maintenance attack | Attempt UART/JTAG/SWD after final locked profile; check factory/service procedures | No unauthorized memory read/write or bypass of data boundary | Red team, board vendor | NOT TESTED |
| HW-T12 | Brownout and injected clock fault | Repeated power cycles and clock tampering near k=49/50 | No early output; no stale or duplicate aggregate release; A and B fault policy documented | Hardware QA | NOT TESTED |
| HW-T13 | Covert timing channel | Generate worst-case encoded sensor patterns and measure B output timing/size | Pre-k no statistical output; after-k only bounded coarse release, with measured residual information risk | Privacy red team | NOT TESTED |
| HW-T14 | Attestation and updates | Challenge device; revoke trust; update and recover | Untrusted or unmeasured firmware quarantined before new telemetry; evidence covers actual hardware | Fleet-security team | NOT TESTED |
| HW-T15 | End-to-end egress budget | Load 10k synthetic interactions/epoch; fuzz sensor classes and CRC faults | No PII fields; no oversized frames; stable memory and declared fail-closed overflow behavior | Firmware QA | NOT TESTED |
| HW-T16 | Privacy regulatory assessment | Model sparse sites, time correlation, auxiliary CCTV and linkage; evaluate Article 35 DPIA | Written DPIA and documented residual risk acceptance before any live deployment | DPO/legal, not engineering sign-off | NOT TESTED |

## Threat-based red-team scenarios
- State-level compromise: malicious signed update, transport downgrade, OTA supply-chain corruption, remote collector compromise.
- Insider: debug dongle, maintenance bypass, fake firmware attestation, privileged clock or policy changes.
- Supply chain: substituted microcontroller, counterfeit isolator, altered bootloader, pre-installed radio.
- Side-channels: power/ground, RF, timing at analytics link, release timing after k, identity inferred from sparse site/time.
None is discharged by a simple unit test.

## Measurements and stage-gate targets (project proposals, not verified metrics)
- 100% of enumerated external interfaces have a signed source/destination owner in approved netlist; **any** unreviewed path fails Gate 1.
- 100% of malformed fixed-format synthetic records rejected in defined corpus; fuzz coverage reported, not assumed complete.
- Exactly 0 observed pre-k statistical transmissions in every bench negative case; this is sample evidence, not a proof against all faults.
- Path A independent latency goal **to be derived** from operational incident-response requirements. Do not invent a universal zero-latency number.
- Temperature, humidity, EMI, ESD, fault injection, 30-day reliability and chemical classifier accuracy are later gates, not passed.
- Every PASS must cite measured date, build/serial ID, test harness commit SHA, waveform/packet digest and accountable reviewer. Unrun tests remain NOT TESTED in evidence registers.
