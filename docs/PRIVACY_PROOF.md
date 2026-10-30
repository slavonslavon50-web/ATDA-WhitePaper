# Privacy assurance and mathematical boundaries (ATDA Path B v1.2)

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

For attribution of the established geometric mechanism and differentiation between person-based k-anonymity, interaction-event release gating and streaming-adaptive privacy research, consult the [source-linked prior-art review](RELATED_WORK_AND_PRIOR_ART.md). A 50-event release rule is **not** person-level k-anonymity; threshold-dependent publication is **not** whole-protocol pure epsilon-DP.

- L. Sweeney (2002), *k-Anonymity: A Model for Protecting Privacy*: https://doi.org/10.1142/S0218488502001648
- A. Ghosh, T. Roughgarden, M. Sundararajan (2008 preprint), *Universally Utility-Maximizing Privacy Mechanisms*: https://arxiv.org/abs/0811.2841


- Dwork and Roth, *The Algorithmic Foundations of Differential Privacy*, 2014 (standard DP definition).
- NIST SP 800-53 Rev.5: privacy and access-control protections; not a proof of DP.
- EDPB, *Guidelines 02/2026 on Anonymisation* (public consultation draft, 08 July 2026): https://www.edpb.europa.eu/documents/guideline/guidelines-022026-on-anonymisation_en
- GDPR Art. 5(1)(b)-(c), Art.25 and Art.35: https://eur-lex.europa.eu/eli/reg/2016/679/oj
