# Results Summary (Canonical Statistics Table)

This is the single source of truth for every statistic cited in the root
[`README.md`](../README.md). Any number appearing in the narrative should match a row here;
if it doesn't, the narrative is wrong, not this file.

> **Reading convention.** Every table below is tagged **[L1]** (Level 1, confirmatory) or
> **[L2]** (Level 2, post-hoc exploratory). L2 numbers are never to be cited as if they carry
> L1's evidentiary weight, regardless of how small the resulting p-value is. See root
> README §1–§2 for the definition of this distinction and §7 for why it matters in
> aggregate.

---

## 0. Hypothesis ↔ evidentiary tier quick reference

| ID | Question | Tier | Pre-specified before results seen? |
|---|---|---|---|
| H1a | size → spend | **L1** | Yes |
| H1b | spend → outcome | **L1** | Yes |
| **H1c** | size → outcome, net of spend (focal test) | **L1** | Yes |
| H1c core-influence diagnostic | Is H1c driven by a few customers? | **L1** | Exclusion rules pre-specified; diagnostic itself run after H1c, but rules fixed before inspection |
| H2 (campaign-type interaction) | Is H1c's null homogeneous across ad types? | **L1→L2 trigger** | Interaction test itself was pre-specified in H2's original form; everything downstream of noticing the local-business pattern is L2 |
| Serving-structure comparison | Why does local-business differ? | **L2** | No |
| H3 (subgroup dependence) | Does H1c depend on local-business inclusion beyond sample-size effects? | **L2** | No |

---

## 1. [L1] H1a / H1b / H1c — full statistical decomposition

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

**Verdict [L1, CONFIRMATORY]:** H1c not rejected; H1a/H1b confirmed. Statistically
consistent with full mediation. Backed by 8 independent robustness methods.

## 2. [L1] H1c — MDE-at-power detail

| Outcome | Sample | β | 95% CI | p | BF₁₀ | MDE @ 80% power |
|---|---|---|---|---|---|---|
| Approval rate | Full (n=4,407) | −0.0025 | [−0.0064, 0.0014] | .251 | 0.047 | ±0.00535 |
| Approval rate | Excl. spike (n=3,432) | −0.0019 | [−0.0060, 0.0022] | .357 | 0.033 | ±0.00535 |
| CPC (log) | Full (n=4,407) | −0.10 | [−0.58, 0.38] | .756 | 0.044 | ±0.684 |
| CPC (log) | Excl. spike (n=3,432) | +0.35 | [−0.13, 0.83] | .073 | 1.9e+05 | ±0.684 |
| Mean ad rank | Full (n=4,407) | +0.27 | [−0.42, 0.96] | .481 | 0.062 | ±0.943 |
| Mean ad rank | Excl. spike (n=3,432) | +0.02 | [−0.79, 0.83] | .937 | 0.020 | ±0.943 |

**Note:** the CPC (log) full-sample MDE (±0.684) is reused as the pre-specified SESOI for
TOST equivalence testing referenced in Level 2 sensitivity analyses (§7 below), to avoid
selecting a post-hoc-favorable equivalence bound.

## 3. [L1] H1c core-model influence diagnostic (new, confirmatory tier)

Customer-level regression (n=228; note: differs from the 263-customer sample above because
this diagnostic uses the panel underlying the campaign-type composition analysis).

| Diagnostic | Result |
|---|---|
| DFBETA threshold (customer-level, 2/√228) | 0.1325 |
| Customers exceeding threshold | 15 / 228 |
| Are these 15 disproportionately local-business advertisers? | No (t-test on `share_6`, p=.53) |
| Pre-specified exclusion rule 1 (thin-observation customers, n=0 excluded at this threshold) | β=−0.2525, p=.0618 |
| Pre-specified exclusion rule 2 (match-rate<50%, n=100 excluded) | β=−0.2137, p=.2696 |
| Pre-specified exclusion rule 3 (rules 1+2 combined, n=100 excluded) | β=−0.2137, p=.2696 |
| Baseline (no exclusion) | β=−0.2525, p=.0618 |
| **Configurations reaching significance** | **0 / 4 (100% consistency)** |

**Verdict [L1, CONFIRMATORY robustness]:** confirmatory grade for H1c is maintained. See
`docs/METHODOLOGY_NOTES.md` entry A4.

## 4. [L1→L2 trigger] H2 — campaign-type heterogeneity (discrete definition, original)

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test** | | | | **.023** |

**Verdict:** H1c's null is not perfectly homogeneous across ad-product categories, though no
individual stratum is significant alone. This is the observation that, upon further
inspection, motivated Level 2 (root README §2, §6.1).

## 5. [L2] Continuous-share re-specification (Option B) — full robustness battery per term

Customer-level panel, n=228, `campaign_type` shares as continuous covariates
(`share_1` = website reference category; `share_4` degenerate, auto-excluded).

| Term | Baseline p | Cluster permutation p | Pairs bootstrap CI excludes 0? | Wild-cluster bootstrap p | n methods (of 5) significant |
|---|---|---|---|---|---|
| size_z × share_2 (shopping) | .307 | .538 | No | .471 | 0 / 5 |
| size_z × share_3 (power content) | .004 | .271 | No | .151 | 1 / 5 |
| size_z × share_6 (local business) | .099 | .010 | Yes | .164 | 3 / 5 |

Joint Wald test (all 3 interaction terms): stat=19.69, df=3, **p=.0002**.

**Verdict [L2, POST-HOC/EXPLORATORY]:** local business is the only term with majority
robustness-method agreement (3/5). This was **not** the pre-specified H2 hypothesis (which
concerned shopping campaigns, motivated by a product-feed-validation-pipeline hypothesis
that did not pan out — shopping's own baseline p=.307). Treating local business's emergence
as significant is itself a post-hoc observation and is labeled as such throughout.

## 6. [L2] Serving-structure heterogeneity master table

| Campaign type | n ad groups | % keyword-matched | Median actual-CPC/bid ratio | Classification |
|---|---|---|---|---|
| Website | 8,086 | 96.8% | 2.77 | Auction-like |
| Shopping | 1,025 | 0.7% | 1.89 | Non-auction-like |
| Power content | 248 | 94.8% | 4.33 | Auction-like |
| Brand/new product | 198 | 92.9% | — (insufficient bid-CPC pairs) | Auction-like |
| **Local business** | **266** | **0.0%** | **0.76** | **Non-auction-like** |

**Verdict [L2, structural fact, not inferential]:** local-business ad groups have zero
matches in `keyword_dim`. This is a directly observed data-join fact, established by
tracing campaign_dim → adgroup_dim → keyword_dim, not an inference.

## 7. [L2] Mechanism sub-chain statistical signatures

| Test | Result | Detected? |
|---|---|---|
| Variance heterogeneity (Brown-Forsythe, log CPC, local-biz vs. pooled-other) | stat=12.93, p=.0003 | **Yes** |
| Relationship (b-path) heterogeneity (spend_z × is_localbiz) | β=+1.125, p=.001; joint Wald p=.0009 | **Yes** |
| Leverage heterogeneity (hat-value, local-biz vs. other customers) | t=−1.18, p=.24 | **No** |
| Counterfactual CPC gap (predicted from auction-type bid→CPC relationship vs. observed) | standardized gap = −0.49 SD, t=−4.75, p<.0001 | **Yes (small-to-moderate magnitude)** |

**Verdict [L2, EXPLORATORY, mixed]:** 3 of 4 tested links detected. This is reported as
partial, mixed support for a mechanism-level explanation of H1c's instability — explicitly
**not** a confirmed causal chain (see `docs/METHODOLOGY_NOTES.md` entry B5, which retracts an
earlier internal overstatement of this result).

## 8. [L2] H3 — subgroup dependence, both passes disclosed

### 8a. Central observation

| | β | p | n |
|---|---|---|---|
| Full sample | −0.2525 | .0618 | 228 |
| Local-business-spending customers (n=72) excluded | −0.4991 | .0060 | 156 |

### 8b. Placebo tests (was this just a sample-size effect?)

| Placebo type | % of draws matching or exceeding observed shift |
|---|---|
| Random exclusion (n=72, 2,000 draws) | 0.9% |
| Size-distribution-matched exclusion (2,000 draws) | 0.4% |

### 8c. Leave-one-campaign-type-out — INITIAL pass (uncorrected, unequal exclusion sizes)

| Excluded type | n excluded | n remaining | β after exclusion | \|β\| shift | Rank |
|---|---|---|---|---|---|
| Website | 202 | **26** | +0.565 | 0.313 | **1st** |
| Local business | 72 | 156 | −0.499 | 0.247 | **2nd** |
| Power content | 13 | 215 | −0.238 | −0.014 | 3rd |
| Shopping | 24 | 204 | −0.192 | −0.061 | 4th |

**This initial ranking placed local business 2nd, not 1st — a result that, taken at face
value, did not support a local-business-specific story.**

### 8d. Leave-one-campaign-type-out — CORRECTED pass (exclusion-size-matched empirical p)

Website's 26-customer remaining sample (95% CI width 1.62) is far less stable than the
other three (CI widths 0.53–0.71; correlation between remaining-n and CI width = −0.98) and
is excluded from ranking as unstable, not as favorable-to-report.

| Excluded type (stable remainder only) | n excluded | n remaining | Empirical p (vs. own-size-matched random placebo) | Rank |
|---|---|---|---|---|
| **Local business** | 72 | 156 | **1.0%** | **1st** |
| Power content | 13 | 215 | 66.3% | 2nd |
| Shopping | 24 | 204 | 91.7% | 3rd |

### 8e. H3 verdict

| Criterion | Met? |
|---|---|
| A. Random-placebo empirical p < 20% | Yes (0.9%) |
| B. Size-matched-placebo empirical p < 20% | Yes (0.4%) |
| C. Ranks 1st among *stable* leave-one-type-out comparisons (corrected) | Yes |
| C (uncorrected, for disclosure) | **No — ranked 2nd** |

**Verdict [L2, EXPLORATORY, partially supported]:** 3/3 criteria met under the corrected
comparison; the initial, uncorrected comparison did not support the local-business-specific
story. Both are reported per `docs/METHODOLOGY_NOTES.md` entry B6. **This finding is not
preregistered, is built on sub-clusters below the conventional cluster-count reliability
threshold (G=13–72), and should not be cited at Level 1 confidence.**

## 9. [L2] Alternative-explanation audits

| Audit | Result |
|---|---|
| Is missingness explained by pure combinatorics (more ad groups → more chance of a miss)? | No — over-dispersion ratio 73×, goodness-of-fit χ²=16,583 (df=6, p<.0001). Residual account-level clustering present; cause unidentified. |
| Is the local-business leverage effect driven by 1–2 extreme accounts? | No sign reversal across leave-k-out (k=1,3,5,10,15); pattern strengthens, not weakens, on removal. |
| Was `size_z`/`n_ad_groups_total` "control" analysis valid? | **No — retracted.** They are the same variable (VIF=∞). See `docs/METHODOLOGY_NOTES.md` entry B3. |
| Was the keyword-approval-pipeline hypothesis (parallel to shopping's) applicable to local business? | No — local-business ad groups have 0% keyword-dimension matches; the hypothesis does not apply to this subgroup by construction. Reported as a dead end, not silently dropped. |

## 10. Research-wide multiplicity audit (supports root README §7)

All 25 officially-reported p-values across this repository's entire research program
(excludes distribution-generating procedures: the 48-way specification curve, the 500-way
split-sample replication).

| Correction | Tests surviving | Which tests |
|---|---|---|
| Bonferroni (α=.05/25=.0020) | **0 / 25** | none |
| Benjamini–Hochberg FDR | **3 / 25** | H3 size-matched-placebo empirical p (.004); H2 continuous share_3 term (.0043); H3 full-vs-excluded H1c comparison (.006) — **all three are Level 2 exploratory results** |

**Reading note:** Level 1's H1c null does not "survive" or "fail" this correction, because
it was never claimed significant — the null is the finding. This table exists to prevent
any single Level 2 result, however small its unadjusted p-value, from being read as if it
carried Level 1's confirmatory weight.

## 11. RDD & policy-change screening (supplementary, not adopted)

See `supplementary_identification/SCREENING_SUMMARY.md` for full detail. Summary: 0/5 RDD
candidates and 0/5 policy-change dates survive decisive re-analysis. Reported as null
supplementary robustness consistent with, not required by, the H1c conclusion.

---

## Evidence-summary table (matches root README §9)

| | Level 1: H1c | Level 2: local-business mechanism |
|---|---|---|
| **Evidence grade** | **Confirmatory** | **Exploratory** |
| Robustness convergence | 8/8 independent methods null (incl. new core-influence check, §3 above) | 3/4 mechanism-chain links; 1 methodological reversal disclosed (§8) |
| Survives research-wide multiplicity audit (§10) | Not applicable (null was never significant) | Partially (FDR only) |
| Cluster sizes | n=228–263 (customer-level, stable) | G≈13–72 per sub-cluster (below rule-of-thumb G≥42 for several) |
| Correct citation form | "no confirmed direct algorithmic advantage of size on this platform" | "patterns consistent with, but not establishing, conditional serving-structure effects" |

**Combined takeaway.** The confirmatory question (does size buy a direct advantage?)
returns a clean, 8-way-robust null, unchanged by a newly-added core-model influence check.
The post-hoc question (why isn't that null perfectly uniform?) surfaces a partially
supported, explicitly-flagged, non-preregistered explanation involving local-business
serving structure — including one internal reversal that is disclosed rather than hidden,
and a research-wide multiplicity audit showing that almost none of this repository's
statistics, pooled, survive conservative correction. Read against root README §3 (SSI
framework) and §10 (boundary conditions): advertiser size exhibits structural signal
irrelevance on this platform at the confirmatory tier; whether and how that irrelevance
varies by serving mechanism is an open, exploratory question for future preregistered work.
