# Boundary Conditions: Is the Spend-Controlled Size Effect Homogeneous?

**Supports:** root README §2.5, §5

This file tests whether Study 1's central null result (size has no direct effect on outcomes once spend is controlled) holds uniformly, or whether it varies across meaningful strata. Two strata are tested: campaign product type (a platform-defined classification, well-measured) and keyword review status (a proxy for platform discretion, poorly powered in this dataset). A third candidate stratification — advertiser industry — was piloted and is reported at the end of this file with an explicit reliability caveat; it is not used to support any claim in the root README.

## 1. Campaign product type (load-bearing for §2.5)

`campaign_type` is a platform-defined ad-product code (1 = website, 2 = shopping, 4 = brand/new-product, 6 = local business), not an industry classification. Each customer is assigned their dominant product type by spend share, and the CPC-based spend-controlled model (§2.4) is re-estimated within each type with n≥15 customers.

| Product type | n (rows) | n (customers) | c' (size), net of spend | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | -0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |

**Joint Wald test for size × product-type interaction:** p = .023 — the size-net-of-spend relationship is not homogeneous across product types.

**What this does and does not mean.** No individual stratum shows a significant size effect (all p > .05), so the headline null from §2.2–2.4 is not overturned within any single stratum. What the joint test indicates is that the *degree* to which size is irrelevant varies somewhat by ad-product category — consistent with the boundary-condition argument in root README §5, where the mechanism (auction-based, unit-level evaluation) is expected to hold directionally across contexts while its exact magnitude is shaped by platform-specific policy layers that differ by product type (e.g., shopping campaigns route through a different approval pipeline than standard search campaigns on this platform).

*Caveat:* this uses the CPC-based outcome, which carries the mechanical cost-sharing component documented in [`01_alternative_outcome_mediation.md`](01_alternative_outcome_mediation.md); the heterogeneity finding should be read as a heterogeneity in the (partly mechanical) CPC coefficient, not as a confirmed heterogeneity in the underlying behavioral relationship.

## 2. Keyword review status (preliminary, supports §5's discretion discussion)

Keyword-level `inspect_status` distinguishes approved keywords (code 20, 99.5% of keywords) from keywords under review (code 10, 0.23%) or restricted approval (code 30, 0.31%); no keywords in this dataset carry the "held" status (code 40) defined in the platform's codebook. This is the closest available proxy for platform discretion in this dataset — a channel through which account-level attributes could plausibly re-enter the allocation process despite the real-time bidding mechanism.

Three overlapping definitions of "non-standard status" were tested (under-review only; restricted-approval only; both combined) because they are not independent tests of different hypotheses — restricted-approval alone accounts for most of the combined definition's customer count (106 of 111 customers). This should be read as one underlying signal probed three ways, not three independent confirmations.

| Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
|---|---|---|---|
| Under-review only | 22 | 230 | .638 |
| Restricted-approval only | 106 | 146 | .016 |
| Combined | 111 | 141 | .016 |

The combined definition's significance is driven almost entirely by the restricted-approval component, not by an independent contribution from the under-review component. Restricted-approval, per the platform's codebook, denotes an *already-resolved* non-standard approval outcome rather than a pending discretionary review — so while this result is directionally interesting, it does not cleanly map onto the "discretionary review as a channel for account-attribute leakage" mechanism that motivated the check. Given the very small stratum sizes (0.2–0.3% of keywords each), this is reported as a preliminary, exploratory finding, not as a confirmatory test of a boundary condition. It should not be read as either confirming or ruling out discretion-based channels; the dataset lacks the power to do so.

## 3. Industry (exploratory pilot, not used to support any claim)

An attempt was made to construct an industry proxy from campaign/ad-group text using multilingual sentence embeddings, UMAP + HDBSCAN clustering, and a four-model local-LLM ensemble forced to select among Korean Standard Industrial Classification (KSIC) categories. Inter-rater reliability across the LLM ensemble (Randolph's free-marginal kappa = 0.557) and cross-validation against an independent keyword-rule classifier (Cohen's kappa = 0.363) both indicate moderate-at-best label reliability. Given this, industry-stratified results are not reported as evidence for any claim in this repository; the pipeline and reliability diagnostics are retained here only for transparency and as a candidate direction for future work with a higher-reliability industry label source.
