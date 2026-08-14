# Ad Group Cold-Start: Growth, Prediction, and Intervention-Timing Analysis

This repository contains the full analysis pipeline for an independent research
project studying **cold-start dynamics in paid-search ad groups** on a Korean
digital advertising platform. The project asks three questions:

- **RQ1** — Does an advertiser's account maturity (accumulated operating
  history) predict the initial growth trajectory of a newly created ad group?
- **RQ2** — Can early operating signals (first 14–30 days) predict later
  performance, and does account maturity add predictive value on top of them?
- **RQ3** — At what point after registration is it most efficient to flag a
  low-growth ad group for intervention?

A companion cross-sectional study is also included in the pipeline: whether
**advertiser size** confers a structural advantage in approval rate,
cost-per-click efficiency, or ad rank, independent of spend.

The repository is organized to make the **entire analytical process
reproducible and auditable** — including the diagnostic dead ends, the
pre-registered power simulations, and the points where an initial modeling
choice (discrete latent-class growth models, customer random-intercept mixed
models, naive pooled cross-validation) was found to be structurally
unreliable and replaced with a more defensible alternative. That process is
documented in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md) and is
treated as part of the project's contribution, not as a section to be edited
out.

## Project framing

The original design assumed "cold start" would resemble *new-advertiser
onboarding*: a brand-new account, its first campaign, and a full growth
lifecycle unfolding inside the observation window. Diagnostic work early in
the pipeline (Steps F–J) showed this framing does not match the data — under
any reasonable registration-date cutoff, essentially none of the
trajectory-usable sample (0–1 of 222 ad groups) reflected a genuinely new
account. The median account behind a "cold-start" ad group had been active
for roughly 7.8 years.

The project was reframed around **item-level cold start**: a new ad group
created inside an *already-established* account. This distinction — closer
to "item cold-start" than "user cold-start" in the recommender-systems
literature — becomes the project's organizing idea, and account maturity
(rather than "is this a new user") becomes the key covariate under test in
RQ1/RQ2, rather than a stratification variable for sample selection.

## Headline results

| RQ | Hypothesis | Method (primary) | Result |
|----|------------|-------------------|--------|
| RQ1 | Account maturity predicts initial 30-day growth slope | Customer-level aggregate OLS (n=29) + cluster permutation test, leave-one-out sensitivity | **Not supported.** β=8.34 (raw), permutation p=.663; standardized effect (β≈.085) is ~17% of the pre-registered large-effect detection threshold (.50). Winsorized/rank-based checks confirm the weak raw-scale coefficient was a high-leverage-point artifact, not a genuine relationship. |
| RQ2a | Early operating signals (coverage, spend slope, CTR/CVR/ROAS) predict later growth | Ridge regression, repeated customer-grouped train/test splits + Leave-One-Customer-Out CV | **Supported at short horizons.** 14-day-ahead prediction: within-customer ρ ≈ 0.39–0.47. Predictive signal decays sharply at 30/60-day horizons (within-customer ρ ≈ 0.06). |
| RQ2b | Adding account maturity improves ad-group-level prediction | Same design, paired base vs. base+maturity models | **Not supported.** Pooled LOCO improvements were traced (via within/between-customer decomposition) to RQ1-level signal leaking into a pooled metric, not genuine ad-group-level gains. Repeated-split Wilcoxon tests were non-significant or significantly *negative*. |
| RQ3 | Optimal decision-day for flagging low-growth ad groups | Precision/recall/lift of early-signal flagging across decision cutoffs (7/14/21 days); *assumption-based* expected-uplift simulation kept separate from the measured result | **Directional, not precise.** Flagging achieves 1.2–1.5x lift over random across all tested cutoffs; 95% bootstrap CIs on predictive ρ overlap across cutoffs 7/14/21, so no single "optimal" day is statistically defensible. Two independent expected-uplift simulations were found to be mathematically incapable of producing a different ranking regardless of assumed intervention effect size — this is reported as a designed-in limitation, not a finding. |

**Combined takeaway:** initial ad-group growth is explained by the ad
group's *own* early operating signal, not by the parent account's
accumulated history — at any level of aggregation tested. A parallel
cross-sectional analysis of advertiser size reaches the same structural
conclusion: raw size-tier gaps in approval rate/CPC/ad rank are statistically
detectable but disappear once spend is controlled for, converging with the
RQ1/RQ2 findings above on a single theme — **structural attributes (size,
tenure) are absorbed by spend or by the unit's own real-time signal, with no
residual direct effect.**

## Key figures

Six figures summarize the full evidentiary chain, from the underlying data
structure through to the final, robustness-checked conclusions. Each script
in `figures/` reads a results JSON/CSV artifact and regenerates its
corresponding PNG — figures are never hand-edited.

<p align="center"><img src="figures/Figure1_variance_decomposition.png" width="800"></p>

**Figure 1 — Multilevel variance decomposition of advertising performance.**
Before testing any hypothesis about advertiser size, this figure establishes
*where* size-related variation could plausibly live. Intraclass correlations
(ICC) for log ad spend and click-through rate are decomposed across the
ad-group / campaign / customer / residual hierarchy (n≈663K observations),
with 30-iteration cluster bootstrap ranges and a month-fixed-effects check to
rule out seasonality artifacts. Spend variation is dominated by
unexplained residual (ICC=0.825) rather than the customer level (ICC=0.050);
CTR variation is concentrated at the ad-group level (ICC=0.301), not the
customer level (ICC=0.200). This is the diagnostic backdrop for the paper's
central claim: "who the customer is" explains comparatively little,
foreshadowing the null result on advertiser-size effects in Figure 2.

<p align="center"><img src="figures/Figure2_fairness_forest_plot.png" width="800"></p>

**Figure 2 — Advertiser-size effect on approval, cost efficiency, and ad
rank, controlling for spend.** This is the study's central confirmatory
test. Cluster-robust point estimates and 95% bootstrap CIs are shown for the
size-tier effect on approval rate, log(CPC), and mean ad rank, in the full
sample and with spike-affected accounts excluded. Every CI both crosses zero
and falls inside its own minimum-detectable-effect (MDE) band, and
approximate Bayes factors favor the null in 5 of 6 tests. In short: raw
size-tier gaps exist, but once spend is controlled for, they vanish.

<p align="center"><img src="figures/Figure3_specification_curve_placebo.png" width="800"></p>

**Figure 3 — Multiverse specification curve and placebo test.** Panel A
runs the size-effect regression across 48 reasonable analytic choices (tier
definition × covariate set) — **0 of 48 are significant at α=.05** for any
outcome. Panel B adds a placebo check: a distributional (Kruskal–Wallis)
test is significant for both the real outcome and an outcome size *shouldn't*
predict (device-type share), showing that raw distributional tests are too
liberal on their own — but the spend-controlled regression used for the
confirmatory test (matching Figure 2) is equally null for both the real and
placebo outcome. This figure is the robustness backbone behind the "not
supported" verdict in Figure 2.

<p align="center"><img src="figures/Figure4_churn_benchmark.png" width="800"></p>

**Figure 4 — Churn-prediction benchmarking (exploratory appendix).** A
secondary, non-confirmatory analysis comparing logistic regression, random
forest, and gradient boosting on account-level churn (2.35% base rate, 213
labeled accounts), using nested cross-validation to correct for optimistic
hyperparameter-tuning bias. All pairwise model comparisons return the same
Wilcoxon p-value (0.0625) — the minimum value obtainable with only 5
repeat-pairs — which the caption flags as a statistical artifact of small
sample size, not evidence of model superiority. Out-of-fold Brier scores show
random forest is best-calibrated (0.0250).

<p align="center"><img src="figures/Figure5_coldstart_funnel_and_RQ1_null.png" width="800"></p>

**Figure 5 — Cold-start sample construction and the RQ1 confirmatory
test.** Panel A is the sample-construction funnel that documents the
project's central reframing: of 250 candidate "cold-start" ad groups
(2025-08-23 to 2026-07-21), 204 survive to a complete 30-day early window —
but the median account behind them is **2,853 days old (~7.8 years)**,
confirming that this is item cold-start, not user cold-start. Panel B is the
RQ1 test itself: account maturity (x-axis) plotted against each customer's
mean initial 30-day growth slope (y-axis, n=29). The flat OLS fit
(permutation p=.663, Spearman ρ=-.020, p=.92) shows no relationship —
maturity does not predict how fast a new ad group ramps up.

<p align="center"><img src="figures/Figure6_RQ2_horizon_RQ3_lift.png" width="800"></p>

**Figure 6 — Cold-start early-signal prediction (RQ2) and
intervention-timing simulation (RQ3).** Panel A shows pooled leave-one-customer-out
prediction improving when account maturity is added — but Panel B decomposes
that gain into between-customer and within-customer components, revealing
the "improvement" is almost entirely between-customer (i.e., RQ1-level
signal leaking into a pooled metric), not a genuine ad-group-level gain.
Panels C and D turn to RQ3: a heatmap of flagging lift across decision
cutoffs (day 7/14/21) and thresholds shows a consistent 1.2–1.4x lift over
random, while the accompanying confidence-interval plot shows those
cutoffs' predictive ρ values overlap heavily — so no single cutoff can be
called statistically optimal.

## Data availability

The underlying panel data (ad-group dimension table, daily/hourly
performance logs) are **proprietary and are not included in this
repository**. They were processed and provided by **SearchM**, a Korean ad-
tech data and analytics provider, under a research data-sharing agreement.
Researchers interested in replication should contact SearchM directly to
request access to an equivalent extract; see [`data/README.md`](data/README.md)
for the expected schema, so that the pipeline can be pointed at a differently
sourced but schema-compatible dataset.

All code in this repository is runnable end-to-end against any dataset that
matches the schema described there. No proprietary data, sample rows, or
platform-identifying details are committed to version control.

## Repository structure

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

## Reproducing the analysis

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

Every step prints its own diagnostics and writes a JSON/CSV artifact to
`outputs/`; nothing is silently overwritten, and every script can be re-run
independently as long as its upstream artifact exists.

## Methodological principles applied throughout

1. **No result is trusted from a single method.** Every confirmatory test in
   this repository is checked against at least two independent inferential
   approaches (e.g., parametric OLS + distribution-free permutation test;
   repeated split-sample validation + Leave-One-Customer-Out CV). Where they
   disagree, the more conservative, assumption-light method is treated as
   authoritative — a rule applied consistently and documented in
   `docs/METHODOLOGY_NOTES.md`.
2. **Every "cutoff" or date threshold is derived from the data at run time**,
   never hard-coded, so that a re-extract of the underlying panel cannot
   silently invalidate downstream thresholds (see
   `src/coldstart_v5/step_a_period_and_spike_check.py`).
3. **Information leakage is checked, not assumed away.** All train/test
   splits are customer-grouped, and every repeated-split loop verifies (and
   logs) that no customer appears in both the train and test partitions of
   any single split.
4. **Sample-exclusion rules are pre-specified and logged**, not applied ad
   hoc — see `sample_definition.known_test_account_ids` and
   `sample_definition.censor_window_days` in `config/config.yaml`.
5. **Null results are reported with the same rigor as positive ones.** RQ1
   and RQ2b are both null findings; both are backed by pre-registered power
   simulations that establish what effect sizes the sample could and could
   not have detected, so that "no effect found" is not conflated with "no
   effect exists."

## License

Code is released under the MIT License (see `LICENSE`). This license covers
the analysis code only — it does not extend to any data, which remains the
property of SearchM and is not distributed with this repository.
