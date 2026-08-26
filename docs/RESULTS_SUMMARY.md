# Results Summary (Canonical Statistics Table)

This is the single source of truth for every statistic cited in the root
[`README.md`](../README.md). Any number appearing in the narrative should match a row here;
if it doesn't, the narrative is wrong, not this file.

> **Reading convention.** Every table below is tagged **[CONF]** (confirmatory: H1, H2),
> **[EXPL]** (post-hoc exploratory: RQ2a, RQ2b, RQ2c), or **[EXPL-M]** (post-hoc, further
> post-hoc extension: M1–M3, root README §16). EXPL and EXPL-M numbers are never to be
> cited as if they carry CONF's evidentiary weight, regardless of how small a resulting
> p-value is, and EXPL-M numbers are, in turn, one tier more provisional than EXPL — see
> root README §16.6 for the outstanding validation debt that keeps M1–M3 below RQ2a–c's own
> confidence. See root README §1–§2 for the confirmatory/post-hoc distinction and §7/§16.2
> for why each tier maintains its own multiplicity accounting.

> **Naming note.** Earlier versions of this file organized §§5–8 under a single "H3." That
> label is retracted (see `docs/METHODOLOGY_NOTES.md`, entry B7) and replaced below with
> RQ2a (where the heterogeneity concentrates), RQ2b (why it might arise), and RQ2c (whether
> H1's conclusion depends on it). The mitigation extension added in §§12–14 below is named
> M1/M2/M3 from first appearance in this file — it was never reported under any other label
> in this document (see `docs/METHODOLOGY_NOTES.md`, entry B8). No number in this file
> changed as part of either relabeling — only section titles and the ID column in §0.

---

## 0. Hypothesis / research-question / mitigation-question ↔ evidentiary tier quick reference

| ID | Question | Tier | Pre-specified before results seen? |
|---|---|---|---|
| H1a | size → spend | **CONF** | Yes |
| H1b | spend → outcome | **CONF** | Yes |
| **H1c** | size → outcome, net of spend (focal test) | **CONF** | Yes |
| H1c core-influence diagnostic | Is H1c driven by a few customers? | **CONF** | Exclusion rules pre-specified; diagnostic itself run after H1c, but rules fixed before inspection |
| H2 (campaign-type interaction) | Is H1c's null homogeneous across ad types? | **CONF** | Yes — the interaction test itself, its stratification scheme, and its threshold were fixed before H1c was run |
| RQ2a (continuous-share re-specification) | Where does H2's heterogeneity concentrate? | **EXPL** | No — motivated by inspecting H2's result |
| RQ2b (serving-structure comparison) | Why might local business differ? | **EXPL** | No |
| RQ2c (subgroup-dependence, formerly "H3") | Does H1c depend on local-business inclusion beyond sample-size effects? | **EXPL** | No |
| M0 (pre-registered gate) | Does a customer-cluster-bootstrap-detectable gap change appear for two candidate strategies on two representative models? | **EXPL-M**, but internally pre-specified | Yes — strategies, models, and the gate rule were fixed before this diagnostic ran |
| M1 (exploratory scan) | Across a wide strategy × model space, which combinations show an FDR-significant gap reduction without a large RMSE cost? | **EXPL-M** | No — post-hoc, high selection-bias risk, disclosed |
| M2 (independent re-test design) | Does a model-class list chosen for theoretical representativeness, not scan performance, confirm any mitigation effect? | **EXPL-M**, but internally pre-specified | Yes — the four model classes and the Size-blind strategy were fixed before this bootstrap was re-run |
| M3 (headline pattern) | Is mitigation effectiveness contingent on predictive-model flexibility? | **EXPL-M**, independently re-tested | No — an observation drawn from M2's results |
| M4 (Campaign-stratified re-test) | Does the campaign-type-stratified strategy improve RMSE/size_gap/localbiz_gap when independently re-tested with M2/M3's protocol? | **EXPL-M**, internally pre-specified | Yes — same 4 model classes as M2, pre-specified for Size-blind, applied to a second strategy |
| M5 (numerical-stability diagnostic) | Does OLS×stratified remain reliable after near-constant-column removal? | **EXPL-M** | No — safeguard added reactively after discovering instability; disclosed as B11 |

---

## 1. [CONF] H1a / H1b / H1c — full statistical decomposition

Customer-level model (n=263 customers). `bid_amount` is the cost-independent primary
outcome; CPC-based estimates are retained for comparison but treated as directionally
informative only.

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a (a-path): size → total spend | +0.537 (p<.001) | +0.537 (p<.001) |
| H1b (b-path): spend → outcome \| size | +1.277 (p<.001) | +0.150 (p=.032) |
| H1c (c′-path): size → outcome \| spend | −0.253 (p=.062) | +0.037 (p=.634) |
| Indirect association (a×b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | <.001 | <.001 |

**Verdict [CONF]:** H1c not rejected; H1a/H1b confirmed. Statistically consistent with
full mediation. Backed by 8 independent robustness methods.

## 2. [CONF] H1c — MDE-at-power detail

| Outcome | Sample | β | 95% CI | p | BF₁₀ | MDE @ 80% power |
|---|---|---|---|---|---|---|
| Approval rate | Full (n=4,407) | −0.0025 | [−0.0064, 0.0014] | .251 | 0.047 | ±0.00535 |
| Approval rate | Excl. spike (n=3,432) | −0.0019 | [−0.0060, 0.0022] | .357 | 0.033 | ±0.00535 |
| CPC (log) | Full (n=4,407) | −0.10 | [−0.58, 0.38] | .756 | 0.044 | ±0.684 |
| CPC (log) | Excl. spike (n=3,432) | +0.35 | [−0.13, 0.83] | .073 | 1.9e+05 | ±0.684 |
| Mean ad rank | Full (n=4,407) | +0.27 | [−0.42, 0.96] | .481 | 0.062 | ±0.943 |
| Mean ad rank | Excl. spike (n=3,432) | +0.02 | [−0.79, 0.83] | .937 | 0.020 | ±0.943 |

## 3. [CONF] H1c core-model influence diagnostic

Customer-level regression (n=228; differs from the 263-customer sample above because this
diagnostic uses the panel underlying the campaign-type composition analysis).

| Diagnostic | Result |
|---|---|
| DFBETA threshold (customer-level, 2/√228) | 0.1325 |
| Customers exceeding threshold | 15 / 228 |
| Are these 15 disproportionately local-business advertisers? | No (t-test on `share_6`, p=.53) |
| Baseline (no exclusion) | β=−0.2525, p=.0618 |
| Pre-specified exclusion rule 1 (thin-observation, n=0 excluded at this threshold) | β=−0.2525, p=.0618 |
| Pre-specified exclusion rule 2 (match-rate<50%, n=100 excluded) | β=−0.2137, p=.2696 |
| Pre-specified exclusion rule 3 (rules 1+2 combined, n=100 excluded) | β=−0.2137, p=.2696 |
| **Configurations reaching significance** | **0 / 4 (100% consistency)** |

**Verdict [CONF]:** confirmatory grade for H1c maintained. See `docs/METHODOLOGY_NOTES.md`
entry A4.

## 4. [CONF] H2 — campaign-type heterogeneity (discrete definition, pre-specified)

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test** | | | | **.023** |

**Verdict [CONF]:** the pre-specified result that, upon inspection, motivated RQ2a–RQ2c
(root README §2, §6) and, one tier further downstream, M1–M3 (root README §16).

## 5. [EXPL] RQ2a — where does the heterogeneity concentrate? (continuous-share re-specification)

Customer-level panel, n=228, `campaign_type` shares as continuous covariates
(`share_1` = website reference category; `share_4` degenerate, auto-excluded).

| Term | Baseline p | Cluster permutation p | Pairs bootstrap CI excludes 0? | Wild-cluster bootstrap p | n methods (of 5) significant |
|---|---|---|---|---|---|
| size_z × share_2 (shopping) | .307 | .538 | No | .471 | 0 / 5 |
| size_z × share_3 (power content) | .004 | .271 | No | .151 | 1 / 5 |
| size_z × share_6 (local business) | .099 | .010 | Yes | .164 | 3 / 5 |

Joint Wald test (all 3 interaction terms): stat=19.69, df=3, **p=.0002**.

**Verdict [EXPL]:** local business is the only term with majority robustness-method
agreement (3/5) — this was not the pre-specified H2 hypothesis (which concerned shopping,
whose own baseline p=.307) and is a post-hoc observation.

## 6. [EXPL] RQ2b — why might local business differ? Serving-structure heterogeneity master table

| Campaign type | n ad groups | % keyword-matched | Median actual-CPC/bid ratio | Classification |
|---|---|---|---|---|
| Website | 8,086 | 96.8% | 2.77 | Auction-like |
| Shopping | 1,025 | 0.7% | 1.89 | Non-auction-like |
| Power content | 248 | 94.8% | 4.33 | Auction-like |
| Brand/new product | 198 | 92.9% | — | Auction-like |
| **Local business** | **266** | **0.0%** | **0.76** | **Non-auction-like** |

**Verdict [EXPL, structural fact]:** established by tracing campaign_dim → adgroup_dim →
keyword_dim; ratios above 1 for other types are not literal overpayment multiples (see
Figure 13 caption).

## 7. [EXPL] RQ2b (continued) — mechanism sub-chain statistical signatures

| Test | Result | Detected? |
|---|---|---|
| Variance heterogeneity (Brown-Forsythe, log CPC, local-biz vs. pooled-other) | stat=12.93, p=.0003 | **Yes** |
| Relationship (b-path) heterogeneity (spend_z × is_localbiz) | β=+1.125, p=.001; joint Wald p=.0009 | **Yes** |
| Leverage heterogeneity (hat-value, local-biz vs. other customers) | t=−1.18, p=.24 | **No** |
| Counterfactual CPC gap | standardized gap = −0.49 SD, t=−4.75, p<.0001 | **Yes (small-to-moderate)** |

**Verdict [EXPL, mixed]:** 3 of 4 tested links detected; reported as partial, mixed support
for a mechanism-level explanation, not a confirmed causal chain (`docs/METHODOLOGY_NOTES.md`
entry B5).

## 8. [EXPL] RQ2c — does H1's conclusion depend on local-business inclusion? (formerly "H3")

### 8a. Central observation

| | β | p | n |
|---|---|---|---|
| Full sample | −0.2525 | .0618 | 228 |
| Local-business-spending customers (n=72) excluded | −0.4991 | .0060 | 156 |

### 8b. Placebo tests

| Placebo type | % of draws matching or exceeding observed shift |
|---|---|
| Random exclusion (n=72, 2,000 draws) | 0.9% |
| Size-distribution-matched exclusion (2,000 draws) | 0.4% |

### 8c. Leave-one-campaign-type-out — INITIAL pass (uncorrected)

| Excluded type | n excluded | n remaining | β after exclusion | \|β\| shift | Rank |
|---|---|---|---|---|---|
| Website | 202 | **26** | +0.565 | 0.313 | **1st** |
| Local business | 72 | 156 | −0.499 | 0.247 | **2nd** |
| Power content | 13 | 215 | −0.238 | −0.014 | 3rd |
| Shopping | 24 | 204 | −0.192 | −0.061 | 4th |

### 8d. Leave-one-campaign-type-out — CORRECTED pass (exclusion-size-matched empirical p)

| Excluded type (stable remainder only) | n excluded | n remaining | Empirical p | Rank |
|---|---|---|---|---|
| **Local business** | 72 | 156 | **1.0%** | **1st** |
| Power content | 13 | 215 | 66.3% | 2nd |
| Shopping | 24 | 204 | 91.7% | 3rd |

**Verdict [EXPL, partially supported]:** 3/3 criteria met under the corrected comparison
only; both passes disclosed per `docs/METHODOLOGY_NOTES.md` entry B6.

## 9. [EXPL] RQ2b (continued) — alternative-explanation audits

| Audit | Result |
|---|---|
| Is missingness explained by pure combinatorics? | No — over-dispersion ratio 73×, χ²=16,583 (df=6, p<.0001) |
| Is the local-business leverage effect driven by 1–2 extreme accounts? | No sign reversal across leave-k-out (k=1,3,5,10,15) |
| Was `size_z`/`n_ad_groups_total` "control" analysis valid? | **No — retracted** (same variable, VIF=∞; entry B3) |
| Was the keyword-approval-pipeline hypothesis applicable to local business? | No — 0% keyword-dimension matches; structural dead end |

## 10. Research-wide multiplicity audit — H1/H2/RQ2a–c only (supports root README §7)

All 25 officially-reported p-values across the H1/H2/RQ2a–c research program. **The M1–M3
mitigation extension (§§12–14 below) is not pooled into this table** — it maintains its
own, separate multiplicity accounting (§13), because it was added in a later phase on a
partially-overlapping but distinct set of models and outcome metrics (root README §7, §16).

| Correction | Tests surviving | Which tests |
|---|---|---|
| Bonferroni (α=.05/25=.0020) | **0 / 25** | none |
| Benjamini–Hochberg FDR | **3 / 25** | RQ2c size-matched-placebo empirical p (.004); RQ2a continuous-share_3 term (.0043); RQ2c full-vs-excluded H1c comparison (.006) — **all three are post-hoc exploratory results** |

## 11. RDD & policy-change screening (supplementary, not adopted)

See `supplementary_identification/SCREENING_SUMMARY.md`. Summary: 0/5 RDD candidates and
0/5 policy-change dates survive decisive re-analysis. Reported as null supplementary
robustness, not an adopted identification strategy.

---

## 12. [EXPL-M] M0 — pre-registered gate (root README §16.1)

A narrower gate, fixed before any exploratory scan, tested whether two candidate strategies
(Size-blind, Campaign-adaptive) produced a customer-cluster-bootstrap-detectable change in
`gap_diff` relative to Baseline, on two models fixed in advance (OLS, HistGB-MAE).

| Strategy | Model | 95% bootstrap CI on gap_diff | Gate triggered? |
|---|---|---|---|
| Size-blind | OLS | includes 0 | No |
| Size-blind | HistGB (MAE loss) | includes 0 | No |
| Campaign-adaptive | OLS | includes 0 | No |
| Campaign-adaptive | HistGB (MAE loss) | includes 0 | No |

**Verdict [pre-specified gate, did not trigger]:** per the rule fixed before this diagnostic
ran, no algorithmic-mitigation claim is supported at this gate's evidentiary tier; the
planned conditional mechanism analysis was correctly skipped, and everything from §13
onward is disclosed as post-hoc exploration (Figure 18 — process diagram).

## 13. [EXPL-M] M1 — exploratory scan across strategies and model specifications (root README §16.2)

| Scan parameter | Value |
|---|---|
| Candidate strategies | up to 12 (Baseline; Size-blind; Spend-normalized; Campaign/Interaction-adaptive; Campaign-stratified; residualized and worst-group variants) |
| Candidate models | 9 (OLS, Ridge, Lasso, ElasticNet, BayesianRidge, RandomForest, HistGB-squared, HistGB-MAE, SVR-RBF) |
| Cross-validation | repeated 5-fold × 30-repetition customer-shuffle |
| Total statistical tests (widest pass) | 728 |
| Tests surviving Benjamini–Hochberg FDR | **463 / 728** |

**Illustrative landscape points (Figure 17; four core strategies × 9 models shown; bubble =
local-business gap, cut0.00):**

| Strategy × model | RMSE | size_gap | localbiz_gap |
|---|---|---|---|
| Baseline × SVR-RBF | 1.3668 | 0.2984 | 0.1180 |
| Size-blind × RandomForest | 1.1745 | 0.1295 | 0.0903 |
| Size-blind × SVR-RBF | 1.2382 | 0.0989 | 0.0412 |

**Winner's-curse check.** An independent bootstrap on the FDR-flagged candidates restricted
to the two models with comparable earlier tooling (OLS, HistGB-squared) found: the OLS
combination showed **no effect** (95% CI included 0), and the HistGB-squared combination
was **reversed** (95% CI entirely positive — the gap widened, not narrowed) relative to
what the FDR scan implied.

**Verdict [EXPL-M, high selection-bias risk, disclosed]:** the 108-combination scan (the
narrower pass reported in root README §16.2, a subset of the 728-test widest pass above) is
retained as a map of the strategy-model landscape and a source of candidate hypotheses, but
no individual FDR-significant cell is cited as evidence on its own. §14 below reports the
one candidate (Size-blind, crossed with four pre-specified model classes) that received
independent confirmation.

## 14. [EXPL-M] M2/M3 — independent, pre-specified-model-class re-test (root README §16.3)

Four model classes were pre-specified for **theoretical representativeness — not scan
performance** — and crossed with a single strategy, Size-blind. Fresh customer-cluster
bootstrap, 200 reps, evaluated against Baseline.

| Model | Class | ΔRMSE [95% CI] | Δsize_gap [95% CI] | Δlocalbiz_gap [95% CI] | Verdict |
|---|---|---|---|---|---|
| OLS | Linear / unregularized | +0.010 [−0.006, +0.027] | −0.018 [−0.043, +0.009] | **+0.082 [+0.051, +0.114]** | No RMSE/size effect; significant **harm** on local-business gap |
| HistGB (squared loss) | Gradient-boosted trees | +0.006 [−0.012, +0.024] | +0.004 [−0.021, +0.030] | **+0.031 [+0.008, +0.055]** | No RMSE/size effect; significant **harm** on local-business gap |
| RandomForest | Bagged tree ensemble | **−0.074 [−0.096, −0.052]** | **−0.167 [−0.201, −0.134]** | **+0.028 [+0.006, +0.051]** | Significant **improvement** on RMSE/size; significant, smaller **harm** on local-business gap |
| SVR-RBF | Kernel machine | **−0.129 [−0.151, −0.107]** | **−0.200 [−0.231, −0.168]** | **−0.077 [−0.094, −0.059]** | Significant **improvement** on all three metrics simultaneously |

**Headline pattern (M3):** mitigation effectiveness of the Size-blind strategy is
contingent on, and roughly monotonic in, predictive-model flexibility. Linear and
boosted-tree specifications show no accuracy or size-parity benefit and a statistically
detectable *increase* in the local-business gap. RandomForest recovers accuracy and
size-parity gains but not local-business parity. Only SVR-RBF achieves a statistically
detectable, simultaneous improvement across all three tracked metrics (Figure 16).

**Verdict [EXPL-M, independently re-tested]:** the one finding in the M-series that has
survived a model-class selection made *before*, not after, seeing which cell performed best
in M1's scan — reported at higher confidence than M1's raw scan results, but below §5–§9's
confirmatory and exploratory tiers (root README §16.6 logs the outstanding validation debt:
Spend-normalized/Campaign-adaptive not yet re-tested at this tier; no SHAP/partial-
dependence mechanism check yet run; cut0.00 only, no cutoff-sensitivity check; no
independent-sample replication).

---

## 15. [EXPL-M] M4 — Campaign-stratified(S9) independent re-test (root README §16.3.1)

| Model | Class | ΔRMSE 95% CI | Δsize_gap 95% CI | Δlocalbiz_gap 95% CI |
|---|---|---|---|---|
| OLS | Linear | [−0.234, 2.940] | [−0.446, 3.685] | [−0.303, 3.760] |
| HistGB | Boosting | [−0.177, 0.238] | [−0.502, 0.339] | [−0.272, 0.457] |
| RandomForest | Bagging | [−0.233, 0.247] | [−0.591, 0.480] | [−0.293, 0.409] |
| SVR-RBF | Kernel | [−0.215, 0.366] | [−0.819, 0.707] | [−0.380, 0.470] |

**Verdict:** 0/4 ALL_THREE_IMPROVED. The reference combined strategy (S9_plus_S1) shows the
same result — full figures are in `rq3_confirm_v2_verdict_patched.csv`.

## 16. [EXPL-M] M5 — Numerical stability diagnostic (root README §16.3.1, entry B11)

| Strategy | Model | tail_ratio (worst metric) | median-direction (localbiz_gap) |
|---|---|---|---|
| S9_Campaign_stratified | OLS | 11.7 | Worsening direction (IQR entirely positive) |
| S9_plus_S1 | OLS | 9.3 | Worsening direction (IQR entirely positive) |
| (the other 10 combinations) | — | < 3 (stable) | Unclear (IQR includes 0) |

**Verdict:** Right-tail instability was confirmed only in the two OLS × stratified
combinations. On a median basis, the worsening of the local-business gap reproduces in the
same direction as Size-blind × OLS (§14, M2/M3) — suggesting this may not be coincidence
but a characteristic of the linear-model structure itself.

---

## Evidence-summary table (matches root README §9)

| | H1 / H2 (Confirmatory) | RQ2a–RQ2c (Post-hoc exploratory) | M1–M3 (Post-hoc, further exploratory) |
|---|---|---|---|
| **Evidence grade** | **Confirmatory** | **Exploratory** | **Exploratory, independently re-tested for one candidate only** |
| Robustness convergence | 8/8 independent methods null for H1; H2 joint test significant | RQ2b: 3/4 mechanism-chain links; 1 methodological reversal disclosed (RQ2c) | M0 gate did not trigger; M1's own top scan candidate reversed under independent bootstrap; M2/M3's four-model-class re-test is the one confirmed pattern |
| Survives own multiplicity audit | Not applicable (H1's null was never significant) | Partially (FDR only; §10) | 463/728 survive FDR in the raw scan (§13), but this is explicitly not treated as evidence on its own — see winner's-curse disclosure |
| Cluster/replicate sizes | n=228–263 (customer-level) | G≈13–72 per sub-cluster | n=228-customer panel bootstrapped 200 reps; no independent sample used |
| Correct citation form | "no confirmed direct algorithmic advantage of size, not uniform across campaign types" | "patterns consistent with, but not establishing, conditional serving-structure effects concentrated in local-business campaigns" | "among four pre-specified model classes, mitigation of the documented disparity is contingent on model flexibility; only the most flexible specification tested closes all three tracked gaps simultaneously" |
| Campaign-stratified re-test | | | 0/4 improved; OLS uniquely worsens localbiz_gap (median-confirmed) — same-direction pattern as Size-blind×OLS |

**Combined takeaway.** The confirmatory questions return a clean, 8-way-robust null with
confirmed heterogeneity. The post-hoc exploratory questions (RQ2a–RQ2c) surface a
partially supported, non-preregistered explanation involving local-business serving
structure. A further, later-added post-hoc extension (M1–M3) then asks whether that
disparity can be reduced algorithmically: a pre-registered gate found no detectable effect
for two candidate strategies on two representative models; a disclosed exploratory scan
across a much wider space flagged candidates that did not survive an independent
winner's-curse check for two of the models tested; and a separate, independent,
pre-specified-model-class re-test found that the Size-blind strategy's mitigation benefit
scales with predictive-model flexibility, with only a kernel-based specification (SVR-RBF)
closing all three tracked gaps simultaneously. None of this changes the H1/H2/RQ2a–c
conclusions above it; it is a downstream question about what to do given those
conclusions, reported at its own, still more provisional, evidentiary tier throughout
(root README §16.4–§16.6).
