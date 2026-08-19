# Early-Flagging Design Artifact and Its Empirical Backtest

**Supports:** root README §3.4

## The design artifact

Section 3.3's within-customer result — an ad group's own early signal predicts its near-term growth, and account maturity adds nothing at the within-customer level — motivates a concrete decision rule for flagging underperforming ad groups early. The rule is specified below as a design artifact in the design-science sense: an explicit, implementable input/output specification, grounded in a stated empirical result, rather than a vague recommendation.

**Artifact: Ad-Group Early Warning Flagging Rule**

- **Input:** `predicted_growth_rank_percentile` (float, [0,1]) — an ad group's predicted growth rank among its cohort, from a model using only that ad group's own early-window features; `day_since_registration` (int)
- **Output:** `flag` (bool), `reason` (str)
- **Parameters:** `flag_threshold` = 0.30; valid decision window = day 7–21 post-registration
- **Design principles:**
  - **DP1.** Base flagging solely on the ad group's own early-period signal (coverage, spend trend, CTR/CVR) — never on account-level history, per §3.3.
  - **DP2.** Evaluate at any point within a bounded window (day 7–21) rather than committing to a single fixed day, per §3.4's finding that no single cutoff is statistically distinguishable as optimal.
  - **DP3.** Threshold on relative rank (percentile) within the observed cohort rather than on an absolute growth value, since growth magnitudes are not comparable across heterogeneous ad groups.

## The empirical backtest, and why it is not reported as a confirmed result

A backtest compared this rule's flagging precision against a naive alternative based on account size/tenure, using within-customer-demeaned predictions (to isolate the same within-customer signal that DP1 claims matters) and a 30% flagging threshold, across nine (active-day-threshold × early-window × later-window) specifications.

**A structural finding, not a bug.** Account maturity is a customer-level constant. Within-customer demeaning of a prediction built from a customer-level constant collapses that prediction to numerical zero in every specification tested (residual standard deviation on the order of 1e-17, i.e., floating-point noise). This is the correct and expected behavior, not an error: it is the same fact demonstrated analytically in §3.3's within/between decomposition, now confirmed in a second, independent (binary-flagging) frame. It means the naive size/tenure rule has **no within-customer predictive content by construction**, so a "naive wins" or "own-signal wins" comparison against it is not a meaningful contest — there is nothing for the own-signal rule to beat on this axis.

**What can be evaluated instead: own-signal against a random baseline.** With the naive comparison ruled out as ill-posed, the own-signal rule's precision was compared against random flagging at the same threshold, across the same nine specifications (n≈20 customers, ≈200 ad groups each). Own-signal precision exceeded the random baseline in 4 of 9 specifications and underperformed it in 5. At this sample size, this pattern is not distinguishable from chance and is **not reported as a confirmed empirical advantage** for the flagging rule.

**Why this does not contradict §3.3.** Section 3.3's result is a continuous-scale finding (Spearman ρ on continuous predicted growth), well powered and significant at short horizons. This backtest instead asks a much coarser question — does thresholding that continuous signal into a binary "flag the bottom 30%" decision produce a precision advantage detectable at n≈20 customers — and the answer is that this specific binary-decision framing does not have enough power to resolve the question one way or the other. A continuous signal being predictive does not guarantee that any particular binarization of it is empirically distinguishable from random at a small sample size; these are different statistical questions with different power requirements.

## How this is used in the main text

Per root README §3.4, the design principles (DP1–DP3) are presented as **theoretically grounded** in §3.3's confirmed within-customer result, not as an empirically validated decision rule. The binary-flagging backtest above is not cited as supporting evidence for the artifact's practical superiority over alternatives. We recommend this as a specific, well-defined direction for future work: a larger cold-start sample, and/or a continuous-scale (rather than binary-threshold) evaluation of the flagging rule's utility, would be needed to empirically validate the artifact rather than only theoretically motivate it.
