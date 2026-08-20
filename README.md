# Not New, But Renewed: Structural Attributes Don't Matter on an Algorithmically-Mediated Ad Platform

*A cross-sectional and longitudinal investigation into advertiser-size fairness and cost-efficiency allocation on a Korean paid-search platform.*

> **Scope note.** All "mediation," "path," and "effect" language in this report describes decomposed statistical association in observational panel data, not identified causation — see §6.4 for the full statement and why. This applies globally and is not repeated at every instance below; where it matters locally, a section links back here instead.

---

## Table of contents

0. [Scope Note](#scope-note-see-banner-above)
1. [Overview & Contributions](#1-overview--contributions)
2. [Introduction & Research Question](#2-introduction--research-question)
3. [Theoretical Framing](#3-theoretical-framing-the-structural-blindness-construct)
4. [Data & Setting](#4-data--setting)
5. [Main Results — Study 1](#5-main-results--study-1)
6. [Effect-Size Interpretation](#6-effect-size-interpretation-why-small-is-the-point-not-the-caveat)
7. [Longitudinal Extension — Study 2](#7-longitudinal-extension--study-2)
8. [Design Artifact](#8-design-artifact)
9. [Boundary Conditions & Generalizability](#9-boundary-conditions--generalizability)
10. [Practical Implications](#10-practical-implications)
11. [Limitations](#11-limitations)
12. [Methodology Summary](#12-methodology-summary)
13. [Discussion](#13-discussion)
14. [How to Reproduce](#14-how-to-reproduce)
15. [Appendices](#15-appendices)
16. [Repository Structure](#16-repository-structure)

---

## 1. Overview & Contributions

**Contributions.**

1. A **mediation-structured audit design** — testing whether a structural attribute's statistical association with an algorithmic outcome is *direct* or *routes entirely through* a legitimate behavioral channel — rather than testing only for a raw outcome gap.
2. An **eight-method robustness battery** (specification curve, placebo test, cluster permutation, bootstrap CI, approximate Bayes factor, MDE-at-power, temporal split replication, cost-sharing-artifact isolation) applied to a single confirmatory hypothesis.
3. A **falsifiable boundary-condition statement** (§9) that turns "nothing shows a residual association" into a scoped, testable claim rather than an unconditional one.
4. A **design artifact** (§8) — a concrete, implementable flagging rule grounded in a confirmed within-customer result, with its own empirical backtest and an honest statement of what that backtest can and cannot show.

**At a glance.**

| Study | Research question | Confirmatory verdict | Key figures |
|---|---|---|---|
| 1 — cross-sectional | Does advertiser size directly affect algorithmic outcomes, net of spend? | Null not rejected (H1c), replicated 8 ways | Figs 1, 2, 3, 7 |
| 1 — boundary | Is that null homogeneous across ad-product categories? | Rejected — joint Wald p = .023 | Fig 8 |
| 2 — longitudinal | Does account maturity affect a new ad group's early growth? | Null, TOST inconclusive | Figs 5, 9 |
| 2 — early signal | Is an ad group's own early signal predictive, and is there an optimal flagging day? | Predictive; no statistically optimal day | Fig 6 |

---

## 2. Introduction & Research Question

Two advertisers run campaigns on the same search-ads platform. One has operated for years and manages hundreds of ad groups; the other is comparatively small. The intuitive expectation is that the larger, more established advertiser receives more favorable algorithmic treatment — faster approval, cheaper clicks, better ad rank — independent of how much either advertiser actually spends. Most existing platform-fairness audits stop at testing whether a raw outcome gap exists across a structural category like account size.

**This report's contribution is a different starting point: does the gap run *directly* through size, or does it run *entirely* through a legitimate, non-protected channel — here, total spend?** That distinction is mapped in §3.2 onto the disparate-treatment / disparate-impact framework from the algorithmic-fairness literature and is the methodological core of the paper. Everything downstream — the eight-method robustness battery (§5.4), the artifact-isolation logic (Figure 7), and the falsifiable boundary-condition statement (§9) — exists to make that association test as hard to fool as possible on one well-documented case.

**The case.** A panel of **321 advertisers** and approximately **19.3 million rows** of daily/hourly performance data from a single Korean search-ads ecosystem (§4). Applying the audit design here, advertiser size shows no detectable *direct* statistical association with approval rate, cost efficiency, or ad rank once total spend is held constant — a pattern this report terms **structural blindness** (§3).

**Research Question (RQ1).** *Is advertiser size directly, statistically associated with algorithmic outcomes — approval rate, cost efficiency, and ad rank — independent of the advertiser's spending behavior, once spend is held constant?*

**Scope statement.** The claim is not an unconditional universal one. Within this platform, how completely the direct association vanishes varies modestly by ad-product category (§5.5, §9a). Beyond this platform, the underlying mechanism is expected to generalize in *direction* to platforms with comparable real-time-auction architecture, and to plausibly weaken under mandatory human review, in illiquid new categories, or where tenure is an explicit ranking feature (§9b).

---

## 3. Theoretical Framing: The Structural Blindness Construct

### 3.1 Definition

**Structural blindness** describes a real-time, auction-based serving system whose observed approval, cost-efficiency, and ranking outcomes track a unit's *current behavioral signal* and show **no detectable residual statistical association** with the *structural attributes of the account behind it*, once the legitimate channel through which that attribute could plausibly operate (here, spend) is held constant. This is a claim about statistical pattern, not about raw outcomes, and not by itself a claim about internal decision logic this analysis cannot observe.

### 3.2 Grounding the construct in the fairness-in-ML literature

The distinction between *disparate treatment* — differential treatment conditional on a structural attribute itself — and *disparate impact* — differential outcomes arising through a legitimate, attribute-correlated channel (Barocas & Selbst, 2016) is mapped directly onto the decomposition tested here. **H1c** (§3.3) asks whether the *direct* path from size to outcome shows a residual association once spend is held constant. A surviving residual association would be a pattern consistent with disparate treatment; a vanishing one, with the indirect path intact, is consistent with disparate-impact-style allocation through a legitimate channel — both are statements about observational pattern, not adjudicated causal claims. Platform-accountability audits more broadly (e.g., Sweeney, 2013; Ali et al., 2019) typically test for a raw outcome gap; this design instead asks *which statistical path* the gap runs through, which is the reusable methodological contribution independent of which way any single application's answer points.

| | Structural attribute | Candidate legitimate mediating channel |
|---|---|---|
| This investigation | Advertiser size (spend-tier) | Total spend |

### 3.3 Formal hypotheses

- **RQ1.** Is size directly associated with outcomes, independent of spend? (§5.3–§5.4)
- **H1a (a-path).** Size is positively associated with total spend. (§5.4, method 8)
- **H1b (b-path).** Spend is positively associated with outcome quality, holding size constant. (§5.4, method 8)
- **H1c (c′-path, central).** Size shows no direct association with outcome quality once spend is held constant. (§5.3–§5.4)
- **H1 (composite).** The entire size–outcome relationship runs through spend, not through size itself. (§5.3–§5.4)
- **H2 (boundary).** H1c's null holds homogeneously across ad-product categories. (§5.5)
- **RQ2 (exploratory).** Does keyword-level discretionary review interact with size? (§9a)

A separate, fully exploratory question sits outside this hypothesis family entirely: **RQ4**, whether churn can be predicted from approval/cost/efficiency features — reported only in **[Appendix D](appendix/churn_prediction_rq4.md)**.

### 3.4 What "confirmed" means

Every null result below is reported alongside its minimum-detectable-effect (MDE) band at 80% power, so a null can be read as *well-powered* rather than merely *undetected* (Figure 2). "Confirmed null" is distinguished throughout from "unconditional universal claim."

---

## 4. Data & Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata incl. `campaign_type` (ad-product code) | 1,504 | 263/321 |
| Ad group dimension (snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status` (review code), bid price | 1,503,289 | 256/321 |

Conversion and ROAS variables were excluded entirely: the platform's conversion API backfills conversions per account on a delayed, inconsistent schedule, which breaks construct validity for anything built on top of it — a design decision made before modeling began.

**Single platform, single agency — a design choice, not only a limitation.** All data originate from one Korean ad-tech provider on one search platform. This bounds external generalizability (§9b), but it is also what makes the internal test clean: every advertiser faces the same ranking algorithm, the same approval pipeline, and the same measurement process, removing a whole class of between-platform confounds that would otherwise entangle any size effect. Framed as an audit-methodology paper (§2), this single-platform design should be read the way a single well-instrumented case study is read in the accountability-audit literature — a proof of concept for the *method*, with an explicitly bounded external-validity claim.

---

## 5. Main Results — Study 1

### 5.1 Where would an advantage even live?

Before testing anything about size, the analysis located *where* performance variation sits.

![Figure 1 | Multilevel variance decomposition of advertising performance](figures/Figure1_variance_decomposition.png)

**Figure 1.** Across ~663K observations, log ad spend is dominated by unexplained residual variance (ICC = 0.825), not by who the customer is (ICC = 0.050). Click-through rate similarly concentrates at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both patterns hold with or without month fixed effects, ruling out seasonality. This motivates, but does not itself test, H1: "who the customer is" is associated with comparatively little of what happens on this platform.

### 5.2 The raw gap looks real — until clustering is accounted for

Splitting advertisers into four spend-based size tiers and comparing approval rate, CPC, and ad rank with a Kruskal–Wallis test shows significant differences (p < .001 for CPC and ad rank; p = .0006 for approval rate). This does not survive a customer-level cluster permutation test (2,000 iterations): most of the apparent gap in approval rate and CPC evaporates once same-customer non-independence is accounted for — the exact failure mode the mediation-based design in §3.2 is built to correct.

### 5.3 The central confirmatory test (H1c)

![Figure 2 | Advertiser-size effect on approval, cost efficiency, and ad rank, controlling for spend](figures/Figure2_fairness_forest_plot.png)

**Figure 2.** Controlling for log spend in a cluster-robust regression, all six outcome × sample combinations return **non-significant** direct-path coefficients for size (cluster-robust p > .07). Every 95% bootstrap CI sits inside, or at the edge of, its own MDE band — the sample is well-powered to detect an effect smaller than what the raw comparison in §5.2 would suggest is "the size of the effect." Approximate Bayes factors favor the null in five of six tests; the sixth (CPC under spike exclusion) is a directionally-reversed sensitivity finding, not a confirmatory one.

### 5.4 Stress-testing across eight independent methods

1. **Multiverse specification curve** — 48 defensible analytic choices; 0/48 reach significance for any outcome.
2. **Placebo test** — device-type share (which size *shouldn't* predict) is significant under the raw distributional test but null under the spend-controlled regression, showing the regression is measuring the right thing.
3. **Customer-and-month fixed-effects panel regression.**
4. **Two-stage least squares** with lagged spend as an instrument — the first-stage F-statistic could not be recovered (code exception); flagged and excluded from any conclusion rather than silently dropped. **No causal identification strategy in this report was successfully completed; all reported patterns remain associational.**
5. **Temporal split-sample replication.**
6. **Benjamini–Hochberg FDR correction** across the six primary hypotheses.

![Figure 3 | Multiverse specification curve and placebo test](figures/Figure3_specification_curve_placebo.png)

**Figure 3.** Panel A: none of 48 specification choices reach significance for any outcome. Panel B: the raw distributional test is significant for *both* the real outcome and the device-share placebo, proving a distributional test alone is not a clean placebo here (size tiers correlate with many unrelated account traits). The informative comparison is the spend-controlled regression, where real and placebo outcomes are equally, indistinguishably null.

7. **Isolating a mechanical artifact in CPC.** Because CPC = cost / click and spend is built from cost, any spend–CPC association carries a mechanical component by construction. A customer-level permutation procedure (reshuffling click within customer, cost fixed; 2,000 iterations) shows the observed spend–log(CPC) coefficient (+1.277) falls *below* the lower bound of the purely-mechanical null distribution (mean +1.552, 95% range [1.544, 1.556]) — informative directionally, not as a stand-alone quantitative claim. A lagged replication (day *t* spend → CPC at *t*+1, *t*+7, immune to same-day cost-sharing) confirms a same-signed, significant association at both lags (β = +0.538, +0.544; both p < .001).
8. **Replicating the mediation structure on a cost-independent outcome.** `bid_amount` shares no cost or click term with spend, so it carries none of the artifact isolated in method 7. At the customer level (n = 263): the indirect (spend-linked) association is significant (bootstrap 95% CI [0.008, 0.159]; permutation p < .001), while the direct association of size, net of spend, is not (p = .634) — the same qualitative pattern as the CPC-based model, now on an artifact-free outcome. Methods 7–8 jointly confirm H1a and H1b.

![Figure 7 | Spend-mediation b-path: CPC-based vs. cost-independent outcome](figures/Figure7_mediation_forest.png)

**Figure 7.** The spend–outcome coefficient shrinks from +1.277 (CPC-based, partly mechanical) to +0.150 (bid_amount-based, cost-independent) once the shared cost term is removed — direction survives, magnitude does not, consistent with the CPC-based estimate being inflated by construction rather than by a stronger underlying association.

**On causal-sounding vocabulary.** Every "path," "mediation," and "effect" statement in this report — including H1a/b/c themselves — describes an associational pattern from observational panel data, not an identified causal effect. This vocabulary is standard in the fairness-audit literature and is used deliberately, not as a hedge added after the fact (§11, item 5). What the eight methods jointly support is a materially stronger form of associational evidence than any single coefficient: the same qualitative pattern (indirect present, direct absent) replicates across a contaminated outcome and an artifact-free outcome, across 48 specifications, against a placebo, across two time splits, and survives multiple-testing correction.

### 5.5 Is the null homogeneous across contexts? (H2)

Close to, but not perfectly, homogeneous — treated here as a substantive finding, not a complication. Stratifying the spend-controlled CPC model by `campaign_type` (a platform-defined ad-product code, not an industry classification — see §9a) and running a joint Wald test on the size × product-type interaction gives **p = .023**.

![Figure 8 | Campaign product-type heterogeneity](figures/Figure8_boundary_condition_forest.png)

**Figure 8.** No individual stratum shows a significant size coefficient on its own, but the joint test is significant:

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | .052 |
| Local business (6) | 1,306 | **27** | +0.312 | .211 |
| Shopping (2) | 2,161 | **17** | +0.245 | .151 |
| **Joint Wald test** | | | | **.023** |

The local-business (n = 27) and shopping (n = 17) strata are small, and the joint test's significance should be read with that in mind (§11).

### 5.6 Conclusion of the confirmatory analysis

Raw size-tier gaps are statistically detectable but fragile once clustering is accounted for. The spend-controlled test — replicated on a cost-independent outcome — returns a clean, well-powered null for the direct association of size (H1c), backed by eight robustness checks, with one precisely characterized exception: the null is not perfectly homogeneous across ad-product categories (H2). The apparent advantage of being a large advertiser is, to first order, consistent with being fully accounted for by spending more rather than by size itself.

---

## 6. Effect-Size Interpretation: Why Small Is the Point, Not the Caveat

The raw distributional comparison (§5.2) produced effect sizes in the ε² = 0.002–0.079 range. Read against the theoretical structure in §3, this is close to the *predicted* result. If H1c is true, the residual, spend-controlled association between size and outcome should be indistinguishable from zero *by construction* — a large residual coefficient would be evidence *against* the mediation-structured account, not for it. What is being reported is not "we found a weak association" but "we found that the gap present in the raw data is close to fully absorbed by a single mediator," a stronger and more specific claim than an unconditional weak-association finding.

**§6.4 — the associational-language statement referenced throughout.** Every "mediation," "path," and "effect" statement in this report describes decomposed statistical association in observational panel data. The one design-based identification attempt (2SLS, §5.4 method 4) could not be completed; its failure is reported openly rather than folded into the confirmatory evidence. This is the full statement the scope note at the top of this document points to.

Because H1c tests whether a direct-path association exists *at all*, its evidentiary weight comes from the MDE framing (Figure 2), not from the raw ε² values — the sample is well-powered to detect a coefficient an order of magnitude smaller than the raw comparison would suggest is "the effect." In a 19.3-million-row panel, small-but-real correlations are the expected texture of any observational relationship; the consistency of the qualitative pattern across eight independent methods (§5.4) is doing the evidentiary work, not the magnitude of any single coefficient.

---

## 7. Longitudinal Extension — Study 2

*The cross-sectional analysis (§5) is this report's confirmatory core; this section is a secondary check on an independent, smaller sample (n = 29 customers, 204 ad groups, no shared rows with §5's data) and is reported as a directional signal, not an independently conclusive result.*

### 7.1 Sample construction and the maturity test

![Figure 5 | Cold-start sample construction and confirmatory test](figures/Figure5_coldstart_funnel_and_RQ1_null.png)

**Figure 5.** Sample-construction funnel (250 candidates → 204 with a complete 30-day window, 29 customers once aggregated). Account maturity shows no significant association with a new ad group's initial 30-day growth slope (OLS β = 8.34, p = .576; cluster permutation p = .663; standardized β = .085, only 17% of the pre-registered detection threshold). A leave-one-out check removing the largest customer (35.8% of the sample) leaves the conclusion unchanged (permutation p = .702).

### 7.2 Early-signal prediction and intervention timing

![Figure 6 | Early-signal prediction and intervention-timing simulation](figures/Figure6_RQ2_horizon_RQ3_lift.png)

**Figure 6.** An ad group's own early operating signal predicts near-term growth (leakage-free 14-day-ahead ρ = 0.386). Adding account maturity does not improve *within-customer* prediction — Panel B shows the apparent pooled gain (Panel A) is concentrated almost entirely in the between-customer component, i.e., maturity re-injecting the same customer-level signal already captured elsewhere, not a genuine ad-group-level improvement. Early-signal flagging achieves a 1.2–1.4× precision lift over random flagging, consistent across days 7, 14, and 21 post-registration (Panel C), with no cutoff statistically distinguishable as optimal (Panel D — 95% CIs overlap across all three days).

### 7.3 Formal equivalence testing

![Figure 9 | TOST equivalence tests](figures/Figure9_tost_equivalence.png)

**Figure 9.** A non-significant p-value does not itself establish an effect is absent, so both null results above were tested for formal equivalence (TOST). Neither reaches it (maturity → growth slope: p = .197; maturity's contribution to prediction: p = .290) — both are well-powered, non-significant associations for which formal equivalence remains inconclusive. This is why §7 is framed as a supporting, directional extension rather than an independently confirmatory companion to §5.

**Design-choice narrative.** Why a customer-level growth-curve slope replaced a latent-class trajectory model, why a customer-level OLS replaced a random-intercept mixed model, and the pre-specified sample-exclusion rules are logged in full in **[`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md)** and are not repeated here — this section reports what was found, not how the estimator was chosen.

---

## 8. Design Artifact

Section 7.2 establishes a confirmed within-customer result: an ad group's own early operating signal predicts its near-term growth, and adding account maturity produces no within-customer improvement at any tested horizon. This motivates a concrete, implementable decision rule, specified below as a design artifact in the design-science-research sense — an explicit input/output specification grounded in a stated empirical result, not a general recommendation. Full spec and backtest grid: **[`docs/DESIGN_ARTIFACT.md`](docs/DESIGN_ARTIFACT.md)**.

### 8.1 The artifact

**Ad-Group Early Warning Flagging Rule**

| Field | Value |
|---|---|
| Input | `predicted_growth_rank_percentile` (float, [0,1]); `day_since_registration` (int) |
| Output | `flag` (bool); `reason` (str) |
| `flag_threshold` | 0.30 |
| Valid decision window | day 7–21 post-registration |

**Design principles.**

- **DP1.** Base flagging solely on the ad group's own early-period signal — never on account-level history (grounded in §7.2's within-customer result).
- **DP2.** Evaluate at any point within a bounded window (day 7–21) rather than a single fixed day (Figure 6C–D: no cutoff is statistically distinguishable as optimal).
- **DP3.** Threshold on relative rank within the observed cohort, not an absolute growth value, since growth magnitudes are not comparable across heterogeneous ad groups.

### 8.2 Empirical backtest and its limits

A naive comparison against a size/tenure-based rule turns out to be structurally ill-posed: account maturity is a customer-level constant, so within-customer demeaning — required to isolate the same within-customer signal DP1 claims matters — collapses the naive rule's predictions to numerical zero in every specification (residual SD ~1e-17). There is nothing for the own-signal rule to beat on that axis.

What was measured instead: own-signal precision at the 30% flagging threshold against a random-flagging baseline, within-customer, across nine specifications (varying minimum active-days and early/later window). **Own-signal precision exceeded the random baseline in 4 of 9 specifications (44%)** — at n ≈ 20 customers per spec, this pattern is not distinguishable from chance. Reported plainly, not rounded up.

### 8.3 Status

Theoretically motivated (§7.2), **not yet empirically validated as superior to alternatives** in binary-decision form — see `docs/DESIGN_ARTIFACT.md` for the full nine-specification backtest grid and recommended next steps (a larger cold-start sample, and/or a continuous precision–recall evaluation rather than a single-threshold binary comparison).

---

## 9. Boundary Conditions & Generalizability

Two questions bound how far the claim travels: (a) does it hold uniformly *within* this platform, and (b) how far does it plausibly extend *beyond* it. Full detail: **[`supplementary_robustness/02_boundary_conditions.md`](supplementary_robustness/02_boundary_conditions.md)**.

**(a) Within-platform heterogeneity.**

- **Campaign product type** (§5.5, H2): joint Wald p = .023 — not perfectly homogeneous, plausibly because different product types route through different approval pipelines (e.g., shopping campaigns undergo product-feed validation standard search does not).
- **Keyword review status** (RQ2, exploratory). Only 0.5% of keywords carry a non-standard `inspect_status`, so this check is under-powered by construction.

  | Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
  |---|---|---|---|
  | Under-review only | 22 | 230 | .638 |
  | Restricted-approval only | 106 | 146 | .016 |
  | Combined | 111 | 141 | .016 |

  The combined definition's significance is driven almost entirely by the restricted-approval component — one signal probed three ways, not three independent confirmations. Reported as preliminary.

- **Industry (exploratory, not confirmatory).** An industry-classification pipeline (multilingual sentence embeddings + LLM ensemble against KSIC categories) was piloted as a third stratification candidate. Inter-rater reliability (Randolph's free-marginal κ = 0.557) and cross-validation against an independent rule-based classifier (Cohen's κ = 0.363) both indicate moderate-at-best label reliability, so industry-stratified results are not reported here. A directionally suggestive signal in one cluster (manufacturing/construction) is noted but not treated as a finding, given this reliability ceiling. Full pipeline and diagnostics: **[`appendix/exploratory_industry_classification.md`](appendix/exploratory_industry_classification.md)**.

**(b) Cross-platform generalizability.** The pattern documented here — real-time, auction-based serving whose outcomes track a unit's own current signal — is a property of the serving architecture, not of this platform's brand specifically. The *direction* is expected to generalize to other real-time bidding platforms with comparable architecture (unit-level auctions, continuous re-ranking, no persistent account-level scoring layer). No claim is made about magnitudes. Conditions under which the pattern would plausibly weaken, stated as falsifiable predictions for future replication:

- Platforms/categories with **mandatory human review** (e.g., regulated verticals), where account-level trust signals could re-enter through reviewer discretion.
- **New categories without established auction liquidity**, where the platform may fall back on account-level heuristics.
- Platforms whose ranking algorithm **explicitly incorporates account tenure or verification status** as a feature (unlike the platform studied here).

---

## 10. Practical Implications

**For an advertiser:**

1. **Budget allocation should track spend, not account size.** The decomposition (§5.3–5.4) is consistent with outcome quality tracking how much is actually spent, not the advertiser's size tier — based on the observational pattern found here.
2. **Expect some variation by campaign product type.** H2 found statistically significant heterogeneity (joint Wald p = .023, §5.5), even though no single product type shows a significant size coefficient alone. Shopping and local-business advertisers should treat the "spend, not size" guidance as somewhat less airtight than website advertisers.
3. **A longitudinal follow-up points the same direction, with less certainty.** §7 suggests account tenure similarly shows little direct association with how a new ad group ramps up, but that result is directional rather than independently conclusive and should be weighted accordingly.

**For a platform researcher or fairness auditor:** the audit logic in §3.2 generalizes as a method independent of this platform's specific findings — test whether a structural attribute's association with outcomes survives controlling for the legitimate channel it plausibly operates through, rather than testing only for a raw gap. §9 spells out the conditions under which this platform's specific null would *not* be expected to replicate elsewhere.

---

## 11. Limitations

| # | Limitation | Where addressed |
|---|---|---|
| 1 | Single agency, single platform, by design | §4, §9b |
| 2 | CPC-based estimates carry a partly mechanical component; bid_amount is the primary quantitative claim wherever the two diverge | §5.4, Fig. 7 |
| 3 | Keyword-review-status boundary check (RQ2) is under-powered (0.5% of keywords) | §9a |
| 4 | Ad-group dimension table is a snapshot; all account-age measures in §7 are lower bounds | §4 |
| 5 | Every H1a/b/c claim is associational, not causally identified; the one identification attempt (2SLS) could not be completed | §5.4, §6 |
| 6 | §7's longitudinal extension is directionally supportive but not TOST-confirmed | §7.3, Fig. 9 |
| 7 | The audit methodology (§3.2) is demonstrated on one attribute/mediator pair on one platform; its generality as a *method* is a methodological argument, not itself cross-validated on a second pair | §3.2, §9 |
| 8 | H2 strata are unevenly sized (n = 184 / 27 / 17); interpret the joint interaction accordingly | §5.5 |
| 9 | RQ4 (churn) is reported separately in Appendix D, outside the main hypothesis family, given a small labeled sample (n = 213, 2.35% churn) and a statistical floor on its model-comparison test | Appendix D |

---

## 12. Methodology Summary

| | Cross-sectional (§5) | Longitudinal extension (§7) |
|---|---|---|
| Primary test | Cluster-robust controlled regression (HC3/cluster SE), replicated on a cost-independent outcome | Customer-level aggregate OLS + cluster permutation test |
| Robustness battery | Cluster permutation, bootstrap CI, approximate Bayes factor, MDE, specification curve, placebo test, 2SLS (incomplete), temporal split replication, cost-sharing-artifact isolation, alternative-outcome replication | Bootstrap CI, winsorizing, rank-rank regression, leave-one-out, within/between decomposition, TOST equivalence |
| Heterogeneity / boundary | `campaign_type` joint Wald (H2, p = .023); keyword review-status (exploratory) | — |
| Sensitivity | Oster's delta (bid_amount b-path), with a numerical-stability guard | — |
| Multiple-testing correction | Benjamini–Hochberg FDR (6 primary hypotheses) | Not applicable — convergence across 5 methods used instead |
| Power check | MDE at 80% power | Simulation reusing real cluster structure (500 iter.); only large effects (β ≈ .5) reliably detectable (88% power) |
| Figures | 1, 2, 3, 7, 8 | 5, 6, 9 |

Known code- and design-level issues (the unrecoverable 2SLS first-stage F-statistic, the Wilcoxon floor-p artifact in the churn appendix, and others) are logged transparently in `docs/METHODOLOGY_NOTES.md`.

---

## 13. Discussion

**Read as a methods paper first.** The primary claim is a reusable audit design: decompose a structural-attribute/outcome relationship into a legitimate-channel path and a residual direct path, and let the *survival or vanishing of the direct path* — not a raw outcome gap — be the fairness verdict (§3.2). This is a design for characterizing statistical patterns rigorously, not a causal-inference method, and should be evaluated on those terms.

**Read as an application, the case here returns a clean null.** Advertiser size shows no direct statistical association with algorithmic outcomes on this platform once spend is controlled — an instance of **structural blindness**. Practically, account size does not appear, in this data, to be a useful proxy for how a given ad group will perform; what the advertiser actually does — how much it spends — is the more informative signal, to the extent this observational pattern holds going forward.

**Theoretically**, this reframes a common platform-fairness concern: an apparent algorithmic-treatment gap by account scale may reflect not the structural attribute itself but the behavior that attribute correlates with (spending capacity) — a claim about statistical structure that would need a credible identification strategy to become a causal one. §9's boundary conditions are the falsifiable scope of that reframing, and §7's longitudinal extension is a directionally consistent, not yet independently conclusive, signal that the pattern may extend to account tenure as well. The lasting contribution is less "size doesn't matter on this platform" and more "here is how to tell, rigorously, whether a structural attribute's association with outcomes is direct or only routes through what it correlates with" — a question that outlives any single platform's answer to it.

---

## 14. How to Reproduce

1. Request a schema-compatible data extract (`data/README.md` documents the expected schema; data are proprietary and not included in this repository — see `data/README.md` for access details).
2. `bash run_pipeline_v4.sh` — earlier-generation pipeline: variance decomposition, advertiser-size fairness battery, churn appendix.
3. `bash run_diagnostics.sh` — Steps A–M of the cold-start diagnostic pipeline (`src/coldstart_v5/`).
4. Run `src/analysis/rq1_growth_curve_test.py` and `src/analysis/rq2_prediction_validation.py` for the confirmatory §7 tests.
5. `bash run_supplementary_robustness.sh` — the four independently runnable robustness analyses under `supplementary_robustness/`.
6. Regenerate all nine figures with `figures/make_figure*.py` (each reads a results JSON/CSV and writes a PNG to `figures/`).

Every step prints its own diagnostics and writes a JSON/CSV artifact; nothing is silently overwritten, and each script can be re-run independently as long as its upstream artifact exists.

---

## 15. Appendices

| Appendix | Contents |
|---|---|
| [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) | Full estimator-selection derivation log (GBTM → growth curve, MixedLM → OLS, censoring reinterpretation, LOCO within/between bug, uplift-formula artifact, exclusion rules) |
| [`docs/RESULTS_SUMMARY.md`](docs/RESULTS_SUMMARY.md) | Canonical statistics table, all studies |
| [`docs/DESIGN_ARTIFACT.md`](docs/DESIGN_ARTIFACT.md) | Full artifact schema and nine-specification backtest grid (summarized in §8) |
| [`supplementary_robustness/01_alternative_outcome_mediation.md`](supplementary_robustness/01_alternative_outcome_mediation.md) | Cost-sharing artifact isolation, full detail |
| [`supplementary_robustness/02_boundary_conditions.md`](supplementary_robustness/02_boundary_conditions.md) | Full stratified tables (§9) |
| [`supplementary_robustness/03_equivalence_and_sensitivity_notes.md`](supplementary_robustness/03_equivalence_and_sensitivity_notes.md) | TOST derivations, Oster's delta detail |
| [`appendix/churn_prediction_rq4.md`](appendix/churn_prediction_rq4.md) | **Appendix D** — exploratory churn prediction (RQ4), outside the main hypothesis family |
| [`appendix/exploratory_industry_classification.md`](appendix/exploratory_industry_classification.md) | Full industry-classification pipeline; not used for confirmatory claims (§9a) |
| [`appendix/hypothesis_id_legacy_mapping.md`](appendix/hypothesis_id_legacy_mapping.md) | Figure-title / hypothesis-ID reconciliation table |

---

## 16. Repository Structure

```
ad-coldstart-analysis/
├── README.md                          <- you are here
├── LICENSE
├── requirements.txt
│
├── config/
│   └── config.yaml                    <- all paths, thresholds, sample-definition rules
│
├── data/
│   └── README.md                      <- expected schema + how to request access (no data files committed)
│
├── src/
│   ├── utils/
│   │   ├── io.py
│   │   └── identifiers.py
│   │
│   ├── coldstart_v5/                  <- diagnostic pipeline (Steps A-M)
│   │   ├── step_a_period_and_spike_check.py
│   │   ├── step_b_true_coldstart_sample.py
│   │   ├── step_c_right_censoring_flags.py
│   │   ├── step_d_customer_clustering_density.py
│   │   ├── step_e_class_count_identifiability_sim.py
│   │   ├── step_f_registration_cutoff_sensitivity.py
│   │   ├── step_g_fixed_window_coverage.py
│   │   ├── step_h_top_customer_profiling.py
│   │   ├── step_i_account_maturity_distribution.py
│   │   ├── step_j_regtm_artifact_check.py
│   │   ├── step_k_power_simulation.py
│   │   ├── step_l_rq2_feature_engineering.py
│   │   └── step_m_intervention_timing_simulation.py
│   │
│   ├── pipeline_v4/                   <- earlier-generation pipeline
│   │   ├── step0_data_prep_v4.py
│   │   ├── step1_variance_decomposition_v4.py
│   │   ├── step2_advertiser_size_fairness_v4.py
│   │   ├── step3_churn_appendix_v4.py
│   │   └── step4_synthesis_v4.py
│   │
│   └── analysis/                      <- confirmatory tests
│       ├── rq1_growth_curve_test.py
│       └── rq2_prediction_validation.py
│
├── supplementary_robustness/
│   ├── supplementary_robustness_README.md
│   ├── 01_alternative_outcome_mediation.md / .py
│   ├── 02_boundary_conditions.md / .py
│   ├── 03_equivalence_and_sensitivity_notes.md / .py
│   └── 04_design_artifact_future_work.md / .py
│
├── figures/                           <- one script per figure; reads results JSON/CSV, writes PNG
│   ├── make_figure1_variance_decomposition.py       -> Figure1_variance_decomposition.png
│   ├── make_figure2_fairness_forest_plot.py         -> Figure2_fairness_forest_plot.png
│   ├── make_figure3_specification_curve_placebo.py  -> Figure3_specification_curve_placebo.png
│   ├── make_figure4_churn_benchmark.py              -> Figure4_churn_benchmark.png
│   ├── make_figure5_coldstart_funnel_and_rq1_null.py-> Figure5_coldstart_funnel_and_RQ1_null.png
│   ├── make_figure6_rq2_horizon_rq3_lift.py         -> Figure6_RQ2_horizon_RQ3_lift.png
│   ├── make_figure7_mediation_forest.py             -> Figure7_mediation_forest.png
│   ├── make_figure8_boundary_condition_forest.py    -> Figure8_boundary_condition_forest.png
│   ├── make_figure9_tost_equivalence.py             -> Figure9_tost_equivalence.png
│   └── Figure*.png                                  <- the 9 rendered figures used above
│
├── appendix/
│   ├── churn_prediction_rq4.md                <- Appendix D
│   ├── exploratory_industry_classification.md
│   └── hypothesis_id_legacy_mapping.md
│
├── docs/
│   ├── METHODOLOGY_NOTES.md
│   ├── RESULTS_SUMMARY.md
│   └── DESIGN_ARTIFACT.md
│
├── run_diagnostics.sh                 <- runs Steps A-M in order
├── run_pipeline_v4.sh                 <- runs the v4 pipeline end-to-end
└── run_supplementary_robustness.sh    <- runs all four supplementary_robustness/*.py scripts
```

> **Note on `editorial_notes.md`.** Author-facing housekeeping notes (the data-availability decision pending finalization, the pre-submission checklist) are kept in a local, non-committed file outside this tree by design, so that internal notes cannot leak into the public README the way they did in an earlier draft's data-availability appendix. Before submission, confirm the data-availability statement in `data/README.md` reflects the finalized access terms rather than the placeholder language above.
