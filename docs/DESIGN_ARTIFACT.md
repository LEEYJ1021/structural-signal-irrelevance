# Design Artifact: Ad-Group Early Warning Flagging Rule

**This is the canonical specification.** The root [`README.md`](../README.md) §8 summarizes this artifact; cite this file for the full schema, parameters, and backtest grid.

---

## 1. Motivation

Section 7.2 of the root README establishes a confirmed within-customer result: an ad group's own early operating signal (coverage, spend trend, CTR/CVR) predicts its near-term growth, and adding account maturity produces no within-customer improvement at any tested horizon. This motivates a concrete, implementable decision rule — specified below as a design artifact in the design-science-research sense: an explicit input/output specification grounded in a stated empirical result, rather than a general recommendation.

## 2. Specification

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

- **DP1.** Base flagging solely on the ad group's own early-period signal — never on account-level history (grounded in §7.2's within-customer result).
- **DP2.** Evaluate at any point within a bounded window (day 7–21) rather than committing to a single fixed day (grounded in Figure 6C–D: no cutoff is statistically distinguishable as optimal).
- **DP3.** Threshold on relative rank (percentile) within the observed cohort rather than an absolute growth value, since growth magnitudes are not comparable across heterogeneous ad groups.

## 3. Empirical backtest

### 3.1 Why the naive (size/tenure) comparison is structurally ill-posed

Account maturity is a customer-level constant. Within-customer demeaning — required to isolate the same within-customer signal that DP1 claims matters — collapses a prediction built purely from a customer-level constant to numerical zero in every specification tested (residual SD ~1e-17, i.e., floating-point noise, not a substantive near-zero effect). This is expected and correct: it is the same fact demonstrated analytically in §7.2's within/between decomposition, now independently confirmed in a binary-flagging frame. It means the naive rule has **no within-customer predictive content by construction**, so a "naive wins / own-signal wins" framing is not a meaningful contest on this axis — there is nothing for the own-signal rule to beat.

### 3.2 What was measured instead: own-signal vs. random baseline

With the naive comparison ruled out, own-signal precision at the 30% flagging threshold was compared against a random-flagging baseline, within-customer, across nine specifications varying the minimum active-days threshold (5 / 7 / 10) and the early/later window pair.

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

**Own-signal precision exceeded the random baseline in 4 of 9 specifications (44%).** At this sample size (n ≈ 20 customers per spec), this pattern is not distinguishable from chance.

### 3.3 Relationship to §7.2's confirmed result

Section 7.2's result is a **continuous-scale** finding (Spearman ρ on continuous predicted growth), well-powered and significant at short horizons (14-day within-customer LOCO ρ up to ≈0.49). This backtest asks a **much coarser** question — does thresholding that continuous signal into a binary "flag the bottom 30%" decision produce a precision advantage detectable at n ≈ 20 customers — and the answer is that this specific binary-decision framing lacks the power to resolve the question either way. A continuous signal being predictive does not guarantee that any particular binarization of it is empirically distinguishable from random at a small sample size; these are different statistical questions with different power requirements. This is **not a contradiction** of §7.2, and should not be read as one.

## 4. Status and recommended next step

DP1–DP3 are **theoretically grounded** in the confirmed §7.2 result. They are **not yet empirically validated** as superior to alternatives in binary-decision form. Recommended next step: (a) a larger cold-start sample (the current n ≈ 20-customer backtest is underpowered for a 9-percentage-point-scale precision comparison), and/or (b) a continuous-scale evaluation of the flagging rule's utility (e.g., a precision-recall curve across thresholds rather than a single 30% cutoff), reported in the same continuous-metric terms as §7.2 rather than as a binary win/loss against a naive baseline.

## 5. Version note

An earlier internal version of this backtest reported a naive-rule "victory" at several window specifications. That result was a computational artifact: the naive predictions had not been within-customer demeaned before ranking, so the comparison implicitly re-injected the same between-customer signal that §7.2's decomposition explicitly excludes. The corrected, within-customer-demeaned version (§3 above) is the one reported here and in the root README; the artifact and its correction are logged for transparency in [`METHODOLOGY_NOTES.md`](METHODOLOGY_NOTES.md).
