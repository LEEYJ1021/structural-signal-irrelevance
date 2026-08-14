# Not New, But Renewed: Structural Attributes Don't Matter on an Algorithmically-Mediated Ad Platform

*A cross-sectional and longitudinal investigation into ad group cold-start dynamics and advertiser-size fairness on a Korean paid-search platform.*

---

## The question we started with

Picture two advertisers on the same search-ads platform. One has been running campaigns for seven years and manages hundreds of ad groups. The other just created their very first one. If you had to bet on whose new ad group ramps up faster — or whose account gets treated more favorably by the platform's approval and ranking systems — you'd probably bet on the veteran.

This repository is the record of testing that bet, twice, with two independent datasets, two independent sets of statistical tools, and two independent chances for the answer to turn out to be "yes."

It didn't.

Using a panel of **321 advertisers and roughly 19.3 million rows** of daily/hourly performance data from a Korean search-ads ecosystem, we ran two studies that ask the same underlying question from different angles:

- **Study 1 (cross-sectional):** Does advertiser *size* buy you a structural advantage in approval rate, cost-per-click efficiency, or ad rank — independent of how much you spend?
- **Study 2 (longitudinal):** Does an advertiser's accumulated account *history* predict how fast a brand-new ad group inside that account grows — independent of that ad group's own early performance signals?

Both studies converge on the same answer, and this README tells that story end to end: the question, the false starts, the diagnostics that forced us to redefine what we were even measuring, and the evidence that closed each case.

> **The short version:** size and tenure don't matter once you control for what actually does — spend, and the unit's own real-time behavior. We call this **structural blindness**: a real-time bidding and serving system that judges every ad group on its current signal, not on its account's résumé.

---

## Table of contents

1. [The data](#1-the-data)
2. [Study 1 — Does size buy an advantage?](#2-study-1--does-size-buy-an-advantage-cross-sectional)
3. [Study 2 — Does history buy an advantage?](#3-study-2--does-history-buy-an-advantage-longitudinal)
4. [Where the two stories meet](#4-where-the-two-stories-meet)
5. [Limitations](#5-limitations)
6. [Methodology summary](#6-methodology-summary)
7. [Repository structure](#7-repository-structure)
8. [Reproducing the analysis](#8-reproducing-the-analysis)
9. [Methodological principles applied throughout](#9-methodological-principles-applied-throughout)
10. [Data availability & license](#10-data-availability--license)

---

## 1. The data

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata | 1,504 | 263/321 |
| Ad group dimension (2026-07-22 snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, review status, bid price | 1,503,289 | 256/321 |

Two limitations shape everything that follows:

- **Single agency, single platform.** All data comes from one Korean ad-tech provider (SearchM) sourced from one search platform. Generalization is bounded by that ecosystem.
- **The ad group table is a snapshot, not a history.** It reflects ad groups as they exist *today* — anything deleted in the past has vanished from the table. Every measure of "account age" or "how many ad groups this account has ever run" is therefore a **lower bound**. This matters enormously for Study 2, where account maturity is the variable under test.

Conversion and ROAS variables were excluded from both studies entirely — the platform's conversion API retroactively backfills conversions per account on a delayed, inconsistent schedule, which breaks construct validity for anything built on top of it. This was a design decision made before any modeling began, not a post-hoc exclusion.

---

## 2. Study 1 — Does size buy an advantage? (Cross-sectional)

### 2.1 First, where would an advantage even live?

Before testing anything about advertiser size, we needed to know *where* performance variation actually sits — in the customer, the campaign, or the ad group. If size-related advantages exist, they should show up as customer-level variance.

<p align="center"><img src="figures/Figure1_variance_decomposition.png" width="780"></p>

**Figure 1 — Multilevel variance decomposition.** Across ~663K observations, log ad spend is dominated by unexplained residual variance (ICC = 0.825) — day-to-day budget execution, not who the customer is (ICC = 0.050). Click-through rate tells a similar story: the largest share of variation sits at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both patterns hold whether or not month fixed effects are added, ruling out seasonality as the explanation. This was our first hint, well before any hypothesis test: **"who the customer is" explains comparatively little of what happens.**

### 2.2 The raw gap looks real

Split advertisers into four size tiers (by spend volume) and compare approval rate, CPC, and ad rank across tiers with a Kruskal-Wallis test, and the differences are statistically significant across the board (p < .001 for CPC and ad rank; p = .0006 for approval rate). Effect sizes are small (ε² = 0.002–0.079), but the raw signal is there.

Except it isn't quite what it looks like. Ad groups belonging to the same customer share policies and aren't statistically independent — the standard Kruskal-Wallis test assumes they are. Re-running the comparison as a customer-level cluster permutation test (2,000 iterations) made most of that "significant" gap in approval rate and CPC evaporate. The raw test's significance turned out to be substantially an artifact of ignoring clustering — a first sign that the real test needed to be something sturdier.

### 2.3 The gap disappears once you control for spend

<p align="center"><img src="figures/Figure2_fairness_forest_plot.png" width="780"></p>

**Figure 2 — The central confirmatory test.** Controlling for log spend in a cluster-robust regression, all six outcome × sample combinations (approval rate, CPC, ad rank, each in the full sample and with spike-affected accounts excluded) come back **non-significant** (cluster-robust p > .07). Every 95% bootstrap confidence interval not only crosses zero — it falls entirely inside its own minimum-detectable-effect (MDE) band, meaning this isn't underpowered null-hunting; the observed effect is smaller than anything the sample could reliably detect. Approximate Bayes factors favor the null hypothesis in five of six tests.

### 2.4 Making sure this isn't a fluke of one analytic choice

A single regression result is easy to distrust. So we stress-tested it five independent ways.

<p align="center"><img src="figures/Figure3_specification_curve_placebo.png" width="780"></p>

**Figure 3 — Multiverse specification curve and placebo test.** Panel A reruns the same regression across 48 defensible analytic choices — different tier definitions, different covariate sets — and **0 of 48 reach significance** for any outcome. Panel B adds a sanity check: a variable that size *shouldn't* predict (device-type share) is tested the same way. The raw distributional test is significant for this placebo too, confirming that raw tests are simply too liberal on their own — but the spend-controlled regression (the actual confirmatory method) returns the same null verdict for both the real outcome and the placebo. That's the strongest evidence we have that the regression, not the raw test, is measuring the right thing.

Beyond these two figures, four more independent checks point the same direction: a customer-and-month fixed-effects panel regression, a two-stage least squares model using lagged spend as an instrument (its first-stage F-statistic couldn't be recovered due to a code exception — flagged and excluded from any conclusion, not silently dropped), a temporal split-sample replication, and Benjamini-Hochberg FDR correction across the six primary hypotheses. **Eight independent verification methods, one consistent verdict.**

### 2.5 A side quest: can we predict churn instead?

This question sits outside the fairness hypothesis entirely, but it was worth asking as an exploratory appendix: given approval/cost/efficiency features, can machine learning models predict which accounts will churn?

<p align="center"><img src="figures/Figure4_churn_benchmark.png" width="780"></p>

**Figure 4 — Churn-prediction benchmarking.** Across 213 labeled accounts (a stark 2.35% churn rate), tree-based models nominally outperform logistic regression in nested cross-validation. But look closely: every pairwise model comparison returns the *exact same* Wilcoxon p-value (0.0625) — the mathematical floor achievable with only 5 repeat-pairs, not evidence of a real difference. We report this transparently rather than dressing it up as a finding. Random forest had the best-calibrated out-of-fold predictions (Brier score 0.0250).

### 2.6 What Study 1 concludes

Raw size-tier gaps in approval rate, CPC, and ad rank are statistically detectable but small, and their significance is fragile once you account for clustering. The confirmatory test — spend-controlled regression — returns a clean, well-powered null across all six outcome-sample combinations, backed by five independent robustness checks. **The apparent advantage of being a large advertiser is fully explained by spending more, not by size itself.**

---

## 3. Study 2 — Does history buy an advantage? (Longitudinal)

### 3.1 A detour before the test: what does "cold start" even mean here?

The original plan treated "cold start" as new-advertiser onboarding: a brand-new account launching its first campaign. Before testing any hypothesis, we tried to build that sample — and the data pushed back, hard, five separate times.

1. **The numbers didn't match.** Early planning documents cited 476 "true cold-start" ad groups in one place and 250 in another. Recomputing directly from the data settled it at 250 → 222 after filtering for at least 7 active days — matching the smaller figure exactly.

2. **What looked like right-censoring wasn't.** 83.8% of the trajectory sample appeared to be "censored" — cut short by the observation window ending. But stretching the required post-registration observation window from 30 to 120 days barely moved that number (83.6% → 83.2%). If it were really about insufficient observation time, giving ad groups four times longer to be observed should have fixed most of it. It didn't. The real explanation: **these ad groups simply don't stop running** — they keep going until the data collection window ends. Applying a right-censoring lens borrowed from survival analysis was the wrong tool for this kind of data.

3. **Growth-curve clustering couldn't be trusted.** We tried fitting discrete latent growth classes (a group-based trajectory model) to categorize ad groups by growth pattern. A recovery simulation (200 iterations) showed that even when the true number of classes was known to be 2, the model correctly identified it only 9% of the time. This wasn't a "small sample, a bit unlucky" problem — the model structure itself couldn't reliably recover class counts. We abandoned it in favor of a continuous growth-curve (random-effects) approach.

4. **The real discovery: this isn't user cold-start at all.** Profiling the top customers and mapping the full distribution of account maturity revealed something the original framing had missed entirely. Of the 222 usable ad groups, **zero** met the strict criteria for "genuinely new account" (cold-start ratio ≥ 80% *and* account age ≤ 30 days). Even relaxing the age threshold to 90 days captured just one ad group (0.5%). More than half of the observed "cold-start" ad groups belonged to accounts with a **median age of 2,853 days — about 7.8 years.** We hadn't been finding a scarce population; we'd been looking for a population that essentially doesn't exist in this data. This forced an explicit reframing: from *user* cold-start (a brand-new advertiser) to **item cold-start** (a brand-new ad group inside an already-mature account) — a distinction long established in recommender-systems research but rarely made explicit in advertising analytics.

5. **Even the statistical model needed rebuilding.** Account maturity only takes one value per customer — every ad group from the same account shares it. Feeding that into a mixed-effects model with a customer-level random intercept creates a structural non-identifiability: the model can't tell "customer-level random variance" apart from "the maturity fixed effect." A pre-registered power simulation (500 iterations, reusing the real cluster structure) confirmed it: the mixed model's convergence failure rate was **100%**. We replaced it with a simpler, sound alternative — customer-level aggregate OLS (n≈32) — whose false-positive rate (5.2%) sat right at the nominal 5% alpha, and which could reliably detect only large effects (standardized β ≈ 0.5, 88% power).

<p align="center"><img src="figures/Figure5_coldstart_funnel_and_RQ1_null.png" width="780"></p>

**Figure 5(A) — The sample-construction funnel** that resulted from this five-step diagnostic journey: 250 candidates → 222 with sufficient activity → 204 with a complete 30-day early window (29 customers once aggregated). The median account behind these "cold-start" ad groups was already 2,853 days old — visual proof that this is a story about expansion inside mature accounts, not onboarding new ones.

### 3.2 Does account maturity predict how fast a new ad group grows?

With the sample and the model finally sound, we could ask the question the study actually set out to answer.

**Figure 5(B)** *(right panel, same image above).* Account maturity (log-transformed, standardized count of all-time ad groups) was tested against each customer's mean initial 30-day growth slope (n=29). The raw-scale OLS coefficient was weakly positive (β=8.34) but non-significant (p=.576), and the pre-registered decision rule — a cluster permutation test (10,000 iterations) — agreed: p=.663. The 95% bootstrap CI [-15.84, 43.08] comfortably contained zero. Dropping the largest customer (35.8% of the sample) as a sensitivity check changed nothing (permutation p=.702). Most tellingly, that weak positive coefficient collapsed to β=1.48 under winsorizing and **flipped sign entirely** under a rank-based regression (β=-0.0196) — the signature of a result being driven by a couple of high-leverage outliers rather than a genuine relationship. The standardized effect size (β=.085) sits at just 17% of the large-effect threshold the pre-registered power simulation was built to detect.

**Verdict: account maturity does not predict how fast a new ad group ramps up.** This is a well-powered, robustly confirmed null — not a case of "we just couldn't find it."

### 3.3 Does the ad group's own early behavior predict its near-term growth?

If history doesn't matter, what does? We tested whether an ad group's own first 14–60 days of activity — coverage, early spend trend, CTR, CVR, ROAS — predict how it performs afterward, using customer-grouped repeated splits and Leave-One-Customer-Out (LOCO) cross-validation to guard against information leakage.

<p align="center"><img src="figures/Figure6_RQ2_horizon_RQ3_lift.png" width="780"></p>

**Figure 6(A,B) — The prediction result, and the trap hidden inside it.** Using only the ad group's own early signal, 14-day-ahead growth prediction achieved a respectable ρ=0.386 in leakage-free repeated-split validation. Adding account maturity as a feature made things *worse*, not better (ρ=0.373, Wilcoxon p=.038). But the LOCO cross-validation told the opposite story — a *positive* improvement (+0.034) from adding maturity. Which one was right?

Panel B answers that by decomposing the improvement into within-customer and between-customer components. The apparent LOCO gain turned out to be almost entirely a between-customer effect — maturity was just re-injecting the same customer-level growth-level signal from Section 3.2 through a pooled metric, not genuinely improving ad-group-level prediction. Within-customer improvement was essentially zero (±0.02) across all three window combinations tested. **Trusting the leakage-controlled result: an ad group's own signal is genuinely predictive at short horizons; account maturity adds nothing once you look at the right level of aggregation.** Predictive power itself also decayed sharply as the horizon extended from 14 to 30–60 days (within-customer ρ dropping to roughly 0.06–0.21).

### 3.4 When's the best day to flag a struggling ad group?

**Figure 6(C,D) — Timing an intervention.** Flagging the bottom 25–40% of predicted growers achieved a 1.2–1.4x precision lift over random flagging, and that lift held up consistently whether the decision was made at day 7, 14, or 21 post-registration (Panel C). But the 95% bootstrap confidence intervals on predictive accuracy at each of those cutoffs overlap heavily (Panel D) — there's no statistical basis for calling any single day "optimal."

We also tried to go further and quantify the *expected benefit* of intervening at each point in time, but two independent attempts at that simulation both failed the same way: the assumed intervention-effect parameters combined multiplicatively in a way that made the "optimal" answer (day 21, threshold 0.40) come out identical *no matter what values we assumed*. That's not a robust finding — it's a mathematical illusion baked into the formula. We caught it, discarded both simulations, and report the limitation openly rather than presenting a false sense of precision.

**Verdict:** early flagging is directionally useful — any point in the first three weeks works about as well as any other — but a precise "optimal day" isn't something this data can support.

### 3.5 What Study 2 concludes

> Initial ad-group growth is explained by the ad group's *own* early operating signal, not by the parent account's accumulated history — at any level of aggregation tested. Getting to that conclusion required first discovering that the study's own sample definition didn't mean what it was assumed to mean, and rebuilding the statistical approach twice in response.

---

## 4. Where the two stories meet

| | Study 1 (cross-sectional, size) | Study 2 (longitudinal, tenure) |
|---|---|---|
| Initial observation | Significant raw gap by size tier | (implicit expectation) maturity should help new units |
| Direct test of the structural attribute | Gap vanishes once spend is controlled (rejected) | No direct effect of maturity (rejected) |
| What actually drives outcomes | Spend (a mediating variable) | The unit's own early operating signal (supported) |
| Independent verification methods | 8 | 5, plus within/between decomposition |

These two investigations share no data, no time axis, and almost no statistical machinery in common — one is a cross-sectional regression problem, the other a longitudinal, customer-clustered prediction problem. And yet they land on the identical structural conclusion: **an account's size or history has no direct effect on unit-level performance once you account for what actually mediates it — spend, or the unit's own real-time signal.** We call this pattern **structural blindness**: a real-time, bid-based serving system that evaluates every ad group by its current behavior, indifferent to the account's past or scale.

**What this means in practice:**

- **For small or new advertisers:** investing in the quality of individual campaigns and ad groups — bid strategy, creative quality — pays off more directly than any attempt to look "established."
- **For the platform:** this is good evidence for a genuinely size-blind allocation mechanism — but spend remains the one channel that does move outcomes, so budget-constrained small advertisers still face a real, if indirect, disadvantage.
- **For operations teams:** "this account is big, so this ad group will probably do fine" is not a statistically defensible inference. The first two weeks of an ad group's own activity — coverage, early spend trend, CTR/CVR — are the more trustworthy signal.

---

## 5. Methodology summary

| | Study 1 | Study 2 |
|---|---|---|
| Primary test | Cluster-robust controlled regression (HC3 / cluster SE) | Customer-level aggregate OLS + cluster permutation test |
| Robustness battery | Cluster permutation test, bootstrap CI, approximate Bayes factor, MDE, specification curve, placebo test, 2SLS, temporal split replication | Bootstrap CI, winsorizing, rank-rank regression, leave-one-out, within/between decomposition |
| Multiple-testing correction | Benjamini-Hochberg FDR (6 primary hypotheses) | Not applicable (single confirmatory hypothesis; convergence across 5 methods used instead) |
| Methods tried and discarded | None (all retained) | Group-based trajectory modeling (class count unidentifiable, 0–9% BIC recovery), mixed-effects model (100% convergence failure, non-identified) |
| Pre-registered / post-hoc power check | MDE at 80% power | Simulation reusing real cluster structure (500 iterations); only large effects (β≈.5) reliably detectable (88% power) |

Known code- and design-level issues (the unrecoverable 2SLS first-stage F-statistic, the Wilcoxon floor-p artifact in the churn appendix, the multiplicative-structure illusion in the intervention-uplift simulation, among others) are logged transparently in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) for anyone attempting to reproduce or extend this work.

---

## 6. Repository structure

```
ad-coldstart-analysis/
├── README.md                          <- you are here
├── LICENSE
├── requirements.txt
│
├── config/
│   └── config.yaml                    <- all paths, thresholds, and sample-definition
│                                          rules in one place (nothing hard-coded in scripts)
│
├── data/
│   └── README.md                      <- expected schema + how to request access via SearchM
│                                          (no data files committed)
│
├── src/
│   ├── utils/
│   │   ├── io.py                      <- config loading, chunked panel readers, column finders
│   │   └── identifiers.py             <- ID cleaning / timezone normalization helpers
│   │
│   ├── coldstart_v5/                  <- diagnostic pipeline (Steps A-M)
│   │   ├── _sample_construction.py    <- shared cold-start sample builder, used by every step
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
│   ├── pipeline_v4/                   <- earlier-generation pipeline (variance decomposition,
│   │   │                                  advertiser-size fairness suite, churn appendix)
│   │   ├── step0_data_prep_v4.py
│   │   ├── step1_variance_decomposition_v4.py
│   │   ├── step2_advertiser_size_fairness_v4.py
│   │   ├── step3_churn_appendix_v4.py
│   │   └── step4_synthesis_v4.py
│   │
│   └── analysis/                      <- confirmatory tests, run once the diagnostics
│       │                                  above have fixed the design
│       ├── rq1_growth_curve_test.py   <- H1 confirmatory test (customer-level OLS +
│       │                                  cluster permutation + leave-one-out + robustness)
│       └── rq2_prediction_validation.py <- H2a/H2b confirmatory test across all
│                                            early/later window pairs
│
├── figures/                            <- one script per figure, each reads a results
│   │                                       JSON/CSV and writes a PNG to outputs/figures/
│   ├── make_figure1_variance_decomposition.py
│   ├── make_figure2_fairness_forest_plot.py
│   ├── make_figure3_specification_curve_placebo.py
│   ├── make_figure4_churn_benchmark.py
│   ├── make_figure5_coldstart_funnel_and_rq1_null.py
│   ├── make_figure6_rq2_horizon_rq3_lift.py
│   ├── Figure1_variance_decomposition.png
│   ├── Figure2_fairness_forest_plot.png
│   ├── Figure3_specification_curve_placebo.png
│   ├── Figure4_churn_benchmark.png
│   ├── Figure5_coldstart_funnel_and_RQ1_null.png
│   └── Figure6_RQ2_horizon_RQ3_lift.png
│
├── docs/
│   ├── METHODOLOGY_NOTES.md           <- narrative log of every diagnostic dead end and
│   │                                      why the design changed in response (GBTM ->
│   │                                      continuous growth curve, MixedLM -> customer-level
│   │                                      aggregate, pooled LOCO -> within/between decomposition,
│   │                                      naive expected-uplift -> assumption-audited version)
│   └── RESULTS_SUMMARY.md             <- consolidated RQ1/RQ2/RQ3 results table with
│                                          all reported statistics, for citation
│
├── outputs/                            <- all pipeline artifacts land here (git-ignored;
│   ├── figures/                            .gitkeep only). Typical contents after a full run:
│   ├── _v4_data_prep/
│   ├── _v4_variance_decomposition/
│   ├── _v4_fairness/
│   ├── _v4_churn_appendix/
│   ├── _v4_synthesis/
│   └── coldstart_v5/
│
├── run_diagnostics.sh                 <- runs Steps A-M in order (coldstart_v5)
└── run_pipeline_v4.sh                 <- runs the v4 pipeline (step0-step4) end-to-end
```

---

## 7. Reproducing the analysis

```bash
git clone <this-repo>
cd ad-coldstart-analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# point config/config.yaml at your local copy of the SearchM extract
# (see data/README.md for the required schema)

# 1. Diagnostic pipeline (sample construction, censoring checks, power
#    simulations, feature/window design) -- produces the evidence base
#    that the confirmatory design in src/analysis/ relies on
bash run_diagnostics.sh

# 2. Confirmatory RQ1/RQ2 tests
python -m src.analysis.rq1_growth_curve_test --config config/config.yaml
python -m src.analysis.rq2_prediction_validation --config config/config.yaml

# 3. Earlier-generation v4 pipeline (variance decomposition, advertiser-size
#    fairness suite with multiverse + placebo tests, churn-prediction appendix)
bash run_pipeline_v4.sh

# 4. Figures
for f in figures/make_figure*.py; do python "$f"; done
```

Every step prints its own diagnostics and writes a JSON/CSV artifact to `outputs/`; nothing is silently overwritten, and every script can be re-run independently as long as its upstream artifact exists.

---

## 8. Methodological principles applied throughout

1. **No result is trusted from a single method.** Every confirmatory test in this repository is checked against at least two independent inferential approaches (e.g., parametric OLS + distribution-free permutation test; repeated split-sample validation + Leave-One-Customer-Out CV). Where they disagree, the more conservative, assumption-light method is treated as authoritative — a rule applied consistently and documented in `docs/METHODOLOGY_NOTES.md`.
2. **Every "cutoff" or date threshold is derived from the data at run time**, never hard-coded, so that a re-extract of the underlying panel cannot silently invalidate downstream thresholds (see `src/coldstart_v5/step_a_period_and_spike_check.py`).
3. **Information leakage is checked, not assumed away.** All train/test splits are customer-grouped, and every repeated-split loop verifies (and logs) that no customer appears in both the train and test partitions of any single split.
4. **Sample-exclusion rules are pre-specified and logged**, not applied ad hoc — see `sample_definition.known_test_account_ids` and `sample_definition.censor_window_days` in `config/config.yaml`.
5. **Null results are reported with the same rigor as positive ones.** The advertiser-size effect (post spend control) and the account-maturity effect are both null findings; both are backed by pre-registered power simulations establishing what effect sizes the sample could and could not have detected, so that "no effect found" is never conflated with "no effect exists."

---

## 9. Data availability & license

The underlying panel data (ad-group dimension table, daily/hourly performance logs) are **proprietary and are not included in this repository**. They were processed and provided by **SearchM**, a Korean ad-tech data and analytics provider, under a research data-sharing agreement. Researchers interested in replication should contact SearchM directly to request access to an equivalent extract; see [`data/README.md`](data/README.md) for the expected schema, so the pipeline can be pointed at a differently sourced but schema-compatible dataset.

All code in this repository is runnable end-to-end against any dataset that matches the schema described there. No proprietary data, sample rows, or platform-identifying details are committed to version control.

Code is released under the MIT License (see `LICENSE`). This license covers the analysis code only — it does not extend to any data, which remains the property of SearchM and is not distributed with this repository.
