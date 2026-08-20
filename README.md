# Not New, But Renewed: Structural Attributes Don't Matter on an Algorithmically-Mediated Ad Platform

*A mediation-based audit of advertiser-size fairness and cost-efficiency allocation on a Korean paid-search platform, with a longitudinal extension to account tenure.*

> **Scope note.** Every "mediation," "path," and "effect" statement in this report describes a decomposed **statistical association** in observational panel data — not an identified causal effect. This note applies globally and is stated in full, with the reasoning behind it, in §5.4; it is not repeated at each instance below.

---

## Table of contents

1. [Overview & Contributions](#1-overview--contributions)
2. [Introduction & Research Question](#2-introduction--research-question)
3. [Theoretical Framing](#3-theoretical-framing-the-structural-blindness-construct)
4. [Data & Setting](#4-data--setting)
5. [Main Results — Study 1 (Cross-Sectional)](#5-main-results--study-1-cross-sectional)
6. [Effect-Size Interpretation](#6-effect-size-interpretation-why-small-is-the-point)
7. [Longitudinal Extension — Study 2](#7-longitudinal-extension--study-2)
8. [Design Artifact](#8-design-artifact-an-early-warning-flagging-rule)
9. [Boundary Conditions & Generalizability](#9-boundary-conditions--generalizability)
10. [Practical Implications](#10-practical-implications)
11. [Limitations](#11-limitations)
12. [Methodology Summary](#12-methodology-summary)
13. [Discussion](#13-discussion)
14. [How to Reproduce](#14-how-to-reproduce)
15. [Appendices](#15-appendices)

---

## 1. Overview & Contributions

Two advertisers run campaigns on the same search-ads platform. One has operated for years and manages hundreds of ad groups; the other is comparatively small. The intuitive expectation is that the larger, more established advertiser receives more favorable algorithmic treatment — faster approval, cheaper clicks, better ad rank — independent of how much either advertiser actually spends. This report tests that expectation twice, on two independent samples, and does not find support for it.

**Contributions.**

1. **A mediation-based audit design.** Rather than asking only "does an outcome gap exist across a structural category," the design decomposes the relationship into a legitimate-channel path and a residual direct path, and treats the *survival or vanishing of the direct path* — not the presence of a raw gap — as the fairness-relevant statistic (§3). The design is intended to generalize to other platforms, structural attributes, and mediating channels.
2. **An empirical demonstration** on a 321-advertiser, ~19.3-million-row panel from a single Korean search-ads platform, with the central result replicated on a cost-artifact-free outcome and stress-tested across eight independent methods (§5).
3. **A falsifiable boundary-condition statement** (§9) specifying the conditions under which the finding is, and is not, expected to hold or generalize — including a documented case of internal heterogeneity (§5.5).
4. **A design artifact** (§8) — an early-warning ad-group flagging rule — derived from a confirmed within-customer result, specified with an explicit input/output schema, together with a transparent account of why its binary-decision backtest remains inconclusive rather than confirmatory.

**At a glance.**

| Study | Research question | Confirmatory verdict | Key figure(s) |
|---|---|---|---|
| 1 — cross-sectional | Does advertiser size directly predict approval / cost efficiency / ad rank, net of spend? | **Null** (H1c not rejected); 8 independent methods agree | Figs. 1, 2, 3, 7 |
| 1 — boundary condition | Is that null homogeneous across ad-product categories? | **Rejected** — joint test p = .023 | Fig. 8 |
| 2 — longitudinal | Does account maturity predict a new ad group's growth? | **Null**; TOST equivalence inconclusive | Figs. 5, 9 |
| 2 — design | Can early operating signal support intervention timing? | Directional; no statistically optimal single day | Fig. 6 |

---

## 2. Introduction & Research Question

Account scale and tenure are routinely treated, in the algorithmic-fairness literature and in practitioner intuition alike, as candidate sources of platform-mediated advantage. Most existing audits of this kind stop at testing whether a raw outcome gap exists across such a structural category. This report asks a more specific question: **is the gap direct, or does the statistical relationship run entirely through a legitimate, non-protected channel** — here, how much an advertiser spends?

That distinction, developed formally in §3, is the paper's methodological core. Everything downstream — the eight-method robustness battery (§5.4), the artifact-isolation logic behind Figure 7, the falsifiable boundary-condition statement in §9 — exists to make that specific test as hard to fool as possible on one well-documented case. The empirical answer this case produces (a clean null for the direct-path association) is one possible output of the method, not the reason the method is worth using: a platform where the direct-path association *did* survive controlling for spend would be an equally valid demonstration of the same audit design, with the opposite verdict.

**The case.** A panel of **321 advertisers and approximately 19.3 million rows** of daily/hourly performance data from a single Korean search-ads ecosystem (§4).

**Research Question 1 (primary).** *Is advertiser size directly, statistically associated with algorithmic outcomes — approval rate, cost efficiency, and ad rank — independent of the advertiser's spending behavior, once spend is held constant?*

**Research Question 2 (longitudinal extension, §7).** *Is an account's accumulated history — how long it has operated, how many ad groups it has run — associated with how a newly registered ad group inside that account performs, independent of the ad group's own early operating signal?*

**Scope statement.** The claim advanced here is conditional, not unconditional. Within this platform, the degree to which size shows no residual association varies modestly by ad-product category (§5.5); the strata driving that variation are small (n = 27 and n = 17 customers) and the finding should be weighted accordingly. Beyond this platform, the underlying mechanism — a real-time auction that scores each unit on its own current signal — is expected to generalize in *direction* to platforms with comparable architecture, and to plausibly weaken under mandatory human review, in new categories without established auction liquidity, or on platforms whose ranking algorithm explicitly incorporates account tenure as a feature (§9).

---

## 3. Theoretical Framing: The Structural Blindness Construct

### 3.1 Definition

**Structural blindness** describes a real-time, auction-based serving system whose observed approval, cost-efficiency, and ranking outcomes track a unit's *current, behavioral signal* — its bids, its clicks, its spend — and show **no detectable residual statistical association** with *structural attributes of the account behind that unit* (such as account size), once the legitimate channel through which structural attributes could plausibly operate (here, total spend) is held constant.

This is a claim about statistical pattern, not about raw outcomes, and not by itself a claim about mechanism in a causal sense (§5.4). Large and small advertisers can and do perform differently; the question is whether that difference is *direct* (size predicts the outcome even net of spend) or *indirect* (size is associated with how much an advertiser spends, and spend is what tracks the outcome).

### 3.2 Deriving the construct from the algorithmic-fairness literature

Structural blindness is derived from a distinction with an established lineage in algorithmic-fairness research, rather than a label attached to a result after the fact.

- **Disparate treatment versus disparate impact.** The fairness-in-ML literature distinguishes *disparate treatment* — differential treatment conditional on a protected or structural attribute itself — from *disparate impact* — differential outcomes arising through a legitimate, attribute-correlated channel (Barocas & Selbst, 2016). Structural blindness maps this distinction onto the decomposition tested here: **H1c** (§3.3) asks whether the *direct* path from size to outcome shows a detectable residual association once the legitimate mediating channel (spend) is held constant. A residual association that survives would be a pattern *consistent with* disparate treatment; one that vanishes, with the *indirect* path intact, would be a pattern *consistent with* disparate-impact-style allocation through a legitimate channel — both are statements about observational statistical patterns, not adjudicated causal claims.
- **Algorithmic accountability audits.** Prior audits of ad-delivery systems have documented outcome gaps by protected or structural category without always decomposing *why* the gap exists (Sweeney, 2013; Ali et al., 2019, on skew in Facebook's ad-delivery optimization). This report's contribution is to reframe that question as *which statistical path the gap runs through* — direct or indirect — rather than only whether a gap exists. That reframing, not the specific null result it produces on this platform, is the paper's theoretical contribution; a researcher applying the same design to a different platform, structural attribute, or candidate mediator would be extending the method, not merely replicating a finding.
- **Information asymmetry in two-sided platform markets.** Platform-economics theory generally assumes a platform can act on participant characteristics it has data on, and this platform's own systems record both account scale and tenure. Structural blindness is the empirical finding that, despite this information being available, the allocation outcomes studied here show no detectable direct association with it once real-time behavioral signals are in the model — a claim about *which* information tracks a real-time auction mechanism's outcomes in practice, offered as a statistical pattern rather than a claim about the platform's internal decision logic, which this analysis cannot directly observe.

| | Structural attribute | Candidate legitimate mediating channel |
|---|---|---|
| This investigation | Advertiser size (spend-tier / all-time ad-group count) | Total spend |

### 3.3 Formal hypotheses

- **H1a (a-path).** Advertiser size is positively associated with an advertiser's total spend.
- **H1b (b-path).** Total spend is positively associated with outcome quality, holding advertiser size constant.
- **H1c (c′-path, central hypothesis).** Advertiser size shows no direct statistical association with outcome quality once total spend is held constant.
- **H1 (composite).** The entire size–outcome relationship runs through its association with spend rather than through size itself — supported if H1a and H1b are confirmed and H1c's null cannot be rejected under a well-powered test.
- **H2 (boundary condition).** H1c's null holds homogeneously across platform-defined ad-product categories.
- **RQ-maturity (longitudinal, §7).** Account maturity is positively associated with a newly registered ad group's initial growth.

Every non-significant result below is reported alongside its minimum-detectable-effect (MDE) band at 80% power, so that a null can be read as *well-powered* rather than merely *undetected* (§5.3, Figure 2).

---

## 4. Data & Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata, including `campaign_type` (ad-product code) | 1,504 | 263 / 321 |
| Ad group dimension (snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263 / 321 |
| Keyword dimension | Brand type, `inspect_status` (review code), bid price | 1,503,289 | 256 / 321 |

Conversion and ROAS variables were excluded entirely: the platform's conversion API retroactively backfills conversions per account on a delayed, inconsistent schedule, which breaks construct validity for anything built on top of it. This was a design decision made before any modeling began.

**The single-platform, single-agency design is a methodological choice, not merely a limitation.** All data originates from one Korean ad-tech provider sourced from one search platform. This bounds external generalizability (§9 states explicitly how far the pattern is expected to travel), but it is also what makes the internal test clean: every advertiser in the panel faces the *same* ranking algorithm, the *same* approval pipeline, and the *same* data-collection process, removing an entire class of between-platform confounds that would otherwise be entangled with any size effect in a multi-platform sample.

---

## 5. Main Results — Study 1 (Cross-Sectional)

### 5.1 Where would an advantage even live?

Before testing anything about advertiser size, the analysis first located *where* performance variation sits — in the customer, the campaign, or the ad group. If a size-related advantage exists, it should show up as customer-level variance.

![Figure 1 | Multilevel variance decomposition of advertising performance](figures/Figure1_variance_decomposition.png)

**Figure 1.** Across ~663K observations, log ad spend is dominated by unexplained residual variance (ICC = 0.825) — day-to-day budget execution, not who the customer is (ICC = 0.050). Click-through rate shows the largest share of variation at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both patterns hold whether or not month fixed effects are added, ruling out seasonality as the explanation — an early indication that "who the customer is" is associated with comparatively little of what happens on this platform.

### 5.2 The raw gap looks real — until clustering is accounted for

Splitting advertisers into four size tiers (by spend volume) and comparing approval rate, CPC, and ad rank across tiers with a Kruskal-Wallis test shows differences that are statistically significant across the board (p < .001 for CPC and ad rank; p = .0006 for approval rate). This raw signal does not survive a more appropriate test: ad groups belonging to the same customer share policies and are not statistically independent, and the standard Kruskal-Wallis test assumes independence that does not hold here. Re-running the comparison as a customer-level cluster permutation test (2,000 iterations) made most of the apparently "significant" gap in approval rate and CPC evaporate — precisely the kind of naive audit the mediation-based design in §3.2 is built to correct.

### 5.3 The central confirmatory test (H1c)

![Figure 2 | Advertiser-size effect on approval, cost efficiency, and ad rank, controlling for spend](figures/Figure2_fairness_forest_plot.png)

**Figure 2.** Controlling for log spend in a cluster-robust regression, all six outcome × sample combinations (approval rate, CPC, ad rank, each in the full sample and with spike-affected accounts excluded) return **non-significant** direct-path coefficients for size (cluster-robust p > .07). Every 95% bootstrap confidence interval not only crosses zero — it falls entirely inside, or right at the edge of, its own minimum-detectable-effect (MDE) band, ruling out "insufficient power" as the explanation for the null. Approximate Bayes factors favor the null in five of six tests; the sixth (CPC under spike exclusion) is flagged as a directionally-reversed sensitivity finding, not a confirmatory one.

**Table 5.1 — H1a/b/c full decomposition** (customer-level, n = 263; `bid_amount` is the cost-independent primary outcome, CPC retained for comparison — see §5.4).

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a: size → total spend | +0.537 (p < .001) | +0.537 (p < .001) |
| H1b: spend → outcome \| size | +1.277 (p < .001) | +0.150 (p = .032) |
| H1c: size → outcome \| spend (direct) | −0.253 (p = .062) | +0.037 (p = .634) |
| Indirect association (a × b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | < .001 | < .001 |

### 5.4 Stress-testing across eight independent methods

A single regression result is easy to distrust, so H1c was stress-tested eight independent ways. Methods 1–6 test H1c directly; methods 7–8 additionally establish H1a and H1b on an outcome immune to a mechanical confound described below.

1. **Multiverse specification curve** — 48 defensible analytic choices (tier definition × covariate set); 0/48 reach significance for any outcome.
2. **Placebo test** — device-type share, which size *shouldn't* predict, is significant under the raw distributional test but null under the spend-controlled regression, evidence the regression (not the raw test) is measuring the right thing.
3. **Customer-and-month fixed-effects panel regression.**
4. **Two-stage least squares** with lagged spend as an instrument. The first-stage F-statistic could not be recovered due to a code exception; this attempt is flagged and excluded from any conclusion, not silently dropped. **No causal identification strategy in this report was successfully completed; all reported patterns remain associational.**
5. **Temporal split-sample replication.**
6. **Benjamini-Hochberg FDR correction** across the six primary hypotheses.

![Figure 3 | Multiverse specification curve and placebo test](figures/Figure3_specification_curve_placebo.png)

**Figure 3.** Panel A: across all 48 specification choices and all three outcomes, none reach significance at α = .05. Panel B: the raw distributional (Kruskal-Wallis) test is significant for *both* the real outcome and the device-share placebo — proof that a distributional test alone is not a clean placebo here, since size tiers correlate with many unrelated account traits. The informative comparison is the spend-controlled regression matching H1c, where real and placebo outcomes are equally, indistinguishably null.

7. **Isolating a mechanical artifact in the CPC outcome.** CPC = cost / click, and spend is built from cost, so any spend–CPC association carries a mechanical component by construction. A customer-level permutation procedure (reshuffling click within customer while holding cost fixed, 2,000 iterations) isolates the size of that component. The observed spend–log(CPC) coefficient (+1.277) falls *below* the lower bound of the resulting purely-mechanical null distribution (mean +1.552, 95% range [1.544, 1.556]) — the CPC-based estimate is not simply inflated beyond the mechanical baseline, but sits close enough to it that it is treated as directionally informative only. A lagged replication (spend at day *t* → CPC at *t*+1 and *t*+7, immune to same-day cost-sharing) confirms a same-signed, significant association at both lags (β = +0.538 and +0.544, both p < .001).
8. **Replicating the mediation structure on a cost-independent outcome.** `bid_amount` shares no cost or click term with spend, so it carries none of the mechanical artifact isolated in method 7. Re-estimating the decomposition on this outcome (Table 5.1, right column) is the load-bearing result for the efficiency claim: the indirect (spend-linked) association is significant, while the *direct* association of size, net of spend, is not (p = .634) — the same qualitative pattern as the CPC-based model, now on an outcome immune to the artifact.

![Figure 7 | Spend-mediation b-path: CPC-based vs. cost-independent outcome](figures/Figure7_mediation_forest.png)

**Figure 7.** The spend–outcome coefficient shrinks from +1.277 (CPC-based, partly mechanical) to +0.150 (bid_amount-based, cost-independent) once the shared cost term is removed. The direction survives; the magnitude does not — a pattern consistent with the CPC-based estimate being inflated by construction rather than by a stronger underlying association.

**On the status of causal-sounding language.** Every "size–spend," "spend–outcome," or "mediation" statement in this report — including the path labels H1a/b/c themselves — describes an **associational** pattern estimated from observational panel data, not an identified causal effect. This vocabulary is used because it is the standard terminology for this class of decomposed statistical pattern in the fairness-audit literature, not because a causal mechanism has been established. The one attempt at design-based identification (method 4, 2SLS) could not be completed, and its failure is reported openly rather than folded into the confirmatory evidence. What the analysis *does* support is a considerably stronger form of associational evidence than a single cross-sectional correlation would provide: the same qualitative pattern — indirect association present, direct association absent — replicates across a mechanically-contaminated outcome (CPC) and a mechanically-independent outcome (bid_amount), across 48 specification choices, against a placebo variable, across two independent time splits, and survives multiple-testing correction. This is the basis on which "the size–outcome relationship runs through its association with spend" is asserted throughout — as a replicated observational pattern, not a causal claim.

**Eight independent verification methods, one consistent verdict**, with method 8 — not the raw CPC coefficient — treated as the primary quantitative evidence for the efficiency-outcome association.

### 5.5 Is the null homogeneous across contexts? (H2)

Close to, but not perfectly, homogeneous — treated here as a substantive finding, not a complication. Stratifying the spend-controlled CPC model by `campaign_type` (a platform-defined ad-product code — website / shopping / brand-new-product / local-business, not an industry classification) and running a joint Wald test on the size × product-type interaction gives **p = .023**.

![Figure 8 | Campaign product-type heterogeneity](figures/Figure8_boundary_condition_forest.png)

**Figure 8.** Website campaigns show a non-significant negative point estimate for size net of spend; local-business and shopping campaigns show non-significant positive point estimates. All three confidence intervals individually cross zero, but the joint test across strata is significant, meaning the *pattern* of where size comes closest to showing a residual association is not random noise, even though no single stratum is itself conclusive.

**Table 5.2 — campaign_type stratified c′ (size, net of spend).**

| Product type | n (rows) | n (customers) | c′ | p |
|---|---|---|---|---|
| Website (1) | 11,894 | **184** | −0.279 | .052 |
| Local business (6) | 1,306 | **27** | +0.312 | .211 |
| Shopping (2) | 2,161 | **17** | +0.245 | .151 |
| **Joint Wald test (size × product-type)** | | | | **.023** |

Sample sizes for the local-business and shopping strata are small (n = 27, n = 17 customers); the joint test's significance should be read with this in mind (§11).

### 5.6 Conclusion of the confirmatory analysis

Raw size-tier gaps in approval rate, CPC, and ad rank are statistically detectable but small, and fragile once clustering is accounted for. The confirmatory test — a spend-controlled regression, replicated on a cost-independent outcome — returns a clean, well-powered null for the *direct* association of size across every outcome-sample combination, backed by eight independent robustness checks, with one precisely characterized exception: the null is not perfectly homogeneous across ad-product categories (§5.5). **The apparent advantage of being a large advertiser is, to first order, statistically consistent with being fully accounted for by spending more rather than by size itself — with modest, product-type-dependent variation in how completely that holds.**

---

## 6. Effect-Size Interpretation: Why Small Is the Point

The raw distributional comparison in §5.2 produced effect sizes in the ε² = 0.002–0.079 range. Read in isolation, small effect sizes on 19.3 million observations can look like a reason for caution. Read against the theoretical structure in §3, they are close to the *predicted* result.

**A near-zero direct-path coefficient is what full statistical mediation predicts, not a weakness of the test that found it.** If H1c is true, the residual, spend-controlled association between size and outcome should be indistinguishable from zero *by construction* — a large residual coefficient would be evidence *against* the mediation-structured account, not for it. The small ε² values in the raw, unconditional comparison reflect a gap that mostly disappears once the mediating variable is introduced; what is reported is not "we found a weak association" but "we found that the gap present in the raw data is close to fully absorbed by a single mediator."

**The relevant question is existence and sign, not magnitude.** Because H1c tests whether a direct-path association exists at all, its evidentiary weight comes from the minimum-detectable-effect framing in Figure 2 — every confidence interval sits inside its own MDE band, meaning the sample is well-powered to detect a coefficient an order of magnitude smaller than the raw ε² values would suggest is "the size of the effect being tested." A small effect size on the raw comparison and a well-powered null on the controlled comparison are two different statistics answering two different questions.

**In a 19.3-million-row panel, small-but-real correlations are the expected texture of any observational relationship**, and screening on the direction and stability of the decomposed association — not on the raw ε² — is the more informative test. The consistency of the qualitative pattern across eight independent methods (§5.4) is doing the evidentiary work here, not the magnitude of any single coefficient.

---

## 7. Longitudinal Extension — Study 2

*The cross-sectional analysis in §5 is this paper's confirmatory core; this section is a secondary check on an independent, smaller, non-overlapping sample (n = 29 customers, 204 ad groups) and is reported as a directional signal, not as an independently conclusive result.*

### 7.1 Sample construction and the maturity test

![Figure 5 | Cold-start sample construction and confirmatory test](figures/Figure5_coldstart_funnel_and_RQ1_null.png)

**Figure 5.** Panel A — the sample-construction funnel (250 candidates → 204 with a complete 30-day window, 29 customers once aggregated). Panel B — account maturity shows no significant association with a new ad group's initial 30-day growth slope (OLS β = 8.34, p = .576; cluster permutation p = .663; standardized β = .085, only 17% of the pre-registered detection threshold). A leave-one-out check removing the largest customer (35.8% of the sample) leaves the conclusion unchanged (permutation p = .702).

### 7.2 Early operating signal vs. account maturity as predictors of growth

![Figure 6 | Early-signal prediction and intervention-timing simulation](figures/Figure6_RQ2_horizon_RQ3_lift.png)

**Figure 6.** Panel A — an ad group's own early operating signal is predictive of near-term growth (within-customer LOCO ρ up to ≈0.49 at 14-day horizon). Panel B — decomposing the apparent gain from adding account maturity into between- and within-customer components shows the gain is concentrated almost entirely between customers (i.e., it is the §7.1 customer-level maturity signal leaking through a pooled metric), not a genuine within-customer improvement. Panels C–D — early-signal flagging achieves a 1.2–1.4× precision lift over random flagging, consistent across decision days 7, 14, and 21 post-registration, with no cutoff statistically distinguishable as optimal (overlapping 95% bootstrap CIs).

**A note on directional divergence between the base early-signal result and the maturity-augmented result.** Across the 48-specification robustness grid underlying this section, the base early-signal model's coefficient is positive in 75% of specifications (100% of those significant), while the maturity-augmented model's *within-customer* improvement is positive in only 16.7% of specifications. A specification-level Spearman correlation between the two (ρ = −0.281, p = .017) indicates these are not simply noisier versions of the same signal: specifications that make the base early-signal model more predictive tend to make the maturity-augmented addition *less* additionally predictive — consistent with account maturity substituting for, rather than complementing, an already-strong early-signal specification, rather than contributing independent information.

### 7.3 Formal equivalence testing

A non-significant p-value does not by itself establish that an effect is absent. Both central null results above were tested for formal equivalence (TOST — two one-sided tests against a pre-specified smallest-effect-size-of-interest).

![Figure 9 | TOST equivalence tests for the two central null results](figures/Figure9_tost_equivalence.png)

**Figure 9.** Neither result reaches formal equivalence: maturity → growth slope, TOST p = .197 (margin ±0.20 standardized effect); maturity's contribution to prediction, TOST p = .290 (margin ±0.05 Spearman ρ). Both are therefore reported as **well-powered, non-significant associations for which formal equivalence remains inconclusive** — not as confirmed nulls in the strict TOST sense. This is why §7 is framed as a supporting, directional extension rather than an independently confirmatory companion to §5; a larger longitudinal sample is the natural next step.

The design-and-estimator decisions behind this section — why a continuous growth-curve slope replaced a discrete latent-class trajectory model, why a customer-level OLS replaced a random-intercept mixed model that failed to converge, and the pre-specified sample-exclusion rules used — are logged in full in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) and are not repeated here.

---

## 8. Design Artifact: An Early-Warning Flagging Rule

Section 7.2's confirmed within-customer result — an ad group's own early signal predicts its near-term growth, and account maturity adds nothing at the within-customer level — motivates a concrete, implementable decision rule for flagging underperforming ad groups early. It is specified here as a design artifact in the design-science sense: an explicit input/output specification grounded in a stated empirical result, not a general recommendation.

### 8.1 The artifact

**Ad-Group Early Warning Flagging Rule**

| | Specification |
|---|---|
| **Input** | `predicted_growth_rank_percentile` (float, [0,1]) — an ad group's predicted growth rank among its cohort, from a model using only that ad group's own early-window features; `day_since_registration` (int) |
| **Output** | `flag` (bool), `reason` (str) |
| **Parameters** | `flag_threshold` = 0.30; valid decision window = day 7–21 post-registration |
| **DP1** | Base flagging solely on the ad group's own early-period signal (coverage, spend trend, CTR/CVR) — never on account-level history (§7.2). |
| **DP2** | Evaluate at any point within a bounded window (day 7–21) rather than committing to a single fixed day (§7.2, Fig. 6C–D: no cutoff is statistically distinguishable as optimal). |
| **DP3** | Threshold on relative rank (percentile) within the observed cohort rather than on an absolute growth value, since growth magnitudes are not comparable across heterogeneous ad groups. |

### 8.2 Empirical backtest, and its limits

A backtest compared this rule's flagging precision against a naive account size/tenure-based alternative, using within-customer-demeaned predictions (to isolate the same within-customer signal DP1 claims matters) at a 30% flagging threshold, across nine (active-day-threshold × early-window × later-window) specifications.

**A structural finding, not a bug.** Account maturity is a customer-level constant. Within-customer demeaning of a prediction built from a customer-level constant collapses that prediction to numerical zero in every specification tested (residual SD on the order of 1e-17 — floating-point noise). This is expected behavior, not an error: it is the same fact demonstrated analytically in §7.2's within/between decomposition, now confirmed independently in a binary-flagging frame. It means the naive size/tenure rule has **no within-customer predictive content by construction** — a "naive wins" or "own-signal wins" comparison against it is not a meaningful contest, since there is nothing on this axis for the own-signal rule to beat.

**What can be evaluated instead.** With the naive comparison ruled out as ill-posed, the own-signal rule's precision was compared against a random-flagging baseline at the same threshold, across the same nine specifications (n ≈ 20 customers, ≈200 ad groups each). Own-signal precision exceeded the random baseline in **4 of 9** specifications and underperformed it in 5. At this sample size, this pattern is not distinguishable from chance and is **not reported as a confirmed empirical advantage.**

**Why this does not contradict §7.2.** Section 7.2's result is a continuous-scale finding (Spearman ρ on continuous predicted growth), well-powered and significant at short horizons. This backtest asks a much coarser question — does thresholding that continuous signal into a binary "flag the bottom 30%" decision produce a precision advantage detectable at n ≈ 20 customers — and the answer is that this specific binary-decision framing does not have enough power to resolve the question either way. A continuous signal being predictive does not guarantee any particular binarization of it is empirically distinguishable from random at a small sample size.

### 8.3 Status

DP1–DP3 are presented as **theoretically grounded** in §7.2's confirmed within-customer result, not as an empirically validated decision rule. The binary-flagging backtest above is not cited as evidence of the artifact's practical superiority over alternatives. A larger cold-start sample, and/or a continuous-scale (rather than binary-threshold) evaluation of the flagging rule's utility, is the recommended direction for empirically validating the artifact rather than only theoretically motivating it. Full backtest grid and specification-level detail: [`docs/DESIGN_ARTIFACT.md`](docs/DESIGN_ARTIFACT.md).

---

## 9. Boundary Conditions & Generalizability

An audit-based statistical pattern is only as useful as the boundary conditions attached to it. Stating those boundaries precisely turns "nothing matters" into the more defensible, falsifiable claim "nothing shows a residual association, except under these specified conditions."

### 9.1 Within-platform heterogeneity

- **Campaign product type** (platform-defined, well-measured; §5.5 / H2): the spend-controlled size coefficient is not perfectly homogeneous across website / shopping / local-business / brand-new-product campaigns (joint Wald p = .023), plausibly because these route through different approval pipelines (e.g., shopping campaigns undergo product-feed validation that standard search campaigns do not). No individual stratum shows a significant size coefficient.

- **Keyword review status** (a proxy for platform discretion). Only 0.5% of keywords in this dataset carry a non-standard `inspect_status` code, so this check is under-powered by construction.

  | Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
  |---|---|---|---|
  | Under-review only | 22 | 230 | .638 |
  | Restricted-approval only | 106 | 146 | .016 |
  | Combined | 111 | 141 | .016 |

  The combined definition's significance is driven almost entirely by the restricted-approval component (106 of 111 customers), not by an independent contribution from the under-review component — one underlying signal probed three ways, not three independent confirmations. Restricted-approval denotes an *already-resolved* non-standard outcome rather than a pending discretionary review, so this result is directionally interesting but does not cleanly map onto the "discretionary review as a leakage channel" mechanism that motivated the check. Reported as preliminary (§11).

### 9.2 Industry (exploratory, not confirmatory)

An industry-classification pipeline (multilingual sentence embeddings, UMAP + HDBSCAN clustering, and a four-model local-LLM ensemble forced to classify against Korean Standard Industrial Classification categories) was piloted as a third stratification candidate. Inter-rater reliability across the LLM ensemble (Randolph's free-marginal κ = 0.557) and cross-validation against an independent keyword-rule classifier (Cohen's κ = 0.363) both indicate moderate-at-best label reliability. Given this, industry-stratified results are **not used as evidence for any claim** in this report. A directionally suggestive signal (a significant negative direct effect in one cluster corresponding to manufacturing/construction, stable under split-half resampling) was observed under this low-reliability labeling but is not reported as a finding; a higher-reliability industry classification is a natural direction for future work. Full pipeline and diagnostics: [`appendix/exploratory_industry_classification.md`](appendix/exploratory_industry_classification.md).

### 9.3 Cross-platform generalizability

The pattern documented here — real-time, auction-based serving whose outcomes track a unit's own current signal — is associated with a property of the serving architecture, not of this platform's brand specifically. The *direction* of the structural-blindness finding is expected to generalize to other real-time bidding-based ad platforms with comparable architecture (unit-level auctions, continuous re-ranking, no persistent account-level scoring layer). No claim is made that the specific magnitudes generalize. Conditions under which the pattern would plausibly weaken are stated as falsifiable predictions for future replication:

- Platforms or ad categories with **mandatory human review** (e.g., regulated verticals such as healthcare, finance, or political advertising), where account-level trust signals could re-enter the outcome through reviewer discretion.
- **New keyword or product categories** without established auction liquidity, where the platform may fall back on account-level heuristics in the absence of sufficient real-time signal.
- Platforms whose ranking algorithm **explicitly incorporates account tenure or verification status** as a ranking feature (unlike the platform studied here, where no such mechanism is documented in public product materials).

---

## 10. Practical Implications

**For an advertiser evaluating whether size will affect algorithmic treatment.**

1. **Budget allocation should track spend, not account size.** The decomposition result (§5.3–5.4) is consistent with outcome quality tracking how much is actually spent, not the size tier of the advertiser behind it. A smaller advertiser willing to match a larger competitor's spend on a given ad group should not expect a structural penalty for being smaller, based on the observational pattern found here.
2. **Expect this to vary somewhat by campaign product type.** H2 found statistically significant heterogeneity across campaign types (§5.5), even though no single product type showed a significant size coefficient on its own. Advertisers running shopping or local-business campaigns specifically should treat the "spend, not size" guidance as somewhat less airtight than for website campaigns.
3. **A longitudinal follow-up points the same direction, with less certainty.** §7 suggests account tenure similarly shows little direct association with how quickly a new ad group ramps up, but that result is directional rather than independently conclusive.

**For a platform researcher or fairness auditor evaluating a similar real-time auction system.** The audit logic in §3.2 generalizes as a method independent of this platform's specific findings — test whether a structural attribute's statistical association with outcomes survives controlling for the legitimate behavioral channel it plausibly operates through, rather than testing only for a raw, unconditional outcome gap. §9 spells out the conditions under which this platform's specific null result would *not* be expected to replicate, and, more generally, the conditions any auditor should check before applying this design elsewhere.

---

## 11. Limitations

| # | Limitation | Where addressed |
|---|---|---|
| 1 | Single agency, single platform, by design | §4, §9.3 |
| 2 | CPC-based estimates carry a partly mechanical component; bid_amount is the primary quantitative claim wherever the two diverge | §5.4, Fig. 7 |
| 3 | Keyword-review-status boundary check (§9.1) is under-powered (0.5% of keywords carry a non-standard status) | §9.1 |
| 4 | The ad-group dimension table is a snapshot, so all account-age/history measures in §7 are lower bounds | §7 |
| 5 | Every decomposition claim (H1a/b/c) is associational, not causally identified; the one design-based identification attempt (2SLS) could not be completed | §5.4 |
| 6 | The §7 longitudinal extension is directionally supportive but not independently conclusive; both central nulls are TOST-inconclusive | §7.3 |
| 7 | The audit methodology (§3.2) is demonstrated on one structural attribute and one candidate mediator on one platform; its generality as a method has not itself been cross-validated against a second attribute–mediator pair in this report | §3.2, §9 |
| 8 | The H2 boundary-condition strata are unevenly sized (n = 184 website vs. n = 27 local-business vs. n = 17 shopping) | §5.5 |
| 9 | The design artifact's binary-decision backtest (§8.2) is inconclusive at current sample size (n ≈ 20 customers) | §8.2 |
| 10 | The exploratory industry-classification stratification (§9.2) uses labels of moderate-at-best reliability and is not used as evidence for any claim | §9.2 |
| 11 | An exploratory churn-prediction check exists outside the main hypothesis family and is reported separately, owing to its small labeled sample (n = 213, 2.35% churn rate) and a statistical floor on its model-comparison test | [`appendix/churn_prediction_rq4.md`](appendix/churn_prediction_rq4.md) |

For the full narrative behind every methodological pivot referenced above, see [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md); for the single canonical statistics table each result feeds into, see [`docs/RESULTS_SUMMARY.md`](docs/RESULTS_SUMMARY.md).

---

## 12. Methodology Summary

| | Study 1 (cross-sectional, §5) | Study 2 (longitudinal, §7) |
|---|---|---|
| Primary test | Cluster-robust controlled regression (HC3 / cluster SE), replicated on a cost-independent outcome | Customer-level aggregate OLS + cluster permutation test |
| Robustness battery | Cluster permutation test, bootstrap CI, approximate Bayes factor, MDE, specification curve, placebo test, 2SLS, temporal split replication, cost-sharing-artifact isolation, alternative-outcome replication | Bootstrap CI, winsorizing, rank-rank regression, leave-one-out, within/between decomposition, TOST equivalence |
| Heterogeneity / boundary conditions | `campaign_type` joint Wald test (H2, p = .023); keyword review-status (exploratory) | — |
| Sensitivity analysis | Oster's delta (bid_amount b-path), with a numerical-stability guard | — |
| Multiple-testing correction | Benjamini-Hochberg FDR (6 primary hypotheses) | Not applicable (single confirmatory hypothesis; convergence across 5 methods used instead) |
| Pre-registered / post-hoc power check | MDE at 80% power | Simulation reusing real cluster structure (500 iterations); only large effects (β ≈ .5) reliably detectable (88% power) |
| Related figures | 1, 2, 3, 7, 8 | 5, 6, 9 |

Known code- and design-level issues (the unrecoverable 2SLS first-stage F-statistic, the Wilcoxon floor-*p* artifact in the churn appendix, the numerically unstable Oster's delta regime, among others) are logged transparently in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md).

---

## 13. Discussion

**Read as a methods contribution first.** This report's primary claim is a reusable audit design: decompose a structural-attribute/outcome relationship into a legitimate-channel path and a residual direct path, and let the *survival or vanishing of the direct-path association* — not the presence of a raw outcome gap — be the fairness-relevant statistic (§3.2). That design is what the eight-method robustness battery (§5.4), the artifact-isolation logic (Fig. 7), and the falsifiable boundary-condition statement (§9) are built to stress-test, and it is what should travel to other platforms, structural attributes, and candidate mediators, independent of which way any single application's finding points. This is a design for characterizing statistical patterns rigorously, not a causal-inference method, and its contribution should be evaluated on those terms.

**Read as an application, the case here returns a clean null.** Advertiser size shows no direct statistical association with algorithmic outcomes on this platform once spend is controlled — an instance of what this report calls **structural blindness**. Practically, this suggests account size does not appear, in this data, to be a useful proxy for how a given ad group will perform on this platform; what the advertiser actually does — how much it spends — is the more informative, more actionable signal, to the extent the observational pattern found here holds going forward.

**Theoretically**, this reframes a common concern in platform-fairness discussions: an apparent algorithmic-treatment gap by account scale may need to be interpreted not as a gap driven by the structural attribute itself, but as a gap in the behavior that attribute is correlated with — a distinction about statistical structure, which future work with a credible identification strategy would be needed to elevate into a causal claim. The boundary conditions in §9 are offered as the falsifiable scope of that reframing, and §7's longitudinal extension is offered as a directionally consistent, though not yet independently conclusive, signal that the same pattern may extend to account tenure as well as account size. The design artifact in §8 is offered as a concrete, if not yet empirically validated, translation of the within-customer result into an operational decision rule.

The paper's lasting contribution, in the authors' view, is less "size doesn't matter on this platform" and more **"here is how to tell, rigorously, whether a structural attribute's association with outcomes is direct or only runs through what it is correlated with"** — a question that outlives any single platform's specific answer to it.

---

## 14. How to Reproduce

```bash
git clone <this-repo>
cd ad-coldstart-analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# point config/config.yaml at your local copy of the source data extract
# (see data/README.md for the required schema)

# 1. Diagnostic pipeline (sample construction, censoring checks, power
#    simulations, feature/window design) — produces the evidence base
#    §7 relies on
bash run_diagnostics.sh

# 2. Earlier-generation pipeline (variance decomposition, advertiser-size
#    fairness suite with multiverse + placebo tests, churn appendix)
bash run_pipeline_v4.sh

# 3. Confirmatory §7 tests
python -m src.analysis.rq1_growth_curve_test --config config/config.yaml
python -m src.analysis.rq2_prediction_validation --config config/config.yaml

# 4. Supplementary robustness analyses (§5.4 method 7-8, §9.1, TOST/Oster,
#    design-artifact backtest — each independently runnable)
bash run_supplementary_robustness.sh

# 5. Figures (all nine, into figures/)
for f in figures/make_figure*.py; do python "$f"; done
```

Every step prints its own diagnostics and writes a JSON/CSV artifact to `outputs/`; nothing is silently overwritten, and every script can be re-run independently as long as its upstream artifact exists. Every cutoff or date threshold is derived from the data at run time, never hard-coded; all train/test splits are customer-grouped, with leakage checked (not assumed away) at every split. See [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) for the full list of methodological principles applied throughout.

**Data availability.** The underlying panel data are proprietary and are not included in this repository. See [`data/README.md`](data/README.md) for the expected schema, so the pipeline can be pointed at a differently-sourced, schema-compatible dataset. Code is released under the MIT License (`LICENSE`); this covers the analysis code only, not any data.

---

## 15. Appendices

| Appendix | Contents |
|---|---|
| [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) | Full estimator-selection derivation log — every point a modeling choice was found unreliable and replaced (GBTM → growth curve, MixedLM → customer-level OLS, censoring reframing, sample-exclusion rules, etc.) |
| [`docs/RESULTS_SUMMARY.md`](docs/RESULTS_SUMMARY.md) | Canonical, citable statistics table for every hypothesis in both studies |
| [`docs/DESIGN_ARTIFACT.md`](docs/DESIGN_ARTIFACT.md) | Full design-artifact specification and the complete nine-specification backtest grid underlying §8 |
| [`supplementary_robustness/01_alternative_outcome_mediation.md`](supplementary_robustness/01_alternative_outcome_mediation.md) | Full derivation of the cost-sharing-artifact isolation and bid_amount mediation replication (§5.4, methods 7–8) |
| [`supplementary_robustness/02_boundary_conditions.md`](supplementary_robustness/02_boundary_conditions.md) | Full stratified tables for campaign_type and keyword review-status (§9.1) |
| [`supplementary_robustness/03_equivalence_and_sensitivity_notes.md`](supplementary_robustness/03_equivalence_and_sensitivity_notes.md) | Full TOST derivations and the Oster's delta numerical-stability discussion |
| [`supplementary_robustness/04_design_artifact_future_work.md`](supplementary_robustness/04_design_artifact_future_work.md) | Narrative account of the design-artifact backtest and why it is reported as future work |
| [`appendix/exploratory_industry_classification.md`](appendix/exploratory_industry_classification.md) | Full industry-classification pipeline (embeddings, clustering, LLM ensemble) — exploratory, not used for any confirmatory claim |
| [`appendix/churn_prediction_rq4.md`](appendix/churn_prediction_rq4.md) | Exploratory churn-prediction appendix, outside the main hypothesis family |
| [`appendix/hypothesis_id_legacy_mapping.md`](appendix/hypothesis_id_legacy_mapping.md) | Cross-reference between current hypothesis IDs and legacy labels baked into figure titles |
