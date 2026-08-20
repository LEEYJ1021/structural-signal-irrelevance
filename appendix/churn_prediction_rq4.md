# Appendix: Exploratory Churn-Prediction Check (RQ4)

**This appendix sits entirely outside the H1/H2 confirmatory hypothesis family in the root [`README.md`](../README.md). It is retained for transparency because the analysis had already been run as part of an earlier-generation pipeline, not because it bears on the paper's central claim.** Readers primarily interested in the structural-blindness finding can skip this appendix without loss of continuity.

---

**RQ4.** *Can advertiser account churn be predicted from approval, cost, and efficiency features?*

![Figure 4 | Churn-prediction benchmarking](../figures/Figure4_churn_benchmark.png)

**Figure 4.** Across 213 labeled accounts (a 2.35% churn rate), tree-based models nominally outperform logistic regression in nested cross-validation, but every pairwise model comparison returns the same Wilcoxon p-value (0.0625) — the mathematical floor achievable with only 5 repeat-pairs, not evidence of a real difference. Random forest had the best-calibrated out-of-fold predictions (Brier score 0.0250).

## Interpretation and caveats

- The labeled sample (n = 213, 2.35% churn rate) is small and severely class-imbalanced; the reported ROC-AUC and Brier-score comparisons should be read as descriptive benchmarking, not a confirmed model-superiority claim.
- Every pairwise model comparison is statistically floored at p = 0.0625 by the repeat-pair count (n = 5) alone — this is a property of the test design, not a substantive near-significance finding, and should not be described as "trending toward significance."
- F1 = 0 for all models at the default 0.5 threshold is expected given the class imbalance and is reported for transparency, not as a model failure.
- Nested-CV AUC estimates are lower than the fixed-hyperparameter baseline for tree-based models, consistent with the removal of optimistic tuning bias rather than genuinely worse models.

## Recommendation

Given the sample-size and statistical-floor issues above, this appendix is kept as a brief, clearly-labeled exploratory check. It should not be cited as supporting evidence for any claim about advertiser size, spend, or algorithmic fairness in the main report.
