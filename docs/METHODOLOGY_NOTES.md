# Methodology Notes

This document is a narrative log of every point in the diagnostic pipeline
(`src/coldstart_v5/`, Steps A-M) where an initial modeling choice was found
to be structurally unreliable and replaced with a more defensible
alternative, and why. It is treated as part of the project's contribution,
not as a section to be edited out once the final design was settled -- the
reasoning here is what makes the confirmatory results in `src/analysis/`
trustworthy rather than merely reported.

Each entry follows the same shape: **what we assumed**, **how the
diagnostic contradicted it**, and **what changed as a result**.

---

## 1. "Cold start" was assumed to mean new-advertiser onboarding

**Assumed:** the project's original framing treated a "cold-start" ad
group as the leading edge of a brand-new advertiser's account -- a first
campaign, unfolding inside the observation window.

**Contradicted by:** Step I (`step_i_account_maturity_distribution.py`),
cross-checked by Step H (`step_h_top_customer_profiling.py`). Under every
registration-date cutoff tested (0-90 days of prior account history),
essentially none of the trajectory-usable sample (0-1 of 222 ad groups)
reflected a genuinely new account; the median account behind a
"cold-start" ad group had `account_age_days` of roughly 7.8 years (a
lower bound, per `data/README.md`'s snapshot caveat). Step J
(`step_j_regtm_artifact_check.py`) ruled out a snapshot/migration date
artifact as the explanation.

**Changed:** the project was reframed around **item-level cold start**: a
new ad group inside an already-established account -- closer to "item
cold-start" than "user cold-start" in the recommender-systems literature.
Account maturity became the key covariate under test in RQ1/RQ2, not a
stratification variable for sample selection.

## 2. Discrete latent-class growth models (GBTM) were the planned RQ1 method

**Assumed:** growth trajectories would be summarized with a
Group-Based Trajectory Model, and RQ1 would ask "how many growth
classes exist, and does maturity predict class membership?"

**Contradicted by:** Step E (`step_e_class_count_identifiability_sim.py`),
a BIC-based class-count recovery simulation at the achievable sample size
(n=222). Recovery probability was ~9% at k=2 true classes and ~0% at
k=3/4 -- the sample cannot reliably tell two classes apart, let alone
three or four, independent of any censoring or clustering issue.

**Changed:** GBTM was dropped from the confirmatory design entirely. RQ1
was rewritten around a continuous growth-curve quantity (an ad group's
initial 30-day cost slope) rather than a discrete class label, avoiding
the class-count identification problem altogether.

## 3. Apparent right-censoring turned out to be a follow-up-window artifact, then something else

**Assumed:** the 83.8% "censored" rate found in Step C
(`step_c_right_censoring_flags.py`) meant many trajectories were cut
short by the observation window ending too soon after registration.

**Contradicted by:** Step F (`step_f_registration_cutoff_sensitivity.py`):
requiring 30 vs. 120 days of guaranteed post-registration follow-up barely
moved the censored rate (83.6% -> 83.2%). If insufficient follow-up time
were the cause, a stricter cutoff should have reduced it sharply. Step G
(`step_g_fixed_window_coverage.py`) then showed the real story: mean
observed-day coverage within fixed post-registration windows was only
70-74%, not the near-100% a genuinely continuously-run ad group would
show -- and unlike the Step F cutoff sweep, this doesn't move with
cutoff, because it's measuring something different (data gaps, not
trajectory truncation).

**Changed:** "censoring" was reinterpreted as ad groups mostly **not
self-terminating** (activity persists to observation end because the ad
group is still running, not because its trajectory was cut off) combined
with **genuine intermittency** (on/off cycling, budget exhaustion,
approval delay) inside the active window. The confirmatory growth-slope
definition (`src/analysis/rq1_growth_curve_test.py`) uses fixed-window
linear trend fitting on zero-filled daily series rather than a
survival/censoring framework, which sidesteps the mismatch.

## 4. A customer random-intercept mixed model (MixedLM) was the planned RQ1 estimator

**Assumed:** growth slopes nested within customers would be modeled with
`statsmodels` MixedLM, `slope ~ maturity`, `groups=customer_id`.

**Contradicted by:** Step K (`step_k_power_simulation.py`). Because
`maturity` varies only at the customer level, it competes directly with
the customer random intercept for the same layer of variation, and the
model is structurally non-identified against it: 100% convergence-failure
rate (singular random-effects covariance / boundary-of-parameter-space
warnings) across every simulation replication, at every tested effect
size -- not merely an occasional convergence issue.

**Changed:** MixedLM was dropped as unusable for this design (not even
kept as a reference point-estimate). The customer-level aggregate
regression (average an ad group's growth slope up to its customer, then
regress the customer-level mean on customer-level maturity, n = customer
count) became the primary inferential model
(`src/analysis/rq1_growth_curve_test.py`), with a cluster (customer-label)
permutation test as the final arbiter whenever it and OLS disagree --
because 29-32 clusters is below the usual comfort threshold (40-50+) for
trusting asymptotic cluster-robust standard errors alone.

## 5. A pooled Leave-One-Customer-Out (LOCO) improvement was initially read as RQ2 support for H2b

**Assumed:** during RQ2 design (`step_l_rq2_feature_engineering.py`), a
positive pooled LOCO rho improvement when adding account maturity to the
base feature set was read as evidence that maturity adds ad-group-level
predictive value.

**Contradicted by:** the within/between-customer decomposition
(`loco_within_between_eval` in `step_l_rq2_feature_engineering.py`).
Splitting the pooled LOCO rho into a between-customer component (customer
mean-level agreement) and a within-customer component (relative ranking
of ad groups belonging to the same customer) showed that, at every tested
window pair, the pooled improvement was concentrated almost entirely in
the between-customer term while the within-customer term showed little
or no improvement (in one window pair, +0.388 between vs. +0.001 within).
A pooled metric that improves because it re-derives the RQ1 (customer-
level) signal is not evidence of genuine ad-group-level predictive gain.

**Changed:** the confirmatory RQ2 design
(`src/analysis/rq2_prediction_validation.py`) requires the
within-customer LOCO improvement to be positive before crediting H2b,
regardless of the pooled or between-customer numbers -- see that module's
docstring for the exact rule.

## 6. Two successive RQ3 "expected uplift" simulations were mathematically incapable of answering the question they were built for

**Assumed:** an expected-uplift formula (`n_true_positive * efficacy *
delta`) swept across intervention-effect assumptions (`delta`, `efficacy`)
would reveal which decision cutoff (7/14/21 days) is optimal, and whether
that ranking is robust to the effect-size assumption.

**Contradicted by:** in the first version, `delta` and `efficacy` entered
the formula as constants multiplying every (cutoff, threshold) cell
identically, so the argmax over cutoffs could never change regardless of
the assumed values -- the "100% stability across 9 scenarios" result this
produced was a mathematical artifact of the formula's structure, not a
substantive robustness finding. A second version made `delta` a function
of the cutoff's remaining follow-up time (`delta_per_day * remaining_days`)
to build in a genuine cutoff/effect-size trade-off -- but `delta_per_day`
and `efficacy` still multiplied every cell identically for a *given*
cutoff, so the ranking was again structurally fixed (this time by
`remaining_days` alone) rather than by the swept parameters.

**Changed:** RQ3's reported result was narrowed to what can be measured
without an intervention-effect assumption: precision/recall/lift of
early-signal flagging against the *realized* low-growth outcome, which
requires no assumption about what an intervention would do
(`step_m_intervention_timing_simulation.py`, Step M3). The expected-uplift
tables (Step M4/M5) are retained only as explicitly labeled,
non-causal what-if illustrations, never as the basis for an "optimal
day" claim. Bootstrapped confidence intervals on the precision/recall
metric (Step M6-3) further showed the 7/14/21-day cutoffs' predictive
rho values are not statistically distinguishable from one another, which
is reported as the actual (appropriately modest) RQ3 finding: early
intervention judgment appears viable within the first three weeks,
without a defensible single optimal day.

## 7. Sample-exclusion rules were derived empirically, then made explicit

**Assumed initially:** none -- test/template accounts were not
anticipated as a distinct category.

**Found:** Step H (`step_h_top_customer_profiling.py`) profiled the top-10
customers driving the Step D clustering concentration using four
independent signals (all-time scale, registration-burst pattern,
template/naming-pattern signal, and real spend) and found two accounts
with near-zero total spend and heavy template signal (single
registration burst, zero bid-amount variance) -- operationally
indistinguishable from test/QA setups rather than real advertising
activity.

**Changed:** `sample_definition.known_test_account_ids` in
`config/config.yaml` now explicitly excludes these two accounts from
every confirmatory analysis, alongside the general rule
(`test_account_exclusion.min_total_cost`,
`test_account_exclusion.max_zero_spend_share`) that produced them -- so
the exclusion is pre-specified and logged, not applied ad hoc per
analysis.

## 8. The largest customer's influence was checked, not assumed away

**Found:** Step D showed one customer contributing 32.9% of the
trajectory-usable sample. Step H's four-signal profiling classified this
customer as a genuine large advertiser (all-time scale in the 100th
percentile, meaningful and varied spend, campaigns spread across the
full observation window) rather than a bulk-generated template account,
so it was not excluded.

**Changed:** because exclusion wasn't warranted, a leave-one-out
sensitivity check on this customer was made a **required**, not optional,
component of the RQ1 confirmatory test
(`src/analysis/rq1_growth_curve_test.py`) -- every reported RQ1 result is
accompanied by the same test re-run with this customer removed, and the
verdict rule requires both runs to agree in sign before H1 is credited.
