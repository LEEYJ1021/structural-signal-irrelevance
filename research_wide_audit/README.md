# research_wide_audit/ — [CROSS-CUTTING]

This folder holds the audit referenced in root README §7 (research-wide multiplicity
audit) and §5.3 (H1c core-model influence diagnostic). Unlike
`supplementary_localbiz_exploratory/`, this audit applies to **both** Level 1 and Level 2:
it asks whether the project's confirmatory backbone (H1c) holds up once every officially
reported statistic in the repository is considered together, not whether any individual
Level 2 finding is robust.

This folder was simplified from a larger internal audit (cluster-SE validity checks,
unexplored-moderator scans, spec-curve selective-reporting review, temporal-precedence
checks, and merge-point coverage audits — see `docs/METHODOLOGY_NOTES.md` for the full
narrative). What remains here is the minimum needed to reproduce the two results actually
cited in the root README:

1. the pooled 25-test multiplicity table behind Figure 14 (root README §7), and
2. the H1c core-model DFBETA/leave-k-out influence check (root README §5.3), run here
   for the first time directly on the confirmatory model rather than on a Level 2
   sub-analysis.

## Contents

- **`research_wide_audit_core.py`** — single script that:
  - pools the 25 officially-reported p-values from across the repository (hard-coded list,
    sourced from `docs/RESULTS_SUMMARY.md`) and applies Bonferroni and BH-FDR correction,
  - re-fits the H1c core model (`log_cpc ~ spend_z + size_z`) on the full Level 1 sample,
    computes customer-level DFBETA, and reports leave-k-out sensitivity for k = 1, 3, 5, 10.

## How to run

```bash
python research_wide_audit_core.py --data-dir /path/to/AD_Data --panel-csv /path/to/h2_composition_panel.csv --out-dir ./detail
```

`--panel-csv` should point at the panel produced by
`supplementary_localbiz_exploratory/localbiz_core_analysis.py` (or an equivalent
customer-level panel with `log_cpc`, `spend_z`, and `size_z`).

## Reading the output

`research_wide_audit_report.json` has two top-level keys:

- `multiplicity_audit` — the pooled correction table behind Figure 14. Read this
  alongside root README §7: it is not a criticism of any individual result, but a
  calibration device so no single exploratory finding is over-weighted.
- `h1c_core_influence` — the DFBETA / leave-k-out diagnostic behind root README §5.3.
  As reported there, none of the four pre-specified exclusion configurations changed the
  H1c significance verdict.
