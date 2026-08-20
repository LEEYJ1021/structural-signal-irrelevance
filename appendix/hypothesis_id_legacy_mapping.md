# Appendix: Hypothesis-ID and Figure-Label Reconciliation

The nine figure files referenced throughout the root [`README.md`](../README.md) were generated across two rounds of internal labeling ("RQ1," "RQ2," "H2b," and so on) baked into the image titles before the current hypothesis-ID scheme (H1a/b/c, H2, §7's RQ-maturity, etc.) was finalized. This table is the permanent cross-reference, so any given figure can be traced unambiguously to the hypothesis it currently tests. A superseded label is never deleted or silently dropped — it remains here with a pointer to what replaced it, so any revision to the hypothesis framing stays auditable.

| Current ID (root README) | Legacy label(s) in figure titles | What it claims | Status |
|---|---|---|---|
| P0 (preliminary) | Figure 1's "(RQ1)" | Performance variance sits mostly at ad-group/residual level, not customer level | Descriptive; motivates but does not test H1 |
| H1a | (unlabeled a-path) | Size → total spend | Confirmed, p < .001 |
| H1b | (unlabeled b-path) | Spend → outcome, controlling for size | Confirmed, p = .032 (bid_amount-based) |
| H1c | Figure 2's "(RQ2, H2b)"; Figure 3's "(RQ2 robustness suite)" | Size → outcome, controlling for spend = 0 | Confirmed null, 8 robustness checks |
| H1 (composite) | — | Indirect association accounts for the entire size–outcome relationship | Supported |
| H2 | Figure 8's "(joint Wald test)" | H1c's null is homogeneous across `campaign_type` strata | Rejected, p = .023 (heterogeneous) |
| §9.1-review | §5(a) keyword-review-status check | Does discretionary review leak account attributes into outcomes? | Exploratory, underpowered |
| RQ4 | Figure 4's legacy "(RQ3, exploratory appendix)" label | Can churn be predicted from approval/cost/efficiency features? | Exploratory, moved to [`appendix/churn_prediction_rq4.md`](churn_prediction_rq4.md), outside the H1 family |
| §7.1-Maturity | Figure 5's "H1 (RQ1)" | Account maturity → initial 30-day growth slope | Null (non-sig); TOST inconclusive |
| §7.2-EarlySignal | Figure 6's "RQ2" / "H2a" | Ad group's own early signal → later growth | Supported, decays with horizon |
| §7.2-MaturityAdd | Figure 6's "RQ2" / "H2b" | Adding account maturity improves early-signal prediction | Rejected; TOST inconclusive |
| §7.2-Flagging | Figure 6's "RQ3" | At what post-registration day should a low-growth ad group be flagged? | Exploratory, directional not precise |

**A note on a dropped label.** An earlier internal draft also carried a formal ID "RQ3" for a piloted advertiser-industry stratification. That check was dropped from the confirmatory hypothesis family entirely due to unusable label reliability (see [`exploratory_industry_classification.md`](exploratory_industry_classification.md)) and does not appear in the table above. The legacy figure-title text "RQ3" appearing on Figure 4 is unrelated — it is a pre-relabeling name for what this table now calls RQ4.

**Naming convention.** `Hx` = a formally testable hypothesis with a directional or point-null prediction. Unlabeled §-prefixed IDs (e.g., §7.1-Maturity) = a question investigated without a single confirmatory point-null (exploratory, preliminary, underpowered, or design-oriented). `P0` = a preliminary/descriptive analysis that motivates a hypothesis but does not itself test one.
