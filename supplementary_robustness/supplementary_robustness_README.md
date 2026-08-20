# Supplementary Robustness Analyses

Four independently runnable analyses, each mapped to a specific section of
the root [`README.md`](../README.md). Run all four with
`bash run_supplementary_robustness.sh` from the repository root, or run any
one script standalone — each reads its own upstream artifact and falls back
to the literal values already reported in its companion `.md` file if that
artifact is absent, so every script (and every figure script that consumes
its JSON output) remains reproducible without the full pipeline.

| File | Feeds | Figure |
|---|---|---|
| [`01_alternative_outcome_mediation.md`](01_alternative_outcome_mediation.md) / `.py` | README §5.4 (methods 7–8) | Figure 7 |
| [`02_boundary_conditions.md`](02_boundary_conditions.md) / `.py` | README §5.5, §9a | Figure 8 |
| [`03_equivalence_and_sensitivity_notes.md`](03_equivalence_and_sensitivity_notes.md) / `.py` | README §7.3, §6.4 | Figure 9 |
| [`04_design_artifact_future_work.md`](04_design_artifact_future_work.md) / `.py` | README §8 | — (backtest table only) |

Each script writes a JSON artifact to `outputs/supplementary_robustness/`,
consumed downstream by the matching `figures/make_figure*.py` script.
Nothing here duplicates `docs/METHODOLOGY_NOTES.md` — that file explains
*why* an estimator was chosen; these files report *what the chosen
estimator found*, in reproducible detail.
