# ATDA cost-benefit, milestones and open R&D

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
