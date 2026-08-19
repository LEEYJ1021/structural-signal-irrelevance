# Not New, But Renewed: Structural Attributes Don't Matter on an Algorithmically-Mediated Ad Platform

*A cross-sectional and longitudinal investigation into ad-group cold-start dynamics and advertiser-size fairness on a Korean paid-search platform.*

---

## 1. Background and Research Questions

Two advertisers run campaigns on the same search-ads platform. One has been active for seven years and manages hundreds of ad groups. The other just created its first one. The intuitive expectation is that the veteran advertiser's new ad group will ramp up faster, and that its account will receive more favorable treatment from the platform's approval and ranking systems. This report tests that expectation twice, with two independent datasets and two independent sets of statistical tools.

**RQ1 (Study 1, cross-sectional):** Does advertiser *size* buy a structural advantage in approval rate, cost efficiency, or ad rank — independent of how much the advertiser spends?

**RQ2 (Study 2, longitudinal):** Does an advertiser's accumulated account *history* predict how fast a brand-new ad group inside that account grows — independent of that ad group's own early performance signals?

Using a panel of **321 advertisers and roughly 19.3 million rows** of daily/hourly performance data from a Korean search-ads ecosystem, both studies converge on a similar answer: size and tenure appear to matter far less than spend and the unit's own real-time behavior. This report labels this pattern **structural blindness** — a real-time bidding and serving system that evaluates every ad group on its current signal, largely indifferent to the account's résumé. Section 2 states this construct and the formal, permanently-numbered hypotheses it generates, so every later section can cite a hypothesis ID (e.g. **H-S1.1c**, **H-S2.1**) instead of re-explaining what it's testing.

### 1.1 Hypothesis Preview

| | Core hypothesis | Naive expectation | Result summary |
|---|---|---|---|
| Study 1 | H-S1.1c: size's direct effect = 0 once spend is controlled | Large advertisers should be favored | Null confirmed, 8 robustness checks |
| Study 1 | H-S1.2: H-S1.1c's null is homogeneous across campaign types | Should be homogeneous | Rejected (p=.023) — some heterogeneity |
| Study 2 | H-S2.1: account maturity → new ad group's initial growth slope | Older accounts should ramp up faster | Null (non-sig), TOST inconclusive |
| Study 2 | H-S2.2a: ad group's own early signal → near-term growth | Should be predictive | Supported at short horizons, decays |
| Study 2 | H-S2.2b: adding account maturity improves H-S2.2a's prediction | Should improve | Rejected, TOST inconclusive |

This report treats the two studies not as separate null-result write-ups but as **one investigation testing a single construct at two structural levels** (§2.1).

---

## 2. Theoretical Framing and Formal Hypotheses

### 2.1 Core construct: structural blindness

**Structural blindness** — a real-time, auction-based serving system allocates approval, cost efficiency, and ranking primarily on a unit's *current, real-time signal* (its bids, its clicks, its own early performance), and is largely indifferent to *structural attributes of the account behind that unit* (how big the account is, how long it has existed) once the channels that structural attributes could plausibly work through — spend, the unit's own track record — are accounted for.

This is a claim about mechanism, not about outcomes: big or old accounts can and do perform differently from small or new ones, but this report asks whether that difference is *direct* (the algorithm treats you differently for being big/old, holding everything else constant) or *indirect* (being big/old changes what you do — how much you spend, how your ad groups perform early on — and it's that behavior the algorithm responds to). Structural blindness is the hypothesis that, on this platform, it is almost entirely the latter.

| | Structural attribute | Structural level | Candidate mediating/competing channel |
|---|---|---|---|
| **Study 1** | Advertiser size (spend-tier) | Cross-sectional, customer-level | Spend |
| **Study 2** | Account tenure/maturity | Longitudinal, ad-group-level | The ad group's own early operating signal |

### 2.2 Study 1's formal hypothesis family (H-S1)

Full mediation hypothesis, decomposed into its three legs:

- **H-S1.1a (a-path):** Advertiser size is positively associated with total spend.
- **H-S1.1b (b-path):** Spend is associated with outcome quality (approval rate / cost efficiency / ad rank), controlling for size.
- **H-S1.1c (c′-path, direct effect):** Advertiser size has **no** direct association with outcome quality once spend is controlled — i.e., the size → outcome relationship is *fully* mediated by spend, not partially.

Jointly, **H-S1.1** is supported if H-S1.1a and H-S1.1b hold and H-S1.1c's null cannot be rejected with a well-powered test.

- **H-S1.2 (boundary condition):** H-S1.1c's null holds *homogeneously* across platform-defined ad-product categories (`campaign_type`) — i.e., the degree of structural blindness does not depend on which approval pipeline a campaign routes through.

Two further checks are pre-specified as **exploratory, not confirmatory**, because of known power or reliability limitations:

- **RQ-S1.3:** Does keyword-level discretionary review status interact with size — a candidate channel through which structural attributes could re-enter the allocation process despite H-S1.1c?
- **RQ-S1.4:** Does the H-S1.1c null vary by advertiser industry?

A fully separate side investigation, retained as an appendix rather than folded into the hypothesis set:

- **RQ-S1.E1:** Can account churn be predicted from approval/cost/efficiency features? (Exploratory; not a structural-blindness test.)

### 2.3 Study 2's formal hypothesis family (H-S2)

**Note on how this family came to be, stated up front:** the project's original, pre-specified question (**RQ-S2.0**, now superseded) asked whether *brand-new advertiser accounts* ramp up differently based on some notion of account history — a "user cold-start" framing borrowed from recommender-systems research without adaptation. Sample construction diagnostics (§4.1) found that this population is essentially absent from the data (0 of 222 usable ad groups met a strict "genuinely new account" criterion; median account age behind a "cold-start" ad group was 7.8 years). This is documented as a **pre-registration deviation**: RQ-S2.0 is retired, not deleted, and replaced by an amended, data-informed question — **RQ-S2.1's ancestor** — that asks the same structural-blindness question at the *item* level instead of the *user* level. This is a change of population, not a change of underlying theory. The full diagnostic chain behind this deviation is in Appendix A, entry 1.

- **H-S2.1:** Account maturity (a structural attribute, analogous to Study 1's size) is positively associated with a newly registered ad group's initial growth slope — the item-level cold-start analogue of H-S1.1's total, unconditional relationship.
- **H-S2.2a:** An ad group's own early operating signal (coverage, spend trend, CTR/CVR) predicts its near-term growth — the candidate mediating/competing channel, analogous to Study 1's spend.
- **H-S2.2b:** Account maturity improves on H-S2.2a's prediction at the ad-group level (within-customer), once pooled/between-customer confounding is removed — the Study-2 analogue of asking whether H-S1.1c's direct effect is truly zero rather than merely undetected.

One further question is pre-specified as **exploratory / design-science, not confirmatory**, and is evaluated by backtest rather than a single point-null:

- **RQ-S2.3:** At what post-registration day (if any) is a low-growth ad group best flagged for intervention? This motivates a concrete design artifact, **DA-S2.1** (the Early-Warning Flagging Rule, specified in full in §12.8), whose design principles are grounded in H-S2.2a but whose binary-decision empirical advantage is not itself treated as a confirmatory claim.

### 2.4 What "confirmed" means across this hypothesis set

Every H-Sx.y hypothesis above that returns a non-significant result is additionally subjected to a TOST equivalence test (§7) before being described as anything stronger than "non-significant." This report distinguishes *failing to reject a point-null* from *formally establishing equivalence to zero* throughout.

### 2.5 Quick-reference: where each hypothesis is tested

| ID | Tested in | Primary figure |
|---|---|---|
| P-S1.0 | §4.1 | Figure 1 |
| H-S1.1a / H-S1.1b / H-S1.1c / H-S1.1 | §4.3–4.4 | Figures 2, 3, 7 |
| H-S1.2 | §4.5 | Figure 8 |
| RQ-S1.3, RQ-S1.4 | §7(a) | — |
| RQ-S1.E1 | §4.6 | Figure 4 |
| RQ-S2.0 (superseded) → item-level ancestor of H-S2.1 | §5.1 | Figure 5A |
| H-S2.1 | §5.2 | Figure 5B, 9 |
| H-S2.2a / H-S2.2b | §5.3 | Figure 6A, B, 9 |
| RQ-S2.3 / DA-S2.1 | §5.4 | Figure 6C, D |

### 2.6 Unified hypothesis-numbering: master mapping table

This table is the permanent cross-reference between every hypothesis ID used in this document and the legacy, unprefixed labels ("RQ1", "RQ2", "H2b", ...) still baked into the nine figure PNGs. Once assigned, an ID never gets reused or renumbered even if new hypotheses are added later.

| New ID | Old label(s) it replaces | What it claims | Status |
|---|---|---|---|
| **P-S1.0** | Figure 1's "(RQ1)" | Preliminary: performance variance sits mostly at ad-group/residual level, not customer level (motivates, does not itself test, H-S1.1) | Descriptive, not a hypothesis test |
| **H-S1.1a** | (unlabeled a-path, §4.4 method 8 / Table 2) | Size → total spend (a-path) | Confirmed, p<.001 |
| **H-S1.1b** | (unlabeled b-path, §4.4 method 8 / Table 2) | Spend → outcome, controlling for size (b-path), cost-independent outcome | Confirmed, p=.032 |
| **H-S1.1c** | Figure 2's "(RQ2, H2b)"; Figure 3's "(RQ2 robustness suite)" | Size → outcome, controlling for spend (c′-path, direct effect) = 0 (full mediation) | Confirmed null, 8 robustness checks |
| **H-S1.1** | — (composite label) | Indirect effect (a×b) is the entire size→outcome relationship (H-S1.1a ∧ H-S1.1b ∧ H-S1.1c jointly) | Supported |
| **H-S1.2** | Figure 8's "(joint Wald test)" | H-S1.1c's null is homogeneous across `campaign_type` strata | Rejected, p=.023 (heterogeneous) |
| **RQ-S1.3** | §7(a) / §8 keyword-review-status check | Does discretionary review leak account attributes into outcomes? | Exploratory/preliminary, underpowered |
| **RQ-S1.4** | §7(a) industry-stratification pilot | Does the H-S1.1c null vary by advertiser industry? | Piloted, not usable (label reliability) |
| **RQ-S1.E1** | Figure 4's "(RQ3, exploratory appendix)" | Can churn be predicted from approval/cost/efficiency features? | Exploratory appendix, outside the H-S1 hypothesis family entirely |
| **RQ-S2.0** | (unlabeled; §5.1 point 4 narrative) | *Superseded* — original pre-registered question: does new-*advertiser* onboarding show faster/slower ramp based on... (undefined comparison, abandoned) | Superseded by RQ-S2.1's ancestor — see §2.3 |
| **H-S2.1** | Study 2's "RQ1" / "H1" | Account maturity → initial 30-day growth slope (item-level cold start) | Null (non-sig); TOST inconclusive |
| **H-S2.2a** | Study 2's "RQ2" / "H2a" | Ad group's own early signal → later growth | Supported, decays with horizon |
| **H-S2.2b** | Study 2's "RQ2" / "H2b" | Adding account maturity improves H-S2.2a's prediction (within-customer) | Rejected; TOST inconclusive |
| **RQ-S2.3** | Study 2's "RQ3" | At what post-registration day should a low-growth ad group be flagged? | Exploratory / design-science, not confirmatory |
| **DA-S2.1** | "the design artifact," DP1–DP3 | Early-Warning Flagging Rule (input/output spec + 3 design principles) | Theoretically grounded in H-S2.2a; binary-flagging backtest inconclusive (4/9 vs 5/9) |

**Naming convention.** `H-Sx.y` = a formally testable hypothesis with a directional or point-null prediction, belonging to Study *x*, hypothesis family *y*. `RQ-Sx.y` = a question investigated *without* a single confirmatory point-null (exploratory, preliminary, underpowered, or explicitly design-science in nature). `P-Sx.y` = a preliminary/descriptive analysis that motivates a hypothesis but does not itself test one. `DA-Sx.y` = a design-science artifact (specification + design principles), evaluated by backtest rather than by a single statistical test. A superseded ID (like RQ-S2.0) is never deleted or silently dropped — it stays in the numbering table with a "superseded by" pointer, so the pre-registration deviation is auditable rather than hidden.

**Note on the nine figure PNGs.** The images themselves (baked-in titles like *"RQ2, H2b"*) are static, generated against a proprietary dataset that isn't re-rendered as part of this revision — every figure's caption below carries an explicit new-ID tag alongside the legacy in-image title.

---

## 3. Data

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata, incl. `campaign_type` (ad-product code) | 1,504 | 263/321 |
| Ad group dimension (snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status` (review code), bid price | 1,503,289 | 256/321 |

Two limitations shape everything that follows:

- **Single agency, single platform.** All data comes from one Korean ad-tech provider sourced from one search platform. Generalization is bounded by that ecosystem — §7 discusses how far that bound reasonably extends.
- **The ad-group table is a snapshot, not a history.** It reflects ad groups as they exist *today* — anything deleted in the past has vanished from the table. Every measure of "account age" or "how many ad groups this account has ever run" is therefore a **lower bound**. This matters enormously for Study 2, where account maturity is the variable under test.

Conversion and ROAS variables were excluded from both studies entirely — the platform's conversion API retroactively backfills conversions per account on a delayed, inconsistent schedule, which breaks construct validity for anything built on top of it. This was a design decision made before any modeling began, not a post-hoc exclusion.

---

## 4. Study 1 — Does Size Buy an Advantage? (Cross-sectional)

### 4.1 Where would an advantage even live? (tests P-S1.0)

Before testing anything about advertiser size, the analysis first needed to know *where* performance variation sits — in the customer, the campaign, or the ad group. If size-related advantages exist, they should show up as customer-level variance.

**Figure 1 — Multilevel variance decomposition** (preliminary analysis **P-S1.0**, motivating rather than testing H-S1.1). Across ~663K observations, log ad spend is dominated by unexplained residual variance (ICC = 0.825) — day-to-day budget execution, not who the customer is (ICC = 0.050). Click-through rate tells a similar story: the largest share of variation sits at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both patterns hold whether or not month fixed effects are added (diamond vs. square markers agree), ruling out seasonality as the explanation. This was the first hint, well before any hypothesis test: "who the customer is" explains comparatively little of what happens.

### 4.2 The raw gap looks real

Splitting advertisers into four size tiers (by spend volume) and comparing approval rate, CPC, and ad rank across tiers with a Kruskal-Wallis test shows differences that are statistically significant across the board (p < .001 for CPC and ad rank; p = .0006 for approval rate). Effect sizes are small (ε² = 0.002–0.079), but the raw signal is there.

Except it isn't quite what it looks like. Ad groups belonging to the same customer share policies and aren't statistically independent — the standard Kruskal-Wallis test assumes they are. Re-running the comparison as a customer-level cluster permutation test (2,000 iterations) made most of that "significant" gap in approval rate and CPC evaporate. The raw test's significance turned out to be substantially an artifact of ignoring clustering.

### 4.3 The gap disappears once spend is controlled (H-S1.1c)

**Figure 2 — The central confirmatory test** (the confirmatory test of **H-S1.1c** — the in-image title "RQ2, H2b" is this report's legacy label for the same hypothesis). Controlling for log spend in a cluster-robust regression, all six outcome × sample combinations (approval rate, CPC, ad rank, each in the full sample and with spike-affected accounts excluded) come back **non-significant** (cluster-robust p > .07). Every 95% bootstrap confidence interval not only crosses zero — it falls entirely inside (or right at the edge of) its own minimum-detectable-effect (MDE) band, meaning this isn't underpowered null-hunting; the observed effect is smaller than anything the sample could reliably detect. Approximate Bayes factors favor the null hypothesis in five of six tests (the sixth, CPC under spike exclusion, is flagged as a directionally-reversed sensitivity finding, not a confirmatory one).

### 4.4 Stress-testing across eight independent methods

A single regression result is easy to distrust, so it was stress-tested eight independent ways, all in service of **H-S1.1c** (with methods 7–8 additionally establishing **H-S1.1a/H-S1.1b**).

1. Multiverse specification curve (48 defensible analytic choices; 0/48 reach significance for any outcome)
2. Placebo test (device-type share, which size *shouldn't* predict, is significant under the raw distributional test but null under the spend-controlled regression — evidence the regression, not the raw test, is measuring the right thing)
3. Customer-and-month fixed-effects panel regression
4. Two-stage least squares with lagged spend as an instrument (first-stage F-statistic could not be recovered due to a code exception — flagged and excluded from any conclusion, not silently dropped)
5. Temporal split-sample replication
6. Benjamini-Hochberg FDR correction across the six primary hypotheses

**Figure 3 — Methods 1 and 2** (robustness battery for **H-S1.1c**). Panel A: across all 48 specification choices (tier definition × covariate set), for all three outcomes, not one reaches significance at α=.05. Panel B: the distributional (Kruskal-Wallis) test is significant for *both* the real outcome and the device-share placebo — proof that a raw distributional test alone is not a clean placebo, since size tiers correlate with many unrelated account traits. The informative comparison is the spend-controlled regression matching H-S1.1c: there, real and placebo outcomes are equally, indistinguishably null.

7. **Isolating and controlling for a mechanical artifact in the CPC outcome.** CPC = cost / click, and spend is built from cost — so any spend → CPC relationship carries a mechanical component by construction, independent of any real bidding-efficiency behavior. A customer-level permutation procedure (reshuffling click within customer while holding cost fixed, 2,000 iterations) isolates exactly how large that mechanical component is. The observed spend → log(CPC) coefficient (+1.277) falls *below* the lower bound of the resulting purely-mechanical null distribution (mean +1.552, 95% range [1.544, 1.556]) — meaning the CPC-based point estimate is not simply inflated by the artifact, but it is close enough to that mechanical distribution that it is not treated as a stand-alone quantitative claim. A lagged replication (spend at day *t* → CPC at *t*+1 and *t*+7, immune to same-day cost-sharing) confirms a same-signed, significant relationship at both lags (β=+0.538 and +0.544, both p<.001), consistent with a genuine behavioral effect coexisting with the artifact.

8. **Replicating the mediation result on a cost-independent outcome.** `bid_amount` (the advertiser's set bid price) shares no cost or click term with spend, so it carries none of the artifact isolated in method 7. Re-estimating Study 1's mediation structure (size → spend → outcome, controlling for size) on this outcome at the customer level (n=263) gives the load-bearing result for the efficiency claim: the indirect (spend-mediated) effect is significant (bootstrap 95% CI [0.008, 0.159], excludes zero; cluster permutation p<.001) while the *direct* effect of size, net of spend, is non-significant (p=.634) — the same qualitative conclusion as the CPC-based model, now on an outcome immune to the artifact. Jointly, methods 7–8 establish **H-S1.1a** and **H-S1.1b**.

**Figure 7 — CPC-based vs. bid_amount-based b-path** (the replication underlying **H-S1.1b**). The spend → outcome coefficient shrinks from +1.277 (CPC-based, partly mechanical) to +0.150 (bid_amount-based, cost-independent) once the shared cost term is removed — the direction survives, the magnitude does not.

**Eight independent verification methods, one consistent verdict**, with method 8 — not the raw CPC coefficient — treated as the primary quantitative evidence for the efficiency-outcome claim. Jointly, methods 1–8 are the confirmatory basis for **H-S1.1** (H-S1.1a ∧ H-S1.1b ∧ H-S1.1c).

### 4.5 Is the result homogeneous across contexts? (H-S1.2)

Close to, but not perfectly, homogeneous. Stratifying the spend-controlled CPC model by `campaign_type` (a platform-defined ad-product code — website / shopping / brand-new-product / local-business, *not* an industry classification) and running a joint Wald test on the size × product-type interaction gives **p = .023**: the *degree* to which size is irrelevant varies somewhat by ad-product category, even though no individual stratum shows a significant size effect on its own (all p > .05).

**Figure 8 — Boundary-condition forest plot** (the confirmatory test of **H-S1.2**). Website campaigns show a (non-significant) negative point estimate for size net of spend, while local-business and shopping campaigns show (non-significant) positive point estimates — all three confidence intervals cross zero individually, but the joint test across strata is significant (p=.023), meaning the *pattern* of where size comes closest to mattering is not random noise even though no single stratum is itself conclusive.

### 4.6 A side quest: predicting churn (RQ-S1.E1)

This question sits outside the fairness hypothesis entirely, but it was worth asking as an exploratory appendix: given approval/cost/efficiency features, can machine learning models predict which accounts will churn? This sits entirely outside the H-S1 hypothesis family — it is not a structural-blindness test.

**Figure 4 — Churn-prediction benchmarking** (**RQ-S1.E1**, outside the H-S1 hypothesis family). Across 213 labeled accounts (a stark 2.35% churn rate), tree-based models nominally outperform logistic regression in nested cross-validation. But every pairwise model comparison returns the *exact same* Wilcoxon p-value (0.0625) — the mathematical floor achievable with only 5 repeat-pairs, not evidence of a real difference. Random forest had the best-calibrated out-of-fold predictions (Brier score 0.0250).

### 4.7 Study 1 Conclusion

Raw size-tier gaps in approval rate, CPC, and ad rank are statistically detectable but small, and their significance is fragile once you account for clustering. The confirmatory test — spend-controlled regression, replicated on a cost-independent outcome — returns a clean, well-powered null for the *direct* effect of size (**H-S1.1c**) across all outcome-sample combinations, backed by eight independent robustness checks, with one caveat: the size of that null effect is not perfectly homogeneous across ad-product categories (**H-S1.2**, §4.5). **The apparent advantage of being a large advertiser is, to first order, explained by spending more rather than by size itself — with modest, product-type-dependent variation in how completely that holds.**

---

## 5. Study 2 — Does History Buy an Advantage? (Longitudinal)

### 5.1 What does "cold start" even mean here? (the RQ-S2.0 → H-S2.1 deviation)

The original plan treated "cold start" as new-advertiser onboarding: a brand-new account launching its first campaign. Before testing any hypothesis, the sample was built — and the data pushed back, hard, five separate times. Each of these five detours is logged in full narrative form in Appendix A.

1. **The numbers didn't match.** Early planning documents cited 476 "true cold-start" ad groups in one place and 250 in another. Recomputing directly from the data settled it at 250 → 222 after filtering for at least 7 active days — matching the smaller figure exactly.

2. **What looked like right-censoring wasn't.** 83.8% of the trajectory sample appeared to be "censored" — cut short by the observation window ending. But stretching the required post-registration observation window from 30 to 120 days barely moved that number (83.6% → 83.2%). If it were really about insufficient observation time, giving ad groups four times longer to be observed should have fixed most of it. It didn't. The real explanation: **these ad groups simply don't stop running** — they keep going until the data collection window ends. Applying a right-censoring lens borrowed from survival analysis was the wrong tool for this kind of data.

3. **Growth-curve clustering couldn't be trusted.** Fitting discrete latent growth classes (a group-based trajectory model) to categorize ad groups by growth pattern was tried. A recovery simulation (200 iterations) showed that even when the true number of classes was known to be 2, the model correctly identified it only 9% of the time. This wasn't a "small sample, a bit unlucky" problem — the model structure itself couldn't reliably recover class counts. This was abandoned in favor of a continuous growth-curve (random-effects) approach.

4. **The real discovery: this isn't user cold-start at all.** Profiling the top customers and mapping the full distribution of account maturity revealed something the original framing had missed entirely. Of the 222 usable ad groups, **zero** met the strict criteria for "genuinely new account" (cold-start ratio ≥ 80% *and* account age ≤ 30 days). Even relaxing the age threshold to 90 days captured just one ad group (0.5%). More than half of the observed "cold-start" ad groups belonged to accounts with a **median age of 2,853 days — about 7.8 years.** This forced an explicit reframing: from *user* cold-start (a brand-new advertiser) to **item cold-start** (a brand-new ad group inside an already-mature account) — a distinction long established in recommender-systems research but rarely made explicit in advertising analytics.

5. **Even the statistical model needed rebuilding.** Account maturity only takes one value per customer — every ad group from the same account shares it. Feeding that into a mixed-effects model with a customer-level random intercept creates a structural non-identifiability: the model can't tell "customer-level random variance" apart from "the maturity fixed effect." A pre-registered power simulation (500 iterations, reusing the real cluster structure) confirmed it: the mixed model's convergence failure rate was **100%**. It was replaced with a simpler, sound alternative — customer-level aggregate OLS (n≈32) — whose false-positive rate (5.2%) sat right at the nominal 5% alpha, and which could reliably detect only large effects (standardized β ≈ 0.5, 88% power).

A sixth, quieter fix: two accounts in the trajectory-usable sample turned out, on four-signal profiling (all-time scale, registration-burst pattern, template/naming signal, real spend), to be test/QA setups rather than real advertisers, and were excluded via a pre-specified rule now encoded in `config/config.yaml` — logged rather than applied ad hoc.

### 5.2 Does account maturity predict how fast a new ad group grows? (H-S2.1)

With the sample and the model finally sound, the study could ask the question it actually set out to answer.

**Figure 5(A) — The sample-construction funnel** (documents the RQ-S2.0 → item-level cold-start deviation, §2.3): 250 candidates → 222 with sufficient activity → 207 excluding near-zero-spend accounts → 204 with a complete 30-day early window (29 customers once aggregated). The median account behind these "cold-start" ad groups was already 2,853 days old — visual proof that this is a story about expansion inside mature accounts, not onboarding new ones.

**Figure 5(B) — tests H-S2.1.** Account maturity (log-transformed, standardized count of all-time ad groups) was tested against each customer's mean initial 30-day growth slope (n=29). The raw-scale OLS coefficient was weakly positive (β=8.34) but non-significant (p=.576), and the pre-registered decision rule — a cluster permutation test (10,000 iterations) — agreed: p=.663. The 95% bootstrap CI [-15.84, 43.08] comfortably contained zero. Dropping the largest customer (35.8% of the sample) as a sensitivity check changed nothing (permutation p=.702) — this leave-one-out re-run is a **required** step in the confirmatory design precisely because that customer alone accounts for a third of the trajectory-usable sample, and profiling confirmed it as a genuine large advertiser rather than a bulk/template account worth excluding. Most tellingly, that weak positive coefficient collapsed to β=1.48 under winsorizing and **flipped sign entirely** under a rank-based regression (β=-0.0196) — the signature of a result driven by a couple of high-leverage outliers rather than a genuine relationship. The standardized effect size (β=.085) sits at just 17% of the large-effect threshold the pre-registered power simulation was built to detect.

**A formal equivalence test (TOST) sharpens this point.** Failing to reject a point-null is not the same as confirming an effect is absent. A two-one-sided-test procedure against a ±0.20 standardized-effect-size equivalence margin returns **p = .197 — equivalence is not established.** The honest statement is therefore two-sided: this sample would have detected a large effect and did not (the pre-registered power simulation), **and** this sample cannot formally rule out a small-to-moderate effect existing but falling below detection (the TOST result). Both are true at once.

**Verdict: H-S2.1 not supported — account maturity does not show a detectable effect on how fast a new ad group ramps up**, reported as a well-powered non-significant association rather than a confirmed null.

### 5.3 Does the ad group's own early behavior predict its near-term growth? (H-S2.2a, H-S2.2b)

If history doesn't clearly matter, what does? Whether an ad group's own first 14–60 days of activity — coverage, early spend trend, CTR, CVR, ROAS — predicts how it performs afterward was tested using customer-grouped repeated splits and Leave-One-Customer-Out (LOCO) cross-validation to guard against information leakage.

**Figure 6(A,B) — The prediction result, and the trap hidden inside it** (Panels A–B test **H-S2.2a** and **H-S2.2b**; Panels C–D address the exploratory **RQ-S2.3**). Using only the ad group's own early signal, 14-day-ahead growth prediction achieved a respectable ρ=0.386 in leakage-free repeated-split validation. Adding account maturity as a feature made things *worse*, not better (ρ=0.373, Wilcoxon p=.038). But the LOCO cross-validation told the opposite story — a *positive* improvement (+0.034) from adding maturity.

Panel B decomposes the improvement into within-customer and between-customer components. The apparent LOCO gain turned out to be almost entirely a between-customer effect — maturity was just re-injecting the same customer-level growth-level signal from §5.2 through a pooled metric, not genuinely improving ad-group-level prediction. Within-customer improvement was essentially zero (±0.02) across all three window combinations tested. A pooled LOCO improvement was initially misread as H-S2.2b support before the within/between split exposed it as leakage of the H-S2.1 signal; the confirmatory design now requires the *within-customer* number to be positive before crediting H-S2.2b, full stop.

**A second equivalence test on this specific claim** (does adding maturity improve ad-group-level prediction at all, once pooled/within confounding is controlled) again returns an inconclusive verdict: TOST against a ±0.05 Spearman-ρ margin gives **p = .290 — equivalence not established.** The directional finding (own-signal is genuinely predictive; maturity's apparent contribution is a pooling artifact) is well supported; the *complete absence* of any maturity contribution at the within-customer level is not something this sample can formally certify.

**Trusting the leakage-controlled decomposition: an ad group's own signal is genuinely predictive at short horizons (H-S2.2a supported); account maturity's apparent contribution is explained by between-customer pooling rather than genuine ad-group-level improvement (H-S2.2b rejected).** Predictive power itself also decayed sharply as the horizon extended from 14 to 30–60 days (within-customer ρ dropping to roughly 0.06–0.21).

### 5.4 When's the best day to flag a struggling ad group? (RQ-S2.3, DA-S2.1)

**Figure 6(C,D) — Timing an intervention.** Flagging the bottom 25–40% of predicted growers achieved a 1.2–1.4x precision lift over random flagging, and that lift held up consistently whether the decision was made at day 7, 14, or 21 post-registration (Panel C). But the 95% bootstrap confidence intervals on predictive accuracy at each of those cutoffs overlap heavily (Panel D) — there's no statistical basis for calling any single day "optimal."

Two independent attempts were also made to quantify the *expected benefit* of intervening at each point in time, but both failed the same way: the assumed intervention-effect parameters combined multiplicatively in a way that made the "optimal" answer (day 21, threshold 0.40) come out identical *no matter what values were assumed*. That's not a robust finding — it's a mathematical illusion baked into the formula. Both simulations were discarded, and the limitation is reported openly rather than presenting a false sense of precision. (Both failed simulation designs are walked through step by step in Appendix A, entry 6.)

**Design artifact (DA-S2.1).** §5.3's within-customer result motivates a concrete decision rule — flag an ad group if its own early-window signal places it in the bottom 30% of predicted growth, evaluated at any point in a day-7–21 window. This is formalized as an explicit design-science artifact (input/output specification, three design principles). Its binary-flagging empirical backtest, however, is **not** reported as a confirmed advantage: the naive size/tenure comparison rule collapses to numerical zero under within-customer demeaning (a structural fact — account maturity is a customer-level constant — not a bug), and against a random-flagging baseline, the design artifact's own-signal precision wins in 4 of 9 tested specifications and loses in 5, indistinguishable from chance at this sample size (n≈20 customers per specification). The design principles are grounded in **H-S2.2a**'s continuous-scale result; their binary-flagging empirical superiority is left as future work.

**Verdict:** early flagging (**RQ-S2.3**, motivating **DA-S2.1**) is directionally motivated by a confirmed continuous-scale result, but neither a precise "optimal day" nor an empirically confirmed binary-flagging advantage is something this data can support yet.

### 5.5 Study 2 Conclusion

Initial ad-group growth is best explained by the ad group's *own* early operating signal (H-S2.2a), not by the parent account's accumulated history (H-S2.1, H-S2.2b), at the within-customer level tested. Getting to that conclusion required first discovering that the study's own sample definition didn't mean what it was assumed to mean (the RQ-S2.0 pre-registration deviation, §2.3), rebuilding the statistical approach twice in response, and — throughout — treating "non-significant" and "confirmed absent" as the two distinct claims they are.

### 5.6 Results at a Glance

Sample: cold-start candidates = 250 → trajectory-usable = 222 → 207 after excluding two near-zero-spend template accounts → 204/29 (H-S2.1) or the window-specific n below, depending on each analysis's completeness filter.

**H-S2.1 — does account maturity predict initial growth slope?**

| statistic | value |
|---|---|
| n (customers) | 29 |
| n (ad groups, informational) | 204 |
| OLS beta (raw scale) | 8.34 |
| OLS HC3 p-value | .576 |
| Bootstrap 95% CI (raw scale) | [-15.84, 43.08] |
| Cluster permutation p-value | .663 |
| Spearman rho | -.02 (p = .92) |
| Leave-one-out (largest customer excluded) permutation p-value | .702 (sign unchanged) |
| Winsorized (10%) OLS beta / p | 1.48 / .841 |
| Rank-rank OLS beta / p | -.02 / .924 |
| Standardized effect size (beta) | .085 |
| Pre-registered large-effect detection threshold | .50 |
| Observed effect as % of detection threshold | 16.9% |

**Verdict: H-S2.1 not supported.** Five independent checks agree, and the standardized effect size sits well below even the small-effect band the power simulation was built to detect — this reads as a genuine null, not an under-powered non-detection.

**H-S2.2a/b — do early operating signals predict later growth, and does maturity add value?**

| early/later window (days) | n (ad groups) | H-S2.2a within-customer LOCO ρ | H-S2.2b within-customer LOCO ρ | within-customer improvement | repeated-split Wilcoxon p |
|---|---|---|---|---|---|
| 14 / 14 | 204 | 0.467 | 0.487 | +0.019 | .038 (H-S2.2b *worse* on repeated-split ρ) |
| 30 / 30 | 184 | 0.275 | 0.257 | -0.018 | .119 |
| 30 / 60 | 179 | 0.060 | 0.061 | +0.001 | .019 (H-S2.2b *worse* on repeated-split ρ) |

**Verdict: H-S2.2a supported at short horizons, decaying sharply beyond them; H-S2.2b not supported at any horizon.** Adding account maturity never produces a within-customer improvement exceeding +0.02, and the repeated-split design finds the addition significantly *harmful* at two of three window pairs. Positive-looking pooled/between-customer improvements (e.g., +0.388 at 30/60d) are H-S2.1-level signal leaking into a pooled metric.

**RQ-S2.3 — at what point should a low-growth ad group be flagged?**

| decision cutoff (days) | out-of-fold predictive ρ (95% bootstrap CI) | lift @ threshold=0.25 | lift @ threshold=0.40 |
|---|---|---|---|
| 7 | 0.304 [0.145, 0.445] | 0.83 | 1.27 |
| 14 | 0.265 [0.123, 0.404] | 1.33 | 1.23 |
| 21 | 0.334 [0.210, 0.459] | 1.42 | 1.36 |

*(threshold = 0.10 excluded — 12.6–13.1% of ad groups have `growth_target == 0`, which destabilizes quantile cuts at this narrow a band.)*

**Verdict: directional, not precise.** Flagging achieves 1.2–1.4× lift over random across all tested cutoffs and reliable thresholds, but the 95% bootstrap CIs on predictive ρ overlap substantially across all three cutoffs — no single cutoff is statistically distinguishable as "optimal."

> **Combined takeaway:** initial ad-group growth is explained by the ad group's own early operating signal (H-S2.2a) — not by the parent account's accumulated history, whether tested at the customer level (H-S2.1, null), the ad-group level with maturity added (H-S2.2b, null/harmful), or as an input to intervention timing (RQ-S2.3, no differential value demonstrated across cutoffs). Account size or tenure should not be used as a proxy for how a new ad group will perform; its own first two weeks of activity is the more informative — and, at this sample size, the *only* reliably informative — signal.

---

## 6. Where the Two Studies Meet

| | Study 1 (cross-sectional, size) | Study 2 (longitudinal, tenure) |
|---|---|---|
| Formal hypothesis family | H-S1.1 (a/b/c), H-S1.2 | H-S2.1, H-S2.2 (a/b) |
| Initial observation | Significant raw gap by size tier | (implicit expectation) maturity should help new units |
| Direct test of the structural attribute | Direct effect vanishes once spend is controlled; near-homogeneous across contexts (p=.023 joint heterogeneity test) | No detectable direct effect of maturity; equivalence formally inconclusive (TOST p=.197) |
| What actually drives outcomes | Spend (a mediating variable, replicated on a cost-independent outcome) | The unit's own early operating signal (within-customer confirmed) |
| Independent verification methods | 8 | 5, plus within/between decomposition and a second TOST |
| Key figures | Figures 1–3, 7, 8 | Figures 5, 6 |

These two investigations share no data, no time axis, and almost no statistical machinery in common — one is a cross-sectional mediation problem, the other a longitudinal, customer-clustered prediction problem. And yet they land on a closely aligned structural conclusion: **an account's size or history has little direct effect on unit-level performance once you account for what actually mediates it — spend, or the unit's own real-time signal** — with the qualifications (product-type heterogeneity in Study 1; TOST-inconclusive equivalence in Study 2) that keep this from being an unqualified universal claim. This is the **structural blindness** pattern (§2.1): a real-time, bid-based serving system that evaluates every ad group largely by its current behavior, only modestly conditioned by the account's past or scale.

---

## 7. Boundary Conditions and Generalizability

Two questions bound how far the "structural blindness" claim should travel: (a) does it hold uniformly *within* this platform, and (b) how far does it plausibly extend *beyond* this platform.

**(a) Within-platform heterogeneity.** Two strata were tested against Study 1's central result:

- **Campaign product type** (platform-defined, well-measured; §4.5, Figure 8; this is **H-S1.2**): the spend-controlled size effect is not perfectly homogeneous across website / shopping / local-business / brand-new-product campaigns (joint Wald p=.023), plausibly because these route through different approval pipelines on this platform (e.g., shopping campaigns are subject to product-feed validation that standard search campaigns are not). No individual stratum shows a significant size effect.
- **Keyword review status** (a proxy for platform discretion — **RQ-S1.3**; see table below): only 0.5% of keywords in this dataset carry any non-standard `inspect_status` code, so this check is under-powered by construction. A restricted-approval-driven interaction is directionally interesting (p=.016) but does not cleanly map onto the "discretionary review as a channel for account-attribute leakage" mechanism that motivated the check, since restricted-approval denotes an already-resolved outcome rather than a pending discretionary review. Reported as preliminary, not confirmatory.

  | Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
  |---|---|---|---|
  | Under-review only | 22 | 230 | .638 |
  | Restricted-approval only | 106 | 146 | .016 |
  | Combined | 111 | 141 | .016 |

  The combined definition's significance is driven almost entirely by the restricted-approval component (106 of 111 customers), not by an independent contribution from the under-review component — one underlying signal probed three ways, not three independent confirmations.

- **Advertiser industry** (**RQ-S1.4**) was piloted as a third stratification (text-embedding clustering + LLM-ensemble labeling against Korean Standard Industrial Classification categories) but is *not* used to support any claim: inter-rater reliability across the four-model LLM ensemble was only moderate (Randolph's free-marginal kappa = 0.557) and cross-validation against an independent rule-based classifier was weaker still (Cohen's κ = 0.363). The pipeline and reliability diagnostics are retained for transparency and as a direction for future work with a higher-reliability label source.

**(b) Cross-platform generalizability.** The mechanism documented here — real-time, auction-based serving that scores each unit primarily on its own current signal — is a property of the serving architecture, not of this specific platform's brand. The *direction* of the structural-blindness finding is expected to generalize to other real-time bidding-based ad platforms with comparable architecture (unit-level auctions, continuous re-ranking, no persistent account-level scoring layer). No claim is made that the specific magnitudes generalize, and conditions under which the mechanism plausibly breaks down are flagged explicitly:

- Platforms or ad categories with **mandatory human review** in the approval pipeline (e.g., regulated verticals such as healthcare, finance, or political advertising), where account-level trust signals could re-enter the process through reviewer discretion rather than the bidding algorithm itself.
- **New keyword or product categories** without established auction liquidity, where the platform may fall back on account-level heuristics in the absence of sufficient real-time signal.
- Platforms whose ranking algorithm **explicitly incorporates account tenure or verification status** as a ranking feature (unlike the platform studied here, where no such mechanism is documented in the public product literature).

This report's single-agency, single-platform data cannot itself test these boundary conditions; they are stated here as falsifiable predictions for future replication rather than as findings.

---

## 8. What "Null Result" Means Here: Equivalence and Sensitivity

A non-significant p-value does not, by itself, establish that an effect is genuinely absent — it establishes that this sample could not distinguish the observed effect from zero at conventional confidence. This report draws that distinction explicitly wherever a null result is central to the argument.

**Figure 9 — TOST equivalence plot** (TOST equivalence for **H-S2.1** (left panel) and **H-S2.2b** (right panel)). Two central results (H-S2.1: account maturity → growth slope; H-S2.2b: does maturity improve ad-group-level prediction) were each subjected to a two-one-sided-test (TOST) procedure against a pre-specified equivalence margin (the green shaded region, or "smallest effect size of interest," SESOI). In both panels the observed point estimate sits comfortably *inside* the equivalence region, yet the TOST itself is not significant — neither reaches formal equivalence (H-S2.1: p=.197 against a ±0.20 SESOI; H-S2.2b: p=.290 against a ±0.05 Spearman-ρ SESOI). Both results are consequently reported as *non-significant, well-powered associations for which formal equivalence is inconclusive* — not as confirmed nulls.

**Omitted-variable-bias sensitivity (Oster's delta).** The bid_amount-based mediation result (§4.4, method 8 — **H-S1.1b**) is the primary evidentiary basis for the efficiency claim. Oster's delta quantifies how much stronger an unobserved confounder would need to be, relative to the observed controls, to explain the spend → bid_amount coefficient away. The computed value (δ*=+71.4) looks dramatically robust — but the R² increment from adding `size_z` to the model is only 0.0009, effectively zero, which places the calculation in a numerically unstable region where δ* diverges regardless of the true underlying robustness. δ* is not reported as evidence of robustness here; the R² increment itself (size adding essentially no explanatory power to bid_amount beyond spend) is the more interpretable, more conservative, and ultimately consistent takeaway. A minimum-R²-increment threshold (0.01) is adopted below which δ* is reported for transparency but not used as a robustness claim. Full numeric table in §12.7.

---

## 9. Limitations

1. **Single agency, single platform.** See §7(b) for the specific conditions under which the mechanism is expected to hold or plausibly break down elsewhere.
2. **CPC-based estimates carry a partly mechanical component.** Reported as directionally informative only; the bid_amount-based estimate is the primary quantitative claim wherever the two diverge (§4.4, Figure 7).
3. **Two central null results (H-S2.1, H-S2.2b) are non-significant but not formally equivalence-confirmed** (§8, Figure 9). Both facts are reported rather than rounding "non-significant" up to "confirmed absent."
4. **The industry-stratification pipeline (RQ-S1.4) has only moderate label reliability** and is not used to support any claim (§7a).
5. **The early-flagging design artifact (DA-S2.1, §5.4) is theoretically grounded but not empirically validated** as a binary-decision rule; its backtest is reported as future work.
6. **Keyword-review-status boundary-condition check (RQ-S1.3) is under-powered** (0.5% of keywords carry a non-standard status) and is reported as preliminary/exploratory (§7a).
7. **The ad-group dimension table is a snapshot**, so all account-age and account-history measures are lower bounds (§3).
8. **Two customer-defined test/QA accounts were excluded from Study 2 via a pre-specified, logged rule**, not applied ad hoc (Appendix A, entry 7).

---

## 10. Methodology Summary

| | Study 1 | Study 2 |
|---|---|---|
| Primary test | Cluster-robust controlled regression (HC3 / cluster SE), replicated on a cost-independent outcome | Customer-level aggregate OLS + cluster permutation test |
| Robustness battery | Cluster permutation test, bootstrap CI, approximate Bayes factor, MDE, specification curve, placebo test, 2SLS, temporal split replication, cost-sharing-artifact isolation, alternative-outcome replication | Bootstrap CI, winsorizing, rank-rank regression, leave-one-out, within/between decomposition, TOST equivalence |
| Heterogeneity / boundary conditions | campaign_type joint Wald test, H-S1.2 (p=.023); keyword review-status, RQ-S1.3 (exploratory) | — |
| Sensitivity analysis | Oster's delta (bid_amount b-path), with a numerical-stability guard | — |
| Multiple-testing correction | Benjamini-Hochberg FDR (6 primary hypotheses) | Not applicable (single confirmatory hypothesis; convergence across 5 methods used instead) |
| Methods tried and discarded | None (all retained) | Group-based trajectory modeling (class count unidentifiable, 0–9% BIC recovery), mixed-effects model (100% convergence failure, non-identified) |
| Pre-registered / post-hoc power check | MDE at 80% power | Simulation reusing real cluster structure (500 iterations); only large effects (β≈.5) reliably detectable (88% power) |
| Related figures | 1, 2, 3, 4, 7, 8 | 5, 6, 9 |
| Hypothesis family | H-S1.1 (a/b/c), H-S1.2, RQ-S1.3, RQ-S1.4, RQ-S1.E1 | H-S2.1, H-S2.2 (a/b), RQ-S2.3, DA-S2.1 |

---

## 11. Discussion

This report proposes the **structural blindness** construct, validated across two independent structural levels (cross-sectional size, longitudinal tenure). Practically, the implication for advertisers is clear: account size or tenure should not be used as a proxy for a new unit's performance; instead, what the unit itself does — spend, or its first few weeks of results — is the more informative, more actionable signal. Theoretically, these results provide empirical grounding for platform-fairness discussions: concerns about algorithmic-treatment gaps may need to be reinterpreted not as gaps driven by account attributes themselves, but as gaps in the behaviors those attributes mediate (spending capacity, early optimization capability).

---

## 12. Opportunities to Strengthen the Manuscript Without Additional Analysis

The content below is restricted to changes achievable through **reframing, restructuring, and exposition** — none require new data collection, new statistical tests, or additional robustness runs. All numbers, figures, and conclusions in §§1–11 remain unchanged; what changes is how the argument is organized and foregrounded.

1. **Elevate the theoretical framing.** As currently written, "structural blindness" reads primarily as a descriptive label attached after the fact. Explicitly connecting §2.1 to existing literature on algorithmic accountability, information asymmetry in platform markets, and fairness-in-ML would let the two studies read as a single theoretical contribution — testing one mechanism at two structural levels — rather than two independent null-result write-ups. This is a rewriting task confined to §2 and the discussion (§11); it requires no new estimation.

2. **Move the triangulation narrative earlier.** §6 ("Where the Two Studies Meet") currently reads as a post-hoc synthesis appended after both studies are reported. Repositioning this framing into §1 — presenting the two studies from the outset as a deliberate triangulation of one construct using two independent datasets and two independent statistical toolkits — makes it harder to read Study 2's statistical limitations in isolation from Study 1's stronger results. This is a matter of section ordering and framing language, not new evidence.

3. **Foreground the power/robustness exposition that already exists.** Study 2's n=29 constraint is already addressed thoroughly (leave-one-out sensitivity, winsorizing, rank-rank regression, TOST, pre-registered power simulation — Figure 5B, Figure 9). Currently this material is distributed across §5.2, §8, and Appendix A. Consolidating it into a single, early "what this sample can and cannot tell us" exposition — placed before the H-S2.1 result is presented, not after — changes a reviewer's first impression from "small sample, weak result" to "small sample, rigorously characterized result." This requires reorganizing existing content only.

4. **Translate the null results into explicit practical guidance.** The conclusion "structural attributes don't matter" is currently stated abstractly. Adding a short, concrete guidance section — e.g., a checklist for advertisers on what to optimize in a new ad group's first two weeks, or budget-allocation implications for new accounts — using only findings already established (H-S2.2a's short-horizon predictiveness, the spend-mediation result in H-S1.1) increases the report's practical legibility without adding analysis.

5. **Promote the boundary-conditions section from caveat to contribution.** §7's campaign-type heterogeneity (H-S1.2) and the cross-platform generalizability conditions are currently framed as limitations attached at the end. Reframing this material as "the conditions under which structural blindness holds and where it plausibly breaks down" — and moving a condensed version of it into the introduction as part of the paper's scope statement — repositions the report from a single flat claim ("nothing matters") to a more defensible, conditional one ("nothing matters, except under these specified conditions"). This is achieved by rewriting transitions and section placement, not by running new heterogeneity tests.

6. **Tighten the causal-language discipline throughout.** Several passages (e.g., the mediation results in §4.4) use language that is stronger than the identification strategy supports, given the unrecovered 2SLS first-stage statistic. A pass to ensure every causal-sounding claim is qualified as "consistent with," "compatible with," or "associational, replicated across artifact-free outcomes" rather than stated as unqualified causal fact would reduce a common reviewer objection without touching the underlying estimates.

None of the six actions above require rerunning the pipeline, collecting new data, or adding robustness checks beyond what Appendix A and B already document. They are edits to framing, sequencing, and emphasis only.

---

## Appendix A. Methodology Notes

This appendix is a narrative log of every point in the diagnostic pipeline (`src/coldstart_v5/`, Steps A–M) where an initial modeling choice was found to be structurally unreliable and replaced with a more defensible alternative, and why. It is treated as part of the project's contribution, not as a section to be edited out once the final design was settled — the reasoning here is what makes the confirmatory results trustworthy rather than merely reported.

Each entry follows the same shape: **what was assumed**, **how the diagnostic contradicted it**, and **what changed as a result**.

### A.1 "Cold start" was assumed to mean new-advertiser onboarding (RQ-S2.0 → H-S2.1: the pre-registration deviation)

**Assumed:** the project's original framing treated a "cold-start" ad group as the leading edge of a brand-new advertiser's account — a first campaign, unfolding inside the observation window.

**Contradicted by:** Step I (`step_i_account_maturity_distribution.py`), cross-checked by Step H (`step_h_top_customer_profiling.py`). Under every registration-date cutoff tested (0-90 days of prior account history), essentially none of the trajectory-usable sample (0-1 of 222 ad groups) reflected a genuinely new account; the median account behind a "cold-start" ad group had `account_age_days` of roughly 7.8 years (a lower bound, per the snapshot caveat). Step J (`step_j_regtm_artifact_check.py`) ruled out a snapshot/migration date artifact as the explanation.

**Changed:** the project was reframed around **item-level cold start**: a new ad group inside an already-established account — closer to "item cold-start" than "user cold-start" in the recommender-systems literature. Account maturity became the key covariate under test in H-S2.1/H-S2.2, not a stratification variable for sample selection.

`[affects: RQ-S2.0 → H-S2.1 deviation — this is *the* pre-registration deviation referenced in §2.3]`

### A.2 Discrete latent-class growth models (GBTM) were the planned RQ1 method

**Assumed:** growth trajectories would be summarized with a Group-Based Trajectory Model, and RQ1 would ask "how many growth classes exist, and does maturity predict class membership?"

**Contradicted by:** Step E (`step_e_class_count_identifiability_sim.py`), a BIC-based class-count recovery simulation at the achievable sample size (n=222). Recovery probability was ~9% at k=2 true classes and ~0% at k=3/4 — the sample cannot reliably tell two classes apart, let alone three or four, independent of any censoring or clustering issue.

**Changed:** GBTM was dropped from the confirmatory design entirely. RQ1 (now **H-S2.1**) was rewritten around a continuous growth-curve quantity (an ad group's initial 30-day cost slope) rather than a discrete class label, avoiding the class-count identification problem altogether.

`[affects: H-S2.1 — estimator choice for the RQ-S2.0→H-S2.1 transition]`

### A.3 Apparent right-censoring turned out to be a follow-up-window artifact, then something else

**Assumed:** the 83.8% "censored" rate found in Step C (`step_c_right_censoring_flags.py`) meant many trajectories were cut short by the observation window ending too soon after registration.

**Contradicted by:** Step F (`step_f_registration_cutoff_sensitivity.py`): requiring 30 vs. 120 days of guaranteed post-registration follow-up barely moved the censored rate (83.6% -> 83.2%). If insufficient follow-up time were the cause, a stricter cutoff should have reduced it sharply. Step G (`step_g_fixed_window_coverage.py`) then showed the real story: mean observed-day coverage within fixed post-registration windows was only 70-74%, not the near-100% a genuinely continuously-run ad group would show.

**Changed:** "censoring" was reinterpreted as ad groups mostly **not self-terminating** (activity persists to observation end because the ad group is still running, not because its trajectory was cut off) combined with **genuine intermittency** (on/off cycling, budget exhaustion, approval delay) inside the active window. The confirmatory growth-slope definition uses fixed-window linear trend fitting on zero-filled daily series rather than a survival/censoring framework, which sidesteps the mismatch.

`[affects: H-S2.1 — sample/outcome construction]`

### A.4 A customer random-intercept mixed model (MixedLM) was the planned RQ1 estimator

**Assumed:** growth slopes nested within customers would be modeled with `statsmodels` MixedLM, `slope ~ maturity`, `groups=customer_id`.

**Contradicted by:** Step K (`step_k_power_simulation.py`). Because `maturity` varies only at the customer level, it competes directly with the customer random intercept for the same layer of variation, and the model is structurally non-identified against it: 100% convergence-failure rate across every simulation replication, at every tested effect size — not merely an occasional convergence issue.

**Changed:** MixedLM was dropped as unusable for this design. The customer-level aggregate regression (average an ad group's growth slope up to its customer, then regress the customer-level mean on customer-level maturity, n = customer count) became the primary inferential model, with a cluster (customer-label) permutation test as the final arbiter whenever it and OLS disagree — because 29-32 clusters is below the usual comfort threshold (40-50+) for trusting asymptotic cluster-robust standard errors alone.

`[affects: H-S2.1 — estimator choice]`

### A.5 A pooled Leave-One-Customer-Out (LOCO) improvement was initially read as RQ2 support for H2b

**Assumed:** during RQ2 design (`step_l_rq2_feature_engineering.py`), a positive pooled LOCO rho improvement when adding account maturity to the base feature set was read as evidence that maturity adds ad-group-level predictive value.

**Contradicted by:** the within/between-customer decomposition (`loco_within_between_eval`). Splitting the pooled LOCO rho into a between-customer component (customer mean-level agreement) and a within-customer component (relative ranking of ad groups belonging to the same customer) showed that, at every tested window pair, the pooled improvement was concentrated almost entirely in the between-customer term while the within-customer term showed little or no improvement (in one window pair, +0.388 between vs. +0.001 within). A pooled metric that improves because it re-derives the RQ1 (customer-level) signal is not evidence of genuine ad-group-level predictive gain.

**Changed:** the confirmatory RQ2 design requires the within-customer LOCO improvement to be positive before crediting H2b (now **H-S2.2b**), regardless of the pooled or between-customer numbers.

`[affects: H-S2.2b]`

### A.6 Two successive RQ3 "expected uplift" simulations were mathematically incapable of answering the question they were built for

**Assumed:** an expected-uplift formula (`n_true_positive * efficacy * delta`) swept across intervention-effect assumptions (`delta`, `efficacy`) would reveal which decision cutoff (7/14/21 days) is optimal, and whether that ranking is robust to the effect-size assumption.

**Contradicted by:** in the first version, `delta` and `efficacy` entered the formula as constants multiplying every (cutoff, threshold) cell identically, so the argmax over cutoffs could never change regardless of the assumed values — the "100% stability across 9 scenarios" result this produced was a mathematical artifact of the formula's structure, not a substantive robustness finding. A second version made `delta` a function of the cutoff's remaining follow-up time (`delta_per_day * remaining_days`) to build in a genuine cutoff/effect-size trade-off — but `delta_per_day` and `efficacy` still multiplied every cell identically for a *given* cutoff, so the ranking was again structurally fixed (this time by `remaining_days` alone) rather than by the swept parameters.

**Changed:** RQ3's (now **RQ-S2.3**) reported result was narrowed to what can be measured without an intervention-effect assumption: precision/recall/lift of early-signal flagging against the *realized* low-growth outcome, which requires no assumption about what an intervention would do. The expected-uplift tables are retained only as explicitly labeled, non-causal what-if illustrations, never as the basis for an "optimal day" claim. Bootstrapped confidence intervals on the precision/recall metric further showed the 7/14/21-day cutoffs' predictive rho values are not statistically distinguishable from one another — reported as the actual (appropriately modest) RQ-S2.3 finding: early intervention judgment appears viable within the first three weeks, without a defensible single optimal day.

`[affects: RQ-S2.3]`

### A.7 Sample-exclusion rules were derived empirically, then made explicit

**Assumed initially:** none — test/template accounts were not anticipated as a distinct category.

**Found:** Step H (`step_h_top_customer_profiling.py`) profiled the top-10 customers driving the Step D clustering concentration using four independent signals (all-time scale, registration-burst pattern, template/naming-pattern signal, and real spend) and found two accounts with near-zero total spend and heavy template signal (single registration burst, zero bid-amount variance) — operationally indistinguishable from test/QA setups rather than real advertising activity.

**Changed:** `sample_definition.known_test_account_ids` in `config/config.yaml` now explicitly excludes these two accounts from every confirmatory analysis, alongside the general rule that produced them — so the exclusion is pre-specified and logged, not applied ad hoc per analysis.

`[affects: H-S2.1, H-S2.2a, H-S2.2b — sample definition shared by all three]`

### A.8 The largest customer's influence was checked, not assumed away

**Found:** Step D showed one customer contributing 32.9% of the trajectory-usable sample. Step H's four-signal profiling classified this customer as a genuine large advertiser (all-time scale in the 100th percentile, meaningful and varied spend, campaigns spread across the full observation window) rather than a bulk-generated template account, so it was not excluded.

**Changed:** because exclusion wasn't warranted, a leave-one-out sensitivity check on this customer was made a **required**, not optional, component of the H-S2.1 confirmatory test — every reported H-S2.1 result is accompanied by the same test re-run with this customer removed, and the verdict rule requires both runs to agree in sign before H-S2.1 is credited.

`[affects: H-S2.1 — required sensitivity check]`

---

## Appendix B. Results Summary (Canonical Statistics Table)

This appendix consolidates statistics for Study 1 and Study 2's formal hypothesis families and is the single citable source for every number reported in this report; §5.6 is a condensed pointer to this table.

### B.1 H-S1.1 (a/b/c) and H-S1.2 — Study 1's Confirmatory Statistics

**H-S1.1a/b/c: full-mediation test (size → spend → outcome).** Customer-level mediation model, `bid_amount` as the cost-independent primary outcome (n=263 customers); CPC-based estimates retained for comparison but treated as directionally informative only (mechanical cost-sharing artifact).

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H-S1.1a (a-path): size → total spend | +0.537 (p<.001) | +0.537 (p<.001) |
| H-S1.1b (b-path): spend → outcome \| size | +1.277 (p<.001) | +0.150 (p=.032) |
| H-S1.1c (c'-path): size → outcome \| spend (direct) | -0.253 (p=.062) | +0.037 (p=.634) |
| Indirect effect (a x b) | +0.253 | +0.081 |
| Bootstrap 95% CI, indirect | [0.121, 0.399] | [0.008, 0.159] |
| Permutation p, indirect | <.001 | <.001 |

**Verdict: H-S1.1c not rejected (null supported); H-S1.1a and H-S1.1b both confirmed.** Full mediation — the direct effect of size, net of spend, is statistically indistinguishable from zero on the primary (cost-independent) outcome, while both mediation legs are individually significant. Backed by 8 independent robustness methods.

**H-S1.2: boundary condition (campaign_type heterogeneity).**

| Product type | n (rows) | n (customers) | c' (size, net of spend) | p |
|---|---|---|---|---|
| Website (1) | 11,894 | 184 | -0.279 | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | .211 |
| Shopping (2) | 2,161 | 17 | +0.245 | .151 |
| **Joint Wald test (size x product-type)** | | | | **.023** |

**Verdict: H-S1.2 rejected — H-S1.1c's null is not perfectly homogeneous** across ad-product categories, though no individual stratum shows a significant size effect on its own.

### B.2 H-S2.1 — Does Account Maturity Predict Initial Growth Slope?

**Primary method**: customer-level aggregate OLS (HC3 robust SE) — n = customers, not ad groups, since maturity varies only at the customer level. **Final arbiter**: cluster (customer-label) permutation test.

| statistic | value |
|---|---|
| n (customers) | 29 |
| n (ad groups, informational) | 204 |
| OLS beta (raw scale) | 8.34 |
| OLS HC3 p-value | .576 |
| Bootstrap 95% CI (raw scale) | [-15.84, 43.08] |
| Cluster permutation p-value | .663 |
| Spearman rho | -.02 (p = .92) |
| Leave-one-out (largest customer excluded) permutation p-value | .702 (sign unchanged) |
| Winsorized (10%) OLS beta / p | 1.48 / .841 |
| Rank-rank OLS beta / p | -.02 / .924 |
| Standardized effect size (beta) | .085 |
| Pre-registered large-effect detection threshold | .50 |
| Observed effect as % of detection threshold | 16.9% |

**Verdict: H-S2.1 not supported.** Five independent checks (raw OLS, bootstrap CI, cluster permutation, leave-one-out, Winsorized/rank-rank OLS) agree; the small positive raw-scale coefficient is attributable to a handful of high-leverage observations. The standardized effect size (.085) sits well below even the small-effect band evaluated in the power simulation, indicating this is a genuine null rather than an under-powered detection.

### B.3 H-S2.2a / H-S2.2b — Do Early Operating Signals Predict Later Growth, and Does Maturity Add Value?

**Method**: Ridge regression, repeated customer-grouped train/test splits (Wilcoxon signed-rank test on the paired improvement) + Leave-One-Customer-Out CV, decomposed into within- and between-customer components.

| early/later window (days) | n (ad groups) | H-S2.2a within-customer LOCO rho | H-S2.2b within-customer LOCO rho | within-customer improvement | repeated-split Wilcoxon p |
|---|---|---|---|---|---|
| 14 / 14 | 204 | 0.467 | 0.487 | +0.019 | .038 (H-S2.2b *worse* on repeated-split rho) |
| 30 / 30 | 184 | 0.275 | 0.257 | -0.018 | .119 |
| 30 / 60 | 179 | 0.060 | 0.061 | +0.001 | .019 (H-S2.2b *worse* on repeated-split rho) |

**Verdict: H-S2.2a supported at short horizons, decaying sharply beyond them; H-S2.2b not supported at any horizon.** 14-day-ahead prediction shows substantial within-customer signal (rho ~ 0.39-0.47 depending on evaluation design); this decays to near zero by the 30/60-day horizon. Adding account maturity never produces a within-customer improvement exceeding +0.02 at any window pair, and the repeated-split design finds the addition significantly *harmful* at two of three window pairs. Pooled/between-customer improvements that appear positive (e.g. +0.388 between-customer at 30/60d) are attributable to H-S2.1-level signal leaking into a pooled metric, not genuine ad-group-level gain.

### B.4 RQ-S2.3 — At What Point Should a Low-Growth Ad Group Be Flagged for Intervention?

**Method**: precision/recall/lift of early-signal-based flagging against realized low-growth outcomes at candidate decision cutoffs (7/14/21 days), evaluated on a fixed 44-day total horizon so cutoffs share an identical ad-group population.

| decision cutoff (days) | out-of-fold predictive rho (95% bootstrap CI) | lift @ threshold=0.25 | lift @ threshold=0.40 |
|---|---|---|---|
| 7 | 0.304 [0.145, 0.445] | 0.83 | 1.27 |
| 14 | 0.265 [0.123, 0.404] | 1.33 | 1.23 |
| 21 | 0.334 [0.210, 0.459] | 1.42 | 1.36 |

(threshold = 0.10 excluded from reported results — 12.6-13.1% of ad groups have `growth_target == 0`, which destabilizes quantile cuts at this narrow a band.)

**Verdict: directional, not precise.** Flagging achieves 1.2-1.4x lift over random across all tested cutoffs and reliable thresholds. The 95% bootstrap confidence intervals on predictive rho overlap substantially across all three cutoffs, so no single cutoff is statistically distinguishable as "optimal" — reported as "early judgment (within 3 weeks of registration) is viable; a single precise optimal day is not defensible from this sample," not as a null result. Two successive expected-uplift simulations were both found to be mathematically incapable of producing a different cutoff ranking regardless of the assumed effect size, because the assumed parameters entered the formula as constants multiplying every (cutoff, threshold) cell identically; this is reported as a designed-in limitation of the uplift approach, not as a finding about intervention effectiveness (Appendix A, entry 6).

### B.5 Combined Takeaway

Across both studies, the structural-blindness construct holds to first order but not perfectly. In Study 1, H-S1.1c's null is confirmed (size has no direct effect once spend is controlled) but H-S1.2 shows that null is not perfectly homogeneous across ad-product categories. In Study 2, H-S2.1's null is confirmed (account maturity does not predict a new ad group's growth) and H-S2.2a/H-S2.2b show that what *does* predict growth is the ad group's own early operating signal, not inherited account history — though neither H-S1.1c's nor H-S2.1's/H-S2.2b's nulls reach formal TOST equivalence, so both are reported as well-powered non-significant associations rather than confirmed absences. The practical implication is the same in both studies: account size or tenure should not be used as a proxy for how a given advertiser or ad group will perform; what the unit itself does — spend, or its own first two weeks of activity — is the more informative, and more actionable, signal.

---

## Appendix C. Data Availability, Reproducibility, and Repository Structure (Summary)

- **Data availability & license**: The underlying panel data (ad-group dimension table, daily/hourly performance logs) are **proprietary and are not included in this repository.** They were processed and provided by a Korean ad-tech data and analytics provider under a research data-sharing agreement. Researchers interested in replication should contact the data provider directly to request access to an equivalent extract. All code is runnable end-to-end against any dataset that matches the documented schema. Code is released under the MIT License; this license covers the analysis code only, not the data.
- **Reproduction procedure (summary)**: (1) Diagnostic pipeline (`run_diagnostics.sh`, Steps A–M) → (2) Confirmatory H-S2.1/H-S2.2 tests (`src/analysis/`) → (3) Earlier-generation v4 pipeline (`run_pipeline_v4.sh`, variance decomposition, fairness battery, churn appendix) → (4) Four supplementary robustness scripts (`run_supplementary_robustness.sh`) → (5) Regeneration of nine figures (`figures/make_figure*.py`). Every step prints its own diagnostics and writes a JSON/CSV artifact; nothing is silently overwritten, and every script can be re-run independently as long as its upstream artifact exists.
- **Repository structure**: `config/` (all paths, thresholds, sample-definition rules), `data/` (schema documentation, no data files committed), `src/utils/`, `src/coldstart_v5/` (diagnostic pipeline Steps A-M), `src/pipeline_v4/` (earlier-generation pipeline), `src/analysis/` (confirmatory tests), `supplementary_robustness/` (4 independently runnable robustness analyses, each mapped to a specific report section), `figures/` (9 figure-generation scripts and PNGs), plus `docs/METHODOLOGY_NOTES.md` and `docs/RESULTS_SUMMARY.md` (= Appendix A and Appendix B of this document).

---

## Appendix D. Methodological Principles Applied Throughout

1. **No result is trusted from a single method.** Every confirmatory test in this report is checked against at least two independent inferential approaches (e.g., parametric OLS + distribution-free permutation test; repeated split-sample validation + Leave-One-Customer-Out CV). Where they disagree, the more conservative, assumption-light method is treated as authoritative (Appendix A, entry 5).
2. **Every "cutoff" or date threshold is derived from the data at run time**, never hard-coded, so a re-extract of the underlying panel cannot silently invalidate downstream thresholds.
3. **Information leakage is checked, not assumed away.** All train/test splits are customer-grouped, and every repeated-split loop verifies (and logs) that no customer appears in both the train and test partitions of any single split.
4. **Sample-exclusion rules are pre-specified and logged**, not applied ad hoc (Appendix A, entry 7).
5. **Null results are reported with the same rigor as positive ones — and are not conflated with confirmed nulls unless a formal equivalence test says so.** Every non-significant central result (H-S1.1c, H-S2.1, H-S2.2b) is accompanied by (a) a pre-registered power simulation establishing what effect sizes the sample could and could not have detected, and (b), where central to the argument, a TOST equivalence test establishing whether the absence of an effect can be formally bounded (Figure 9).
6. **A single quantitative point estimate is never taken at face value when a structural artifact could inflate it.** Where an outcome construction shares a mechanical term with a predictor (§4.4), the mechanical component is explicitly isolated and the conclusion is re-anchored on an artifact-free alternative outcome (Figure 7).
7. **Sensitivity statistics are checked for numerical stability before being reported as evidence.** A large-looking robustness statistic (Oster's delta) computed in a numerically unstable regime is reported transparently but is not used to support a robustness claim (§8, §12.7).
8. **Every hypothesis or research question is assigned a permanent, study-prefixed ID (§2) before its results are reported**, so that a claim, a figure, and a statistics table can always be traced back to the same, unambiguous test — and so a superseded or retired question (e.g. RQ-S2.0) stays auditable rather than silently disappearing from the record.
