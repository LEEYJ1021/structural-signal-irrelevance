# supplementary_localbiz_exploratory/ — [POST-HOC / EXPLORATORY]

This folder holds the Level 2 exploratory analysis referenced in root README §6. Every
number produced here is post-hoc: none of it was preregistered, and none of it upgrades
the evidence grade of Level 1's H1c null (root README §5). See the root README's evidence
tags before citing anything from this folder.

This folder was simplified from a larger internal working set of scripts and detail
outputs (panel diagnostics, influence diagnostics, mechanism scans, keyword-join
diagnostics, etc. — see `docs/METHODOLOGY_NOTES.md` for the full narrative log of that
process). What remains here is the minimum needed to reproduce the three results actually
cited in the root README:

1. the continuous-share H2 regression (root README §6.1),
2. the serving-structure comparison that motivates P5 (root README §6.2), and
3. the H3 subgroup-dependence test, including the exclusion-size-matched correction
   (root README §6.4, Figure 12).

## Contents

- **`localbiz_core_analysis.py`** — single script, run top to bottom, that:
  - rebuilds the customer × campaign-type spend-composition panel from the four base
    tables (ad performance log, campaign / ad-group / keyword dimensions),
  - re-estimates H1c with continuous campaign-type shares as moderators (replaces the
    original discrete-tier design; see root README §6.1),
  - computes the serving-structure comparison table (keyword-match rate, bid/CPC ratio)
    behind Figure 13,
  - runs the H3 subgroup-dependence test with both a naive random-exclusion placebo and
    the exclusion-size-matched correction described in root README §6.4.

## How to run

```bash
python localbiz_core_analysis.py --data-dir /path/to/AD_Data --out-dir ./detail
```

Outputs are written as a single `localbiz_core_report.json` plus one CSV per major result
table, all in `--out-dir`. No intermediate artifacts beyond what's needed to regenerate
Figures 12 and 13 are produced.

## Reading the output

- Anything under `h2_composition` in the report concerns §6.1 — treat p-values here as
  approximate (small clusters; see root README's small-cluster note in §6).
- Anything under `serving_structure` feeds Figure 13.
- Anything under `h3_subgroup_dependence` feeds Figure 12 and §6.4. The report includes
  both the uncorrected (raw coefficient-shift) ranking and the exclusion-size-matched
  correction, in that order — per the disclosure policy referenced in root README §12,
  the corrected ranking should never be quoted without also showing the uncorrected one.
