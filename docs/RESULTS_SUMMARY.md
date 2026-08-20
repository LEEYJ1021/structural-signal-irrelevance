# Results Summary (Canonical Statistics Table)

This is the single source of truth for every statistic cited in the root
[`README.md`](../README.md). Any number appearing in the narrative should
match a row here; if it doesn't, the narrative is wrong, not this file.
Cross-reference: [`hypothesis_id_legacy_mapping.md`](../appendix/hypothesis_id_legacy_mapping.md)
maps every ID below to its figure and legacy label.

---

## H1a / H1b / H1c — full statistical decomposition (size → spend → outcome)

Customer-level model (n = 263 customers). `bid_amount` is the cost-independent
primary outcome; CPC-based estimates are retained for comparison but treated
as directionally informative only (README §5.4, method 7).

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a (a-path): size → total spend | +0.537 (p < .001) | +0.537 (p < .001) |
| H1b (b-path): spend → outcome \| size | +1.277 (p < .001) | +0.150 (p = .032) |
| H1c (c′-path): size → outcome \| spend | −0.253 (p = .062) | +0.037 (p = .634) |
| Indirect association (a × b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | < .001 | < .001 |

**Verdict.** H1c not rejected (null supported); H1a and H1b both confirmed.
Statistically consistent with full mediation. Backed by 8 independent
robustness methods (README §5.4).

## H1c — MDE-at-power detail (Figure 2)

| Outcome | Sample | β | 95% CI | p | BF₁₀ | MDE @ 80% power |
|---|---|---|---|---|---|---|
| Approval rate | Full (n=4,407) | −0.0025 | [−0.0064, 0.0014] | .251 | 0.047 | ±0.00535 |
| Approval rate | Excl. spike (n=3,432) | −0.0019 | [−0.0060, 0.0022] | .357 | 0.033 | ±0.00535 |
| CPC (log) | Full (n=4,407) | −0.10 | [−0.58, 0.38] | .756 | 0.044 | ±0.684 |
| CPC (log) | Excl. spike (n=3,432) | +0.35 | [−0.13, 0.83] | .073 | 1.9e+05 | ±0.684 |
| Mean ad rank | Full (n=4,407) | +0.27 | [−0.42, 0.96] | .481 | 0.062 | ±0.943 |
| Mean ad rank | Excl. spike (n=3,432) | +0.02 | [−0.79, 0.83] | .937 | 0.020 | ±0.943 |

## H2 — boundary condition (`campaign_type` heterogeneity, Figure 8)

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test (size × product-type)** | | | | **.023** |

**Verdict.** H2 rejected — H1c's null is not perfectly homogeneous across
ad-product categories, though no individual stratum shows a significant
size coefficient alone. Local-business (n=27) and shopping (n=17) are small
strata; see README §11, limitation 8.

## §7.1-Maturity — account maturity vs. initial growth slope (Figure 5)

| statistic | value |
|---|---|
| n (customers) | 29 |
| n (ad groups, informational) | 204 |
| OLS beta (raw scale) | 8.34 |
| OLS HC3 p-value | .576 |
| Bootstrap 95% CI (raw scale) | [−15.84, 43.08] |
| Cluster permutation p-value | .663 |
| Spearman rho | −.02 (p = .92) |
| Leave-one-out (largest customer excluded) permutation p-value | .702 (sign unchanged) |
| Winsorized (10%) OLS beta / p | 1.48 / .841 |
| Rank-rank OLS beta / p | −.02 / .924 |
| Standardized effect size (beta) | .085 |
| Pre-registered large-effect detection threshold | .50 |
| Observed effect as % of detection threshold | 16.9% |

## §7.2-EarlySignal / §7.2-MaturityAdd — early signal vs. maturity (Figure 6A–B)

| early/later window (days) | n (ad groups) | Own-signal within-customer LOCO ρ | +Maturity within-customer LOCO ρ | within-customer improvement | repeated-split Wilcoxon p |
|---|---|---|---|---|---|
| 14 / 14 | 204 | 0.467 | 0.487 | +0.019 | .038 (worse on repeated-split ρ) |
| 30 / 30 | 184 | 0.275 | 0.257 | −0.018 | .119 |
| 30 / 60 | 179 | 0.060 | 0.061 | +0.001 | .019 (worse on repeated-split ρ) |

## §7.2-Flagging — decision-cutoff exploration (Figure 6C–D)

| decision cutoff (days) | out-of-fold predictive ρ (95% bootstrap CI) | lift @ threshold=0.25 | lift @ threshold=0.40 |
|---|---|---|---|
| 7 | 0.304 [0.145, 0.445] | 0.83 | 1.27 |
| 14 | 0.265 [0.123, 0.404] | 1.33 | 1.23 |
| 21 | 0.334 [0.210, 0.459] | 1.42 | 1.36 |

## TOST equivalence (Figure 9)

| Test | Observed effect | Equivalence margin (SESOI) | TOST p | Equivalence established? |
|---|---|---|---|---|
| RQ1: maturity → growth slope | 0.085 | ±0.20 | .197 | No |
| RQ2/H2b: maturity → prediction improvement | 0.023 | ±0.05 | .290 | No |

## RQ2 — keyword review-status boundary check (exploratory)

| Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
|---|---|---|---|
| Under-review only | 22 | 230 | .638 |
| Restricted-approval only | 106 | 146 | .016 |
| Combined | 111 | 141 | .016 |

## RQ4 — churn-prediction benchmark (Appendix D, exploratory, Figure 4)

| Model | Baseline AUC | Nested-CV AUC | Brier score |
|---|---|---|---|
| Logistic regression | 0.40 [0.14, 0.66] | 0.37 [0.10, 0.65] | 0.0277 |
| Random forest | 0.74 [0.62, 0.86] | 0.735 [0.62, 0.85] | 0.0250 |
| Gradient boosting | 0.78 [0.58, 0.98] | 0.79 [0.63, 0.97] | 0.0323 |

All pairwise Wilcoxon comparisons: p = 0.0625 (floored by n = 5 repeat-pairs).
n = 213 labeled accounts, 2.35% churn rate.

---

**Combined takeaway.** The cross-sectional finding (H1c) is confirmed with
high power and replicated across eight methods, with one precisely
characterized exception (H2). The longitudinal extension (§7) is
directionally consistent but not TOST-confirmed. Account size — and,
provisionally, tenure — does not appear to be a useful proxy for how a
given advertiser or ad group will perform; what the unit itself does is
the more informative signal, within the associational limits stated in
README §6.4 and §11.
