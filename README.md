# Structural Signal Irrelevance on an Algorithmically-Mediated Ad Platform

**A confirmatory test of whether advertiser size retains a residual, direct association
with algorithmic outcomes once total spend is held constant (H1, H2), followed by a
disclosed set of post-hoc exploratory research questions into why that relationship is
not uniformly expressed across advertising contexts (RQ2a–RQ2c).**

> **Repository status.** This is a research repository, not a publication. It documents a
> working analysis pipeline and an evidentiary structure that separates pre-specified
> confirmatory hypotheses from post-hoc exploratory research questions. Where an earlier
> pass in the analysis — or an earlier pass in how it was *named* — was later refined or
> corrected, both versions are kept on record; this is intended as a feature of
> methodological transparency rather than a list of errors. Nothing here should be cited
> as a peer-reviewed result.

> **How to read this repository.** Every claim below carries an explicit evidence tag:
> **[CONFIRMATORY]**, **[POST-HOC / EXPLORATORY]**, or **[FUTURE WORK]**. A reader who only
> wants the pre-registered-style result should read §5 (H1, H2) and stop. A reader
> interested in *why* H2's heterogeneity was not perfectly uniform should continue to §6,
> understanding that everything there was formulated after H1/H2 were run and is reported
> at "consistent with, but does not establish" strength.

> **A note on naming.** Earlier drafts of this repository numbered the post-hoc
> investigation into H2's heterogeneity as a single "H3." That choice is retracted here —
> see [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md), entry B7. Calling a
> post-hoc investigation a "hypothesis," however clearly tagged, risks implying it was set
> out in advance. This version instead uses three explicitly-named **research questions**
> — RQ2a (where), RQ2b (why), RQ2c (does H1's conclusion depend on it) — reserving the word
> "hypothesis" for H1 and H2, the two claims that were genuinely pre-specified. No
> underlying statistic changed; only the name and section boundaries of that investigation
> changed.

> **A note on figure labels.** Figures 1 and 4 carry embedded titles referencing "RQ1" and
> "RQ3." Those labels are internal stage-numbering from the underlying `Ad_Advance` v4
> data pipeline (RQ1 = multilevel variance decomposition, RQ2 = the advertiser-size
> fairness battery reported here as H1/H2, RQ3 = the unrelated churn-prediction appendix)
> and predate, and are unrelated to, this README's H1/H2/RQ2a–c hypothesis-and-
> research-question structure. Where this README refers to Figures 1 and 4, it describes
> them by function (a preliminary structural check; an unrelated appendix), never by their
> embedded "RQ" label, to avoid the two numbering schemes being read as the same thing.

> **A note on figures in this version.** Only the figures that carry the main argument
> (§5–§7) are embedded inline. The remaining supplementary and out-of-scope figures are
> moved to **[Appendix A](#appendix-a--supplementary-figures)**, each with a one-line
> pointer back to the section it supports. Figures belonging to the descoped longitudinal
> companion study (Study 2) are **not part of this repository's evidence base** and are
> only mentioned, not shown — see [Appendix B](#appendix-b--out-of-scope-figures-study-2).

---

## Table of contents

1. [At a Glance](#1-at-a-glance)
2. [How the Research Question Evolved](#2-how-the-research-question-evolved)
3. [Theoretical Framework](#3-theoretical-framework)
4. [Data & Setting](#4-data--setting)
5. [Confirmatory Hypotheses — H1 and H2](#5-confirmatory-hypotheses--h1-and-h2)
6. [Post-hoc Exploratory Research Questions — RQ2a, RQ2b, RQ2c](#6-post-hoc-exploratory-research-questions--rq2a-rq2b-rq2c)
7. [Research-wide Multiplicity Audit](#7-research-wide-multiplicity-audit)
8. [Methodological Positioning](#8-methodological-positioning)
9. [Synthesis](#9-synthesis)
10. [Boundary Conditions & Generalizability](#10-boundary-conditions--generalizability)
11. [Limitations](#11-limitations)
12. [Transparency Log](#12-transparency-log)
13. [Figure Gallery — What's Where](#13-figure-gallery--whats-where)
14. [Repository Structure](#14-repository-structure)
15. [How to Reproduce](#15-how-to-reproduce)
16. [Appendix A — Supplementary Figures](#appendix-a--supplementary-figures)
17. [Appendix B — Out-of-Scope Figures (Study 2)](#appendix-b--out-of-scope-figures-study-2)

---

## 1. At a Glance

| | Confirmatory (H1, H2) | Post-hoc exploratory (RQ2a–RQ2c) |
|---|---|---|
| **Question** | Does advertiser size directly associate with algorithmic outcomes, net of spend (H1)? Does that association vary by campaign type (H2)? | Where does the heterogeneity concentrate (RQ2a)? Why might it arise (RQ2b)? Does H1's conclusion depend on it (RQ2c)? |
| **Status** | Pre-specified, run once, not revised after seeing results | Formulated after H2 was run and its heterogeneity observed |
| **Sample** | 321 advertisers, ~19.3M rows; core test n=263 customers, 4,407 CPC obs. | Sub-clusters of the same sample, G≈13–72 per campaign type |
| **Central result** | H1c null (β=−0.253, p=.062); 8/8 robustness methods agree. H2 joint interaction significant (p=.023) with no individual stratum significant. | Local-business campaigns show structurally distinct serving characteristics, plausibly associated with the modest variability seen in the H1c estimate |
| **Evidence grade** | **Confirmatory** | **Exploratory — consistent with, but does not establish, a causal mechanism** |

**One-line summary:** the pre-specified test of whether advertiser size buys a direct
algorithmic advantage returns a clean, 8-way-robust **null** (H1) [CONFIRMATORY]. A
pre-specified test of whether that null holds uniformly across campaign types finds it
does not (H2) [CONFIRMATORY]. Three post-hoc research questions then ask where (RQ2a), why
(RQ2b), and how much this matters for H1's headline conclusion (RQ2c); together they
surface a plausible, but not established, explanation — local-business advertising appears
to run through a structurally different, non-auction serving pathway [POST-HOC /
EXPLORATORY]. Neither tier substitutes for the other.

---

## 2. How the Research Question Evolved

The research question was refined in two stages, both disclosed here so a reader can
weigh each part of the evidence appropriately.

**Stage 1 (original, pre-specified).**
> *Does advertiser size confer a direct algorithmic performance advantage on a paid-search
> platform, independent of spend — and is that association uniform across campaign
> types?*

This is the question H1 and H2 (§5) answer. The hypothesis battery (H1a/H1b/H1c/H2), the
sample, the outcome variables, and the robustness plan were fixed before the central
regression was run.

**Stage 2 (post-hoc, formulated after seeing H2's results).**
> *Under what platform-serving conditions might advertiser size translate into a
> performance advantage?*

This question was formulated after H2 returned a significant joint interaction test with
no individually significant stratum, and after inspecting `campaign_type` heterogeneity
suggested that local-business campaigns behave structurally differently from the rest of
the sample. It is disclosed as a two-stage process, and split into three named research
questions (RQ2a, RQ2b, RQ2c — §6), so that Stage-2 findings are weighted as what they are —
outputs of the same investigation that produced Stage 1, not an independent confirmation
of it, and not a third pre-specified hypothesis.

---

## 3. Theoretical Framework

### 3.1 Two competing accounts (H1's object of test)

- **Statistical discrimination / structural entrenchment** (Phelps 1972; Arrow 1973;
  Spence 1973): a decision-maker facing incomplete information about counterparty quality
  falls back on cheap, observable, structural proxies — here, advertiser size — even when
  a more direct behavioral signal (spend) is available. Predicts a **significant residual
  association** of size with outcomes, net of spend.
- **Algorithmic behavioral meritocracy** (Dwork et al. 2012, individual fairness): a
  well-specified, real-time auction system should condition allocation on current
  behavior, not accumulated structural status. Predicts **no residual association**.

### 3.2 Structural Signal Irrelevance (SSI)

> **Definition.** In an algorithmically-mediated market, let S be a structural attribute
> (size), B a legitimate behavioral signal (spend), Y an algorithmic outcome. The system
> exhibits **structural signal irrelevance with respect to S** when Y ⊥ S | (B, X) holds —
> assessed via decomposition of S's association with Y into a path mediated by B and a
> direct residual path net of B.

A single confirmatory null on H1c is evidence *toward* SSI; a robust SSI claim rests on
convergence across many independent robustness methods (achieved for H1, §5) and,
ideally, replication across contexts (attempted, at exploratory strength, in §6).

### 3.3 Boundary conditions on SSI (P1–P5)

- **P1 (real-time conditioning).** SSI is more likely where allocation is per-transaction
  on current behavioral signals without human-review buffering.
- **P2 (auction/market liquidity).** SSI is more likely in categories with enough
  transaction volume that even a small unit accumulates a usable behavioral signal quickly.
- **P3 (discretionary review re-entry).** Sub-processes with human discretionary review
  are SSI-violation *candidates* even within an otherwise SSI-consistent system.
- **P4 (measurability).** SSI can only be evaluated where the behavioral signal and
  outcome are measured with completeness that does not itself correlate with S. Where it
  does not (as with Conversion/ROAS, excluded in §4), SSI is **not testable**, not
  violated.
- **P5 (mechanism applicability) — new, motivated by RQ2b's findings.** The SSI audit
  design presupposes that the outcome is generated by an auction/bidding serving
  mechanism. Where this premise does not hold (in this sample: local-business campaigns,
  §6.3, [Figure 13](#figure-13)), the SSI test may fall **outside its own scope of
  applicability** rather than being violated. **[POST-HOC / EXPLORATORY — a candidate
  boundary condition, not an established one; see `FUTURE_RESEARCH_STUDY3.md` for a
  preregistered confirmatory test.]**

---

## 4. Data & Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata incl. `campaign_type` | 1,504 | 263/321 |
| Ad group dimension (2026-07-22 snapshot) | Bid price, registration timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status`, bid price | 1,503,289 | 256/321 |

**Construct-validity exclusion.** Conversion/ROAS variables are excluded from all outcome
sets by design (P4 above): Naver's conversion-tracking backfill lag is plausibly
correlated with advertiser size itself, which would risk manufacturing the very
direct-path pattern H1c is designed to detect as a measurement artifact rather than a
genuine finding.

---

## 5. Confirmatory Hypotheses — H1 and H2

**Status: [CONFIRMATORY].** Every analysis in this section — sample, variables, model,
robustness plan — was specified before the central regression was estimated, and none of
it was revised after seeing results.

### 5.1 Preliminary check: multilevel structure of the data

Before testing H1c, a variance-decomposition step (Figure 1) checks that most variance in
spend and CTR sits at the customer level rather than being an artifact of ad-group or
campaign clustering, which motivates the customer-level clustering used throughout. (See
the figure-label note above: this figure's embedded "RQ1" tag is a pipeline stage number,
not this README's H1.)

<a id="figure-1"></a>
![Figure 1 — Multilevel variance decomposition](figures/Figure1_variance_decomposition.png)
*Figure 1 [CONFIRMATORY, preliminary] — variance decomposition of spend and CTR across ad
group, campaign, customer, and residual levels; agreement between the unconditional and
month-FE-conditional ICC indicates the structure is not driven by seasonality.*

### 5.2 H1 — Does advertiser size confer a direct advantage, net of spend?

Controlling for log spend in a cluster-robust regression (n=263 customers, 4,407 CPC
observations), all six outcome × sample combinations return non-significant direct-path
coefficients for size (cluster-robust p > .07).

| Path | CPC-based (secondary) | bid_amount-based (primary, cost-independent) |
|---|---|---|
| H1a: size → spend | +0.537 (p<.001) | +0.537 (p<.001) |
| H1b: spend → outcome \| size | +1.277 (p<.001) | +0.150 (p=.032) |
| **H1c: size → outcome \| spend** | −0.253 (p=.062) | +0.037 (p=.634) |
| Indirect (a×b), bootstrap 95% CI | [0.121, 0.399] | [0.008, 0.159] |

<a id="figure-2"></a>
![Figure 2 — Advertiser-size effect, controlling for spend](figures/Figure2_fairness_forest_plot.png)
*Figure 2 [CONFIRMATORY] — the H1c point estimate and 95% CI sit comfortably inside the
pre-registered minimum-detectable-effect band for all three outcomes, both on the full
sample and after excluding spike accounts.*

**Verdict:** H1c not rejected (null supported). H1a/H1b confirmed. Statistically
consistent with full mediation, backed by an 8-way robustness battery (§5.4).

### 5.3 H1c core-model influence diagnostic [CONFIRMATORY robustness check]

An influence diagnostic was applied to the primary H1c model itself, using rules fixed
before any coefficient was inspected: DFBETA-flagged influential customers were 15/228
(threshold 2/√228 = 0.1325). These 15 are **not** disproportionately local-business
advertisers (t-test on `share_6`, p=.53). Three pre-specified exclusion rules (thin
observation customers; low performance-match-rate customers; both combined) were applied
before inspecting whether they would change the significance verdict: **0/4
configurations reached significance**, a 100% consistency rate.

**Verdict: confirmatory grade maintained.**

### 5.4 Robustness battery for H1 (summary)

| # | Method | Result | Detail |
|---|---|---|---|
| 1 | Specification curve (48 choices) | 0/48 reach significance | [Figure 3](#figure-3) |
| 2 | Placebo test (device-type share) | Regression-level test correctly null on placebo | [Figure 3](#figure-3) |
| 3 | Customer × month FE panel | Consistent with central estimate | — |
| 4 | 2SLS (lagged spend instrument) | Incomplete (code exception); excluded from conclusions | — |
| 5 | Temporal split (era1 vs era2) | Consistent | — |
| 6 | Benjamini–Hochberg FDR | Null survives correction | [§7](#7-research-wide-multiplicity-audit) |
| 7 | Mechanical-artifact isolation (CPC vs bid_amount) | Confirmed real, not purely mechanical | [Figure 7](#figure-7) |
| 8 | Cost-independent outcome replication | Same qualitative pattern | [Figure 7](#figure-7) |

<a id="figure-3"></a>
![Figure 3 — Multiverse specification curve and placebo test](figures/Figure3_specification_curve_placebo.png)
*Figure 3 [CONFIRMATORY] — Panel A: 0/48 specification-curve estimates reach significance
across three outcomes. Panel B: the placebo comparison is informative only in the
spend-controlled (H2b) regression, where real and placebo outcomes are equally null; the
distributional (KW) test alone is not a clean placebo since size tiers correlate with many
account traits.*

<a id="figure-7"></a>
![Figure 7 — Spend-mediation b-path](figures/Figure7_mediation_forest.png)
*Figure 7 [CONFIRMATORY] — the spend→outcome (b-path) coefficient is directionally
consistent across the CPC-based and cost-independent (bid_amount-based) outcome
definitions, supporting H1b independent of the mechanical CPC=cost/click relationship.*

**On identification (RDD / policy-change screening).** As a supplementary check on
whether a stronger causal design was reachable beyond the incomplete 2SLS attempt, RDD
and policy-change event-study designs were screened. Neither survived customer-level
re-analysis as a usable identification strategy (0/5 RDD candidates; all 5 auto-detected
event dates non-significant). Both are reported as failed robustness checks whose null
results are directionally consistent with H1c, not as adopted identification designs. The
full screening detail and figure are in **[Appendix A, Figure 11](#figure-11)**.

### 5.5 H2 — Does the H1c relationship vary by campaign type?

Stratifying the H1c model by `campaign_type` (n=184/27/17 for website/local-business/
shopping), a joint Wald test on the size × product-type interaction gives **p=.023**. No
individual stratum is significant alone. This test — its variables, its stratification
scheme, and its significance threshold — was specified before the central H1c regression
was run.

<a id="figure-8"></a>
![Figure 8 — Campaign product-type heterogeneity](figures/Figure8_boundary_condition_forest.png)
*Figure 8 [CONFIRMATORY] — the c' (size, net of spend) estimate by campaign type, with a
significant joint interaction test (p=.023) but no individually significant stratum. This
is the pre-specified result that motivates the post-hoc research questions in §6.*

**Verdict:** H2 is supported — H1c's null is not perfectly homogeneous across ad-product
categories, though no individual stratum is significant alone. **H2 does not itself say
where or why**; those are post-hoc questions, addressed in §6.

**H1/H2 conclusion:** *A uniform, direct advertiser-size advantage on this platform's
algorithmic outcomes is not confirmed, and that non-uniformity itself varies detectably by
campaign type.* This is the confirmatory backbone of the paper.

---

## 6. Post-hoc Exploratory Research Questions — RQ2a, RQ2b, RQ2c

**Status: [POST-HOC / EXPLORATORY throughout this entire section].** None of what follows
was preregistered. Each research question was formulated after H2 (§5.5) returned its
result and after inspecting the data. Every subsection ends with an explicit statement of
what the evidence does and does not support. These are research questions, not
hypotheses — see the naming note at the top of this document.

> **Small-cluster note (applies to all of §6).** Several analyses below rely on
> campaign-type sub-clusters with G≈13 (power content) to G≈72 (local business), below the
> conventional G≥42 rule-of-thumb for cluster-robust standard error validity. Where checked
> directly, standard cluster-robust p-values diverge from wild-cluster-bootstrap p-values
> by up to 0.16–0.17 in these subgroups. p-values in this section should be read as
> approximate.

### 6.1 RQ2a — Where does the heterogeneity concentrate?

**Question:** H2 established that the size–outcome relationship is not homogeneous across
campaign types. Which type(s) drive that heterogeneity?

A continuous-share re-specification (covariates as continuous campaign-type shares rather
than discrete strata) found the same qualitative pattern as H2: a joint interaction test
significant overall (p=.0002), but with only local business surviving a three-round
robustness screen (permutation test, pairs bootstrap, wild-cluster bootstrap) at 3/5
methods.

**Important:** this was **not** the pre-specified H2 hypothesis, which had been motivated
by a shopping-campaign product-feed-validation-pipeline theory that did not pan out
(shopping's own term: baseline p=.307, 0/5 methods significant). Local business's
emergence as the concentration point of H2's heterogeneity is itself a post-hoc
observation, not a replication of a prior prediction.

**Verdict [POST-HOC/EXPLORATORY]:** local business is the campaign type where H2's
heterogeneity concentrates most robustly, though this was discovered rather than
predicted.

### 6.2 RQ2b — Why might local business behave differently?

**Question:** What platform-level mechanism could produce local business's distinct
pattern?

#### 6.2.1 Serving-mechanism heterogeneity across campaign types

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
structural facts, confirmed by tracing the join chain (campaign_dim → adgroup_dim →
keyword_dim) rather than assumed. This is the key visual evidence behind proposition P5
(§3.3). Note that ratios above 1 for other campaign types (website 2.77, power content
4.33) should not be read as "advertisers paid 2.77–4.33× their bid" — `bid_amount` and
actual CPC are captured at different aggregation levels, so only the qualitative
below-1-vs-above-1 classification, not the magnitude of ratios above 1, is treated as
informative here.*

Local-business ad groups show zero matches to the keyword-dimension table. This is
consistent with local-business ads being served through a location/business-channel
mechanism rather than keyword auction — the `business_channel_id_mobile/pc` fields present
in `adgroup_dim` are circumstantially consistent with this, though it has not been
independently verified against Naver's official product documentation.

#### 6.2.2 Statistical signatures consistent with a distinct CPC-generation process

Three diagnostics, run on the auction-classified vs. non-auction-classified campaign
types: variance heterogeneity (Brown-Forsythe p<.0001), relationship (b-path)
heterogeneity (spend_z × is_localbiz = +1.125, p=.001), and a counterfactual-magnitude
comparison (standardized gap of −0.49 SD, p<.0001). A fourth check — leverage
(hat-value) — did **not** show a significant difference. This is reported as **partial,
mixed support** for a mechanism-level explanation, not an established causal chain.

#### 6.2.3 Alternative explanations audited

Before accepting any mechanism-level story, mundane data artifacts were tested and
several were ruled out or reframed:

- A naive "control for ad-group count" analysis was found to be invalid — `size_z` and
  `n_ad_groups_total` are the same underlying variable. A combinatorial null model was
  built instead: if missingness were purely a mechanical function of "more ad groups →
  higher chance one is unmatched," a simple binomial model should fit the observed
  pattern. It does not (over-dispersion ratio 73×; χ²=16,583, df=6, p<.0001), indicating
  some account-level clustering beyond pure combinatorics. See
  **[Appendix A, Figure 15](#figure-15)** for the observed-vs-predicted plot.
- Influence diagnostics (corrected for a DFBETA scale-mismatch, §12) found no sign
  reversal across leave-k-out removal; removing the most influential accounts strengthened
  rather than weakened the pattern.
- A keyword-review/approval-pipeline mechanism (parallel to the shopping-campaign
  hypothesis) does not apply to local business — local-business ad groups have zero
  keyword-dimension matches, so this specific candidate is a structural dead end rather
  than a tested-and-failed hypothesis.

**Verdict [POST-HOC/EXPLORATORY, mixed]:** advertising-type heterogeneity in serving
structure is a real, observable feature of this platform, most pronounced for
local-business campaigns; several statistical signatures are consistent with this
structural difference mattering for how CPC is generated; and this is not fully explained
away by sample-size mechanics alone. **This does not establish** that platform serving
structure *causes* H2's heterogeneity, that this pattern would replicate in an independent
sample, or that any number in this subsection carries H1/H2's confirmatory weight.

**Theoretical proposition (exploratory, not established):** structural advantage may be
*conditional* on platform-serving conditions rather than *automatic* — a reframing of the
paper's contribution from "large advertisers are/are not favored" to "when structural
scale converts into performance may depend on how the platform serves the ad." This is the
basis for proposition P5 (§3.3).

### 6.3 RQ2c — Does H1's conclusion depend on local-business inclusion?

**Question:** Beyond describing where and why heterogeneity exists (RQ2a, RQ2b), does
H1c's headline null actually *depend* on local-business customers being in the sample,
more than would be expected from sample-size reduction alone? This is a sensitivity
check on H1's conclusion, not a mechanism claim, and is treated as its own research
question because it answers a different kind of question than RQ2a/RQ2b.

Excluding all 72 local-business-spending customers shifts H1c from β=−0.253 (p=.062,
n=228) to β=−0.499 (p=.006, n=156). Placebo tests (random-exclusion and size-matched)
found this magnitude of shift in under 1% of draws, suggesting the shift is not purely a
sample-size artifact. An initial leave-one-type-out comparison ranked local-business
exclusion 2nd by raw coefficient shift, behind website exclusion — but website exclusion
left only 26 customers, an unstable remaining sample. A corrected comparison that matches
exclusion size across types found local-business exclusion had by far the lowest empirical
p-value among the three campaign types with stable remaining samples. Both the initial and
corrected comparisons are shown together, per the repository's disclosure policy, in
**[Appendix A, Figure 12](#figure-12)**.

**Verdict [POST-HOC/EXPLORATORY, partially supported, on corrected analysis]:**
*consistent with a local-business-specific dependency, not conclusively established.* The
initial, uncorrected comparison did not support this conclusion; only the corrected
comparison does. Both are disclosed together (§12, entry B6) precisely because the
uncorrected pass initially cut against the emerging narrative.

### 6.4 What §6, taken together, does and does not support

> **Does support (at exploratory strength):** H2's heterogeneity concentrates most
> robustly in local-business campaigns (RQ2a); advertising-type differences in serving
> structure are a real, observable feature of this platform and several statistical
> signatures are consistent with this mattering for how CPC is generated (RQ2b); and
> H1c's null is not fully insensitive to local-business inclusion, beyond what sample-size
> mechanics alone would predict (RQ2c).
>
> **Does not support:** a claim that platform serving structure has been shown to *cause*
> H2's instability; a claim that any of RQ2a–RQ2c would replicate in an independent
> sample; or a claim that any single number in §6 should be read at the same confidence
> level as §5's H1/H2 results.

---

## 7. Research-wide Multiplicity Audit

Every hypothesis- or research-question family in this repository corrects for multiple
comparisons internally. This section additionally pools every p-value reported anywhere in
this repository as an official statistic (n=25) into a single test family.

<a id="figure-14"></a>
![Figure 14 — Research-wide multiplicity audit across all 25 reported p-values](figures/Figure14_multiplicity_audit.png)
*Figure 14 [CROSS-CUTTING] — each point is one officially-reported p-value, colored by
family, sorted by significance. The dashed line is the pooled Bonferroni threshold (0/25
tests clear it); the dotted line is the rank-dependent BH-FDR threshold (3/25 clear it,
all from the RQ2c subgroup-dependence analysis, §6.3). This figure is kept in the main body
because it is the single evidence-calibration device the rest of this README leans on —
see the reading note below. (The legend's "H3" label reflects the source script's original
variable naming and refers to what this README calls RQ2c.)*

| Correction | Tests surviving |
|---|---|
| Bonferroni (α=.05/25=.002) | **0 / 25** |
| Benjamini–Hochberg FDR | **3 / 25** (all from the exploratory RQ2c subgroup-dependence analysis, §6.3) |

**Reading this table correctly:** this is the single most useful piece of
evidence-calibration information in this repository. Under a fully pooled, maximally
conservative view of every number this project has produced, only the RQ2c result
survives, and only under the more permissive FDR correction. H1's null does not need to
"survive" this correction because it was never claimed significant — the null is the
finding. This table exists so that no result from §6 is read as carrying the same
statistical weight as §5's central, well-powered confirmatory results.

---

## 8. Methodological Positioning

This repository is designed as a **mediation audit** (Sandvig et al. 2014; Metaxa et al.
2021; Raji et al. 2020) — appropriate when platform access for a sock-puppet or
field-experimental audit is unavailable. It supports a sharper procedural-fairness claim
than a raw correlation audit but does not support causal identification; 2SLS, RDD, and
policy-change screenings found no usable identification design and are reported as null
supplementary robustness (§5.4, [Appendix A, Figure 11](#figure-11)), not as adopted
strategies.

Within this design, the **confirmatory (H1, H2) / post-hoc exploratory (RQ2a–RQ2c) split**
is the operative discipline: §5 answers the mediation-audit's pre-specified questions; §6
investigates *where* and *why* H2's answer was not perfectly clean, and *whether* H1's
headline conclusion depends on it, using methods chosen after seeing the data, and is
reported at correspondingly lower evidentiary strength throughout.

---

## 9. Synthesis

| | H1 / H2 (Confirmatory) | RQ2a–RQ2c (Post-hoc exploratory) |
|---|---|---|
| Evidence grade | **Confirmatory** | **Exploratory** |
| Robustness convergence | 8/8 independent methods null for H1; H2 joint test significant, no stratum significant alone | RQ2b: 3/4 mechanism-chain links detected; mixed. RQ2c: 3/3 sensitivity criteria met on corrected analysis only |
| Survives research-wide multiplicity audit (§7) | Not applicable (H1's null was never claimed significant) | Partially (FDR only, not Bonferroni; all 3 FDR survivors are from RQ2c) |
| Correct citation form | "advertiser size shows no confirmed direct algorithmic advantage on this platform, and that non-relationship is not perfectly uniform across campaign types" | "patterns are consistent with, but do not establish, a local-business-specific, serving-structure-linked explanation for H2's heterogeneity" |

**Combined message:** the pre-specified questions — does size buy a direct algorithmic
advantage (H1), and is that answer uniform across campaign types (H2) — return a
confirmatory null with confirmed heterogeneity. Three post-hoc research questions then ask
where that heterogeneity concentrates (RQ2a), why it might arise (RQ2b), and whether it
matters for H1's headline conclusion (RQ2c). Together they surface a plausible,
partially-supported, unconfirmed explanation involving platform serving structure. A
one-page visual summary tying both studies together (Study 1's cross-sectional result
alongside the descoped Study 2 longitudinal companion) exists as
**[Figure 10](#appendix-b--out-of-scope-figures-study-2)** — see Appendix B for why it is
referenced but not embedded here.

---

## 10. Boundary Conditions & Generalizability

See §3.3 for P1–P5. P1–P4 were derived from the platform-governance literature prior to
data collection; **P5 is post-hoc**, formulated from RQ2b's findings, and is marked as a
candidate proposition pending independent test (see `FUTURE_RESEARCH_STUDY3.md`).

**Procedural vs. distributive fairness.** This repository's confirmatory finding concerns
procedural fairness only. It is silent on distributive fairness (whether behavior-only
allocation is itself equitable across advertisers with unequal starting resources).

---

## 11. Limitations

| # | Limitation | Tier |
|---|---|---|
| 1 | Single agency, single platform — generalizability is architecturally scoped, not empirically tested across platforms | Both |
| 2 | Mediation audit, not a causal-inference study, by design; RDD/2SLS/policy-change screening found no usable identification design | H1/H2 |
| 3 | Sub-clusters used in RQ2a–RQ2c are unevenly sized (G≈13–72); standard cluster-robust SEs diverge from wild-bootstrap SEs by up to 0.17 in these subgroups | RQ2a–RQ2c |
| 4 | Conversion/ROAS excluded entirely (P4 measurability boundary) | H1/H2 |
| 5 | RQ2c's leave-one-type-out ranking was corrected for unequal exclusion-sample stability; both passes are disclosed (§6.3, §12) | RQ2c |
| 6 | RQ2b's mechanism sub-chain is only partially confirmed (3/4 links); leverage heterogeneity specifically was not detected | RQ2b |
| 7 | An earlier "control for ad-group count" analysis was invalidated once `size_z` and `n_ad_groups_total` were found to be the same variable; the replacement combinatorial-null-model analysis is itself only suggestive (§6.2.3) | RQ2b |
| 8 | 22/25 officially-reported p-values do not survive the more permissive FDR correction when pooled (§7) | Both |
| 9 | Procedural fairness only; distributive fairness is not addressed | Both |
| 10 | Single-sample, single-time-axis result; a separately-scoped longitudinal companion study exists (`FUTURE_RESEARCH_STUDY2.md`) but is not part of this evidence base | H1/H2 |
| 11 | The post-hoc investigation in §6 was originally numbered as a single "H3" hypothesis; renaming it to RQ2a–RQ2c (§12, entry B7) is a naming correction, not a change in the underlying evidence, but readers of earlier drafts or of cited pipeline scripts may still encounter the old "H3" label | RQ2a–RQ2c |

---

## 12. Transparency Log

*Full narrative log in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md).*

| # | Item | Resolution |
|---|---|---|
| 1 | Original framing described RDD/policy-change screening as "failed identification attempts" | Reframed as supplementary robustness under mediation-audit positioning (§8); statistics unchanged |
| 2 | DFBETA influence-diagnostic scale mismatch: row-level DFBETA summed across ~190 daily observations per customer was compared against a customer-count-based threshold | Corrected to customer-level (1 customer = 1 row) regression DFBETA; the "0 customers exceed threshold" claim from the earlier pass was superseded |
| 3 | Leave-one-type-out ranking (§6.3) initially placed local-business exclusion 2nd, before the exclusion-size instability of the top-ranked alternative was identified | Both passes reported in §6.3, [Appendix A Figure 12](#figure-12), with the reason for the correction stated explicitly |
| 4 | `size_z` and `n_ad_groups_total` found to be mathematically the same variable | Earlier "mechanical artifact ruled out" conclusion based on a regression using both was retracted; replaced with a combinatorial null-model test (§6.2.3, [Appendix A Figure 15](#figure-15)) |
| 5 | An earlier internal draft described the local-business mechanism findings (§6.2.2) as a "confirmed causal chain" | Reframed as "3 of 4 tested links show a statistically detectable pattern," not a causal claim |
| 6 | 2SLS first-stage F-statistic returned `None` due to an uncaught exception | 2SLS excluded from all confirmatory conclusions |
| 7 | The post-hoc investigation into H2's heterogeneity was originally numbered "H3," alongside pre-specified H1/H2 | Renamed to three explicitly-named research questions, RQ2a/RQ2b/RQ2c, to prevent the numbering itself from implying pre-registration; see `docs/METHODOLOGY_NOTES.md` entry B7 |

---

## 13. Figure Gallery — What's Where

All figures live as standalone PNGs in [`figures/`](figures/) regardless of where they
render. This table is the map: **Body** figures are embedded inline above; **Appendix A**
figures are embedded in the appendix, one section down, with supplementary detail;
**Appendix B** figures are named but not shown, because they belong to a descoped,
out-of-scope study. Note: several figure titles/legends embed the pipeline's original
internal labels ("RQ1," "RQ3," "H3") from earlier stages of the `Ad_Advance` project; see
the naming notes at the top of this document — these are not the same numbering as this
README's H1/H2/RQ2a–c structure, and each caption below clarifies the mapping where it
matters.

| # | Title | Tier | Where it renders |
|---|---|---|---|
| 1 | Multilevel variance decomposition (embedded label: "RQ1," a pipeline stage number) | [CONFIRMATORY, preliminary] | **Body**, §5.1 |
| 2 | Advertiser-size effect, controlling for spend | [CONFIRMATORY] | **Body**, §5.2 |
| 3 | Multiverse specification curve + placebo | [CONFIRMATORY] | **Body**, §5.4 |
| 4 | Churn-prediction benchmarking (embedded label: "RQ3," an unrelated pipeline appendix) | [EXPLORATORY, non-confirmatory appendix] | **Appendix A** |
| 5, 6, 9, 10 | Cold-start funnel, prediction-horizon, TOST equivalence, integrated framework | Study 2 (longitudinal companion) | **Appendix B** (mention only, not embedded) |
| 7 | Spend-mediation b-path | [CONFIRMATORY] | **Body**, §5.4 |
| 8 | Product-type heterogeneity (H2) | [CONFIRMATORY] | **Body**, §5.5 |
| 11 | Alternative-identification screening (RDD + policy-change, null) | [CONFIRMATORY, supplementary] | **Appendix A** |
| 12 | Leave-one-type-out, uncorrected vs. corrected (embedded label: "H3," now RQ2c) | [POST-HOC] | **Appendix A** |
| 13 | Serving-structure heterogeneity by campaign type (RQ2b) | [POST-HOC] | **Body**, §6.2 |
| 14 | Research-wide multiplicity audit (25 p-values; legend embeds "H3," now RQ2c) | [CROSS-CUTTING] | **Body**, §7 |
| 15 | Combinatoric null model vs. observed missingness (RQ2b) | [POST-HOC] | **Appendix A** |

**Why this split.** Figures 1, 2, 3, 7, 8, and 13 carry the argument a reader needs to
follow §5–§6 without leaving the page; Figure 14 is kept in the body because it is the
calibration device the whole README depends on when weighing §5 against §6. Figures 4, 11,
12, and 15 are genuine parts of this repository's evidence base but are detail/robustness
material that a first read does not need — they are one click away in Appendix A, each
still carrying its own evidence tag. Figures 5, 6, 9, and 10 belong to a different sample,
a different study, and a study that was explicitly descoped from this repository's
evidence base (§11, limitation 10) — showing them inline here would visually imply they
support this paper's claims, which they do not; Appendix B explains this and links to
where they do belong.

---

## 14. Repository Structure

```
structural-signal-irrelevance/
├── README.md                          <- you are here
├── FUTURE_RESEARCH_STUDY2.md          <- descoped longitudinal study
├── FUTURE_RESEARCH_STUDY3.md          <- proposed preregistered confirmatory test of P5 / RQ2a-c findings
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
│   └── pipeline_v4/                              <- H1/H2 (confirmatory) pipeline
│       ├── step0_data_prep_v4.py
│       ├── step1_variance_decomposition_v4.py
│       ├── step2_advertiser_size_fairness_v4.py
│       ├── step3_churn_appendix_v4.py
│       └── step4_synthesis_v4.py
│
├── supplementary_robustness/                     <- H1 supplementary robustness
│   ├── supplementary_robustness_README.md
│   ├── 01_alternative_outcome_mediation.md / .py
│   ├── 02_boundary_conditions.md / .py
│   └── 03_equivalence_and_sensitivity_notes.md / .py
│
├── supplementary_identification/                 <- H1 RDD/policy-change screening
│   ├── SCREENING_SUMMARY.md
│   ├── step11_alt_identification_RDD_policy.py
│   ├── step11b_donut_hole_full_scan.py
│   └── step11c_customer_level_reanalysis.py
│
├── supplementary_localbiz_exploratory/           <- RQ2a-RQ2c (post-hoc, local-business) analysis
│   ├── README.md                                 <- [POST-HOC/EXPLORATORY] scope banner, links back to root §6
│   └── localbiz_core_analysis.py                 <- panel build + RQ2a continuous-share regression + RQ2b serving-structure comparison + RQ2c subgroup test, in one script
│                                                     (script variable names still use legacy "H2"/"H3" labels internally; see mapping note in the script header)
│
├── research_wide_audit/                          <- cross-cutting audit, applies to BOTH tiers
│   ├── README.md                                 <- explains why this sits outside supplementary_localbiz_exploratory/
│   └── research_wide_audit_core.py               <- §7's pooled 25-test multiplicity audit + §5.3's H1c core-model influence/leave-k-out check, in one script
│
├── figures/                                      <- one PNG per figure, referenced throughout this README
│   └── Figure*.png                               <- Figure1–Figure15; Figures 12–15 are sourced from the
│                                                     detail/ JSON files above rather than hand-maintained scripts
│
├── appendix/
│   ├── churn_prediction_rq4.md
│   ├── exploratory_industry_classification.md
│   └── hypothesis_id_legacy_mapping.md           <- maps legacy pipeline/script labels ("RQ1-RQ4," "H3") to this README's H1/H2/RQ2a-c naming
│
└── docs/
    ├── METHODOLOGY_NOTES.md
    ├── RESULTS_SUMMARY.md
    └── DESIGN_ARTIFACT.md
```

**Note on consolidation.** `supplementary_localbiz_exploratory/` and `research_wide_audit/`
were previously organized as a larger set of numbered sub-folders (panel build, regression
robustness, influence diagnostics, a two-customer case deep-dive, a mechanism-candidate
scan, a keyword-join diagnostic, a channel-ID structure check, an uncorrected and a
corrected sensitivity script, a causal-chain script, and several artifact-check scripts,
each with its own `detail/` output). None of those intermediate scripts changed a headline
number reported in this README; each was a diagnostic step in reaching the numbers now
reproduced directly by `localbiz_core_analysis.py` and `research_wide_audit_core.py`. That
fuller, step-by-step version of the process — including the dead ends, the corrected
DFBETA scale bug, and the keyword-join investigation — is preserved narratively in
`docs/METHODOLOGY_NOTES.md` for anyone who wants the full audit trail; it is not
reproduced here as a folder of scripts.

**Note on legacy labels inside scripts.** The underlying `.py` scripts still use their
original internal variable/function names (e.g., `h3_leave_one_out`,
`step11_alt_identification`), which predate the RQ2a/RQ2b/RQ2c renaming documented in §12,
entry B7. These names are cosmetic and do not affect any computed statistic;
`appendix/hypothesis_id_legacy_mapping.md` provides the full mapping for anyone tracing a
number in this README back to the script that produced it.

---

## 15. How to Reproduce

1. Request a schema-compatible data extract (`data/README.md`).
2. Run the H1/H2 pipeline (`run_pipeline_v4.sh`) — this reproduces §5 in full and nothing
   else; it does not depend on, or trigger, any §6 script.
3. Run `supplementary_localbiz_exploratory/localbiz_core_analysis.py` to reproduce §6
   (panel build, RQ2a continuous-share regression, RQ2b serving-structure comparison, and
   RQ2c subgroup-dependence test). Treat its output as exploratory regardless of
   significance level, per §6's evidence tags.
4. Run `research_wide_audit/research_wide_audit_core.py` (or `run_research_wide_audit.sh`)
   to regenerate §7's pooled multiplicity table and §5.3's core-model influence check.
5. Regenerate figures from the results JSON/CSV produced by the scripts above. Figures
   with Korean-language labels (12, 13) require a Hangul-capable font on the machine
   generating them (e.g., `apt-get install fonts-nanum`, then
   `matplotlib.rc("font", family="NanumGothic")` and
   `matplotlib.rcParams["axes.unicode_minus"] = False`).

---

## Appendix A — Supplementary Figures

These figures are part of this repository's evidence base — each is cited from the body
above — but are detail-level or robustness-level material rather than the core argument,
so they are collected here rather than inline.

<a id="figure-11"></a>
### Figure 11 — Alternative-identification screening (RDD + policy-change)
*Supports [§5.4](#54-robustness-battery-for-h1-summary) and [§8](#8-methodological-positioning).*

![Figure 11 — Alternative-identification screening](figures/Figure11_identification_screening.png)
*Figure 11 [CONFIRMATORY, supplementary] — RDD and policy-change event-study designs were
screened as a stronger alternative to 2SLS. Neither survived customer-level re-analysis as
a usable identification strategy (0/5 RDD candidates; all 5 auto-detected event dates
non-significant). Both are reported openly as failed robustness checks whose null results
are directionally consistent with H1c, not as adopted identification designs.*

<a id="figure-12"></a>
### Figure 12 — Leave-one-type-out: uncorrected vs. corrected ranking (RQ2c)
*Supports [§6.3](#63-rq2c--does-h1s-conclusion-depend-on-local-business-inclusion). The
figure's own legend still reads "H3" — see the naming note at the top of this document;
this is the same analysis, now called RQ2c.*

![Figure 12 — Leave-one-type-out: uncorrected vs. corrected ranking](figures/Figure12_h3_leave_one_type_out.png)
*Figure 12 [POST-HOC / EXPLORATORY] — Panel A: the initial, uncorrected ranking by raw
coefficient shift (website ranks 1st only because its remaining sample, n=26, is
unstable). Panel B: the corrected, exclusion-size-matched empirical-p ranking among the
three campaign types with stable remaining samples — local business is the clear outlier.
Both panels are shown together per the disclosure policy in `docs/METHODOLOGY_NOTES.md` —
the corrected ranking is never presented without the uncorrected one.*

<a id="figure-15"></a>
### Figure 15 — Combinatoric null model vs. observed missingness (RQ2b)
*Supports [§6.2.3](#623-alternative-explanations-audited).*

![Figure 15 — Observed vs. combinatorially-predicted missingness rate](figures/Figure15_combinatoric_null_model.png)
*Figure 15 [POST-HOC / EXPLORATORY] — the gap between observed and
independent-binomial-predicted missingness rates, especially at low-to-mid ad-group
counts, is the basis for the over-dispersion finding; the residual cause is
unidentified.*

<a id="figure-4"></a>
### Figure 4 — Churn-prediction benchmarking (embedded label: "RQ3," unrelated pipeline appendix)
*Not part of the H1/H2/RQ2a–c fairness questions tested in §5–§6; retained for completeness
of the broader Ad_Advance pipeline (`appendix/churn_prediction_rq4.md`).*

![Figure 4 — Churn-prediction benchmarking](figures/Figure4_churn_benchmark.png)
*Figure 4 [EXPLORATORY, non-confirmatory appendix] — model comparison (logistic
regression, random forest, gradient boosting) on a severely class-imbalanced churn label
(2.35% of 213 labeled accounts). This is an independent research direction from the SSI
fairness question and is included here only because it shares the same underlying
Ad_Advance data pipeline; it does not bear on H1a/H1b/H1c, H2, or RQ2a–c.*

---

## Appendix B — Out-of-Scope Figures (Study 2)

The figures below belong to a **descoped longitudinal companion study** — a separate
sample (n=29 customers, 204 ad groups), a separate time axis (account maturity vs. a new
ad group's early growth trajectory), and a separate research question (RQ1–RQ3 on
cold-start prediction, in Study 2's own internal numbering — unrelated to this document's
H1/H2/RQ2a–c) from this repository's evidence base. They are **not cited as evidence for
any claim in §1–§11 above** and are listed here only so a reader who encounters them
elsewhere (e.g., in `FUTURE_RESEARCH_STUDY2.md` or an old citation) can see why they are
absent from the main narrative, per the repository's disclosure policy (§11, limitation
10; `docs/METHODOLOGY_NOTES.md`).

| # | Title | Belongs to |
|---|---|---|
| 5 | Cold-start sample construction funnel & RQ1 confirmatory null (Study 2's own numbering) | `FUTURE_RESEARCH_STUDY2.md`, RQ1 |
| 6 | Cold-start early-signal prediction (RQ2) & intervention-timing simulation (RQ3) (Study 2's own numbering) | `FUTURE_RESEARCH_STUDY2.md`, RQ2/RQ3 |
| 9 | TOST equivalence tests for Study 2's two central null results | `FUTURE_RESEARCH_STUDY2.md`, §7.3 |
| 10 | Integrated framework — Study 1 (this repo) vs. Study 2 (descoped) side by side | `FUTURE_RESEARCH_STUDY2.md`, synthesis |

**Why Figure 10 is listed here even though it depicts this repository's own Study 1
result.** Figure 10 is a two-panel comparison figure: the left panel is this repository's
H1a/H1b/H1c result, and the right panel is Study 2's separate, descoped RQ1–RQ2 result on
an independent sample. Because the figure as a single artifact asserts a joint narrative
across both studies, and Study 2 is not part of this repository's evidence base, the
figure is not embedded here — showing only the left panel would misrepresent the figure,
and showing both panels would import Study 2's claims into this repository's narrative.
Readers interested in the full two-study comparison should consult
`FUTURE_RESEARCH_STUDY2.md` directly, where Study 2's own evidence tags and caveats
(including its TOST-inconclusive equivalence tests, Figure 9) are presented in full.

If a schema-compatible extract for Study 2 becomes available for replication, and RQ1–RQ3
are formally preregistered as their own confirmatory tests, that work is expected to live
in its own repository or a clearly separated section — not folded into this one — per the
same confirmatory/post-hoc discipline documented in §2 and §8 above.

---

*Theoretical framing (§3), the SSI construct, the confirmatory/post-hoc split, and the
research-wide multiplicity audit (§7) are repository-level additions intended to make
every empirical claim legible as either a pre-specified test or a disclosed post-hoc
exploration. They do not alter any underlying reported statistic — they change only how
each statistic is labeled and weighted. This revision additionally renames the post-hoc
investigation from a single "H3" to three named research questions (RQ2a, RQ2b, RQ2c;
§12, entry B7) and clarifies that Figures 1 and 4's embedded "RQ1"/"RQ3" labels are an
unrelated, older pipeline-stage numbering — without altering any figure's content,
underlying statistic, or evidence tag.*
