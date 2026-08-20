# Supplementary Robustness 04 — Design Artifact: Full Backtest Grid & Future Work

This is a working companion to the canonical artifact spec,
[`docs/DESIGN_ARTIFACT.md`](../docs/DESIGN_ARTIFACT.md), and to root
[`README.md`](../README.md) §8. Script:
[`04_design_artifact_future_work.py`](04_design_artifact_future_work.py).

---

## 1. Full nine-specification backtest grid

Own-signal precision at the 30% flagging threshold vs. a random-flagging
baseline, within-customer, varying the minimum active-days threshold
(5/7/10) and the early/later window pair:

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

Own-signal precision exceeds the random baseline in **4 of 9
specifications (44%)**. At n ≈ 20 customers per spec, this pattern is not
distinguishable from chance — reported plainly, not rounded up to a
"generally wins" claim.

## 2. Why the naive size/tenure comparison was dropped, not just reported as "loses"

Account maturity is a customer-level constant. Within-customer demeaning —
required to isolate the same within-customer signal DP1 claims matters —
collapses the naive rule's predictions to numerical zero in every
specification (residual SD ~1e-17, i.e., floating-point noise). The naive
rule therefore has **no within-customer predictive content by
construction**: there is nothing for the own-signal rule to beat on this
axis, so "naive vs. own-signal" is not a meaningful contest and is not
reported as one (full derivation: `docs/METHODOLOGY_NOTES.md`, entry 9).

## 3. Relationship to the continuous-scale §7.2 result

README §7.2's result is a **continuous-scale** finding (Spearman ρ on
continuous predicted growth), well-powered and significant at short
horizons (14-day within-customer LOCO ρ up to ≈0.49). This backtest asks a
**much coarser** question — does thresholding that signal into a binary
"flag the bottom 30%" decision produce a detectable precision advantage
at n ≈ 20 customers — and the answer is that this specific binary-decision
framing lacks the power to resolve the question either way. This is not a
contradiction of §7.2 and should not be read as one.

## 4. Recommended next steps

1. **A larger cold-start sample.** The current n ≈ 20-customer backtest is
   underpowered for a 9-percentage-point-scale precision comparison.
2. **A continuous-scale evaluation** of the flagging rule's utility (e.g.,
   a full precision–recall curve across thresholds), reported in the same
   continuous-metric terms as §7.2 rather than as a single-threshold
   binary win/loss.
3. **A held-out replication window**, once enough calendar time has
   elapsed to construct an independent cold-start cohort, to check whether
   the 4/9 pattern above is stable or itself noise.
