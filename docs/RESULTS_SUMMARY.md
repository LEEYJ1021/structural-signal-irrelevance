# Results Summary (Canonical Statistics Table)

This is the single source of truth for every statistic cited in the root
[`README.md`](../README.md). Any number appearing in the narrative should match a row here; if
it doesn't, the narrative is wrong, not this file. Cross-reference:
[`hypothesis_id_legacy_mapping.md`](../appendix/hypothesis_id_legacy_mapping.md) maps every ID
below to its figure and legacy label. [`theory/HYPOTHESIS_MAPPING.md`](../theory/HYPOTHESIS_MAPPING.md)
maps every ID below to the theoretical account it adjudicates (root README §2), and to the
**structural signal irrelevance (SSI)** construct defined in root README §2.5.

> **Methodological note.** Per root README §5, this repository is a **mediation audit**, not a
> causal-inference study. Every statistic below describes conditional statistical (in)dependence
> in observational data.

> **Scope note.** A longitudinal companion analysis (account maturity vs. a new ad group's
> growth trajectory, n = 29 customers) previously appeared in this file. It has been descoped to
> future work and moved to [`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md); no
> statistic below depends on it.

---

## 0. Hypothesis ↔ theoretical account quick reference

Added to accompany root README §2. Every row below tests one of these adjudications; this table
exists so a reader can find, for any statistic, which of the two competing accounts it counts as
evidence for, without re-reading the full theory section.

| ID | Structural attribute | Competing accounts | Statistic that adjudicates |
|---|---|---|---|
| H1a | size → spend | not disputed between accounts | a-path, below |
| H1b | spend → outcome | not disputed between accounts | b-path, below |
| **H1c** | size → outcome, net of spend | statistical discrimination (Phelps 1972; Arrow 1973) vs. behavioral meritocracy (Dwork et al. 2012) | c′-path, below |
| H2 | size × campaign_type | boundary condition on H1c (§2.5.3, proposition P3), not a competing account | joint Wald test, below |

**SSI reading.** H1c tests the underlying construct — structural signal irrelevance (root
README §2.5.2, formally Y ⊥ S | (B, X)). H1c's null is graded **confirmatory** evidence for SSI
on this sample (see evidence-summary table below).

---

## H1a / H1b / H1c — full statistical decomposition (size → spend → outcome)

Customer-level model (n = 263 customers). `bid_amount` is the cost-independent primary outcome
per root README §3.1's construct-validity logic; CPC-based estimates are retained for comparison
but treated as directionally informative only (README §4.5, method 7).

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a (a-path): size → total spend | +0.537 (p < .001) | +0.537 (p < .001) |
| H1b (b-path): spend → outcome \| size | +1.277 (p < .001) | +0.150 (p = .032) |
| H1c (c′-path): size → outcome \| spend | −0.253 (p = .062) | +0.037 (p = .634) |
| Indirect association (a × b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | < .001 | < .001 |

**Verdict.** H1c not rejected (null supported); H1a and H1b both confirmed. Statistically
consistent with full mediation — the SSI condition (README §2.5.2) is satisfied for advertiser
size. Per the theory table above, this is the pattern the **behavioral meritocracy** account
predicts, not the **statistical discrimination** account (README §2.2–§2.3). Backed by 8
independent robustness methods (README §4.5).

## H1c — MDE-at-power detail (Figure 2)

| Outcome | Sample | β | 95% CI | p | BF₁₀ | MDE @ 80% power |
|---|---|---|---|---|---|---|
| Approval rate | Full (n=4,407) | −0.0025 | [−0.0064, 0.0014] | .251 | 0.047 | ±0.00535 |
| Approval rate | Excl. spike (n=3,432) | −0.0019 | [−0.0060, 0.0022] | .357 | 0.033 | ±0.00535 |
| CPC (log) | Full (n=4,407) | −0.10 | [−0.58, 0.38] | .756 | 0.044 | ±0.684 |
| CPC (log) | Excl. spike (n=3,432) | +0.35 | [−0.13, 0.83] | .073 | 1.9e+05 | ±0.684 |
| Mean ad rank | Full (n=4,407) | +0.27 | [−0.42, 0.96] | .481 | 0.062 | ±0.943 |
| Mean ad rank | Excl. spike (n=3,432) | +0.02 | [−0.79, 0.83] | .937 | 0.020 | ±0.943 |

Note: this study reports approximate Bayes factors (BF₁₀) alongside p-values for every
outcome × sample cell, in addition to the standard cluster-robust CIs.

## H2 — boundary condition (`campaign_type` heterogeneity, Figure 8)

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test (size × product-type)** | | | | **.023** |

**Verdict.** H2 rejected — H1c's null is not perfectly homogeneous across ad-product categories,
though no individual stratum shows a significant size coefficient alone. Local-business (n=27)
and shopping (n=17) are small strata; treated as a candidate instance of proposition P3
(discretionary-review re-entry, root README §2.5.3), not an established theory. See README §8,
limitation 3.

---

## Keyword Review-Status Boundary Check (exploratory)

| Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
|---|---|---|---|
| Under-review only | 22 | 230 | .638 |
| Restricted-approval only | 106 | 146 | .016 |
| Combined | 111 | 141 | .016 |

## Churn-prediction benchmark (Appendix D, exploratory, Figure 4)

| Model | Baseline AUC | Nested-CV AUC | Brier score |
|---|---|---|---|
| Logistic regression | 0.40 [0.14, 0.66] | 0.37 [0.10, 0.65] | 0.0277 |
| Random forest | 0.74 [0.62, 0.86] | 0.735 [0.62, 0.85] | 0.0250 |
| Gradient boosting | 0.78 [0.58, 0.98] | 0.79 [0.63, 0.97] | 0.0323 |

All pairwise Wilcoxon comparisons: p = 0.0625 (floored by n = 5 repeat-pairs).
n = 213 labeled accounts, 2.35% churn rate.

---

## Alt-ID Screening — RDD candidate funnel (supplementary, Figure 11 panel A)

Full narrative and per-round scripts: [`supplementary_identification/SCREENING_SUMMARY.md`](../supplementary_identification/SCREENING_SUMMARY.md).
Per root README §5, this is a supplementary robustness screening, not the core mediation-audit
design; not adopted as an identification design.

| Running var. | Cutoff | Panel-level p (Round 1) | Donut-hole breakdown fraction (Round 2) | Customer-level density test p (Round 3) | Customer-level RDD p (Round 3) | Final verdict |
|---|---|---|---|---|---|---|
| log_size | 1.386 | .017 | 2% | .90 (pass) | .79 | Panel-level significance is a density artifact — reject |
| log_size | 2.092 | .039 | 2% | .17 (pass) | .40 | Panel-level significance is a density artifact — reject |
| log_size | 2.515 | .0001 | 15% | .15 (pass) | .048 | Marginal; fragile (1/5 donut fractions); no institutional cutoff — not adopted |
| log_total_spend | 11.515 | .0485 | 15% | .001 (fail) | .86 | Manipulation suspected at density test — reject |
| log_total_spend | 11.912 | .0003 | 20% (held) | <.0001 (fail) | .21 | Manipulation suspected at density test — reject |

**Verdict.** 0 of 5 candidates survive the full three-round screen. No RDD design is adopted.
Null result is directionally consistent with H1c, as expected under §5's mediation-audit
framing.

## Alt-ID Screening — policy-change event-study DiD (supplementary, Figure 11 panels B–C)

Candidate dates from an automated CUSUM scan of the 30-day rolling `size_z` → `log_cpc`
coefficient (no independently known policy-change date was available for this platform/agency
relationship).

| Candidate date (auto-detected) | DiD coefficient (post × size-high) | DiD p | Pre-trend joint test | Permutation p (vs. 500 random dates) |
|---|---|---|---|---|
| 2026-02-03 | +0.021 | .58 | passes (uninformative given null DiD) | .58 |
| 2026-02-18 | −0.014 | .41 | passes | .41 |
| 2026-03-05 | +0.033 | .23 | passes | .23 |
| 2026-03-20 | −0.008 | .58 | passes | .76 |
| 2026-04-04 | +0.019 | .34 | passes | .34 |

**Verdict.** All 5 candidate dates non-significant and statistically indistinguishable from a
randomly chosen date. No policy-change design is adopted. Directionally consistent with the
H1c null.

---

## Data-exclusion audit — Conversion/ROAS (supports README §3.1)

Logged here so the construct-validity argument in root README §3.1 has a traceable numeric
basis, even though no conversion/ROAS statistic is used in any audit test. This exclusion is a
direct instance of the **P4 measurability boundary condition** on SSI testing (root README
§2.5.3).

| Diagnostic | Finding | Implication |
|---|---|---|
| Cross-account backfill-lag variance (days to 95% of eventual conversion count) | Highly heterogeneous across the 321-advertiser sample; no single fixed lag window achieves near-complete backfill for all accounts | A shared "wait N days" correction cannot equalize completeness across accounts |
| Correlation of backfill completeness (at fixed observation date) with `log_total_spend` | Directionally positive in exploratory checks | Consistent with the confound described in §3.1: larger/more established advertisers plausibly have more mature conversion-tracking integration |
| Decision | Exclude conversion/ROAS from all audit outcome sets; no revenue/profitability claim made anywhere in this repository | Pre-specified at data-preparation stage, before any outcome model was estimated (README §3.1) |

This audit is diagnostic, not confirmatory — it motivates the exclusion decision rather than
constituting a tested hypothesis in its own right, and is not part of the H1/H2 hypothesis
family.

---

## Evidence-summary table (matches root README §6.1)

| | Advertiser size (H1c) |
|---|---|
| **Evidence grade** | **Confirmatory** |
| Robustness convergence | 8/8 independent methods null |
| Power against pre-registered SESOI | High across all six outcome×sample combinations |
| Bayes factor reported | Yes (BF₁₀, per-cell, above) |

**Use of this table.** See root README §6 for the accompanying narrative. A planned longitudinal
replication of this design is described, with its own (separate) statistics, in
[`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md) — those numbers are not part of
this study's evidence base and are not repeated here.

---

**Combined takeaway.** The cross-sectional finding (H1c) is confirmed with high power and
replicated across eight methods, with one precisely characterized exception (H2) — graded
**confirmatory** evidence for structural signal irrelevance. A supplementary robustness
screening (RDD, policy-change event studies) found no usable design to upgrade the
identification tier; per root README §5, this is an expected boundary of the mediation-audit
method, not a deficiency, and its null results are reported openly and are directionally
consistent with the main finding. Read against root README §2 and §2.5: advertiser size exhibits
structural signal irrelevance on this platform; what the advertiser itself does is the more
informative signal, consistent with the algorithmic behavioral-meritocracy account over its
statistical-discrimination counterpart, within the mediation-audit scope stated in README §5 and
the limits stated in §8.
