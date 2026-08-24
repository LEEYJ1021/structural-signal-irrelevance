# `supplementary_mitigation_study/` — M1–M3 Algorithmic Mitigation Study

> **[POST-HOC / EXPLORATORY]** This folder implements the analysis behind root
> [`README.md`](../README.md) §16 and [`docs/RESULTS_SUMMARY.md`](../docs/RESULTS_SUMMARY.md)
> §§12–14. It is a further, later-added post-hoc extension of RQ2a–RQ2c
> (`supplementary_localbiz_exploratory/`), asking whether the local-business-concentrated
> disparity documented there can be *reduced* by an algorithmic design choice at
> model-input time. Nothing in this folder changes the evidence grade of H1, H2, or
> RQ2a–RQ2c.

## Naming

Every script and identifier in this folder uses this repository's own naming — **M0** (the
pre-registered gate), **M1** (the exploratory scan), **M2** (the independent re-test
design), **M3** (the headline model-class pattern) — never any legacy pipeline label. See
`docs/METHODOLOGY_NOTES.md`, entry B8, for why that naming discipline was applied to this
folder *before* it was drafted, rather than corrected afterward.

## What's in this folder

This folder holds the **code**, not its output. Running the three scripts below in order
regenerates every M-series statistic reported in root README §16 and
`docs/RESULTS_SUMMARY.md` §§12–14, and every data point plotted in Figures 16–18
(`figures/scripts/`). No CSV/JSON result files are checked into this folder — they are
regenerated artifacts, not source; see `data/README.md` for the schema-compatible extract
each script expects as input.

| File | Stage | Produces (when run) |
|---|---|---|
| `mitigation_common.py` | Shared library | Strategy definitions (Baseline, Size-blind, Spend-normalized, Campaign-adaptive, + post-hoc variants), the three tracked metrics (RMSE, size_gap, localbiz_gap at configurable cutoffs), and the customer-cluster bootstrap used by all three stages |
| `step_m0_pregate.py` | **M0 — pre-registered gate** | `gap_diff` bootstrap CIs for 2 candidate strategies (Size-blind, Campaign-adaptive) × 2 representative models (OLS, HistGB-MAE), fixed before any exploratory scan. Gates whether M1 proceeds. |
| `step_m1_exploratory_scan.py` | **M1 — exploratory scan** | Repeated 5-fold × 30-repetition customer-shuffle CV across up to 12 strategies × 9 models × 4 local-business cutoffs; Wilcoxon signed-rank + Benjamini–Hochberg FDR across all resulting tests; a winner's-curse bootstrap check restricted to the two FDR-flagged candidates for which comparable earlier tooling exists (OLS, HistGB-squared) |
| `step_m2_m3_model_class_bootstrap.py` | **M2 design → M3 result** | An independent, customer-cluster bootstrap (200 reps) for the Size-blind strategy crossed with four model classes pre-specified for theoretical representativeness (OLS, HistGB, RandomForest, SVR-RBF) — the one M-series result reported at higher confidence than M1's raw scan |

## Why the gate (M0) matters

Per `docs/METHODOLOGY_NOTES.md` entry B9, no individual FDR-significant cell from M1's wide
scan is treated as evidence on its own — a wide search is expected to produce
FDR-significant candidates even absent a real effect. `step_m0_pregate.py` runs first and
independently: only because its gate did not trigger (all four gate cells' 95% CIs included
0) did the analysis proceed to the explicitly-labeled exploratory scan (M1) followed by the
independent, pre-specified re-test (M2/M3), rather than a single undifferentiated pass. See
Figure 18 (root README §16.1) for the process diagram this sequencing produces.

## Running the pipeline

```bash
# from the repository root, with a schema-compatible extract in place (see data/README.md)
python supplementary_mitigation_study/step_m0_pregate.py
python supplementary_mitigation_study/step_m1_exploratory_scan.py
python supplementary_mitigation_study/step_m2_m3_model_class_bootstrap.py

# then regenerate the figures that read these outputs
python figures/scripts/figure18_mitigation_evidentiary_process.py
python figures/scripts/figure17_strategy_model_landscape.py
python figures/scripts/figure16_mitigation_model_class_bootstrap.py
```

Each `step_*.py` script writes its own result artifacts (CSV/JSON) under this folder as it
runs; those artifacts are not checked into the repository (see `.gitignore`) because they
are fully reproducible from the raw extract and the code here.

## Scope note

This folder does not depend on, and is not depended on by,
`supplementary_localbiz_exploratory/` (RQ2a–RQ2c) at the code level — it consumes the same
customer-level panel but re-derives every feature and metric it needs. It also does not
depend on `docs/DESIGN_ARTIFACT.md`'s ad-group flagging rule, which belongs to the
descoped Study 2 companion and shares no sample, model, or outcome variable with the
M-series.
