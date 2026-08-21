# Structural Signal Irrelevance on an Algorithmically-Mediated Ad Platform

**A two-level mediation-audit study of (1) whether advertiser size retains a residual,
direct association with algorithmic outcomes once total spend is held constant, and
(2) why that relationship is not uniformly expressed across advertising contexts.**

> **Repository status.** This is a research repository, not a publication. It documents a
> working analysis pipeline, its full diagnostic history — including reversed intermediate
> results, corrected errors, and abandoned framings — and a two-level evidentiary structure
> distinguishing pre-specified confirmatory tests from post-hoc exploratory analysis. Nothing
> here should be cited as a peer-reviewed result.

> **How to read this repository.** Every claim below carries an explicit evidence tag:
> **[CONFIRMATORY]**, **[POST-HOC / EXPLORATORY]**, or **[FUTURE WORK]**. This tagging is not
> decorative — it is the single most important convention in this repository. A reader who
> only wants the pre-registered-style result should read Level 1 and stop. A reader interested
> in why that result was not cleaner should continue to Level 2, understanding that everything
> there is exploratory, was motivated by patterns observed *after* Level 1 was run, and is
> reported at "consistent with, but does not establish" strength — never stronger.

---

## Table of contents

1. [At a Glance](#1-at-a-glance)
2. [How the Research Question Evolved](#2-how-the-research-question-evolved)
3. [Theoretical Framework](#3-theoretical-framework)
4. [Data & Setting](#4-data--setting)
5. [Level 1 — Confirmatory Study: Does Size Matter?](#5-level-1--confirmatory-study-does-size-matter)
6. [Level 2 — Post-hoc Exploratory Study: Why Might the Effect Vary?](#6-level-2--post-hoc-exploratory-study-why-might-the-effect-vary)
7. [Research-wide Multiplicity Audit](#7-research-wide-multiplicity-audit)
8. [Methodological Positioning — Mediation Audit, Two Evidentiary Tiers](#8-methodological-positioning--mediation-audit-two-evidentiary-tiers)
9. [Synthesis](#9-synthesis)
10. [Boundary Conditions & Generalizability](#10-boundary-conditions--generalizability)
11. [Limitations](#11-limitations)
12. [Transparency Log — Known Issues, Reversals, and Corrections](#12-transparency-log--known-issues-reversals-and-corrections)
13. [Figure Gallery](#13-figure-gallery)
14. [Repository Structure](#14-repository-structure)
15. [How to Reproduce](#15-how-to-reproduce)

---

## 1. At a Glance

| | Level 1 (Confirmatory) | Level 2 (Post-hoc Exploratory) |
|---|---|---|
| **Question** | Does advertiser size directly associate with algorithmic outcomes, net of spend? | Why does that relationship appear to vary across advertising contexts? |
| **Status** | Pre-specified, run once, not revised after seeing results | Motivated entirely by patterns observed *after* Level 1 was completed |
| **Sample** | 321 advertisers, ~19.3M rows; core test n=263 customers, 4,407 CPC obs. | Sub-clusters of the same sample, G≈13–72 per campaign type |
| **Central result** | H1c null (β=−0.253, p=.062); 8/8 robustness methods agree | Local-business campaigns show structurally distinct serving characteristics (0% keyword-auction matching) associated with instability in the H1c estimate when included/excluded |
| **Evidence grade** | **Confirmatory** | **Exploratory — consistent with, but does not establish, a causal mechanism** |
| **Key caveat** | None beyond the standard mediation-audit scope (§8) | Built on clusters below the G≥42 rule-of-thumb for cluster-robust SE validity; not preregistered; one reported finding (leave-one-type-out ranking) reversed after a methodological correction — both passes reported in §12 |

**One-line summary:** the pre-specified test of whether advertiser size buys a direct
algorithmic advantage returns a clean, well-powered, 8-way-robust **null**
[CONFIRMATORY]. A post-hoc look at *why* this null is not perfectly uniform across
campaign types surfaces a plausible, but not established, explanation: local-business
advertising appears to run through a structurally different, non-auction serving pathway
[POST-HOC / EXPLORATORY]. Neither finding is a substitute for the other, and the second
does not upgrade the confidence of the first.

---

## 2. How the Research Question Evolved

This section exists because failing to disclose *when* a research question was formulated
is itself a form of HARKing, even if every individual statistic is reported honestly.
This repository's research question was **not** static from the start. It evolved in two
stages, and both stages are disclosed here rather than folded into a single retrospective
framing.

**Stage 1 (original, pre-specified).**
> *Does advertiser size confer a direct algorithmic performance advantage on a paid-search
> platform, independent of spend?*

This is the question Level 1 (§5) answers. The hypothesis battery (H1a/H1b/H1c/H2), the
sample, the outcome variables, and the robustness plan were fixed before the central
regression was run.

**Stage 2 (post-hoc, formulated after seeing Level 1's results).**
> *Under what platform-serving conditions might advertiser size translate into a
> performance advantage?*

This second question did **not** exist when Level 1 was designed. It was formulated after
Level 1 returned a null result and after inspecting `campaign_type` heterogeneity revealed
that local-business campaigns behave structurally differently from the rest of the sample.
Framing this as a single, seamless research arc from the outset would misrepresent how the
analysis actually unfolded. It is disclosed here as a two-stage process precisely so a
reader can weigh Stage-2 findings appropriately: they are the output of the same
investigation that produced Stage 1, not an independent confirmation of it.

---

## 3. Theoretical Framework

### 3.1 Two competing accounts (Level 1's object of test)

- **Statistical discrimination / structural entrenchment** (Phelps 1972; Arrow 1973; Spence
  1973): a decision-maker facing incomplete information about counterparty quality falls
  back on cheap, observable, structural proxies — here, advertiser size — even when a more
  direct behavioral signal (spend) is available. Predicts a **significant residual
  association** of size with outcomes, net of spend.
- **Algorithmic behavioral meritocracy** (Dwork et al. 2012, individual fairness):
  a well-specified, real-time auction system should condition allocation on current
  behavior, not accumulated structural status. Predicts **no residual association** of size
  with outcomes, net of spend.

### 3.2 Structural Signal Irrelevance (SSI)

> **Definition.** In an algorithmically-mediated market, let S be a structural attribute
> (size), B a legitimate behavioral signal (spend), Y an algorithmic outcome. The system
> exhibits **structural signal irrelevance with respect to S** when Y ⊥ S | (B, X) holds —
> assessed via decomposition of S's association with Y into a path mediated by B and a
> direct residual path net of B.

SSI is a descriptive, outcome-side property of the observed system — distinct from
statistical discrimination (a decision-maker-side causal account of *why*) and from
individual fairness (a normative benchmark). A single confirmatory null on H1c is evidence
*toward* SSI; a robust SSI claim rests on convergence across many independent robustness
methods (achieved in Level 1, §5) and, ideally, replication across contexts (attempted, at
exploratory strength only, in Level 2, §6).

### 3.3 Boundary conditions on SSI (P1–P5)

- **P1 (real-time conditioning).** SSI is more likely where allocation is per-transaction on
  current behavioral signals without human-review buffering.
- **P2 (auction/market liquidity).** SSI is more likely in categories with enough
  transaction volume that even a small unit accumulates a usable behavioral signal quickly.
- **P3 (discretionary review re-entry).** Sub-processes with human discretionary review are
  SSI-violation *candidates* even within an otherwise SSI-consistent system.
- **P4 (measurability).** SSI can only be evaluated where the behavioral signal and outcome
  are measured with completeness that does not itself correlate with S. Where it does not
  (as with Conversion/ROAS, excluded in §4), SSI is **not testable**, not violated.
- **P5 (mechanism applicability) — new, motivated entirely by Level 2 findings.** The SSI
  audit design presupposes that the outcome is generated by an auction/bidding serving
  mechanism. Where this premise does not hold (in this sample: local-business campaigns,
  0% keyword-auction matching, §6.2, [Figure 13](#figure-13)), the SSI test may fall
  **outside its own scope of applicability** rather than being violated.
  **[POST-HOC / EXPLORATORY — this proposition did not exist before Level 2's findings and
  is reported as a candidate boundary condition, not an established one.]**

---

## 4. Data & Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata incl. `campaign_type` | 1,504 | 263/321 |
| Ad group dimension (2026-07-22 snapshot) | Bid price, registration timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status`, bid price | 1,503,289 | 256/321 |

**Construct-validity exclusion.** Conversion/ROAS variables are excluded from all outcome
sets by design (P4 above): Naver's conversion-tracking backfill lag is plausibly correlated
with advertiser size itself, which would risk manufacturing the very direct-path pattern
H1c is designed to detect, as a measurement artifact rather than a genuine finding.

---

## 5. Level 1 — Confirmatory Study: Does Size Matter?

**Status: [CONFIRMATORY].** Every analysis in this section was specified — sample,
variables, model, robustness plan — before the central regression was estimated, and none
of it was revised after seeing results.

### 5.1 Central test (H1c)

Controlling for log spend in a cluster-robust regression (n=263 customers, 4,407 CPC
observations), all six outcome × sample combinations return non-significant direct-path
coefficients for size (cluster-robust p > .07). Bootstrap CIs sit inside or at the edge of
their pre-registered minimum-detectable-effect band at 80% power. Approximate Bayes factors
favor the null in 5 of 6 tests.

| Path | CPC-based (secondary) | bid_amount-based (primary, cost-independent) |
|---|---|---|
| H1a: size → spend | +0.537 (p<.001) | +0.537 (p<.001) |
| H1b: spend → outcome \| size | +1.277 (p<.001) | +0.150 (p=.032) |
| **H1c: size → outcome \| spend** | −0.253 (p=.062) | +0.037 (p=.634) |
| Indirect (a×b), bootstrap 95% CI | [0.121, 0.399] | [0.008, 0.159] |

**Verdict:** H1c not rejected (null supported). H1a/H1b confirmed. Statistically consistent
with full mediation. Backed by an 8-way independent robustness battery (specification
curve, placebo test, FE panel, temporal split, FDR correction, mechanical-artifact
isolation, cost-independent outcome replication, and — see §5.2 — a core-model influence
diagnostic).

### 5.2 H1c core-model influence diagnostic [CONFIRMATORY robustness check]

Because influence diagnostics are often applied only to secondary or exploratory models,
this repository applies one to the **primary H1c model itself**, prior to any exploratory
branching, using rules fixed before any coefficient was inspected:

- DFBETA-flagged influential customers: 15/228 (customer-level regression, threshold
  2/√228 = 0.1325).
- These 15 are **not** disproportionately local-business advertisers (t-test on `share_6`,
  p=.53) — ruling out the naive worry that Level 2's focal subgroup was driving Level 1's
  headline result.
- Three pre-specified exclusion rules (thin-observation customers; low performance-match-
  rate customers; both combined) were applied *before* inspecting whether they would change
  the significance verdict. Result: **0/4 configurations (baseline + 3 rules) reached
  significance.** Consistency rate 100%.

**Verdict: confirmatory grade maintained.** The H1c null is not an artifact of a handful of
influential observations, and does not depend on which of several defensible, pre-specified
data-quality exclusion rules is applied.

### 5.3 Robustness battery (summary)

| # | Method | Result |
|---|---|---|
| 1 | Specification curve (48 choices) | 0/48 reach significance |
| 2 | Placebo test (device-type share) | Regression-level test correctly null on placebo |
| 3 | Customer × month FE panel | Consistent with central estimate |
| 4 | 2SLS (lagged spend instrument) | Incomplete (code exception); excluded from conclusions |
| 5 | Temporal split (era1 vs era2) | Consistent |
| 6 | Benjamini–Hochberg FDR | Null survives correction |
| 7 | Mechanical-artifact isolation (CPC vs bid_amount) | Confirmed real, not purely mechanical |
| 8 | Cost-independent outcome replication | Same qualitative pattern |

**Level 1 conclusion:** *A uniform, direct advertiser-size advantage on this platform's
algorithmic outcomes is not confirmed.* This negative result is the confirmatory backbone
of the paper.

---

## 6. Level 2 — Post-hoc Exploratory Study: Why Might the Effect Vary?

**Status: [POST-HOC / EXPLORATORY throughout this entire section].** None of what follows
was preregistered. All of it was motivated by patterns observed after Level 1 was
completed. None of it upgrades Level 1's evidence grade, and none of it should be read as
having established a causal mechanism. Every subsection ends with an explicit statement of
what the evidence does and does not support.

> **Small-cluster warning (applies to all of §6).** Several analyses below rely on
> campaign-type sub-clusters with G≈13 (power content) to G≈72 (local business), below or
> near the conventional G≥42 rule-of-thumb for cluster-robust standard error validity. Where
> checked directly, standard cluster-robust p-values diverge from wild-cluster-bootstrap
> p-values by up to 0.16–0.17 in these subgroups. Treat all p-values in this section as
> approximate.

### 6.1 Campaign-type heterogeneity (the trigger for Level 2)

Stratifying the H1c model by `campaign_type` (n=184/27/17 for website/local-business/
shopping), a joint Wald test on the size × product-type interaction gives p=.023. No
individual stratum is significant alone. A continuous-share re-specification (Option B)
found the same qualitative pattern: a joint interaction test significant overall (p=.0002),
but with only one campaign type — local business — surviving three-round robustness
screening (permutation test, pairs bootstrap, wild-cluster bootstrap) at 3/5 methods.
**This is the observation that motivated everything else in §6.** It is not, on its own,
strong evidence of anything; it is the anomaly that prompted investigation.

### 6.2 Serving-mechanism heterogeneity across campaign types

| Campaign type | n ad groups | % ad groups keyword-matched | Median actual-CPC / bid ratio | Classified |
|---|---|---|---|---|
| Website | 8,086 | 96.8% | 2.77 | Auction-like |
| Shopping | 1,025 | 0.7% | 1.89 | Non-auction-like |
| Power content | 248 | 94.8% | 4.33 | Auction-like |
| Brand/new product | 198 | 92.9% | — | Auction-like |
| **Local business** | **266** | **0.0%** | **0.76** | **Non-auction-like** |

<a id="figure-13"></a>
![Figure 13 — Serving-structure heterogeneity across campaign types](figures/Figure13_serving_structure.png)
*Figure 13 [POST-HOC / EXPLORATORY] — local business is the only campaign type with 0%
keyword-auction matching and an actual-CPC/bid ratio below 1, both directly observed
structural facts.*

Local-business ad groups show **zero** matches to the keyword-dimension table — a
structural fact, confirmed by tracing the join chain (campaign_dim → adgroup_dim →
keyword_dim) rather than assumed. This is consistent with local-business ads being served
through a location/business-channel mechanism rather than keyword auction (the
`business_channel_id_mobile/pc` fields present in `adgroup_dim` are circumstantially
consistent with this, though this was not independently verified against Naver's official
product documentation).

**What this does and does not establish:** this is an observed structural fact about the
data (keyword-join coverage), not an inference. What it does *not* establish is that this
structural difference is the *cause* of H1c's instability — that is addressed, at
exploratory strength, in §6.3–6.4.

### 6.3 Statistical signatures consistent with a distinct CPC-generation process

Three separate diagnostics, run on the auction-classified vs. non-auction-classified
campaign types:

- **Variance heterogeneity:** Brown-Forsythe test on log(CPC) across types, p<.0001;
  local-business std=1.67 vs. pooled-other std=1.41 (p=.0003).
- **Relationship (b-path) heterogeneity:** in a pooled model with a local-business
  indicator, spend_z × is_localbiz = +1.125 (p=.001); joint Wald on both interaction terms,
  p=.0009.
- **Leverage:** local-business customers do **not** show significantly elevated regression
  leverage relative to others (hat-value t-test, p=.24) — this specific link in the
  mechanism chain was **not** confirmed.
- **Counterfactual magnitude:** predicting local-business CPC from the auction-type
  bid→CPC relationship and comparing to observed CPC gives a standardized gap of
  −0.49 SD (t=−4.75, p<.0001) — a real but modest-sized deviation.

**Verdict on this sub-chain: 3 of 4 tested links show a statistically detectable pattern; 1
does not.** This is reported as **partial, mixed support** for a mechanism-level
explanation — not as an established causal chain. The original internal framing of this as
a "confirmed causal chain" is explicitly retracted; see §12.

### 6.4 H3 (subgroup dependence) — including the reversal that occurred

**H3, as an exploratory question:** does H1c's null depend on whether local-business
customers are included, beyond what would be expected from sample-size reduction alone?

**What was found, in the order it was found — including the part that initially pointed the
other way:**

1. Excluding all 72 local-business-spending customers shifts H1c from β=−0.253 (p=.062,
   n=228) to β=−0.499 (p=.006, n=156) — a reversal from non-significant to significant.
2. A random-placebo test (2,000 draws of 72 customers) found this magnitude of shift in only
   0.9% of draws; a size-matched placebo found it in 0.4% — both suggesting the shift is not
   purely a sample-size artifact.
3. **An initial leave-one-type-out comparison across all five campaign types ranked
   local-business exclusion 2nd out of 4 by raw coefficient shift — website exclusion ranked
   1st.** Taken at face value, this would have *undermined* the local-business-specific
   story.
4. On inspection, website exclusion removed 202/228 customers, leaving only 26 — a sample
   too small for a stable estimate (95% CI width 1.62 vs. 0.71 for local-business exclusion;
   correlation between remaining-n and CI width = −0.98). A corrected comparison,
   re-running the random-placebo test separately **for each campaign type's own exclusion
   size** (rather than comparing raw coefficient shifts across differently-sized
   exclusions), found that among the three types with stable remaining samples (shopping,
   power content, local business), local-business exclusion had by far the lowest empirical
   p-value (1.0% vs. 91.7% and 66.3%).

<a id="figure-12"></a>
![Figure 12 — H3 leave-one-type-out: uncorrected vs. corrected ranking](figures/Figure12_h3_leave_one_type_out.png)
*Figure 12 [POST-HOC / EXPLORATORY] — Panel A: the initial, uncorrected ranking by raw
coefficient shift (website ranks 1st only because its remaining sample, n=26, is
unstable). Panel B: the corrected, exclusion-size-matched empirical-p ranking among the
three campaign types with stable remaining samples (local business is the clear outlier).
Both panels are shown together, per the disclosure policy in `docs/METHODOLOGY_NOTES.md`
entry B6 — the corrected ranking is never presented without the uncorrected one.*

**Both passes are reported here deliberately.** The first (uncorrected) comparison did not
support a local-business-specific story; the correction that reversed this was
methodologically justified (comparing estimates of similar precision) but was applied
*after*, and *because of*, an unfavorable initial result. A reader should weigh this
accordingly: the corrected conclusion is defensible, but it was not the first answer the
data gave, and it was not preregistered either way.

**Overall H3 verdict: partially supported, on corrected analysis.** Reported strength:
*consistent with a local-business-specific dependency, not conclusively established.*

### 6.5 Alternative explanations audited (and one partially ruled in, not fully ruled out)

Before accepting any mechanism-level story, this repository tested whether the observed
patterns could instead be explained by mundane data artifacts:

- **Was the observed missingness/influence pattern just a mechanical artifact of accounts
  having more ad groups?** `size_z` and `n_ad_groups_total` were discovered to be **the same
  variable** (size_z is a standardized log-transform of ad-group count), which invalidated
  an earlier "control for ad-group count" analysis (VIF=∞). A combinatorial null model was
  built instead: if missingness were purely a function of "more ad groups → higher chance
  one is unmatched," a simple binomial model should fit. It does **not** fit well
  (over-dispersion ratio 73×; goodness-of-fit χ²=16,583, df=6, p<.0001) — account-level
  clustering beyond pure combinatorics is present.

  <a id="figure-15"></a>
  ![Figure 15 — Observed vs. combinatorially-predicted missingness rate](figures/Figure15_combinatoric_null_model.png)
  *Figure 15 [POST-HOC / EXPLORATORY] — the persistent gap between observed and
  independent-binomial-predicted missingness rates, especially at low-to-mid ad-group
  counts, is the basis for the over-dispersion finding: some account-level clustering
  beyond pure combinatorics is present, though its cause remains unidentified.*

  **Verdict: the size↔missingness association is not fully reducible to sample-size
  mechanics, but the residual cause is unidentified.**
- **Was the localbiz leverage effect driven by 1–2 extreme accounts?** Influence diagnostics
  (corrected for a DFBETA scale-mismatch bug, documented in §12) found no sign reversal
  across leave-k-out removal (k=1,3,5,10,15); if anything, removing the most influential
  accounts *strengthened* rather than weakened the pattern.
- **Was it a keyword-review/approval-pipeline effect (parallel to the shopping-campaign
  hypothesis in §6.1)?** No — local-business ad groups have zero keyword-dimension matches
  at all, so this specific mechanism candidate does not apply; it was a dead end, reported
  as such rather than quietly dropped.

### 6.6 What Level 2, taken together, does and does not support

> **Does support (at exploratory strength):** advertising-type heterogeneity in serving
> structure is a real, observable feature of this platform, most pronounced for
> local-business campaigns; several statistical signatures (variance, relationship slope,
> counterfactual CPC gap, corrected subgroup-dependence test) are consistent with this
> structural difference mattering for how CPC is generated; and this is not fully explained
> away by sample-size mechanics alone.
>
> **Does not support:** a claim that platform serving structure has been shown to *cause*
> H1c's instability; a claim that this pattern would replicate in an independent sample; or
> a claim that any single number above should be read at the same confidence level as
> Level 1's H1c result.

**Theoretical proposition (exploratory, not established):** structural advantage may be
*conditional* on platform-serving conditions rather than *automatic*. This reframes the
paper's contribution from "large advertisers are/are not favored" to "when structural scale
converts into performance may depend on how the platform serves the ad" — a claim Level 2
is consistent with but has not confirmed.

---

## 7. Research-wide Multiplicity Audit

Every hypothesis-family in this repository corrects for multiple comparisons internally.
This section additionally pools **every p-value reported anywhere in this repository as an
official statistic** (n=25; excludes purely distribution-generating procedures such as the
48-specification curve or the 500-way split-sample replication) into a single test family.

<a id="figure-14"></a>
![Figure 14 — Research-wide multiplicity audit across all 25 reported p-values](figures/Figure14_multiplicity_audit.png)
*Figure 14 [CROSS-CUTTING] — each point is one officially-reported p-value, colored by
hypothesis family, sorted by significance. The dashed line is the pooled Bonferroni
threshold (0/25 tests clear it); the dotted line is the rank-dependent BH-FDR threshold
(3/25 clear it, all from the Level 2 H3 analysis).*

| Correction | Tests surviving |
|---|---|
| Bonferroni (α=.05/25=.002) | **0 / 25** |
| Benjamini–Hochberg FDR | **3 / 25** (all from the exploratory H3 subgroup-dependence analysis, §6.4) |

**Reading this table correctly:** this is not a criticism to bury — it is the single most
important piece of evidence-calibration information in this repository. It means that if a
reader insists on a fully pooled, maximally conservative view of every number this project
has produced, essentially nothing survives except the exploratory H3 result, and even that
only survives the more permissive FDR correction. Level 1's H1c null does not "survive" this
correction because it was never significant to begin with — the null is the finding. This
table exists precisely so that no exploratory result from §6 can be quietly read as having
the same statistical weight as Level 1's central, well-powered null.

---

## 8. Methodological Positioning — Mediation Audit, Two Evidentiary Tiers

This repository is designed as a **mediation audit** (Sandvig et al. 2014; Metaxa et al.
2021; Raji et al. 2020) — appropriate when platform access for a sock-puppet or
field-experimental audit is unavailable. It supports a sharper procedural-fairness claim
than a raw correlation audit but does not support causal identification (2SLS/RDD/
policy-change screenings, found no usable identification design and are reported as null
supplementary robustness, not as adopted strategies — see
`supplementary_identification/SCREENING_SUMMARY.md`).

Within this design, the **Level 1 / Level 2 split** is the operative discipline: Level 1
answers the mediation-audit's pre-specified question; Level 2 investigates *why* that
answer was not perfectly clean, using methods chosen after seeing the data, and is reported
at correspondingly lower evidentiary strength throughout, never described as confirming or
disconfirming Level 1.

---

## 9. Synthesis

| | Level 1 (H1c) | Level 2 (localbiz mechanism) |
|---|---|---|
| Evidence grade | **Confirmatory** | **Exploratory** |
| Robustness convergence | 8/8 independent methods null | 3/4 mechanism-chain links detected; mixed |
| Survives research-wide multiplicity audit (§7) | Null was never claimed significant — not applicable | Partially (FDR only, not Bonferroni) |
| Correct citation form | "advertiser size shows no confirmed direct algorithmic advantage on this platform" | "patterns are consistent with, but do not establish, conditional serving-structure effects" |

**Combined message:** the pre-specified question — does size buy a direct algorithmic
advantage? — returns a confirmatory null. A post-hoc look at why that null is not perfectly
uniform surfaces a plausible, partially-supported, unconfirmed explanation involving
platform serving structure. Neither claim should be read as strengthening the other.

---

## 10. Boundary Conditions & Generalizability

See §3.3 for P1–P5. P1–P4 were derived from the platform-governance literature prior to
data collection; **P5 is post-hoc**, formulated entirely from Level 2's findings, and is
explicitly marked as a candidate proposition pending independent test — not a confirmed
addition to the SSI framework.

**Procedural vs. distributive fairness.** This repository's confirmatory finding concerns
procedural fairness only (does the algorithm condition on structural status net of current
behavior). It is silent on distributive fairness (whether behavior-only allocation is
itself equitable across advertisers with unequal starting resources).

---

## 11. Limitations

| # | Limitation | Level |
|---|---|---|
| 1 | Single agency, single platform — generalizability is architecturally scoped, not empirically tested across platforms | Both |
| 2 | This is a mediation audit, not a causal-inference study, by design; RDD/2SLS/policy-change screening found no usable identification design | Level 1 |
| 3 | H2 strata and Level 2 sub-clusters are unevenly sized (G≈13–72); standard cluster-robust SEs diverge from wild-bootstrap SEs by up to 0.17 in these subgroups | Level 2 |
| 4 | Conversion/ROAS excluded entirely (P4 measurability boundary) | Level 1 |
| 5 | Level 2's leave-one-type-out ranking reversed after a correction for unequal exclusion-sample stability; both passes are disclosed in §6.4 and §12, not only the corrected one | Level 2 |
| 6 | Level 2's mechanism sub-chain (§6.3) is only partially confirmed (3/4 links); leverage heterogeneity specifically was not detected | Level 2 |
| 7 | `size_z` and `n_ad_groups_total` were discovered to be the same underlying variable, invalidating an earlier "mechanical artifact" control analysis; the replacement combinatorial-null-model analysis is itself only suggestive (§6.5) | Level 2 |
| 8 | Research-wide, 22/25 officially-reported p-values do not survive even the more permissive FDR correction when pooled (§7) | Both — read all individual-family significance claims with this in mind |
| 9 | This repository establishes procedural fairness only; distributive fairness is not addressed | Both |
| 10 | Single-sample, single-time-axis result; a separately-scoped longitudinal companion study exists (`FUTURE_RESEARCH_STUDY2.md`) but is not part of this evidence base | Level 1 |

---

## 12. Transparency Log — Known Issues, Reversals, and Corrections

*Full narrative log in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md). This table
lists only the highest-stakes items; consult the full log for every entry.*

| # | Issue | Resolution |
|---|---|---|
| 1 | Original framing described RDD/policy-change screening as "failed identification attempts" | Reframed as supplementary robustness under mediation-audit positioning (§8); underlying statistics unchanged |
| 2 | DFBETA influence-diagnostic scale mismatch: row-level DFBETA summed across ~190 daily observations per customer was compared against a customer-count-based threshold | Corrected to customer-level (1 customer = 1 row) regression DFBETA; conclusions about sign-stability unchanged, but the "0 customers exceed threshold" claim was invalid and is retracted |
| 3 | Leave-one-type-out ranking (§6.4) initially placed local-business exclusion 2nd, contradicting the emerging local-business narrative; this was **not suppressed** and is disclosed alongside the corrected 1st-place ranking, with the reason for the correction (unequal, unstable remaining-sample sizes) stated explicitly | Both passes reported in §6.4, [Figure 12](#figure-12) |
| 4 | `size_z` and `n_ad_groups_total` found to be mathematically the same variable (VIF=∞ in an attempted "control" regression) | Earlier "mechanical artifact ruled out" conclusion based on that regression is retracted; replaced with a combinatorial null-model test (§6.5, [Figure 15](#figure-15)) |
| 5 | An earlier internal draft described the local-business mechanism findings (§6.3) as a "confirmed causal chain" | Retracted; reframed as "3 of 4 tested links show a statistically detectable pattern," explicitly not a causal claim |
| 6 | 2SLS first-stage F-statistic silently returned `None` due to an uncaught exception | 2SLS excluded from all confirmatory conclusions |

---

## 13. Figure Gallery

All figures render inline below and also live as standalone PNGs in
[`figures/`](figures/) for direct download or embedding elsewhere.

### Figures 1–11 (Level 1, confirmatory)

Figures 1, 2, 3, 7, 8, and 11 are the original Level 1 robustness figures (variance
decomposition, the H1c fairness forest plot, the specification-curve/placebo test, the
spend-mediation b-path comparison, the campaign-type-heterogeneity forest plot that
motivated Level 2, and the RDD/policy-change identification-screening summary,
respectively). See `docs/RESULTS_SUMMARY.md` for the statistics behind each.

### Figures 12–15 (new — Level 2 exploratory + cross-cutting audit)

<a id="figure-12"></a>
### Figure 12 — H3 leave-one-type-out: uncorrected vs. corrected ranking [POST-HOC / EXPLORATORY]
*used in §6.4, §12 (entry 3)*

![Figure 12](figures/Figure12_h3_leave_one_type_out.png)

Panel A shows the initial, uncorrected ranking by raw coefficient shift — website exclusion
ranks 1st, but only because its remaining sample (n=26) is unstable (95% CI width 1.62).
Panel B re-ranks using an exclusion-size-matched empirical p-value among the three campaign
types with stable remaining samples; local-business exclusion is the clear outlier
(empirical p=1.0%). Both panels are shown together per the disclosure policy in
`docs/METHODOLOGY_NOTES.md` entry B6 — the corrected ranking is not presented without the
uncorrected one.

---

<a id="figure-13"></a>
### Figure 13 — Serving-structure heterogeneity across campaign types [POST-HOC / EXPLORATORY]
*used in §6.2, §6.3*

![Figure 13](figures/Figure13_serving_structure.png)

Local business is the only campaign type with 0% keyword-auction matching and an
actual-CPC/bid ratio below 1 — both directly observed structural facts (not inferences),
established by tracing the campaign_dim → adgroup_dim → keyword_dim join chain.

---

<a id="figure-14"></a>
### Figure 14 — Research-wide multiplicity audit across all 25 reported p-values [CROSS-CUTTING]
*used in §7*

![Figure 14](figures/Figure14_multiplicity_audit.png)

Each point is one officially-reported p-value, colored by hypothesis family, sorted by
significance. The dashed line is the pooled Bonferroni threshold (0/25 tests clear it); the
dotted line is the rank-dependent BH-FDR threshold (3/25 clear it, all from the Level 2 H3
analysis). No Level 1 test needs to clear either line, since H1c's null was never claimed
significant.

---

<a id="figure-15"></a>
### Figure 15 — Observed vs. combinatorially-predicted data-missingness rate [POST-HOC / EXPLORATORY]
*used in §6.5*

![Figure 15](figures/Figure15_combinatoric_null_model.png)

If missingness were purely "more ad groups → higher chance one is unmatched by chance," the
dashed line (independent-binomial prediction) should track the solid line (observed rate)
closely. The persistent gap, especially at low-to-mid ad-group counts, is the basis for the
over-dispersion finding (§6.5): some account-level clustering beyond pure combinatorics is
present, though its cause remains unidentified.

### Figure index

| # | Title | Script | Tier |
|---|---|---|---|
| 1 | Multilevel variance decomposition | `figures/make_figure1_variance_decomposition.py` | [CONFIRMATORY] |
| 2 | Advertiser-size effect, controlling for spend | `figures/make_figure2_fairness_forest_plot.py` | [CONFIRMATORY] |
| 3 | Multiverse specification curve + placebo | `figures/make_figure3_specification_curve_placebo.py` | [CONFIRMATORY] |
| 4 | Churn-prediction benchmarking (appendix) | `figures/make_figure4_churn_benchmark.py` | [EXPLORATORY, non-confirmatory appendix] |
| 7 | Spend-mediation b-path | `figures/make_figure7_mediation_forest.py` | [CONFIRMATORY] |
| 8 | Product-type heterogeneity (H2 trigger) | `figures/make_figure8_boundary_condition_forest.py` | [CONFIRMATORY → triggers Level 2] |
| 11 | Alternative-identification screening (RDD + policy-change, null) | `figures/make_figure11_identification_screening.py` | [CONFIRMATORY, supplementary] |
| **12** | **H3 leave-one-type-out, uncorrected vs. corrected** | `figures/make_figure12_h3_leave_one_type_out.py` | **[POST-HOC]** |
| **13** | **Serving-structure heterogeneity by campaign type** | `figures/make_figure13_serving_structure.py` | **[POST-HOC]** |
| **14** | **Research-wide multiplicity audit (25 p-values)** | `figures/make_figure14_multiplicity_audit.py` | **[CROSS-CUTTING]** |
| **15** | **Combinatoric null model vs. observed missingness** | `figures/make_figure15_combinatoric_null_model.py` | **[POST-HOC]** |

Figures 5, 6, 9, and 10 from an earlier version of this repository belonged to the descoped
longitudinal study and have moved to
[`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md).

---

## 14. Repository Structure

```
structural-signal-irrelevance/
├── README.md                          <- you are here
├── FUTURE_RESEARCH_STUDY2.md          <- descoped longitudinal study
├── FUTURE_RESEARCH_STUDY3.md          <- proposed preregistered confirmatory test of P5 / Level 2 findings
├── LICENSE
├── requirements.txt
│
├── config/
│   └── config.yaml
│
├── data/
│   └── README.md
│
├── src/
│   ├── utils/
│   │   ├── io.py
│   │   └── identifiers.py
│   │
│   └── pipeline_v4/                              <- Level 1 (confirmatory) pipeline, unchanged
│       ├── step0_data_prep_v4.py
│       ├── step1_variance_decomposition_v4.py
│       ├── step2_advertiser_size_fairness_v4.py
│       ├── step3_churn_appendix_v4.py
│       └── step4_synthesis_v4.py
│
├── supplementary_robustness/                     <- Level 1 supplementary robustness, unchanged
│   ├── supplementary_robustness_README.md
│   ├── 01_alternative_outcome_mediation.md / .py
│   ├── 02_boundary_conditions.md / .py
│   └── 03_equivalence_and_sensitivity_notes.md / .py
│
├── supplementary_identification/                 <- Level 1 RDD/policy-change screening, unchanged
│   ├── SCREENING_SUMMARY.md
│   ├── step11_alt_identification_RDD_policy.py
│   ├── step11b_donut_hole_full_scan.py
│   └── step11c_customer_level_reanalysis.py
│
├── supplementary_localbiz_exploratory/           <- ALL Level 2 (post-hoc, local-business) content
│   ├── README.md                                 <- [POST-HOC/EXPLORATORY] scope banner, links back to root §6
│   ├── run_all.sh
│   │
│   ├── 01_panel_build/
│   │   └── h2_composition_panel_build_v2.py
│   ├── 02_composition_regression/
│   │   └── h2_composition_regression_robustness_v2.py
│   ├── 03_influence_diagnostics/
│   │   ├── h2_localbiz_influence_diagnostics.py          <- superseded, kept for provenance
│   │   └── h2_localbiz_influence_diagnostics_fixed.py    <- corrected DFBETA scale (METHODOLOGY_NOTES B2)
│   ├── 04_case_deepdive/
│   │   └── h2_two_customers_deepdive.py
│   ├── 05_mechanism_search/
│   │   ├── h2_localbiz_split_replication_mechanism.py
│   │   ├── h2_localbiz_mechanism_candidate_scan.py
│   │   ├── h2_localbiz_keyword_join_diagnostic.py
│   │   └── h2_channel_id_account_structure_check.py
│   ├── 06_h3_subgroup_dependence/
│   │   ├── h3_subgroup_dependence_test.py
│   │   └── h3_type_matched_fairness_correction.py        <- corrects the leave-one-type-out ranking (METHODOLOGY_NOTES B6)
│   ├── 07_causal_chain/
│   │   └── localbiz_structural_heterogeneity_causal_chain.py
│   ├── 08_artifact_checks/
│   │   ├── definition_reconciliation_and_threshold_sensitivity.py
│   │   ├── mechanical_artifact_test_fixed.py             <- supersedes the invalidated "control" analysis (METHODOLOGY_NOTES B3)
│   │   └── combinatoric_null_model_test.py
│   │
│   └── detail/                                   <- all raw JSON/CSV outputs, one subfolder per script group
│       ├── h2_panel_build_report.json
│       ├── h2_composition_panel.csv
│       ├── h2_composition_customer_level.csv
│       ├── h2_composition_regression_robustness_report_v2.json
│       ├── h2_localbiz_influence_diagnostics_report_fixed.json
│       ├── h2_two_customers_daily_detail.csv
│       ├── h2_localbiz_split_replication_mechanism_report.json
│       ├── h2_localbiz_mechanism_candidate_scan_report.json
│       ├── mechanism_scan_detail/
│       ├── h2_channel_id_structure_detail.csv
│       ├── h3_subgroup_dependence_report.json                        <- feeds Figure 12
│       ├── h3_subgroup_dependence_detail/
│       ├── h3_type_matched_fairness_correction_report.json           <- feeds Figure 12
│       ├── h3_type_matched_fairness_detail/
│       ├── localbiz_structural_heterogeneity_causal_chain_report.json <- feeds Figure 13
│       ├── localbiz_causal_chain_detail/
│       ├── definition_reconciliation_report.json
│       ├── definition_reconciliation_detail/
│       ├── mechanical_artifact_fixed_detail/
│       └── combinatoric_null_model_detail/                           <- feeds Figure 15
│           └── part1_bin_summary.csv
│
├── research_wide_audit/                          <- NEW, cross-cutting, applies to BOTH Level 1 & Level 2
│   ├── README.md                                 <- explains why this sits outside supplementary_localbiz_exploratory/
│   ├── research_wide_methodological_audit.py     <- §7's pooled 25-test multiplicity audit; also runs sub-audits
│   ├── h1c_core_influence_root_cause_and_regrade.py  <- §5.2's confirmatory core-model influence check
│   └── detail/
│       ├── research_wide_methodological_audit_report.json
│       ├── research_wide_audit_detail/
│       │   ├── part1_all_reported_tests.csv                          <- feeds Figure 14
│       │   ├── part2_cluster_se_validity.csv
│       │   ├── part3_h1c_core_influence.csv
│       │   ├── part4_unexplored_moderators.csv
│       │   └── part7_merge_point_coverage_bias.csv
│       ├── h1c_core_influence_root_cause_report.json
│       └── h1c_root_cause_detail/
│           ├── part1_influential_customer_profile.csv
│           └── part2_unmatched_customer_list.csv
│
├── figures/                                      <- one script per figure; Figures 12–15 are NEW
│   ├── make_figure1_variance_decomposition.py
│   ├── make_figure2_fairness_forest_plot.py
│   ├── make_figure3_specification_curve_placebo.py
│   ├── make_figure4_churn_benchmark.py
│   ├── make_figure7_mediation_forest.py
│   ├── make_figure8_boundary_condition_forest.py
│   ├── make_figure11_identification_screening.py
│   ├── make_figure12_h3_leave_one_type_out.py     <- NEW
│   ├── make_figure13_serving_structure.py         <- NEW
│   ├── make_figure14_multiplicity_audit.py        <- NEW
│   ├── make_figure15_combinatoric_null_model.py   <- NEW
│   └── Figure*.png
│
├── appendix/
│   ├── churn_prediction_rq4.md
│   ├── exploratory_industry_classification.md
│   └── hypothesis_id_legacy_mapping.md
│
├── docs/
│   ├── METHODOLOGY_NOTES.md
│   ├── RESULTS_SUMMARY.md
│   └── DESIGN_ARTIFACT.md
│
├── run_pipeline_v4.sh
├── run_supplementary_robustness.sh
├── run_supplementary_identification.sh
└── run_research_wide_audit.sh                    <- NEW: runs research_wide_audit/*.py end-to-end
```

---

## 15. How to Reproduce

1. Request a schema-compatible data extract (`data/README.md`).
2. Run the Level 1 pipeline (`run_pipeline_v4.sh`) — this reproduces §5 in full and nothing
   else; it does not depend on, or trigger, any Level 2 script.
3. Run the Level 2 exploratory pipeline (`supplementary_localbiz_exploratory/run_all.sh`)
   only if the goal is to reproduce §6; treat its output as exploratory regardless of
   significance level, per §6's evidence tags.
4. Run `research_wide_audit/research_wide_methodological_audit.py` (or
   `run_research_wide_audit.sh`) to regenerate §7's pooled multiplicity table and §5.2's
   core-model influence check.
5. Regenerate Figures 1–4, 7, 8, 11 with the existing `figures/make_figure*.py` scripts.
6. Regenerate the new Figures 12–15 with `figures/make_figure12..15*.py` — each reads a
   results JSON/CSV from `supplementary_localbiz_exploratory/detail/` or
   `research_wide_audit/detail/` and writes a PNG to `figures/`. These four scripts render
   Korean-language labels and require a Hangul-capable font on the machine generating them
   (e.g., `apt-get install fonts-nanum`, then `matplotlib.rc("font", family="NanumGothic")`
   and `matplotlib.rcParams["axes.unicode_minus"] = False`, as done at the top of each
   script) — without this, Korean labels render as empty boxes.

---

*Theoretical framing (§3), the SSI construct, the Level 1/Level 2 evidentiary split, and the
research-wide multiplicity audit (§7) are repository-level additions intended to make every
empirical claim legible as either a pre-specified test or a disclosed post-hoc exploration.
They do not alter any underlying reported statistic — they change only how each statistic is
labeled and weighted.*
