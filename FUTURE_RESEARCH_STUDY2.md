# Future Research: A Longitudinal Extension — Account Maturity & Cold-Start Growth

**Status: planned / future work, not part of the current manuscript.** This document consolidates
a second, longitudinal study that was originally developed alongside the cross-sectional
advertiser-size analysis reported in the main [`README.md`](README.md). That cross-sectional
study (advertiser size vs. algorithmic outcomes, n = 321 advertisers) is confirmatory,
well-powered, and stands on its own. This longitudinal companion (account maturity vs. a new ad
group's growth trajectory, n = 29 customers) was intended as a conceptual replication on an
independent sample and an independent time axis, testing the same underlying construct —
**structural signal irrelevance (SSI)**, defined in root README §2.5 — via a different structural
attribute (tenure instead of size) and a different legitimate mediator (an ad group's own early
operating signal instead of spend).

**Why it was descoped.** The confirmatory sample bottomed out at n = 29 customer-level clusters
after a defensible, fully-traced reduction path (§2 below). At that sample size the design was
well-powered only against a theoretically motivated *large* effect (β ≈ .50) and its formal TOST
equivalence tests did not reach equivalence at tighter margins. Five independent estimators
converged on a null, directionally consistent with the main study's pattern — but "directionally
consistent, underpowered for small effects, TOST-inconclusive" is a materially weaker evidentiary
statement than the main study's "8/8 methods null, high power, Bayes factors favor the null."
Rather than let this asymmetry dilute the confirmatory strength of the cross-sectional result, the
longitudinal analysis is reported here, in full, as a template and a starting point for a properly
powered follow-up study — not folded into the main manuscript's evidence base.

**What is preserved here.** Every statistic, script reference, figure, and methodological pivot
originally documented for this study is reproduced below without alteration, exactly as it was
computed. Nothing here is a new result; this is a relocation, not a re-analysis. Section headers
below intentionally mirror the structure the study had when it was part of the main repository,
so old cross-references still resolve to the right place.

---

## Table of contents

1. [Theoretical Extension — The Temporal Dimension](#1-theoretical-extension--the-temporal-dimension)
2. [Study Design — Cold-Start Reframing & Growth Trajectory](#2-study-design--cold-start-reframing--growth-trajectory)
3. [Statistical Power and Sample Adequacy at n = 29](#3-statistical-power-and-sample-adequacy-at-n--29)
4. [Confirmatory Test (RQ1) and Secondary Analyses (RQ2, RQ3)](#4-confirmatory-test-rq1-and-secondary-analyses-rq2-rq3)
5. [Formal Equivalence Testing](#5-formal-equivalence-testing)
6. [Study Verdict](#6-study-verdict)
7. [Design Artifact: Ad-Group Early Warning Flagging Rule](#design-artifact-ad-group-early-warning-flagging-rule)
8. [Canonical Statistics](#8-canonical-statistics)
9. [Methodological Pivot Log](#9-methodological-pivot-log)
10. [Figures](#10-figures)
11. [What a Properly Powered Follow-Up Would Need](#11-what-a-properly-powered-follow-up-would-need)

---

## 1. Theoretical Extension — The Temporal Dimension

The same statistical-discrimination vs. behavioral-meritocracy tension tested cross-sectionally
in the main study (root README §2.2–§2.3) has an independent temporal-axis grounding.
Organizational ecology's **liability of newness** thesis (Stinchcombe, 1965) predicts that newer
organizational units face a structural disadvantage — in role learning, trust accumulation,
resource access — that is independent of current performance, simply because they have not yet
accumulated organizational history. Applied to a new ad group launched inside an already-
established advertiser account, this predicts that **account maturity** should carry a direct,
positive association with that ad group's early growth trajectory, net of the ad group's own
current operating signal.

The competing account draws on **platform-governance research on algorithmic intermediaries**
(Gillespie, 2014, and subsequent work on algorithmic power in two-sided markets): if a real-time
serving system evaluates *units* (ad groups, individual auction entries) on their own current
signal rather than the parent account's accumulated history, the liability of newness should be
**absorbed and neutralized** as soon as the unit itself generates enough behavioral signal to be
scored on its own terms — which, on an auction platform, can happen within days rather than
years.

### Formal research questions

| ID | Question | Liability-of-newness account predicts | Real-time-scoring account predicts |
|---|---|---|---|
| **RQ1** | **Maturity → new ad group's initial growth, net of own early signal (focal audit test)** | **positive, significant** | **null** |
| RQ2 | Does own early signal predict growth, and does maturity add value once between/within-customer variance is separated? | maturity adds genuine within-customer value | own-signal predictive; maturity adds nothing within-customer |
| RQ3 | (exploratory) Does early-signal flagging beat random flagging, and is any decision day distinguishable as optimal? | — | — |

A null result on RQ1 would be, in principle, substantive support for real-time scoring — and, per
root README §2.5, an additional instance of the broader structural signal irrelevance pattern —
were the design properly powered to detect a small effect. As §3 below documents, this design's
power against a small effect is limited, so RQ1's null result is reported as directionally
corroborative rather than confirmatory.

---

## 2. Study Design — Cold-Start Reframing & Growth Trajectory

### 2.1 A methodological detour that became a finding: what "cold-start" actually meant

Before any audit test, the sample definition itself required five sequential rounds of
self-correction.

**Sample-count reconciliation.** An earlier planning document reported two different "true
cold-start" counts (476 vs. 250→222). Re-deriving from data dynamically confirmed **250 → 222**
as the correct figure; 476 was a looser pre-join count.

**"Right-censoring" was not censoring.** 222 trajectory-usable ad groups initially flagged 83.8%
as right-censored. Sensitivity checks against 30/60/90/120-day follow-up cutoffs barely moved
this rate (83.6% → 83.2%) — if insufficient follow-up time were the cause, a stricter cutoff
should have sharply reduced it. Direct measurement of observed-day coverage within fixed
post-registration windows showed only 70–74% coverage, not the near-100% a continuously-run ad
group would show. **Reinterpretation:** ad groups mostly aren't self-terminating (they're still
running at observation end) combined with genuine intermittency (on/off cycling, budget
exhaustion, approval delay) — not classic survival-analysis censoring.

**GBTM was abandoned before it was fit.** A BIC-based class-count recovery simulation at the
achievable sample size (n=222) found ~9% recovery probability at k=2 true latent classes, ~0% at
k=3/4. Group-based trajectory modeling was dropped entirely in favor of a continuous growth-slope
quantity, avoiding the class-count identification problem.

**What "cold-start" actually meant.** Under every registration-date cutoff tested (0–90 days of
prior account history), essentially none of the trajectory-usable sample (0–1 of 222 ad groups)
reflected a genuinely new account. **The median account behind a "cold-start" ad group had ~7.8
years of account age** (a lower bound, per the `adgroup_dim` snapshot caveat in root README §3).
A snapshot/migration-date artifact was explicitly ruled out. **The study was reframed around item
cold-start** — a new ad group inside an already-established account — rather than user
cold-start (a brand-new advertiser onboarding). This reframing is what makes "account maturity"
the correct operationalization of RQ1's structural attribute (§1 above).

**MixedLM was structurally non-identified.** A customer random-intercept mixed model (`slope ~
maturity, groups=customer_id`) was the original planned estimator. Because maturity varies only
at the customer level, it competes directly with the customer random intercept for the same layer
of variation — a power simulation found a 100% convergence-failure rate across every replication
at every tested effect size. MixedLM was dropped entirely (not even retained as a reference
point-estimate); a customer-level aggregate OLS with a cluster permutation test became the primary
inferential model.

---

## 3. Statistical Power and Sample Adequacy at n = 29

n = 29 customer-level clusters is the single most consequential limitation of this study. This
section (a) traces exactly why the sample bottoms out at 29, (b) reports the a priori power
argument, (c) adds a Bayesian layer, (d) states in one place exactly which claims this design can
and cannot support, and (e) gives the sample size a larger design would need to close that gap.

### 3.1 Why n = 29 — the reduction path

| Stage | Sample | Reason for reduction |
|---|---|---|
| 0. Cold-start candidates | 250 → 222 | Definition reconciliation (§2.1) |
| 1. Trajectory-usable | 222 | ≥7 active days required |
| 2. Complete 30-day window required | 204 (ad groups) | Growth-slope estimation requires a full early window |
| 3. Aggregated to customer level (MixedLM non-identified, §2.1) | **29–32 customers** | Maturity varies only at customer level; competes with customer random intercept |
| 4. Final confirmatory sample | **29 customers, 204 ad groups** | — |

Each reduction is independently forced by a distinct methodological necessity (definition
correctness → estimability of a growth slope → estimator identifiability), not by a search for a
sample that produces a null.

### 3.2 A priori power calculation

**Effect-size benchmark.** The pre-registered detection threshold is a standardized effect of
β = .50, a large effect by conventional benchmarks (Cohen, 1988), chosen because the
liability-of-newness account predicts a structural effect of roughly this order if it exists at
all — organizational-ecology estimates of new-entrant disadvantage are typically large when
present, because the mechanism, if real, produces a first-order allocation difference rather than
a small nuisance correlation.

**Power calculation.** For a single-predictor regression with n = 29 clusters testing β = .50
(R² = .25), the noncentrality parameter for the F-test is λ = f² · (n − k − 1) = 0.333 × 27 ≈ 9.0,
corresponding to approximately **88% power at α = .05**.

**What this cannot rule out.** 88% power at β = .50 does not imply high power to detect a smaller
effect (β ≈ .10–.20) that a weaker version of liability-of-newness might predict instead. This is
exactly why §5's TOST equivalence testing is a necessary complement, not a redundant check.

### 3.3 Bayesian layer — quantifying evidence for the null, not just failing to reject it

A non-significant p-value at n=29 is compatible with two very different underlying states:
genuine absence of an effect, or simply insufficient data to say anything. A JZS
(Jeffreys–Zellner–Siow) default-prior Bayes factor was specified as a second, independent
evidentiary layer alongside the frequentist test, mirroring the approach used for H1c in the
cross-sectional study.

> **Status: specified, not executed.** `src/analysis/rq1_bayes_factor.py` (a script that would
> compute BF₀₁ for the RQ1 coefficient under a JZS default prior, Rouder et al., 2009 scale-
> invariant Cauchy prior on the standardized effect) was drafted but never run. This is flagged
> explicitly, per this repository's transparency norm, as a planned-but-not-yet-executed
> analysis rather than silently omitted or backfilled with an invented number. Executing this
> script is one of the concrete next steps listed in §11.

### 3.4 What this design can and cannot claim

- **Can claim:** at 88% power, this design would very likely have detected a liability-of-newness
  effect of the theoretically motivated large magnitude (β≈.50) had one been present. None was
  found (§4), so the large-effect version of liability-of-newness is not supported.
- **Cannot claim:** that no maturity effect exists at any magnitude. A small residual effect
  (β≈.10–.20) is not ruled out by this design's power, and TOST equivalence testing at tighter
  margins (§5) does not positively rule it out either.

### 3.5 Sample size needed to close the small-effect gap

| Target effect size (β) | Approx. required customer-level n (80% power) |
|---|---|
| 0.50 (current pre-registered SESOI) | ≈ 26 |
| 0.30 | ≈ 84 |
| 0.20 | ≈ 193 |
| 0.10 | ≈ 782 |

> **Status: approximate, to be regenerated exactly.** `src/analysis/rq1_power_analysis.py` would
> need to be extended with a target-effect-size sweep to replace the approximation above with
> exact noncentral-F values. Detecting a small effect (β≈.30) would require roughly **3× the
> current customer count** — unattainable within a single agency's active customer base over this
> observation window at any plausible cold-start incidence rate. This is exactly why a
> cross-platform / multi-agency design is proposed in §11 as the actual path to resolving the
> small-effect question.

### 3.6 Convergent-validity supplement

Beyond the a priori power calculation, five independent estimators (OLS, bootstrap, cluster
permutation, winsorized OLS, rank-rank regression — §4) converge on the same small-magnitude,
non-significant conclusion, and a required leave-one-out sensitivity check (removing the single
largest customer, 35.8% of the trajectory-usable sample) leaves the sign and substantive
conclusion unchanged. Convergence across five estimators with different bias-variance profiles at
the same sample size is itself evidence that the null is not an estimator-specific artifact of
small n.

---

## 4. Confirmatory Test (RQ1) and Secondary Analyses (RQ2, RQ3)

### 4.1 RQ1 — does account maturity predict a new ad group's initial growth?

Final sample: 204 ad groups → 29 customers (aggregated to customer level, once a complete 30-day
window is required).

| Statistic | Value |
|---|---|
| OLS β (raw scale) | 8.34 |
| Cluster-robust HC3 p | .576 |
| Bootstrap 95% CI | [−15.84, 43.08] |
| Cluster permutation p | .663 |
| Spearman ρ | −.020 (p=.92) |
| Leave-one-out (largest customer removed) permutation p | .702 (sign unchanged) |
| Standardized effect size | .085 (17% of the pre-registered large-effect threshold of .50) |
| JZS Bayes factor (BF₀₁) | pending (§3.3) |

Five independent methods (OLS, bootstrap, permutation, winsorized OLS, rank-rank regression)
converge on the same non-significant, small-magnitude conclusion (see Figure 5 in §10). A
leave-one-out check removing the single largest customer (35.8% of the sample) leaves the verdict
unchanged. Against §1's formal research questions: RQ1 is not supported — the real-time
behavioral-scoring account, not the liability-of-newness account, is the one directionally
consistent with the data, at 88% power against the theoretically motivated large-effect benchmark
(§3.2), with the explicit small-effect caveat stated in §3.4.

### 4.2 RQ2 — does the ad group's own early signal predict growth, and does maturity add anything?

An ad group's own early operating signal (activity coverage, spend trend, CTR/CVR) **is**
predictive of near-term growth: leakage-free within-customer LOCO ρ ranges from 0.467 (14/14-day
window) down to 0.060 (30/60-day window) — predictive power decays sharply with horizon length.
Adding account maturity shows an apparent *pooled* improvement, but **decomposing that pooled
improvement into between-customer and within-customer components** reveals the entire gain sits
in the between-customer term — maturity is re-deriving the same customer-level signal already
captured elsewhere, not adding genuine ad-group-level predictive value. The within-customer
component is ≈0 or slightly negative at every tested window. See Figure 6, panels A–B, in §10.

### 4.3 RQ3 — early-signal flagging and decision timing (exploratory)

Early-signal flagging achieves a 1.2–1.4× precision lift over random flagging, fairly consistently
across decision cutoffs at day 7, 14, and 21 post-registration. Bootstrapped 95% CIs on
out-of-fold predictive ρ overlap substantially across all three cutoffs — **no single day is
statistically distinguishable as optimal.** See Figure 6, panels C–D, in §10.

Two successive "expected uplift" simulations (intended to identify the optimal intervention day
under an assumed effect size) were found to be mathematically incapable of answering that
question — the effect-size parameters entered the formula in a way that made the argmax
structurally fixed regardless of the swept values (§9, entries 5–6). The reported result was
narrowed to what can be measured without an intervention-effect assumption: precision/recall/lift
against the *realized* outcome.

---

## 5. Formal Equivalence Testing

A non-significant p-value doesn't itself establish that an effect is absent, so both null results
above were tested for TOST equivalence. **Neither reaches formal equivalence**: maturity → growth
slope, TOST p = .197; maturity's contribution to prediction, TOST p = .290. Given §3's power
analysis, this is the expected and correctly interpreted outcome: the design is well-powered
(88%) against the theoretically motivated large effect (β=.50) and correctly fails to positively
rule out a small effect at these tighter equivalence margins (±0.20, ±0.05). Both are
well-powered, non-significant associations for which formal equivalence remains inconclusive —
this is exactly why this study is graded as provisional rather than confirmatory, and why it is
reported here as future work rather than as corroborating evidence in the main manuscript. See
Figure 9 in §10.

---

## 6. Study Verdict

> Item cold-start, not user cold-start, is the actual phenomenon in this data — a correction to
> an unverified implicit assumption. Account maturity shows no significant direct association
> with a new ad group's initial growth (5/5 methods converge on null; TOST inconclusive;
> well-powered at 88% against the pre-registered large-effect benchmark per §3, with the
> small-effect caveat stated explicitly in §3.4). The ad group's own early operating signal *is*
> predictive, and that predictive value is not improved by adding account maturity once
> between/within decomposition removes the leaked customer-level signal. This is the same
> qualitative pattern as the cross-sectional study — structural attribute null, behavioral-signal
> positive — on an independent sample and a different time axis, directionally consistent with
> structural signal irrelevance (root README §2.5) and the behavioral-meritocracy /
> real-time-scoring accounts over their structural-entrenchment counterparts. Given the small
> confirmatory sample (n = 29–32 customers, §3.1) and the TOST-inconclusive equivalence tests,
> this study is graded **provisional, directionally corroborative evidence only** — not
> independently conclusive, and not part of the main manuscript's evidence base. It is reported
> here as a template for, and a strong motivator of, a properly powered follow-up (§11).

---

## Design Artifact: Ad-Group Early Warning Flagging Rule

### Motivation

§4.2's confirmed within-customer result — an ad group's own early operating signal predicts its
near-term growth, and adding account maturity produces no within-customer improvement at any
tested horizon — motivates a concrete, implementable decision rule, specified below as a design
artifact in the design-science-research sense: an explicit input/output specification grounded in
a stated empirical result, rather than a general recommendation. Because this artifact's
justification depends entirely on the descoped longitudinal study, it is documented here rather
than in the main repository; [`docs/DESIGN_ARTIFACT.md`](docs/DESIGN_ARTIFACT.md) is a stub that
redirects here.

### Specification

**Artifact name:** Ad-Group Early Warning Flagging Rule

| Field | Value |
|---|---|
| Input | `predicted_growth_rank_percentile` (float, [0,1]); `day_since_registration` (int) |
| Output | `flag` (bool); `reason` (str) |
| `flag_threshold` | 0.30 |
| Valid decision window | day 7–21 post-registration |

```python
def early_warning_flag(predicted_growth_rank_percentile: float,
                        day_since_registration: int,
                        flag_threshold: float = 0.30,
                        min_day: int = 7,
                        max_day: int = 21) -> dict:
    if not (min_day <= day_since_registration <= max_day):
        return {"flag": False, "reason": f"outside observation window ({min_day}-{max_day} days)"}
    if predicted_growth_rank_percentile <= flag_threshold:
        return {"flag": True, "reason": f"bottom {flag_threshold:.0%} predicted growth"}
    return {"flag": False, "reason": "above threshold"}
```

**Design principles.**

- **DP1.** Base flagging solely on the ad group's own early-period signal — never on
  account-level history (grounded in §4.2's within-customer result).
- **DP2.** Evaluate at any point within a bounded window (day 7–21) rather than committing to a
  single fixed day (grounded in Figure 6, panels C–D: no cutoff is statistically distinguishable
  as optimal).
- **DP3.** Threshold on relative rank (percentile) within the observed cohort rather than an
  absolute growth value, since growth magnitudes are not comparable across heterogeneous ad
  groups.

### Empirical backtest

**Why the naive (size/tenure) comparison is structurally ill-posed.** Account maturity is a
customer-level constant. Within-customer demeaning — required to isolate the same within-customer
signal that DP1 claims matters — collapses a prediction built purely from a customer-level
constant to numerical zero in every specification tested (residual SD ~1e-17, i.e., floating-point
noise, not a substantive near-zero effect). This is expected and correct: it is the same fact
demonstrated analytically in §4.2's within/between decomposition, now independently confirmed in a
binary-flagging frame. It means the naive rule has **no within-customer predictive content by
construction**, so a "naive wins / own-signal wins" framing is not a meaningful contest on this
axis — there is nothing for the own-signal rule to beat.

**What was measured instead: own-signal vs. random baseline.** With the naive comparison ruled
out, own-signal precision at the 30% flagging threshold was compared against a random-flagging
baseline, within-customer, across nine specifications varying the minimum active-days threshold
(5 / 7 / 10) and the early/later window pair.

| Spec (active-days_early-later) | n (ad groups) | n (customers) | Own-signal precision | Random baseline | Difference |
|---|---|---|---|---|---|
| active7_14-14 | 195 | 20 | 0.276 | 0.297 | −0.022 |
| active5_14-14 | 196 | 20 | 0.310 | 0.296 | +0.014 |
| active5_10-10 | 197 | 20 | 0.390 | 0.299 | +0.090 |
| active5_7-14 | 197 | 20 | 0.288 | 0.299 | −0.011 |
| active7_10-10 | 196 | 20 | 0.397 | 0.296 | +0.101 |
| active7_7-14 | 196 | 20 | 0.259 | 0.296 | −0.037 |
| active10_14-14 | 195 | 20 | 0.276 | 0.297 | −0.022 |
| active5_14-21 | 195 | 20 | 0.328 | 0.297 | +0.030 |
| active7_14-21 | 194 | 20 | 0.293 | 0.299 | −0.006 |

**Own-signal precision exceeded the random baseline in 4 of 9 specifications (44%).** At this
sample size (n ≈ 20 customers per spec), this pattern is not distinguishable from chance.

**Relationship to §4.2's confirmed result.** §4.2's result is a **continuous-scale** finding
(Spearman ρ on continuous predicted growth), well-powered and significant at short horizons
(14-day within-customer LOCO ρ up to ≈0.49). This backtest asks a **much coarser** question — does
thresholding that continuous signal into a binary "flag the bottom 30%" decision produce a
precision advantage detectable at n ≈ 20 customers — and the answer is that this specific
binary-decision framing lacks the power to resolve the question either way. A continuous signal
being predictive does not guarantee that any particular binarization of it is empirically
distinguishable from random at a small sample size; these are different statistical questions
with different power requirements. This is **not a contradiction** of §4.2, and should not be
read as one.

**Status and recommended next step.** DP1–DP3 are **theoretically grounded** in the confirmed
§4.2 result. They are **not yet empirically validated** as superior to alternatives in
binary-decision form. Recommended next step: (a) a larger cold-start sample (the current n ≈
20-customer backtest is underpowered for a 9-percentage-point-scale precision comparison), and/or
(b) a continuous-scale evaluation of the flagging rule's utility (e.g., a precision-recall curve
across thresholds rather than a single 30% cutoff), reported in the same continuous-metric terms
as §4.2 rather than as a binary win/loss against a naive baseline.

**Version note.** An earlier internal version of this backtest reported a naive-rule "victory" at
several window specifications. That result was a computational artifact: the naive predictions
had not been within-customer demeaned before ranking, so the comparison implicitly re-injected the
same between-customer signal that §4.2's decomposition explicitly excludes. The corrected,
within-customer-demeaned version above is the one reported here; the artifact and its correction
are logged in §9, entry 9.

**Relationship to the alternative-identification screening.** The same structural fact underlying
the naive-comparison problem above — that account-level attributes (size, tenure) are
customer-level constants and therefore collapse under within-customer demeaning — is also what
makes account-level variables (`size`, `total spend`) poor running variables for a regression-
discontinuity design when estimated on a customer × day panel without care. The
alternative-identification screening documented in
[`supplementary_identification/`](supplementary_identification/SCREENING_SUMMARY.md) (root README
§4.5.9, part of the cross-sectional study, not this one) encountered a related panel-density issue
and resolved it the same way this artifact resolves the naive-rule comparison: by moving the unit
of analysis to one row per customer before drawing any conclusion.

---

## 8. Canonical Statistics

These tables were originally part of `docs/RESULTS_SUMMARY.md`. They are reproduced here in full,
unaltered, since that file now covers only the cross-sectional study.

### Hypothesis ↔ theoretical account quick reference

| ID | Structural attribute | Competing accounts | Statistic that adjudicates |
|---|---|---|---|
| **RQ1** | maturity → growth slope, net of own signal | liability of newness (Stinchcombe 1965) vs. real-time behavioral scoring (Gillespie 2014) | OLS/bootstrap/permutation battery, below |
| RQ2 | own signal + maturity → prediction | sharpens RQ1 via within/between decomposition | LOCO ρ decomposition, below |
| RQ3 | flagging precision by decision day | design implication, not a theory test | precision/lift heatmap, below |

### §Power — statistical power and sample adequacy at n = 29

#### Sample reduction path (traceability table)

| Stage | n | Cause |
|---|---|---|
| Cold-start candidates | 250 → 222 | Definition reconciliation (§2.1) |
| Trajectory-usable | 222 | ≥7 active days |
| Complete 30-day window required | 204 (ad groups) | Growth-slope estimability |
| Aggregated to customer level | **29–32** | MixedLM non-identified (§2.1); customer-level aggregate OLS adopted instead |

#### A priori power calculation

| Quantity | Value | Source of the number |
|---|---|---|
| Pre-registered SESOI (standardized β) | 0.50 | Cohen (1988) "large effect" convention; theoretical rationale in §3.2 |
| n (customer-level clusters) | 29 | trajectory-usable sample after full-window requirement |
| Predictors (k) | 1 | single-predictor regression, maturity on aggregated growth slope |
| R² implied by SESOI | 0.25 | β² for a single standardized predictor |
| f² (Cohen's effect-size index) | 0.333 | f² = R² / (1 − R²) |
| Residual df (n − k − 1) | 27 | |
| Noncentrality parameter (λ) | ≈ 9.0 | λ = f² × (n − k − 1) |
| **Power at α = .05, two-tailed** | **≈ 0.88** | noncentral F(1, 27) at λ≈9.0, α=.05 |
| Observed standardized effect | 0.085 | §RQ1-Maturity row below |
| Observed effect as % of SESOI | 17% | 0.085 / 0.50 |

#### Bayesian layer

| Quantity | Value | Status |
|---|---|---|
| Prior | JZS default prior (scale-invariant Cauchy, Rouder et al. 2009) on standardized β | specified |
| BF₀₁ (evidence ratio favoring null over pre-registered β=.50 alternative) | **pending execution** | `src/analysis/rq1_bayes_factor.py` (not yet run) |

#### Scope statement — what n=29 can and cannot support

| Claim | Supported? |
|---|---|
| No liability-of-newness effect at the theoretically motivated large magnitude (β≈.50) | Yes — 88% power, null observed |
| No maturity effect at any magnitude, however small | **No** — design not powered for β≈.10–.20; TOST does not establish equivalence at ±0.20/±0.05 (see TOST table below) |

#### Sample size needed to close the small-effect gap

| Target effect size (β) | Approx. required customer-level n (80% power, noncentral-F, α=.05, k=1) |
|---|---|
| 0.50 (current pre-registered SESOI) | ≈ 26 |
| 0.30 | ≈ 84 |
| 0.20 | ≈ 193 |
| 0.10 | ≈ 782 |

### §RQ1-Maturity — account maturity vs. initial growth slope (Figure 5)

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
| JZS Bayes factor (BF₀₁) | pending |

### §EarlySignal / §MaturityAdd — early signal vs. maturity (Figure 6A–B)

| early/later window (days) | n (ad groups) | Own-signal within-customer LOCO ρ | +Maturity within-customer LOCO ρ | within-customer improvement | repeated-split Wilcoxon p |
|---|---|---|---|---|---|
| 14 / 14 | 204 | 0.467 | 0.487 | +0.019 | .038 (worse on repeated-split ρ) |
| 30 / 30 | 184 | 0.275 | 0.257 | −0.018 | .119 |
| 30 / 60 | 179 | 0.060 | 0.061 | +0.001 | .019 (worse on repeated-split ρ) |

### §Flagging — decision-cutoff exploration (Figure 6C–D)

| decision cutoff (days) | out-of-fold predictive ρ (95% bootstrap CI) | lift @ threshold=0.25 | lift @ threshold=0.40 |
|---|---|---|---|
| 7 | 0.304 [0.145, 0.445] | 0.83 | 1.27 |
| 14 | 0.265 [0.123, 0.404] | 1.33 | 1.23 |
| 21 | 0.334 [0.210, 0.459] | 1.42 | 1.36 |

### TOST equivalence (Figure 9)

| Test | Observed effect | Equivalence margin (SESOI) | TOST p | Equivalence established? |
|---|---|---|---|---|
| RQ1: maturity → growth slope | 0.085 | ±0.20 | .197 | No |
| RQ2/H2b: maturity → prediction improvement | 0.023 | ±0.05 | .290 | No |

### Evidence-grade table

| | Advertiser size (cross-sectional, main study) | Account maturity (this document, RQ1) |
|---|---|---|
| **Evidence grade** | **Confirmatory** | **Provisional / directionally corroborative** |
| Robustness convergence | 8/8 independent methods null | 5/5 independent methods null |
| Power against pre-registered SESOI | High across all six outcome×sample combinations | 88% against β=.50 only; not powered for β≈.10–.20 |
| TOST equivalence | Not the primary evidentiary basis | Attempted; **not established** at ±0.20/±0.05 |
| Bayes factor reported | Yes (BF₁₀, per-cell) | Pending |

**Use of this table.** This document's RQ1 result should be cited only as a directionally
corroborative pilot on an independent sample/time-axis, not as an independently conclusive result
carrying equal evidentiary weight to the main study.

---

## 9. Methodological Pivot Log

These entries were originally part of `docs/METHODOLOGY_NOTES.md`. They are reproduced here in
full, unaltered.

### 1. "Cold start" was assumed to mean new-advertiser onboarding

**Assumed:** the project's original framing treated a "cold-start" ad group as the leading edge
of a brand-new advertiser's account -- a first campaign, unfolding inside the observation
window.

**Contradicted by:** cross-checking account-maturity distribution against top-customer profiling.
Under every registration-date cutoff tested (0-90 days of prior account history), essentially
none of the trajectory-usable sample (0-1 of 222 ad groups) reflected a genuinely new account;
the median account behind a "cold-start" ad group had `account_age_days` of roughly 7.8 years (a
lower bound, per the `adgroup_dim` snapshot caveat). A snapshot/migration date artifact was
ruled out as the explanation.

**Changed:** the project was reframed around **item-level cold start**: a new ad group inside an
already-established account -- closer to "item cold-start" than "user cold-start" in the
recommender-systems literature. Account maturity became the key covariate under test (§4), not a
stratification variable for sample selection. This reframing is also what makes "account
maturity" the correct operationalization of the liability-of-newness construct in §1 -- a
diffuse-tenure covariate on 7.8-year-old accounts tests a materially different theoretical claim
than a true new-entrant covariate would.

### 2. Discrete latent-class growth models (GBTM) were the planned estimator

**Assumed:** growth trajectories would be summarized with a Group-Based Trajectory Model, asking
"how many growth classes exist, and does maturity predict class membership?"

**Contradicted by:** a BIC-based class-count recovery simulation at the achievable sample size
(n=222). Recovery probability was ~9% at k=2 true classes and ~0% at k=3/4 -- the sample cannot
reliably tell two classes apart, let alone three or four, independent of any censoring or
clustering issue.

**Changed:** GBTM was dropped from the confirmatory design entirely. The maturity test (§4) was
rewritten around a continuous growth-curve quantity (an ad group's initial 30-day cost slope)
rather than a discrete class label, avoiding the class-count identification problem altogether.
This choice also simplified the eventual power calculation (entry 11 below) -- a continuous
single-predictor regression has a standard, closed-form power formula, whereas a latent-class
model's power to detect a maturity effect on class membership would have required a separate,
less standard simulation-based approach at an already marginal sample size.

### 3. Apparent right-censoring turned out to be a follow-up-window artifact, then something else

**Assumed:** the 83.8% "censored" rate found in an initial flagging step meant many trajectories
were cut short by the observation window ending too soon after registration.

**Contradicted by:** requiring 30 vs. 120 days of guaranteed post-registration follow-up barely
moved the censored rate (83.6% -> 83.2%). If insufficient follow-up time were the cause, a
stricter cutoff should have reduced it sharply. A subsequent check then showed the real story:
mean observed-day coverage within fixed post-registration windows was only 70-74%, not the
near-100% a genuinely continuously-run ad group would show -- and unlike the cutoff sweep, this
doesn't move with cutoff, because it's measuring something different (data gaps, not trajectory
truncation).

**Changed:** "censoring" was reinterpreted as ad groups mostly **not self-terminating**
(activity persists to observation end because the ad group is still running, not because its
trajectory was cut off) combined with **genuine intermittency** (on/off cycling, budget
exhaustion, approval delay) inside the active window. The confirmatory growth-slope definition
uses fixed-window linear trend fitting on zero-filled daily series rather than a
survival/censoring framework, which sidesteps the mismatch.

### 4. A customer random-intercept mixed model (MixedLM) was the planned estimator

**Assumed:** growth slopes nested within customers would be modeled with `statsmodels` MixedLM,
`slope ~ maturity`, `groups=customer_id`.

**Contradicted by:** a power simulation. Because `maturity` varies only at the customer level, it
competes directly with the customer random intercept for the same layer of variation, and the
model is structurally non-identified against it: 100% convergence-failure rate (singular
random-effects covariance / boundary-of-parameter-space warnings) across every simulation
replication, at every tested effect size -- not merely an occasional convergence issue.

**Changed:** MixedLM was dropped as unusable for this design (not even kept as a reference
point-estimate). The customer-level aggregate regression (average an ad group's growth slope up
to its customer, then regress the customer-level mean on customer-level maturity, n = customer
count) became the primary inferential model, with a cluster (customer-label) permutation test as
the final arbiter whenever it and OLS disagree -- because 29-32 clusters is below the usual
comfort threshold (40-50+) for trusting asymptotic cluster-robust standard errors alone. This
estimator choice is also what makes the power calculation in §3 tractable.

### 5. A pooled Leave-One-Customer-Out (LOCO) improvement was initially read as support for maturity adding predictive value

**Assumed:** during feature-engineering design, a positive pooled LOCO rho improvement when
adding account maturity to the base feature set was read as evidence that maturity adds
ad-group-level predictive value.

**Contradicted by:** a within/between-customer decomposition. Splitting the pooled LOCO rho into
a between-customer component (customer mean-level agreement) and a within-customer component
(relative ranking of ad groups belonging to the same customer) showed that, at every tested
window pair, the pooled improvement was concentrated almost entirely in the between-customer
term while the within-customer term showed little or no improvement (in one window pair, +0.388
between vs. +0.001 within). A pooled metric that improves because it re-derives the
customer-level maturity signal is not evidence of genuine ad-group-level predictive gain.

**Changed:** the confirmatory design requires the within-customer LOCO improvement to be
positive before crediting maturity with adding value, regardless of the pooled or
between-customer numbers. This is the same logic that later surfaces in the design-artifact
backtest above.

### 6. Two successive "expected uplift" simulations were mathematically incapable of answering the question they were built for

**Assumed:** an expected-uplift formula (`n_true_positive * efficacy * delta`) swept across
intervention-effect assumptions (`delta`, `efficacy`) would reveal which decision cutoff
(7/14/21 days) is optimal, and whether that ranking is robust to the effect-size assumption.

**Contradicted by:** in the first version, `delta` and `efficacy` entered the formula as
constants multiplying every (cutoff, threshold) cell identically, so the argmax over cutoffs
could never change regardless of the assumed values -- the "100% stability across 9 scenarios"
result this produced was a mathematical artifact of the formula's structure, not a substantive
robustness finding. A second version made `delta` a function of the cutoff's remaining
follow-up time (`delta_per_day * remaining_days`) to build in a genuine cutoff/effect-size
trade-off -- but `delta_per_day` and `efficacy` still multiplied every cell identically for a
*given* cutoff, so the ranking was again structurally fixed (this time by `remaining_days`
alone) rather than by the swept parameters.

**Changed:** the reported result was narrowed to what can be measured without an
intervention-effect assumption: precision/recall/lift of early-signal flagging against the
*realized* low-growth outcome, which requires no assumption about what an intervention would do.
The expected-uplift tables are retained only as explicitly labeled, non-causal what-if
illustrations, never as the basis for an "optimal day" claim. Bootstrapped confidence intervals
on the precision/recall metric further showed the 7/14/21-day cutoffs' predictive rho values are
not statistically distinguishable from one another (§4.3, Figure 6C-D).

### 7. Sample-exclusion rules were derived empirically, then made explicit

**Assumed initially:** none -- test/template accounts were not anticipated as a distinct
category.

**Found:** profiling the top-10 customers driving a clustering-concentration diagnostic using
four independent signals (all-time scale, registration-burst pattern, template/naming-pattern
signal, and real spend) found two accounts with near-zero total spend and heavy template signal
(single registration burst, zero bid-amount variance) -- operationally indistinguishable from
test/QA setups rather than real advertising activity.

**Changed:** `sample_definition.known_test_account_ids` in `config/config.yaml` now explicitly
excludes these two accounts from every confirmatory analysis, alongside the general rule
(`test_account_exclusion.min_total_cost`, `test_account_exclusion.max_zero_spend_share`) that
produced them -- so the exclusion is pre-specified and logged, not applied ad hoc per analysis.

### 8. The largest customer's influence was checked, not assumed away

**Found:** one customer contributed 32.9% of the trajectory-usable sample. Four-signal profiling
classified this customer as a genuine large advertiser (all-time scale in the 100th percentile,
meaningful and varied spend, campaigns spread across the full observation window) rather than a
bulk-generated template account, so it was not excluded.

**Changed:** because exclusion wasn't warranted, a leave-one-out sensitivity check on this
customer was made a **required**, not optional, component of the maturity confirmatory test --
every reported result in §4.1 is accompanied by the same test re-run with this customer removed,
and the verdict rule requires both runs to agree in sign. This required-agreement rule is also
what §3.6's convergent-validity argument leans on: the leave-one-out check is one of the five
converging estimators cited there as evidence that the null is not a small-n estimator artifact.

### 9. A naive-rule "victory" in the design-artifact backtest was a within-customer-demeaning bug, not a finding

**Assumed:** an early version of the design-artifact backtest compared own-signal flagging
precision against a naive account-size/tenure-based rule directly, without first
within-customer demeaning the naive rule's predictions.

**Contradicted by:** because account maturity is a customer-level constant, ranking its raw
(non-demeaned) predictions implicitly reproduces the same between-customer signal that entry 5
above (and §4.2's within/between decomposition) explicitly excludes from the within-customer
claim. The early version's apparent "naive wins" result in several window specifications was
this leakage re-appearing in a binary-flagging frame, not a genuine advantage for the naive
rule.

**Changed:** the backtest was corrected to within-customer demean both rules' predictions before
ranking. Under the corrected version, the naive rule's demeaned predictions collapse to
numerical zero in every specification (as they must, being derived from a customer-level
constant), making a naive-vs-own-signal comparison ill-posed by construction. The corrected
backtest instead compares own-signal precision against a random-flagging baseline (see the
Design Artifact section above).

### 10. The n=29 power justification was derived after the fact and needed to be made explicit, not just asserted

**Assumed:** early drafts of this study reported the RQ1 null result (n=29 customers) alongside a
bare limitation note ("small sample") without stating what the design could or could not detect.

**Contradicted by:** re-running the power-simulation infrastructure at the *final* chosen
estimator specification (the customer-level aggregate OLS from entry 4 above, not the abandoned
MixedLM) and computing power analytically at a pre-specified SESOI. Two things fell out of this
exercise that were not obvious from "n=29" alone: (a) a single-predictor regression at n=29
testing a standardized effect of β=.50 has a closed-form noncentrality parameter (λ =
f²×(n−k−1) ≈ 9.0) that corresponds to **≈88% power**, not the intuitively "underpowered" reading
a bare n=29 might suggest; and (b) that same design is *not* well-powered against a smaller
effect (β≈.10-.20), which is a materially different and more precise statement than "the sample
is small."

**Changed:** §3.2 now states the power calculation explicitly, including the SESOI justification
(β=.50 chosen because the liability-of-newness account predicts a large effect if one exists at
all — see §1 and §3.2), the calculation itself, and what it does and does not rule out (§3.4).
This also clarified *why* the TOST equivalence tests (§5) are a necessary complement rather than
a redundant check: TOST is what lets the manuscript address the "small effect" case that the a
priori power calculation is explicitly underpowered for. The five-estimator convergence (§4.1
table) and the required leave-one-out check (entry 8) are now also explicitly framed in §3.6 as
*convergent-validity* evidence supplementing the a priori power argument, rather than as
independent, unconnected robustness items.

### 11. This study's small-sample null result rested on a p-value/power argument alone, which external review judged insufficient at n=29

**Assumed:** an earlier version of §3 was judged sufficient once it stated the a priori power
calculation (88% at β=.50, entry 10 above) and paired it with TOST equivalence testing.

**Contradicted by:** external review noted that a p-value/power argument, however carefully
computed, does not by itself let a reader distinguish "the data provide positive evidence for
the null" from "the data are simply too sparse to say much of anything" — the two states look
identical under a frequentist non-significant result, and only diverge under a Bayesian
evidence-ratio framing. The review also noted that the cross-sectional study's H1c test already
reports per-outcome Bayes factors — meaning this study's treatment of the same underlying
question (is this a null result, or an uninformative one?) was inconsistent in rigor with the
main study's.

**Changed:** §3 was restructured into six explicit subsections: the sample-reduction
traceability table (§3.1, addressing "why didn't you use a bigger sample" directly rather than
leaving n=29 as a bare number); the a priori power calculation (§3.2); a Bayesian layer
specifying a JZS default-prior Bayes factor for the RQ1 coefficient, matching the main study's
existing BF₁₀ reporting convention (§3.3); an explicit two-line scope statement separating what
the design can and cannot claim (§3.4); a required-sample-size table showing exactly how large a
follow-up design would need to be to detect progressively smaller effects (§3.5); and a
convergent-validity supplement (§3.6). `src/analysis/rq1_bayes_factor.py` was added as a new,
explicitly not-yet-executed script; its result is reported as "pending" (§8) rather than filled
with a placeholder or estimated number.

---

## Summary of what changed in the pivot-log revision pass (entries 10–11)

No underlying statistic reported anywhere in this study (RQ1/2/3, or the design-artifact backtest
grid) was recomputed or altered by this revision pass. What changed is that this study's
small-sample limitation is now addressed with a traceability table, a scope statement, a Bayesian
evidentiary layer (pending execution), and a quantified path to resolving it, rather than a
single power number and a caveat.

---

## 10. Figures

The following figures, originally part of the main repository's `figures/` directory, belong to
this study and are not referenced from the current `README.md`:

- **Figure 5 — Cold-start sample construction and RQ1 confirmatory test**
  (`figures/Figure5_coldstart_funnel_and_RQ1_null.png`) — used in §2.1 and §4.1 above.
- **Figure 6 — Cold-start early-signal prediction and intervention-timing simulation**
  (`figures/Figure6_RQ2_horizon_RQ3_lift.png`) — used in §4.2 and §4.3 above.
- **Figure 9 — TOST equivalence tests for the two central null results**
  (`figures/Figure9_tost_equivalence.png`) — used in §5 above.
- **Figure 10 — Integrated framework: structural signal irrelevance across two independent
  tests** (`figures/Figure10_integrated_framework.png`) — originally synthesized this study
  together with the cross-sectional advertiser-size study. It illustrates what the combined
  picture would look like *if* this study were confirmatory; since it is not (§6), the figure is
  retained here as an illustration of the target end-state for the follow-up study proposed in
  §11, not as a claim this repository currently makes.

Regeneration scripts (`make_figure5_*.py`, `make_figure6_*.py`, `make_figure9_*.py`,
`make_figure10_*.py`) remain in `figures/` alongside the scripts for the main study's figures, but
are not invoked by the main study's reproduction steps (root README §12).

---

## 11. What a Properly Powered Follow-Up Would Need

Per §3.5, closing the small-effect gap at even a moderate benchmark (β≈.30) would require roughly
3× the current customer count (~84 customers vs. the current 29) — unreachable within a single
agency's active customer base over the current observation window. A credible follow-up should:

1. **Extend the observation window** and/or **pool across agencies** operating on the same
   platform to reach a customer-level n in the 80–200 range, depending on the target effect size.
2. **Execute the two pending analyses** specified but not yet run in this document: the JZS
   Bayes-factor script (§3.3) and the exact target-effect-size power sweep (§3.5).
3. **Re-run the design-artifact backtest** (Design Artifact section above) at the larger sample
   size, since the current n≈20-customer backtest is explicitly underpowered for its own
   9-percentage-point-scale precision comparison.
4. **Revisit Figure 10's integrated framing** once (and only once) this study's own TOST tests
   reach equivalence or its power against a smaller effect size is credibly established — at
   that point a genuine two-study synthesis, cross-sample and cross-time-axis, would be
   appropriate, and root README's Synthesis section (§6) could be extended to include it, along
   with a corresponding update to the evidence-summary table in `docs/RESULTS_SUMMARY.md`.

Until then, this document stands alone as a well-documented pilot and template, not as
corroborating evidence for the confirmatory cross-sectional finding reported in the main
`README.md`.

**References for this document:** Cohen, J. (1988). *Statistical Power Analysis for the
Behavioral Sciences* (2nd ed.). Gillespie, T. (2014). The relevance of algorithms. In *Media
Technologies*. Rouder, J. N., Speckman, P. L., Sun, D., Morey, R. D., & Iverson, G. (2009).
Bayesian t tests for accepting and rejecting the null hypothesis. *Psychonomic Bulletin &
Review*, 16(2). Stinchcombe, A. L. (1965). Social structure and organizations. In *Handbook of
Organizations*.
