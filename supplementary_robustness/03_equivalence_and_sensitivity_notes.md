# Supplementary Robustness 03 — Equivalence & Sensitivity Notes

Feeds root [`README.md`](../README.md) §6.4 and §7.3. Script:
[`03_equivalence_and_sensitivity_notes.py`](03_equivalence_and_sensitivity_notes.py).

---

## 1. Why TOST, and why here specifically

A non-significant p-value does not itself establish that an effect is
absent — it establishes only that the observed effect is not distinguishable
from zero at the chosen alpha, given the sample's power. The two central
null results in the longitudinal extension (§7) are therefore additionally
tested for **formal equivalence** (Two One-Sided Tests, TOST) against a
pre-specified smallest-effect-size-of-interest (SESOI) margin, rather than
being reported as confirmed nulls on p-value grounds alone.

## 2. TOST results

| Test | Observed effect (standardized) | SESOI margin | TOST p | Equivalence established? |
|---|---|---|---|---|
| RQ1: account maturity → initial 30-day growth slope | 0.085 | ±0.20 | .197 | **No** |
| RQ2/H2b: maturity's contribution to within-customer prediction | 0.023 | ±0.05 | .290 | **No** |

**Reading this table.** Neither result reaches formal equivalence — the
observed effect sits inside the equivalence region visually (Figure 9),
but the TOST procedure's own p-value does not clear .05, chiefly because
of the modest sample size (n = 29 customers). This is why §7 throughout is
framed as *directionally supportive*, not as an independently confirmed
null, and is the basis for the associational-language statement in
README §6.4: absence of significance and formal equivalence are treated
as two different, non-interchangeable claims throughout this report.

## 3. SESOI derivation

- **RQ1 margin (±0.20):** set at 40% of the pre-registered large-effect
  detection threshold used in the Step K power simulation (README §7.1,
  standardized β = .50), a conventional fraction for a "practically
  negligible" bound in an underpowered small-cluster design.
- **RQ2/H2b margin (±0.05):** set at half of the smallest within-customer
  LOCO improvement (Δρ ≈ 0.10) that would have been considered practically
  meaningful for the design-artifact use case in §8, so a null that clears
  this margin would licence treating maturity as *usably* irrelevant, not
  merely undetectably so.

## 4. Oster's delta (bid_amount b-path sensitivity)

Oster's delta (Oster, 2019) estimates how much stronger unobserved
confounding would need to be, relative to observed confounding, to fully
explain away the spend → bid_amount coefficient reported in
[`01_alternative_outcome_mediation.md`](01_alternative_outcome_mediation.md).

| Statistic | Value | Numerical-stability flag |
|---|---|---|
| R² (controlled) | 0.192 | — |
| R²-max (Oster's assumption, 1.3×R̃²) | 0.250 | — |
| δ (delta) | 41.7 | **Flagged: numerically unstable** |

**Why this is reported but not used as a robustness claim.** δ is
computed as a ratio whose denominator (R²-max − R²-controlled) is small
here (0.058), which inflates δ and makes it highly sensitive to small
perturbations in R²-max — a large δ in this regime reflects numerical
instability in the denominator, not necessarily genuine robustness to
confounding (per Appendix C, methodological principle 7). It is retained
here transparently rather than cited anywhere in the main report as
supporting evidence.

## 5. Reference

Oster, E. (2019). Unobservable selection and coefficient stability:
Theory and evidence. *Journal of Business & Economic Statistics*, 37(2),
187–204.
