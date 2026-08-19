# Not New, But Renewed: Structural Attributes Don't Matter on an Algorithmically-Mediated Ad Platform

*A cross-sectional investigation into advertiser-size fairness and cost-efficiency allocation on a Korean paid-search platform.*

> **Cross-reference note.** This document is the single narrative entry point. Wherever a claim rests on a deeper derivation, it links to the source file: [`docs/RESULTS_SUMMARY.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/docs) (the canonical statistics table) and the relevant files under [`supplementary_robustness/`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness) (each independently runnable and mapped to a specific section below). Internal working notes — the full hypothesis-relabeling audit trail and a self-directed revision log — have been moved out of the main narrative into **Supplementary Materials (§12)**, so that the sections below read as a single continuous argument rather than a mix of results and working notes.

**A note on how to read this paper.** This report's central contribution is a **mechanism-based audit methodology** — a way of testing whether a structural attribute's association with algorithmic outcomes is *direct* (disparate treatment) or *fully channeled through a legitimate behavioral variable* (disparate impact), rather than simply asking whether an outcome gap exists. The Korean search-ads platform analyzed here is the **case through which that methodology is developed and stress-tested**, not the paper's point. Readers should weigh the eight-method robustness battery, the mediation-decomposition design, and the falsifiable boundary-condition framework (§7) as the paper's primary claim to contribution — the specific empirical null (§4) is the demonstration, not the thesis.

---

## Table of contents

1. [Introduction and Research Question](#1-introduction-and-research-question)
2. [Theoretical Framing: The Structural Blindness Construct](#2-theoretical-framing-the-structural-blindness-construct)
3. [Data and Setting](#3-data-and-setting)
4. [Empirical Strategy and Results](#4-empirical-strategy-and-results)
5. [Reframing Effect Size: Why Small Is the Point, Not the Caveat](#5-reframing-effect-size-why-small-is-the-point-not-the-caveat)
6. [Extension: A Longitudinal Robustness Signal](#6-extension-a-longitudinal-robustness-signal)
7. [Boundary Conditions and Generalizability](#7-boundary-conditions-and-generalizability)
8. [Practical Implications](#8-practical-implications)
9. [Limitations](#9-limitations)
10. [Methodology Summary](#10-methodology-summary)
11. [Discussion](#11-discussion)
12. [Supplementary Materials](#12-supplementary-materials)
    - [S.1 — Hypothesis-ID mapping and figure-label reconciliation](#s1--hypothesis-id-mapping-and-figure-label-reconciliation)
    - [S.2 — Methodology notes (full derivation log)](#s2--methodology-notes-full-derivation-log)
    - [Appendix A — Results summary (canonical statistics table)](#appendix-a--results-summary-canonical-statistics-table)
    - [Appendix B — Data availability, reproducibility, and repository structure](#appendix-b--data-availability-reproducibility-and-repository-structure)
    - [Appendix C — Methodological principles applied throughout](#appendix-c--methodological-principles-applied-throughout)

---

## 1. Introduction and Research Question

Two advertisers run campaigns on the same search-ads platform. One has been active for years and manages hundreds of ad groups; the other is comparatively small. The intuitive expectation is that the larger advertiser receives more favorable algorithmic treatment — faster approval, cheaper clicks, better ad rank — independent of how much either advertiser actually spends. This intuition is widespread in the algorithmic-fairness literature, where account scale and tenure are routinely treated as candidate sources of platform-mediated advantage, and most existing audits stop at testing whether a raw outcome gap exists across that structural category.

**This paper's contribution is a different starting point: a mediation-based audit design that asks not "is there a gap" but "is the gap direct or does it run entirely through a legitimate, non-protected channel."** That distinction — mapped in §2.2 onto the disparate-treatment / disparate-impact framework from the fairness-in-ML literature — is the methodological core of the paper. Everything downstream (the eight-method robustness battery in §4.4, the artifact-isolation logic in Figure 7, the falsifiable boundary-condition statement in §7) exists to make that mechanism test as hard to fool as possible on a single, well-documented case. The empirical answer this case happens to produce — a clean null for the direct path — is one possible output of the method, not the reason the method is worth publishing; a platform where the direct path *did* survive controlling for spend would be an equally valid demonstration of the same audit design, just with the opposite verdict.

The case: a panel of **321 advertisers and approximately 19.3 million rows** of daily/hourly performance data drawn from a single Korean search-ads ecosystem. Applying the audit design to this platform, advertiser size shows no detectable *direct* association with approval rate, cost efficiency, or ad rank once the channel size plausibly operates through — total spend — is held constant. What appears, at first glance, to be a size advantage is fully accounted for by the fact that larger advertisers spend more, not by size itself. This pattern, termed **structural blindness** (§2), describes a real-time, auction-based serving system that allocates outcomes primarily on a unit's current behavioral signal and is largely indifferent to the structural attributes of the account behind it.

**Research Question (RQ1).** *Does advertiser size confer a direct structural advantage in algorithmic outcomes — approval rate, cost efficiency, and ad rank — on an algorithmically-mediated advertising platform, independent of the advertiser's spending behavior?*

Answering RQ1 credibly requires more than a single regression coefficient. Section 4 below reports eight independent verification strategies converging on the same answer, and the analysis is intentionally sequenced to let a reader retrace the reasoning: first, where performance variance actually resides in the system (§4.1); second, why a naive comparison across advertiser-size tiers is misleading (§4.2); third, the confirmatory spend-controlled test (§4.3); fourth, the eight-method robustness battery, including replication on a cost-independent outcome that removes a mechanical confound in cost-per-click (§4.4); and fifth, a formal test of whether this null result holds uniformly across contexts or varies by product category (§4.5).

**Scope statement.** The claim advanced here is not an unconditional universal one. Within this platform, the degree to which size is irrelevant varies modestly by ad-product category (§4.5, §7a). Beyond this platform, the underlying mechanism — a real-time auction that scores each unit on its own current signal — is expected to generalize in *direction* to other platforms with comparable architecture, and is expected to plausibly weaken under mandatory human review, in new categories without established auction liquidity, or on platforms whose ranking algorithm explicitly incorporates account tenure as a feature (§7b). Section 7 develops both boundaries as a substantive contribution of the analysis, not as an appended caveat.

---

## 2. Theoretical Framing: The Structural Blindness Construct

### 2.1 Definition

**Structural blindness** describes a real-time, auction-based serving system that allocates approval, cost efficiency, and ranking primarily on a unit's *current, behavioral signal* — its bids, its clicks, its spend — and is largely indifferent to *structural attributes of the account behind that unit*, such as account size, once the legitimate channels through which structural attributes could plausibly operate (here, total spend) are held constant.

This is a claim about **mechanism**, not about raw outcomes. Large and small advertisers can and do perform differently — the question is whether that difference is *direct* (the algorithm conditions on size itself, holding everything else constant) or *indirect* (size changes behavior — how much an advertiser spends — and it is that behavior the algorithm responds to). The analysis below asks, and answers, whether the direct channel exists — and does so using a design meant to be reusable well beyond this specific finding.

### 2.2 Deriving the construct from the fairness-in-ML literature, not labeling after the fact — the paper's methodological core

Structural blindness is not an ad hoc name attached to a null result; it is derived directly from a distinction with a well-established lineage in algorithmic-fairness research, and the hypotheses in §2.3 are written to operationalize that distinction rather than to describe a finding after it was observed. **This subsection is the methodological center of gravity of the entire paper** — the audit design generalizes to any structural-attribute-versus-algorithmic-outcome question on any platform with a legitimate mediating channel, independent of which direction any particular application's answer points.

- **Disparate treatment versus disparate impact.** The fairness-in-ML literature separates *disparate treatment* — differential treatment that is conditional on a protected or structural attribute itself — from *disparate impact* — differential outcomes that arise through a legitimate, attribute-correlated channel (e.g., an attribute that predicts a legitimate input, which in turn predicts the outcome). Structural blindness maps this distinction directly onto the mediation structure tested here: **H1c** (§2.3) asks specifically whether the *direct*, treatment-style path from size to outcome survives once the legitimate mediating channel (spend) is held constant. A direct effect that survives is evidence of disparate treatment; a direct effect that vanishes, with the *indirect* path (H1a × H1b) remaining intact, is evidence that any size-outcome gap is a disparate-impact-style pattern running through a legitimate, non-protected channel. This is, in that specific sense, a mediation-based accountability audit rather than a simple outcome-gap audit — the research design was built around this distinction from the outset, which is why the hypothesis family below decomposes the size-outcome relationship into three legs (a, b, c′) rather than testing a single unconditional gap.
- **Algorithmic accountability.** Most platform-fairness audits ask *whether* an outcome gap exists across a structural category. This investigation reframes that as a *mechanism* question: is the gap direct or indirect? **That reframing — not the specific null result it produces on this one platform — is the paper's theoretical contribution.** A researcher applying this same design to a different platform, a different structural attribute (age of account, geography, verified-badge status), or a different candidate mediator would be extending the method, not merely replicating a finding.
- **Information asymmetry in two-sided platform markets.** Platform-economics theory generally assumes a platform can act on participant characteristics it has data on — and this platform's own systems record both account scale and tenure. Structural blindness is the empirical finding that, despite this information being available, the allocation mechanism studied here does not appear to condition on it directly once real-time behavioral signals are in the model. That is a substantive claim about *which* information a real-time auction mechanism actually uses in practice, not merely a claim about outcome parity.

| | Structural attribute | Candidate legitimate mediating channel |
|---|---|---|
| **This investigation** | Advertiser size (spend-tier) | Total spend |

### 2.3 Formal Research Question and Hypotheses

Every hypothesis below is stated once, formally, as a single sentence, and is tested in the section indicated.

- **RQ1.** *Does advertiser size confer a direct structural advantage in algorithmic outcomes — approval rate, cost efficiency, and ad rank — independent of the advertiser's spending behavior?* (§4.3–§4.4)
- **H1a (a-path).** *Advertiser size is positively associated with an advertiser's total spend.* (§4.4, method 8)
- **H1b (b-path).** *Total spend is positively associated with outcome quality — approval rate, cost efficiency, and ad rank — holding advertiser size constant.* (§4.4, method 8)
- **H1c (c′-path, the central hypothesis).** *Advertiser size has no direct association with outcome quality once total spend is held constant — that is, the size–outcome relationship is fully, not partially, mediated by spend.* (§4.3, §4.4)
- **H1 (composite).** *The entire size–outcome relationship operates through spend rather than through size itself* — supported if H1a and H1b are confirmed and H1c's null cannot be rejected under a well-powered test. (§4.3–§4.4)
- **H2 (boundary condition).** *H1c's null holds homogeneously across platform-defined ad-product categories* — i.e., the degree of structural blindness does not depend on which approval pipeline a campaign routes through. (§4.5)

One further question is pre-specified as **exploratory**, evaluated without a single confirmatory point-null because of a known power limit:

- **RQ2.** *Does keyword-level discretionary review status interact with advertiser size* — a candidate channel through which structural attributes could re-enter the allocation process despite H1c? (§7a)

A separate, self-contained exploratory appendix, outside the RQ1 hypothesis family:

- **RQ4.** *Can advertiser account churn be predicted from approval, cost, and efficiency features?* (§4.7)

### 2.4 What "confirmed" means throughout

Every hypothesis above that returns a non-significant result is reported alongside its minimum-detectable-effect (MDE) band at 80% power (§4.3, Figure 2), so that a null result can be read as *well-powered* rather than merely *undetected*. This report distinguishes "failing to reject a point-null with a characterized detection floor" from "an unconditional universal claim" throughout, and states which of the two applies at every point a null result is central to the argument.

### 2.5 Quick-reference: where each hypothesis is tested

| ID | Tested in | Primary figure |
|---|---|---|
| P0 (preliminary, motivates but does not test H1) | §4.1 | Figure 1 |
| H1a / H1b / H1c / H1 | §4.3–4.4 | Figures 2, 3, 7 |
| H2 | §4.5 | Figure 8 |
| RQ2 | §7a | — |
| RQ4 | §4.7 | Figure 4 |

---

## 3. Data and Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata, including `campaign_type` (ad-product code) | 1,504 | 263/321 |
| Ad group dimension (snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status` (review code), bid price | 1,503,289 | 256/321 |

Conversion and ROAS variables were excluded entirely: the platform's conversion API retroactively backfills conversions per account on a delayed, inconsistent schedule, which breaks construct validity for anything built on top of it. This was a design decision made before any modeling began, not a post-hoc exclusion.

### 3.1 The single-platform, single-agency design as a methodological choice

All data originates from one Korean ad-tech provider sourced from one search platform. This is stated here as a design property with two sides, not simply as a limitation to be disclosed and moved past.

On one side, it bounds external generalizability — the findings describe this platform's specific allocation mechanism, and §7b states explicitly how far the mechanism is expected to travel to other architectures. On the other side, single-platform, single-agency sourcing is precisely what makes the internal test clean: every advertiser in the panel faces the *same* ranking algorithm, the *same* approval pipeline, and the *same* data-collection process, which removes an entire class of between-platform confounds (different auction mechanics, different fee structures, different measurement conventions) that would otherwise be entangled with any size effect in a multi-platform sample. A multi-platform design would trade this internal cleanliness for external breadth; the design adopted here makes the opposite trade deliberately, and §7b is the corresponding statement of how far the resulting mechanism claim is expected to extend beyond the single context it was estimated in. Framed as an audit-methodology paper (§1), this single-platform design should be read the way a single well-instrumented case study is read in the accountability-audit literature: as a proof of concept for the *method*, whose external validity claim is explicitly bounded rather than implied.

---

## 4. Empirical Strategy and Results

### 4.1 Where would an advantage even live? (motivates H1, does not itself test it)

Before testing anything about advertiser size, the analysis first located *where* performance variation sits — in the customer, the campaign, or the ad group. If a size-related advantage exists, it should show up as customer-level variance.

![Figure 1 | Multilevel variance decomposition of advertising performance](figures/Figure1_variance_decomposition.png)

**Figure 1 — Multilevel variance decomposition** (`figures/make_figure1_variance_decomposition.py`). Across ~663K observations, log ad spend is dominated by unexplained residual variance (ICC = 0.825) — day-to-day budget execution, not who the customer is (ICC = 0.050). Click-through rate tells a similar story: the largest share of variation sits at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both patterns hold whether or not month fixed effects are added, ruling out seasonality as the explanation. This is the first indication, prior to any hypothesis test, that "who the customer is" explains comparatively little of what happens on this platform.

### 4.2 The raw gap looks real — until clustering is accounted for

Splitting advertisers into four size tiers (by spend volume) and comparing approval rate, CPC, and ad rank across tiers with a Kruskal-Wallis test shows differences that are statistically significant across the board (p < .001 for CPC and ad rank; p = .0006 for approval rate).

This raw signal, however, does not survive a more appropriate test. Ad groups belonging to the same customer share policies and are not statistically independent — the standard Kruskal-Wallis test assumes independence that does not hold here. Re-running the comparison as a customer-level cluster permutation test (2,000 iterations) made most of the apparently "significant" gap in approval rate and CPC evaporate. The raw test's significance was substantially an artifact of ignoring clustering — precisely the kind of naive audit that the mechanism-based design in §2.2 is built to correct.

### 4.3 The central confirmatory test: the direct effect vanishes once spend is controlled (H1c)

![Figure 2 | Advertiser-size effect on approval, cost efficiency, and ad rank, controlling for spend](figures/Figure2_fairness_forest_plot.png)

**Figure 2 — The central confirmatory test of H1c.** Controlling for log spend in a cluster-robust regression, all six outcome × sample combinations (approval rate, CPC, ad rank, each in the full sample and with spike-affected accounts excluded) return **non-significant** direct effects of size (cluster-robust p > .07). Every 95% bootstrap confidence interval not only crosses zero — it falls entirely inside, or right at the edge of, its own minimum-detectable-effect (MDE) band. This is the evidentiary core of the well-powered-null claim in §2.4: the observed effect is smaller than anything this sample could reliably detect, which rules out "we just didn't have the power to see it" as the explanation for the null. Approximate Bayes factors favor the null in five of six tests; the sixth (CPC under spike exclusion) is flagged as a directionally-reversed sensitivity finding and is not treated as confirmatory.

### 4.4 Stress-testing across eight independent methods

A single regression result is easy to distrust, so H1c was stress-tested eight independent ways, with methods 7–8 additionally establishing H1a and H1b. Methods 1–6 are summarized below; full derivations for methods 7–8 are in [`supplementary_robustness/01_alternative_outcome_mediation.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness).

1. **Multiverse specification curve** (48 defensible analytic choices; 0/48 reach significance for any outcome).
2. **Placebo test** (device-type share, which size *shouldn't* predict, is significant under the raw distributional test but null under the spend-controlled regression — evidence the regression, not the raw distributional test, is measuring the right thing).
3. **Customer-and-month fixed-effects panel regression.**
4. **Two-stage least squares with lagged spend as an instrument.** The first-stage F-statistic could not be recovered due to a code exception; this attempt is flagged and excluded from any conclusion, not silently dropped (see §9, limitation 8).
5. **Temporal split-sample replication.**
6. **Benjamini-Hochberg FDR correction** across the six primary hypotheses.

![Figure 3 | Multiverse specification curve and placebo test](figures/Figure3_specification_curve_placebo.png)

**Figure 3 — Methods 1 and 2.** Panel A: across all 48 specification choices (tier definition × covariate set) and all three outcomes, not one reaches significance at α = .05. Panel B: the raw distributional (Kruskal-Wallis) test is significant for *both* the real outcome and the device-share placebo — proof that a distributional test alone is not a clean placebo here, since size tiers correlate with many unrelated account traits. The informative comparison is the spend-controlled regression matching H1c: there, real and placebo outcomes are equally, indistinguishably null.

7. **Isolating a mechanical artifact in the CPC outcome.** CPC = cost / click, and spend is built from cost, so any spend → CPC relationship carries a mechanical component by construction, independent of real bidding-efficiency behavior. A customer-level permutation procedure (reshuffling click within customer while holding cost fixed, 2,000 iterations) isolates how large that mechanical component is. The observed spend → log(CPC) coefficient (+1.277) falls *below* the lower bound of the resulting purely-mechanical null distribution (mean +1.552, 95% range [1.544, 1.556]) — meaning the CPC-based estimate is not simply inflated by the artifact, though it sits close enough to the mechanical distribution that it is treated as directionally informative rather than as a stand-alone quantitative claim. A lagged replication (spend at day *t* → CPC at *t*+1 and *t*+7, immune to same-day cost-sharing) confirms a same-signed, significant relationship at both lags (β = +0.538 and +0.544, both p < .001), consistent with a genuine behavioral effect coexisting with the mechanical artifact.

8. **Replicating the mediation result on a cost-independent outcome.** `bid_amount` (the advertiser's set bid price) shares no cost or click term with spend, so it carries none of the mechanical artifact isolated in method 7. Re-estimating the mediation structure (size → spend → outcome, controlling for size) on this outcome at the customer level (n = 263) is the load-bearing result for the efficiency claim: the indirect (spend-mediated) association is significant (bootstrap 95% CI [0.008, 0.159], excludes zero; cluster permutation p < .001), while the *direct* association of size, net of spend, is non-significant (p = .634) — the same qualitative pattern as the CPC-based model, now on an outcome immune to the artifact. Jointly, methods 7–8 are the confirmatory basis for H1a and H1b.

**On the status of every causal-sounding phrase in this report.** Every "size → spend," "spend → outcome," or "mediation" statement here — including the path labels H1a/b/c themselves — describes an **associational** pattern estimated from observational panel data, not an identified causal effect, and is written that way deliberately rather than as a hedge added after the fact. The one attempt at design-based identification (method 4, two-stage least squares) could not be completed, and its failure is reported openly rather than folded into the confirmatory evidence. What the analysis *can* support, and does support, is a considerably stronger form of associational evidence than a single cross-sectional correlation: the same qualitative pattern — indirect effect present, direct effect absent — replicates across a mechanically-contaminated outcome (CPC) and a mechanically-independent outcome (bid_amount, method 8), across 48 specification choices (method 1), against a placebo variable (method 2), across two independent time splits (method 5), and survives multiple-testing correction (method 6). A single associational claim would be fragile; an associational pattern that eight independent, differently-vulnerable methods converge on is a materially stronger form of evidence, and is the basis on which "the size–outcome relationship runs through spend" is asserted throughout this report — as an associational, replicated finding, not a causal one.

![Figure 7 | Spend-mediation b-path: CPC-based vs. cost-independent outcome](figures/Figure7_mediation_forest.png)

**Figure 7 — CPC-based vs. bid_amount-based b-path.** The spend → outcome coefficient shrinks from +1.277 (CPC-based, partly mechanical) to +0.150 (bid_amount-based, cost-independent) once the shared cost term is removed — the direction survives, the magnitude does not, which is exactly the pattern method 7's artifact-isolation predicts if the CPC-based estimate is inflated by construction rather than by a stronger true effect.

**Eight independent verification methods, one consistent verdict**, with method 8 — not the raw CPC coefficient — treated as the primary quantitative evidence for the efficiency-outcome claim. Jointly, methods 1–8 are the confirmatory basis for H1 (H1a ∧ H1b ∧ H1c).

### 4.5 Is the null homogeneous across contexts? (H2)

Close to, but not perfectly, homogeneous — and this is treated as a substantive finding rather than a complication. Stratifying the spend-controlled CPC model by `campaign_type` (a platform-defined ad-product code — website / shopping / brand-new-product / local-business, not an industry classification) and running a joint Wald test on the size × product-type interaction gives **p = .023**: the *degree* to which size is irrelevant varies somewhat by ad-product category, even though no individual stratum shows a significant size effect on its own (all p > .05).

![Figure 8 | Campaign product-type heterogeneity](figures/Figure8_boundary_condition_forest.png)

**Figure 8 — Boundary-condition forest plot** (the confirmatory test of H2; full stratified table and the RQ2 check in [`supplementary_robustness/02_boundary_conditions.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness)). Website campaigns show a non-significant negative point estimate for size net of spend, while local-business and shopping campaigns show non-significant positive point estimates — all three confidence intervals cross zero individually, but the joint test across strata is significant (p = .023), meaning the *pattern* of where size comes closest to mattering is not random noise even though no single stratum is itself conclusive. This is precisely the kind of qualification a mechanism-level construct is supposed to produce: not "nothing ever matters," but "nothing matters, to a precisely measured and category-dependent degree" (§7).

### 4.6 Exploratory extension (RQ2)

One further stratification was piloted as a boundary-condition check and is reported as exploratory, not confirmatory, evidence; it is developed in full in §7a.

### 4.7 A side investigation, outside the RQ1 hypothesis family (RQ4)

Whether machine-learning models can predict advertiser churn from approval/cost/efficiency features sits entirely outside the structural-blindness hypothesis family — it is retained as a self-contained exploratory appendix because it was already run, not because it bears on RQ1.

![Figure 4 | Churn-prediction benchmarking](figures/Figure4_churn_benchmark.png)

**Figure 4 — Churn-prediction benchmarking** (RQ4, outside the H1 hypothesis family). Across 213 labeled accounts (a 2.35% churn rate), tree-based models nominally outperform logistic regression in nested cross-validation, but every pairwise model comparison returns the same Wilcoxon p-value (0.0625) — the mathematical floor achievable with only 5 repeat-pairs, not evidence of a real difference. Random forest had the best-calibrated out-of-fold predictions (Brier score 0.0250).

### 4.8 Conclusion of the confirmatory analysis

Raw size-tier gaps in approval rate, CPC, and ad rank are statistically detectable but small, and their significance is fragile once clustering is accounted for. The confirmatory test — a spend-controlled regression, replicated on a cost-independent outcome — returns a clean, well-powered null for the *direct* association of size (H1c) across every outcome-sample combination, backed by eight independent robustness checks, with one precisely characterized caveat: the null is not perfectly homogeneous across ad-product categories (H2, §4.5). **The apparent advantage of being a large advertiser is, to first order, fully accounted for by spending more rather than by size itself — with modest, product-type-dependent variation in how completely that holds, and with the associational status of every mediation claim kept explicit throughout.**

---

## 5. Reframing Effect Size: Why Small Is the Point, Not the Caveat

The raw distributional comparison in §4.2 produced effect sizes in the ε² = 0.002–0.079 range. Read in isolation, small effect sizes on 19.3 million observations can look like a reason for caution. Read against the theoretical structure in §2, they are close to the *predicted* result, and the argument for that is worth making explicitly rather than leaving the effect-size table to speak for itself.

**A near-zero direct effect is what full mediation predicts, not a weakness of the test that found it.** H1c's claim is that size has *no remaining direct* association with outcomes once spend is controlled. If H1c is true, the residual, spend-controlled association between size and outcome should be indistinguishable from zero *by construction* — a large residual effect size would in fact be evidence *against* the mediation account, not for it. The small ε² values in the raw, unconditional comparison (§4.2) reflect a gap that mostly *disappears* once the mediating variable is introduced (§4.3); what is being reported is not "we found a weak effect" but "we found that the effect that exists in the raw data is close to fully absorbed by a single mediator," which is a considerably stronger and more specific claim than an unconditional weak-effect finding would be.

**The relevant question is existence and sign, not magnitude, and the analysis is built to answer that question precisely.** Because H1c is a test of whether a direct path exists at all, its evidentiary weight comes from the *minimum-detectable-effect* framing in Figure 2 — every confidence interval sits inside its own MDE band, meaning the sample is well-powered to detect an effect an order of magnitude smaller than the raw ε² values would suggest is "the size of the effect being tested." A small effect size on the raw comparison and a well-powered null on the controlled comparison are two different statistics answering two different questions, and conflating them is the error this section is written to preempt.

**In a 19.3-million-row panel, small-but-real correlations are the expected texture of any observational relationship, and screening on the direction and stability of the mediation path — not on the raw ε² — is the more informative test.** The consistency of the qualitative pattern (indirect effect present, direct effect absent) across eight independent methods (§4.4) is doing the evidentiary work here, not the magnitude of any single coefficient. A specification-curve result of "0/48 configurations reach significance" and a placebo test that shows the *same* raw pattern for a variable size *shouldn't* predict (Figure 3) are both effect-size-independent forms of evidence, and both point the same direction as the small ε² values.

---

## 6. Extension: A Longitudinal Robustness Signal

*(Condensed. The cross-sectional analysis in §4 is the paper's confirmatory core; this section is a brief, secondary check on an independent, smaller sample and is reported strictly as a directional signal, not as an independently conclusive result.)*

A natural follow-up to §4's cross-sectional test is whether an account's *accumulated history* — how long it has operated, how many ad groups it has run — predicts how a newly registered ad group inside that account performs, using an independent longitudinal sample (n = 29 customers, 204 ad groups, sharing no rows with §4's data).

![Figure 5 | Cold-start sample construction and confirmatory test](figures/Figure5_coldstart_funnel_and_RQ1_null.png)

**Figure 5** — Sample-construction funnel (250 candidates → 204 with a complete 30-day window, 29 customers once aggregated) and the confirmatory test: account maturity shows no significant relationship with a new ad group's initial 30-day growth slope (OLS β = 8.34, p = .576; cluster permutation p = .663; standardized β = .085, only 17% of the pre-registered detection threshold). A leave-one-out check removing the largest customer (35.8% of the sample) leaves the conclusion unchanged (permutation p = .702).

![Figure 6 | Early-signal prediction and intervention-timing simulation](figures/Figure6_RQ2_horizon_RQ3_lift.png)

**Figure 6** — An ad group's own early operating signal predicts near-term growth (ρ = 0.386, leakage-free 14-day-ahead); adding account maturity does not improve *within-customer* prediction (an apparent pooled gain is attributable to between-customer signal leaking through a pooled metric). Early-signal flagging achieves a 1.2–1.4× precision lift over random flagging, consistent across days 7, 14, and 21 post-registration, with no cutoff statistically distinguishable as optimal.

![Figure 9 | TOST equivalence tests](figures/Figure9_tost_equivalence.png)

**Figure 9** — Because a non-significant p-value does not itself establish an effect is absent, both null results above were tested for formal equivalence (TOST). Neither reaches it (maturity → growth slope: p = .197; maturity's contribution to prediction: p = .290), so both are reported as well-powered, non-significant associations for which formal equivalence remains inconclusive. This is why §6 is framed as a supporting, directional extension rather than an independently confirmatory companion to §4 — a larger longitudinal sample is the natural next step.

Full statistics for this section are in Appendix A; the underlying design decisions (why a growth-curve slope replaced a latent-class trajectory model, why a customer-level OLS replaced a random-intercept mixed model, and the sample-exclusion rules used) are logged in §12.2 for transparency and are not repeated here.

---

## 7. Boundary Conditions and Generalizability

This section is the paper's account of the *conditions* under which structural blindness holds, treated as a contribution in its own right: a mechanism claim is only as useful as the boundary conditions attached to it, and stating those boundaries precisely turns "nothing matters" into the more defensible, falsifiable claim "nothing matters, except under these specified conditions." Two questions bound how far the claim travels: (a) does it hold uniformly *within* this platform, and (b) how far does it plausibly extend *beyond* this platform. Full detail lives in [`supplementary_robustness/02_boundary_conditions.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness).

**(a) Within-platform heterogeneity.** Two strata were tested against the central result:

- **Campaign product type** (platform-defined, well-measured; §4.5; this is H2): the spend-controlled size effect is not perfectly homogeneous across website / shopping / local-business / brand-new-product campaigns (joint Wald p = .023), plausibly because these route through different approval pipelines (e.g., shopping campaigns undergo product-feed validation that standard search campaigns do not). No individual stratum shows a significant size effect.
- **Keyword review status** (a proxy for platform discretion; RQ2). Only 0.5% of keywords in this dataset carry a non-standard `inspect_status` code, so this check is under-powered by construction. A restricted-approval-driven interaction is directionally interesting (p = .016) but does not cleanly map onto the "discretionary review as a leakage channel" mechanism that motivated the check, since restricted-approval denotes an already-resolved outcome rather than a pending discretionary review. Reported as preliminary.

  | Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
  |---|---|---|---|
  | Under-review only | 22 | 230 | .638 |
  | Restricted-approval only | 106 | 146 | .016 |
  | Combined | 111 | 141 | .016 |

  The combined definition's significance is driven almost entirely by the restricted-approval component (106 of 111 customers), not by an independent contribution from the under-review component — one underlying signal probed three ways, not three independent confirmations.

**(b) Cross-platform generalizability.** The mechanism documented here — real-time, auction-based serving that scores each unit primarily on its own current signal — is a property of the serving architecture, not of this platform's brand specifically. The *direction* of the structural-blindness finding is expected to generalize to other real-time bidding-based ad platforms with comparable architecture (unit-level auctions, continuous re-ranking, no persistent account-level scoring layer). No claim is made that the specific magnitudes generalize, and conditions under which the mechanism plausibly weakens are stated explicitly as falsifiable predictions for future replication:

- Platforms or ad categories with **mandatory human review** in the approval pipeline (e.g., regulated verticals such as healthcare, finance, or political advertising), where account-level trust signals could re-enter the process through reviewer discretion rather than the bidding algorithm.
- **New keyword or product categories** without established auction liquidity, where the platform may fall back on account-level heuristics in the absence of sufficient real-time signal.
- Platforms whose ranking algorithm **explicitly incorporates account tenure or verification status** as a ranking feature (unlike the platform studied here, where no such mechanism is documented in public product materials).

This is also, precisely, the reusable output of the audit design in §2.2: any application of this method to a new platform or attribute should end with a boundary-condition statement of this shape.

---

## 8. Practical Implications

**For an advertiser evaluating whether size will affect algorithmic treatment:**

1. **Budget allocation should track spend, not account size.** The mediation result (§4.3–4.4) is consistent with outcome quality — approval rate, cost efficiency, ad rank — tracking how much is actually spent, not the size tier of the advertiser behind it. A smaller advertiser willing to match a larger competitor's spend on a given ad group should not expect a structural penalty for being smaller.
2. **Expect this to vary somewhat by campaign product type.** The size-is-largely-irrelevant pattern is not perfectly uniform: H2 found statistically significant heterogeneity across campaign types (joint Wald p = .023, §4.5), even though no single product type showed a significant size effect on its own. Advertisers running shopping or local-business campaigns specifically should treat the "spend, not size, is what matters" guidance as somewhat less airtight than for website campaigns.
3. **A longitudinal follow-up points the same direction, with less certainty.** §6's extension suggests account tenure similarly shows little direct association with how quickly a new ad group ramps up, but that specific result is directional rather than independently conclusive (§6) and should be weighted accordingly.

**For a platform researcher or fairness auditor evaluating a similar real-time auction system:** the accountability-audit logic in §2.2 generalizes as a method independent of this platform's specific findings — test whether a structural attribute's association with outcomes survives controlling for the legitimate behavioral channel it plausibly operates through, rather than testing only for a raw, unconditional outcome gap. §7 spells out the conditions (mandatory human review, illiquid new categories, tenure-aware ranking algorithms) under which this platform's specific null result would *not* be expected to replicate — and, more generally, the conditions any auditor should check before applying this design elsewhere.

---

## 9. Limitations

1. **Single agency, single platform**, by design (§3.1). §7b states the specific conditions under which the mechanism is expected to hold or plausibly weaken elsewhere.
2. **CPC-based estimates carry a partly mechanical component.** Reported as directionally informative only; the bid_amount-based estimate is the primary quantitative claim wherever the two diverge (§4.4, Figure 7).
3. **The keyword-review-status boundary-condition check (RQ2) is under-powered** (0.5% of keywords carry a non-standard status) and is reported as preliminary (§7a).
4. **The ad-group dimension table is a snapshot**, so all account-age and account-history measures used in the §6 extension are lower bounds.
5. **Every mediation claim (H1a/b/c) describes an associational, not a causally identified, pattern** — the one design-based identification attempt (2SLS, §4.4 method 4) could not be completed, so causal language throughout is deliberately qualified (§4.4).
6. **The longitudinal extension in §6 is directionally supportive but not independently conclusive**: its central null results are non-significant but not formally equivalence-confirmed (TOST inconclusive; Figure 9).
7. **The audit methodology (§2.2) is demonstrated on one structural attribute (size) and one candidate mediator (spend)** on one platform; its generality as a method — rather than the correctness of the specific size/spend finding — is an argument made on methodological grounds (§2.2, §7) and has not itself been cross-validated against a second attribute-mediator pair in this paper.

For the full narrative behind every methodological pivot referenced above, see §12.2 (Methodology Notes); for the single canonical statistics table each result feeds into, see Appendix A.

---

## 10. Methodology Summary

| | Cross-sectional analysis (§4) | Longitudinal extension (§6) |
|---|---|---|
| Primary test | Cluster-robust controlled regression (HC3 / cluster SE), replicated on a cost-independent outcome | Customer-level aggregate OLS + cluster permutation test |
| Robustness battery | Cluster permutation test, bootstrap CI, approximate Bayes factor, MDE, specification curve, placebo test, 2SLS, temporal split replication, cost-sharing-artifact isolation, alternative-outcome replication | Bootstrap CI, winsorizing, rank-rank regression, leave-one-out, within/between decomposition, TOST equivalence |
| Heterogeneity / boundary conditions | campaign_type joint Wald test (H2, p = .023); keyword review-status (RQ2, exploratory) | — |
| Sensitivity analysis | Oster's delta (bid_amount b-path), with a numerical-stability guard | — |
| Multiple-testing correction | Benjamini-Hochberg FDR (6 primary hypotheses) | Not applicable (single confirmatory hypothesis; convergence across 5 methods used instead) |
| Pre-registered / post-hoc power check | MDE at 80% power | Simulation reusing real cluster structure (500 iterations); only large effects (β ≈ .5) reliably detectable (88% power) |
| Related figures | 1, 2, 3, 4, 7, 8 | 5, 6, 9 |

Known code- and design-level issues (the unrecoverable 2SLS first-stage F-statistic, the Wilcoxon floor-p artifact in the churn appendix, among others) are logged transparently in §12.2. The exact statistics each test produced live in Appendix A.

---

## 11. Discussion

**Read as a methods paper first.** This report's primary claim is a reusable audit design: decompose a structural-attribute/outcome relationship into a legitimate-channel path and a residual direct path, and let the *survival or vanishing of the direct path* — not the presence of a raw outcome gap — be the fairness verdict (§2.2). That design is what the eight-method robustness battery (§4.4), the artifact-isolation logic (Figure 7), and the falsifiable boundary-condition statement (§7) are built to stress-test, and it is what should travel to other platforms, other structural attributes, and other candidate mediators, independent of which way any single application's finding points.

**Read as an application, the case here happens to return a clean null.** Advertiser size shows no direct association with algorithmic outcomes on this platform once spend is controlled — an instance of what the paper calls **structural blindness**: a real-time auction that allocates on current behavioral signal and is largely indifferent to the structural attributes behind it. Practically, the implication for advertisers is clear: account size should not be used as a proxy for how a given ad group will perform on this platform; what the advertiser actually does — how much it spends — is the more informative, more actionable signal.

**Theoretically**, this reframes a common concern in platform-fairness discussions: an apparent algorithmic-treatment gap by account scale may need to be interpreted not as a gap driven by the structural attribute itself, but as a gap in the behavior that attribute is correlated with (spending capacity). The boundary conditions in §7 are offered as the falsifiable scope of that reframing, not as an unconditional claim, and the longitudinal extension in §6 is offered as a directionally consistent, though not yet independently conclusive, signal that the same pattern may extend to account tenure as well as account size. The paper's lasting contribution, in the authors' view, is less "size doesn't matter on this platform" and more "here is how to tell, rigorously, whether a structural attribute matters directly or only through what it makes people do" — a question that outlives any single platform's specific answer to it.

---

## 12. Supplementary Materials

The material in this section supports the analysis above but is separated from it so that §§1–11 read as a continuous argument rather than a mix of results and internal working notes.

### S.1 — Hypothesis-ID mapping and figure-label reconciliation

The nine figure files referenced throughout this report were generated with an earlier round of (unprefixed) internal labels — "RQ1," "RQ2," "H2b," and so on — baked into the image titles. The table below is the permanent cross-reference between the formal IDs used in §§1–11 and those legacy labels, so that any given figure can be traced unambiguously to the hypothesis it tests. A superseded label is never deleted or silently dropped; it remains in the table with a pointer to what replaced it, so any revision to the hypothesis framing stays auditable. (An earlier internal draft also carried a formal ID "RQ3" for a piloted advertiser-industry stratification; that check was dropped from the hypothesis family entirely due to unusable label reliability and does not appear below. The legacy figure-title text "RQ3" appearing on Figure 4 is unrelated — it is a pre-relabeling name for what this table now calls RQ4, reconciled in the row below.)

| Current ID (this report) | Legacy label(s) in figure titles | What it claims | Status |
|---|---|---|---|
| **P0** | Figure 1's "(RQ1)" | Preliminary: performance variance sits mostly at ad-group/residual level, not customer level | Descriptive, motivates but does not test H1 |
| **H1a** | (unlabeled a-path, §4.4 method 8) | Size → total spend (a-path) | Confirmed, p < .001 |
| **H1b** | (unlabeled b-path, §4.4 method 8) | Spend → outcome, controlling for size (b-path), cost-independent outcome | Confirmed, p = .032 |
| **H1c** | Figure 2's "(RQ2, H2b)"; Figure 3's "(RQ2 robustness suite)" | Size → outcome, controlling for spend (c′-path, direct effect) = 0 | Confirmed null, 8 robustness checks |
| **H1 (composite)** | — | Indirect effect (a×b) is the entire size→outcome relationship | Supported |
| **H2** | Figure 8's "(joint Wald test)" | H1c's null is homogeneous across `campaign_type` strata | Rejected, p = .023 (heterogeneous) |
| **RQ2** | §7(a) keyword-review-status check | Does discretionary review leak account attributes into outcomes? | Exploratory, underpowered |
| **RQ4** | Figure 4's legacy "(RQ3, exploratory appendix)" label | Can churn be predicted from approval/cost/efficiency features? | Exploratory appendix, outside the H1 family |
| **§6-Maturity** | Figure 5's "H1 (RQ1)" | Account maturity → initial 30-day growth slope (longitudinal extension) | Null (non-sig); TOST inconclusive |
| **§6-EarlySignal** | Figure 6's "RQ2"/"H2a" | Ad group's own early signal → later growth | Supported, decays with horizon |
| **§6-MaturityAdd** | Figure 6's "RQ2"/"H2b" | Adding account maturity improves early-signal prediction | Rejected; TOST inconclusive |
| **§6-Flagging** | Figure 6's "RQ3" | At what post-registration day should a low-growth ad group be flagged? | Exploratory, directional not precise |

**Naming convention.** `Hx` = a formally testable hypothesis with a directional or point-null prediction. `RQx` = a question investigated without a single confirmatory point-null (exploratory, preliminary, underpowered, or design-oriented). `P0` = a preliminary/descriptive analysis that motivates a hypothesis but does not itself test one.

### S.2 — Methodology notes (full derivation log)

This is a narrative log of every point in the underlying diagnostic pipeline where an initial modeling choice was found to be structurally unreliable and replaced with a more defensible alternative, retained here for transparency and reproducibility rather than as part of the main argument. Full version: [`docs/METHODOLOGY_NOTES.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/docs).

**Discrete latent-class growth models were the originally planned estimator for the §6 extension.** Growth trajectories were initially to be summarized with a Group-Based Trajectory Model. A BIC-based class-count recovery simulation at the achievable sample size (n = 222) found a recovery probability of ~9% at k = 2 true classes and ~0% at k = 3/4 — the sample cannot reliably distinguish class counts, independent of any censoring or clustering issue. This was dropped in favor of a continuous growth-curve quantity (a customer's initial 30-day cost slope), avoiding the class-count identification problem.

**Apparent right-censoring in the §6 sample turned out to be a different phenomenon entirely.** An initial 83.8% "censored" rate (trajectories apparently cut short by the observation window ending) barely moved under a 30-to-120-day follow-up-window sensitivity check (83.6% → 83.2%). If insufficient follow-up were the cause, a longer window should have reduced it sharply; it did not. Fixed-window coverage diagnostics showed mean observed-day coverage within fixed post-registration windows was only 70–74%, not the near-100% a continuously-run ad group would show. The explanation: these ad groups mostly do not self-terminate (activity persists to observation end because the ad group is still running) combined with genuine intermittency (on/off cycling, budget exhaustion, approval delay). The confirmatory growth-slope definition uses fixed-window linear trend fitting on zero-filled daily series rather than a survival/censoring framework.

**A customer random-intercept mixed model was the originally planned §6 estimator.** Because account maturity varies only at the customer level, it competes directly with a customer-level random intercept for the same layer of variation, producing structural non-identifiability. A pre-registered power simulation (500 iterations, reusing the real cluster structure) confirmed a 100% convergence-failure rate. This was replaced with a customer-level aggregate OLS (n ≈ 29–32), with a cluster (customer-label) permutation test as the final arbiter whenever it and OLS disagree, because this cluster count sits below the usual 40–50+ comfort threshold for trusting asymptotic cluster-robust standard errors alone.

**A pooled Leave-One-Customer-Out (LOCO) improvement was initially misread as evidence that account maturity adds ad-group-level predictive value.** A within/between-customer decomposition showed the apparent pooled gain was concentrated almost entirely in the between-customer component — maturity was re-injecting the same customer-level growth signal already established through a pooled metric, not genuinely improving ad-group-level prediction. The confirmatory design now requires the *within-customer* improvement specifically to be positive before crediting any maturity-adds-value claim (§6).

**Two successive "expected uplift" simulations for the intervention-timing question were mathematically incapable of answering the question they were built for.** An expected-uplift formula swept across intervention-effect assumptions produced an "optimal day" result that was structurally invariant to the swept parameters — a mathematical artifact of how the formula's terms combined, not a substantive robustness finding. Both versions were discarded, and the reported result was narrowed to what can be measured without an intervention-effect assumption: precision/recall/lift of early-signal flagging against the realized outcome (§6).

**Sample-exclusion rules for the §6 extension were derived empirically, then made explicit and pre-specified.** Two accounts in the longitudinal sample were found, via four-signal profiling (all-time scale, registration-burst pattern, template/naming signal, real spend), to be test/QA setups rather than real advertisers, and were excluded via a pre-specified, logged rule rather than an ad hoc one.

**The largest customer's influence on the §6 extension was checked, not assumed away.** One customer contributes roughly a third of the longitudinal sample. Four-signal profiling classified this customer as a genuine large advertiser rather than a bulk/template account, so it was not excluded — instead, a leave-one-out sensitivity check on this customer was made a required (not optional) component of every reported result in §6.

---

### Appendix A — Results summary (canonical statistics table)

*Full version: [`docs/RESULTS_SUMMARY.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/docs).*

**H1a/b/c: full-mediation test (size → spend → outcome).** Customer-level mediation model, `bid_amount` as the cost-independent primary outcome (n = 263 customers); CPC-based estimates retained for comparison but treated as directionally informative only.

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a (a-path): size → total spend | +0.537 (p < .001) | +0.537 (p < .001) |
| H1b (b-path): spend → outcome \| size | +1.277 (p < .001) | +0.150 (p = .032) |
| H1c (c′-path): size → outcome \| spend (direct) | -0.253 (p = .062) | +0.037 (p = .634) |
| Indirect effect (a × b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | < .001 | < .001 |

**Verdict: H1c not rejected (null supported); H1a and H1b both confirmed.** Full mediation — the direct effect of size, net of spend, is statistically indistinguishable from zero on the primary (cost-independent) outcome, while both mediation legs are individually significant. Backed by 8 independent robustness methods.

**H2: boundary condition (campaign_type heterogeneity).**

| Product type | n (rows) | n (customers) | c' (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | -0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test (size × product-type)** | | | | **.023** |

**Verdict: H2 rejected — H1c's null is not perfectly homogeneous** across ad-product categories, though no individual stratum shows a significant size effect on its own.

**§6-Maturity — does account maturity predict initial growth slope?** Primary method: customer-level aggregate OLS (HC3 robust SE); final arbiter: cluster (customer-label) permutation test.

| statistic | value |
|---|---|
| n (customers) | 29 |
| n (ad groups, informational) | 204 |
| OLS beta (raw scale) | 8.34 |
| OLS HC3 p-value | .576 |
| Bootstrap 95% CI (raw scale) | [-15.84, 43.08] |
| Cluster permutation p-value | .663 |
| Spearman rho | -.02 (p = .92) |
| Leave-one-out (largest customer excluded) permutation p-value | .702 (sign unchanged) |
| Winsorized (10%) OLS beta / p | 1.48 / .841 |
| Rank-rank OLS beta / p | -.02 / .924 |
| Standardized effect size (beta) | .085 |
| Pre-registered large-effect detection threshold | .50 |
| Observed effect as % of detection threshold | 16.9% |

**§6-EarlySignal / §6-MaturityAdd — early operating signals vs. account maturity as predictors of near-term growth.**

| early/later window (days) | n (ad groups) | Own-signal within-customer LOCO ρ | +Maturity within-customer LOCO ρ | within-customer improvement | repeated-split Wilcoxon p |
|---|---|---|---|---|---|
| 14 / 14 | 204 | 0.467 | 0.487 | +0.019 | .038 (worse on repeated-split ρ) |
| 30 / 30 | 184 | 0.275 | 0.257 | -0.018 | .119 |
| 30 / 60 | 179 | 0.060 | 0.061 | +0.001 | .019 (worse on repeated-split ρ) |

**§6-Flagging — at what point should a low-growth ad group be flagged?**

| decision cutoff (days) | out-of-fold predictive ρ (95% bootstrap CI) | lift @ threshold=0.25 | lift @ threshold=0.40 |
|---|---|---|---|
| 7 | 0.304 [0.145, 0.445] | 0.83 | 1.27 |
| 14 | 0.265 [0.123, 0.404] | 1.33 | 1.23 |
| 21 | 0.334 [0.210, 0.459] | 1.42 | 1.36 |

**Combined takeaway.** The cross-sectional finding (H1c: size has no direct effect once spend is controlled) is confirmed with high power and replicated across eight methods, with a precisely characterized exception (H2: not perfectly homogeneous by product type). The longitudinal extension (§6) is directionally consistent — account maturity likewise shows no detectable direct association with a new ad group's growth, and an ad group's own early signal is the more informative predictor — but its central results do not reach formal TOST equivalence, so §6 is reported as supportive rather than independently conclusive. The practical implication is the same throughout: account size (and, provisionally, tenure) should not be used as a proxy for how a given advertiser or ad group will perform; what the unit itself does — spend, or its own early activity — is the more informative, and more actionable, signal.

---

### Appendix B — Data availability, reproducibility, and repository structure

- **Data availability & license.** The underlying panel data (ad-group dimension table, daily/hourly performance logs) are **proprietary and are not included in this repository.** They were processed and provided by a Korean ad-tech data and analytics provider under a research data-sharing agreement. Researchers interested in replication should contact the data provider directly to request access to an equivalent extract — see [`data/README.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main) for the expected schema. All code is runnable end-to-end against any dataset matching the documented schema. Code is released under the MIT License; this license covers the analysis code only, not the data.
- **Reproduction procedure (summary).** (1) Diagnostic pipeline → (2) Confirmatory tests (`src/analysis/`) → (3) Earlier-generation pipeline (variance decomposition, fairness battery, churn appendix) → (4) Supplementary robustness scripts (`run_supplementary_robustness.sh`, see [`supplementary_robustness/`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness)) → (5) Regeneration of nine figures (`figures/make_figure*.py`). Every step prints its own diagnostics and writes a JSON/CSV artifact; nothing is silently overwritten, and every script can be re-run independently as long as its upstream artifact exists.
- **Repository structure.** `config/` (paths, thresholds, sample-definition rules), `data/` (schema documentation, no data files committed), `src/utils/`, `src/coldstart_v5/` (diagnostic pipeline), `src/pipeline_v4/` (earlier-generation pipeline), `src/analysis/` (confirmatory tests), [`supplementary_robustness/`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness) (independently runnable robustness analyses, each mapped to a specific section above — `01_alternative_outcome_mediation.md`, `02_boundary_conditions.md`, `03_equivalence_and_sensitivity_notes.md`, `04_design_artifact_future_work.md`), `figures/` (9 figure-generation scripts and PNGs), plus [`docs/`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/docs) (`METHODOLOGY_NOTES.md` = §12.2 above; `RESULTS_SUMMARY.md` = Appendix A above).

---

### Appendix C — Methodological principles applied throughout

1. **No result is trusted from a single method.** Every confirmatory test is checked against at least two independent inferential approaches (e.g., parametric OLS + distribution-free permutation test; repeated split-sample validation + Leave-One-Customer-Out CV). Where they disagree, the more conservative, assumption-light method is treated as authoritative (§12.2).
2. **Every cutoff or date threshold is derived from the data at run time**, never hard-coded, so a re-extract of the underlying panel cannot silently invalidate downstream thresholds.
3. **Information leakage is checked, not assumed away.** All train/test splits are customer-grouped, and every repeated-split loop verifies (and logs) that no customer appears in both partitions of any single split.
4. **Sample-exclusion rules are pre-specified and logged**, not applied ad hoc (§12.2).
5. **Null results are reported with the same rigor as positive ones — and are not conflated with confirmed nulls unless a formal equivalence test says so.** Every non-significant central result is accompanied by (a) a pre-registered power simulation establishing what effect sizes the sample could and could not have detected, and (b), where central to the argument, a TOST equivalence test establishing whether the absence of an effect can be formally bounded (Figure 9).
6. **A single quantitative point estimate is never taken at face value when a structural artifact could inflate it.** Where an outcome construction shares a mechanical term with a predictor (§4.4), the mechanical component is explicitly isolated and the conclusion is re-anchored on an artifact-free alternative outcome (Figure 7).
7. **Sensitivity statistics are checked for numerical stability before being reported as evidence.** A large-looking robustness statistic (Oster's delta) computed in a numerically unstable regime is reported transparently but is not used to support a robustness claim (full table in [`supplementary_robustness/03_equivalence_and_sensitivity_notes.md`](https://github.com/LEEYJ1021/ad-coldstart-analysis/tree/main/supplementary_robustness)).
8. **Every hypothesis or research question is assigned a permanent ID before its results are reported** (§2.3), so a claim, a figure, and a statistics table can always be traced back to the same, unambiguous test.
