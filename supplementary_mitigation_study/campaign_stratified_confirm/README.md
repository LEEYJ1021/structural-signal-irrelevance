# supplementary_mitigation_study/campaign_stratified_confirm/

Reproduction scripts for root `README.md` §16.3.1, "M2/M3 extended — Campaign-stratified
(S9) independent re-test." See `docs/METHODOLOGY_NOTES.md` entries B10 (finding) and B11
(methodological incident) for the full narrative.

## Why this exists

M2/M3 (root README §16.3) independently re-tested the **Size-blind** mitigation strategy
against four pre-specified model classes, but left the other M1-scan candidates —
Spend-normalized, Campaign-adaptive, and the residualized/worst-group variants — without
the same treatment (§16.6, outstanding validation debt). Advisor feedback separately asked
for a comparison of "the pooled model vs. a model that distinguishes campaign type," which
is the **Campaign-stratified (S9)** strategy, not Size-blind. This subfolder closes that
gap: it re-tests S9 with exactly the same protocol used for Size-blind in M2/M3 — four
model classes, customer-level 5-fold out-of-fold (OOF) evaluation, 200-rep
customer-cluster bootstrap — rather than comparing a pooled model to a
campaign-type-stratified model on different, non-comparable samples.

## Run order

```bash
# 1) OOF cross-validation re-test of 4 models x 3 strategies (S1/S9/S9+S1), 200-rep bootstrap
python rq3_confirm_v2_campaign_stratified_full.py
#   -> rq3_confirm_v2_bootstrap_raw.csv, rq3_confirm_v2_verdict.csv

# 2) Recompute OLS x {S9_Campaign_stratified, S9_plus_S1} only, with near-constant-column
#    removal, and merge back in (the other 10 combinations reuse step 1's output as-is)
python rq3_confirm_v2_patch_ols_stratified.py
#   -> rq3_confirm_v2_bootstrap_raw_patched.csv, rq3_confirm_v2_verdict_patched.csv
#   -> rq3_confirm_v2_dropped_columns_log_patch.csv

# 3) Compute mean/CI alongside median/IQR for every combination, and auto-flag any
#    combination with an unstable right tail (post-processing only, no refitting)
python rq3_confirm_v2_robust_summary_postprocess.py
#   -> rq3_confirm_v2_robust_summary.csv

# 4) Generate Figure 19 (lives under figures/scripts/, reads only the artifacts above)
python ../../figures/scripts/figure19_campaign_stratified_model_class_bootstrap.py
#   -> figures/Figure19_campaign_stratified_model_class_bootstrap.png
```

## Summary finding (entry B10)

Independently re-testing Campaign-stratified (S9) with the same four model classes used
for Size-blind in M2/M3, 0 of 4 combinations show a simultaneous, statistically
significant improvement across ΔRMSE, Δsize_gap, and Δlocalbiz_gap. This is consistent
with Campaign-adaptive never triggering the M0 pre-registered gate in the first place. For
OLS specifically, the local-business gap is significantly **worse** on a median basis —
the same direction already observed for Size-blind × OLS/HistGB (§16.3, M2/M3). This is
read as suggestive evidence that linear/inflexible model classes tend to harm
local-business fairness, independent of which mitigation strategy (dropping the size
feature vs. stratifying by campaign type) is applied.

## Methodological-incident summary (entry B11)

- The initial version of the re-test script used in-sample prediction (predicting on the
  same rows used for training within each bootstrap draw). This produced an overfitting
  artifact that showed as a uniform, unnatural-looking "improvement" across every model
  class — particularly severe for Campaign-stratified, where the sample is split by
  campaign type and each split is small. This was corrected by switching to
  customer-level 5-fold OOF evaluation.
- After the OOF correction, two combinations — OLS × S9_Campaign_stratified and
  OLS × S9_plus_S1 — still showed separately unstable upper confidence bounds (14–25),
  10–40x wider than every other combination. This is attributed to near-constant columns:
  within the local-business subgroup, the remaining campaign-share columns lose nearly
  all variance, which makes the OLS design matrix close to singular.
- Two fixes were applied: (1) a per-fold safeguard that drops near-constant columns from
  both train and test sets (drop log: `rq3_confirm_v2_dropped_columns_log_patch.csv`),
  which brought the unstable upper bound down from 25 to 3.9; (2) even after that fix, a
  residual right-tail instability remained for these two combinations only
  (tail_ratio 7–12x), so those two cells are reported as median/IQR instead of the usual
  mean-based 95% CI — a departure from M2/M3's original reporting convention, disclosed
  explicitly here rather than silently applied.

## File list

| File | Role |
|---|---|
| `rq3_confirm_v2_campaign_stratified_full.py` | Step 1: full OOF-based re-test |
| `rq3_confirm_v2_patch_ols_stratified.py` | Step 2: near-constant-column patch for OLS×stratified |
| `rq3_confirm_v2_robust_summary_postprocess.py` | Step 3: median/IQR and instability flags |

## Caveats (see root README §16.6 and §11 Limitations 12–15 for the full M-series list)

- `S9_plus_S1` (Campaign-stratified combined with Size-blind) was not part of the original
  M1 scan; this re-test is its only evidence source, so it should not be adopted on the
  strength of this result alone.
- The OLS-specific median/IQR reporting departs from M2/M3's mean/95%-CI convention for
  these two cells only; it is not a repository-wide change in reporting practice.
- Whether the instability's root cause is the absence of regularization (vs. a
  weakly-regularized Ridge baseline) or the linear-model structure itself has not yet
  been separated — flagged as a candidate next step, not resolved here.
