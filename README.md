# Structural Signal Irrelevance on an Algorithmically-Mediated Ad Platform

**A cross-sectional mediation-audit study of whether advertiser size retains any residual,
direct statistical association with algorithmic outcomes on a Korean paid-search platform, once
the legitimate behavioral channel it operates through (total spend) is held constant.**

> **Repository status.** This is a research repository, not a publication. Everything below
> documents a working analysis pipeline, its full diagnostic history, a theoretical framework
> that both names a new construct (**structural signal irrelevance**, §2.7) and connects it to
> the statistical-discrimination / algorithmic-fairness / platform-governance / algorithm-audit
> literatures, and figures generated from the pipeline — organized for internal review,
> reproducibility, and eventual manuscript preparation. Nothing here should be cited as a
> peer-reviewed result.

> **Methodological positioning (read this first).** This study is designed and reported as a
> **mediation audit** (§5), not as a causal-inference study. Every "path," "mediation," and
> "effect" statement describes conditional statistical (in)dependence in observational panel
> data. A supplementary attempt to upgrade the identification tier (2SLS; RDD/policy-change
> event studies, §4.5.9) was screened and did not reach a usable causal design — this is
> reported as an expected boundary of the mediation-audit method, not as a failure. See §5 for
> the full positioning statement.

> **Scope note.** An earlier version of this repository also contained a second, longitudinal
> study (account maturity vs. a new ad group's growth trajectory, n = 29 customers) run as a
> conceptual replication of the design tested here. That study has been **descoped from this
> paper** — its sample was small (customer-level n = 29–32) and its equivalence tests did not
> reach formal TOST equivalence, so it is reported separately as planned follow-up work rather
> than as part of this manuscript's evidence base. See
> [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md) for the full write-up of that
> descoped study and the research agenda built on it. Nothing in the sections below relies on
> it, and no cross-study claim is made in this document.

---

## Table of contents

1. [At a Glance](#1-at-a-glance)
2. [Theoretical Framework — Two Competing Accounts and a New Construct](#2-theoretical-framework--two-competing-accounts-and-a-new-construct)
3. [Data & Setting](#3-data--setting)
4. [Central Analysis — Advertiser-Size Fairness](#4-central-analysis--advertiser-size-fairness)
5. [Methodological Positioning — This Study as a Mediation Audit](#5-methodological-positioning--this-study-as-a-mediation-audit)
6. [Synthesis](#6-synthesis)
7. [Boundary Conditions & Generalizability](#7-boundary-conditions--generalizability)
8. [Limitations](#8-limitations)
9. [Transparency Log — Known Code/Design Issues](#9-transparency-log--known-codedesign-issues)
10. [Figure Gallery](#10-figure-gallery)
11. [Repository Structure](#11-repository-structure)
12. [How to Reproduce](#12-how-to-reproduce)

---

## 1. At a Glance

| | Cross-sectional analysis |
|---|---|
| **Structural attribute tested** | Advertiser size (spend tier) |
| **Legitimate mediator / alternative signal** | Total spend |
| **Theoretical accounts pitted against each other** | Statistical discrimination (Phelps 1972; Arrow 1973) vs. algorithmic behavioral meritocracy (Dwork et al. 2012) — [§2.2](#22-competing-account-i--statistical-discrimination-and-structural-entrenchment) |
| **Sample** | 321 advertisers, ~19.3M rows |
| **Central audit test** | H1c — direct path (size → outcome, net of spend) |
| **Evidence grade (§6)** | **Confirmatory** — 8/8 robustness methods agree, high power |
| **Key figures** | [1](#10-figure-gallery), [2](#10-figure-gallery), [3](#10-figure-gallery), [7](#10-figure-gallery), [8](#10-figure-gallery), [11](#10-figure-gallery) |
| **Secondary finding** | Null is not perfectly homogeneous across ad-product categories (H2, joint Wald p = .023) |
| **Supplementary robustness screening** | RDD (5 candidates) and policy-change event studies (5 dates) were screened as a supplement to the mediation-audit design; **neither survived customer-level re-analysis, consistent with the mediation-audit boundary stated in §5** |

**One-line summary:** across eight independent robustness methods on a single, well-powered
cross-sectional sample, advertiser size shows **structural signal irrelevance** (§2.7) — no
detectable residual association with algorithmic outcomes once total spend is held constant.
This is a mediation-audit finding, not a causal claim. See [Figure 11](#10-figure-gallery) for
the supplementary robustness screening. A planned longitudinal extension of this same design is
described separately in [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md).

---

## 2. Theoretical Framework — Two Competing Accounts and a New Construct

### 2.1 Why this is a theoretical question, not just a fairness-audit question

The applied question — *does a large advertiser get treated better by the algorithm,
independent of what it currently does?* — sits on top of a much older question in economics
and, more recently, algorithmic fairness: when a decision-maker cannot fully observe a
counterparty's quality, does it fall back on cheap, observable, structural proxies for that
quality, or does it condition allocation on current, verifiable behavior instead? Framing the
question this way turns a single-platform audit into a test between two theoretical accounts,
each of which makes an opposite, falsifiable prediction about the sign and significance of the
same coefficient (H1c). §2.2–§2.5 state both accounts and derive the formal hypotheses tested in
[§4](#4-central-analysis--advertiser-size-fairness). §2.7 then names the pattern this test is
designed to detect as a standalone construct, independent of which account it turns out to
support.

### 2.2 Competing Account I — Statistical discrimination and structural entrenchment

**Signaling theory** (Spence, 1973) and **statistical discrimination theory** (Phelps, 1972;
Arrow, 1973) both start from the same premise: a decision-maker facing incomplete information
about a counterparty's underlying quality will condition its treatment of that counterparty on
cheap, observable correlates of quality, even when a more direct behavioral signal exists.
Phelps' original formulation is a Bayesian decision-maker who sets an outcome (a wage, in the
labor-market original) equal to the posterior expectation of quality given an observed signal;
applied to a paid-search platform, advertiser size is exactly this kind of cheap, persistent,
observable correlate of plausible advertiser quality (operational sophistication, financial
stability, campaign-management competence).

**Prediction:** if the platform's ranking/serving algorithm — whether by explicit design or as
an emergent property of training/tuning — uses advertiser size as a statistical-discrimination-
style proxy, then it should retain a **direct, residual association** with algorithmic outcomes,
over and above whatever it explains through the legitimate behavioral channel (spend, bidding
behavior) it correlates with.

### 2.3 Competing Account II — Algorithmic behavioral meritocracy

The algorithmic fairness literature offers the directly opposite prediction. **Individual
fairness** (Dwork et al., 2012) treats similar treatment for similar current behavior —
independent of group- or category-level attributes — as the technical benchmark for a
well-specified algorithmic system. Applied here: a real-time, auction-based serving system
should, in principle, allocate outcomes on the basis of what an advertiser is currently doing,
not on accumulated structural status, both because real-time behavioral signals are cheaper and
more predictive once an auction is running, and because conditioning on structural status
independent of current behavior is difficult to justify as serving the platform's own stated
objective (auction efficiency) rather than entrenching incumbents.

**Prediction:** once current behavior (spend) is held constant, advertiser size should show **no
residual association** with algorithmic outcomes.

We refer to this as the **behavioral meritocracy** account. It is a positive, testable claim
about how the algorithm behaves — not a normative claim that behavior-only allocation is
sufficient for fairness in a fuller distributive sense (addressed in
[§7](#7-boundary-conditions--generalizability) and [§8](#8-limitations)).

### 2.4 Formal hypotheses

| ID | Hypothesis | Statistical-discrimination account predicts | Behavioral-meritocracy account predicts |
|---|---|---|---|
| H1a | Size → total spend (a-path; not in dispute) | positive, significant | positive, significant |
| H1b | Spend → outcome, net of size (b-path; not in dispute) | positive, significant | positive, significant |
| **H1c** | **Size → outcome, net of spend (c′-path; focal audit test)** | **significant, direction favoring size** | **null (c′ ≈ 0)** |
| H2 | Homogeneity of the H1c null across ad-product categories | — | homogeneous null (a rejection is a bounded exception, not a reversal) |

A null result on H1c is treated as substantive support for behavioral meritocracy, not merely as
an absence of finding — and, per §2.7, as one instance of the broader **structural signal
irrelevance** pattern this repository is built to detect.

### 2.5 Structural Signal Irrelevance: construct definition and research agenda

§2.2–§2.4 treat statistical discrimination and behavioral meritocracy as competing predictions
about a coefficient. This subsection does something different: it names the *pattern itself* —
independent of which theory turns out to explain it — as a standalone construct, so that it can
be studied, compared across platforms, and falsified on its own terms in future work.

#### 2.5.1 Why naming the pattern matters

A reviewer encountering §2.2–§2.4 alone could read this repository as "two existing theories
applied to a new dataset." That is an accurate but incomplete description. What §2.2–§2.4 do not
yet provide is a name for the *state of the system* when the behavioral-meritocracy prediction
holds — a state that is theoretically interesting in its own right, independent of which account
produced it, because it describes a property of the **algorithm**, not a property of either
theory. Naming and formalizing that state is the contribution of this subsection.

#### 2.5.2 Definition

> **Definition (Structural Signal Irrelevance, SSI).** In an algorithmically-mediated market,
> let S denote a structural attribute of a participating unit (a static or slowly-accumulating
> property such as size, tenure, or reputation stock), let B denote a current behavioral signal
> the same unit generates (e.g., spend, bidding activity, engagement), and let Y denote an
> algorithmic outcome (e.g., ranking, approval, price). The system exhibits **structural signal
> irrelevance with respect to S** when
>
> &nbsp;&nbsp;&nbsp;&nbsp; Y ⊥ S | (B, X)
>
> holds (or is not rejected) for a specified covariate set X, where the conditional
> (in)dependence is assessed via decomposition of S's association with Y into a path mediated
> by B and a direct residual path net of B. SSI is a property of *the observed system*, not a
> claim about the mechanism that produced it, and not a normative claim that the resulting
> allocation is fair in a distributive sense (§7).

Three features distinguish SSI from the constructs already invoked in §2.2–§2.3:

1. **Relative to statistical discrimination:** statistical discrimination theory is a
   *decision-maker-side* account of *why* a system might condition on S. SSI is an
   *outcome-side* description of *whether* it does — SSI can be observed (or fail to be
   observed) regardless of whether one accepts the statistical-discrimination account as the
   correct causal story for why it failed to be observed.
2. **Relative to individual fairness:** Dwork et al.'s (2012) individual fairness is a
   *normative benchmark* ("similar individuals should be treated similarly"). SSI is a
   *descriptive test* restricted to one specific attribute axis (structural vs. behavioral) and
   makes no claim that satisfying it is sufficient for fairness overall (§7's procedural/
   distributive distinction depends on exactly this restriction).
3. **Relative to mediation analysis generically:** a single coefficient showing full mediation
   is evidence *toward* SSI, not SSI itself. As used in this repository, a robust SSI claim
   rests on **convergence across many independent robustness methods within the same design**
   (§6), and would be strengthened further by replication on independent samples or time axes —
   a direction proposed as future work in
   [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md) rather than claimed here.

#### 2.5.3 Boundary conditions — when SSI should and should not be expected

Combining the platform-governance literature cited in §2.3 with organizational and market
structure logic yields four falsifiable propositions about when SSI should hold:

- **P1 (real-time conditioning).** SSI is more likely in systems where allocation decisions are
  made per-transaction on current behavioral signals without a human-review buffer, because such
  systems have less structural opportunity to fall back on S. (Gillespie, 2014.)
- **P2 (auction/market liquidity).** SSI is more likely in categories with enough transaction
  volume that even a small unit accumulates a usable B quickly. In illiquid categories, systems
  are structurally more likely to fall back on S as a proxy, so SSI should be expected to *fail*
  there.
- **P3 (discretionary review re-entry).** Sub-processes with human discretionary review
  (approval queues, manual verification) are predicted to be SSI-violation *candidates* even
  within an otherwise SSI-consistent system, because discretion re-opens a channel for S to
  matter. (The H2 exception in §4.6 is offered as an empirical instance of this proposition,
  not as a demonstrated mechanism.)
- **P4 (measurability).** SSI can only be evaluated where B is measured with completeness that
  does not itself correlate with S. Where B (or the outcome Y) is differentially observed as a
  function of S — the exact concern that motivates excluding Conversion/ROAS in §3.1 — SSI is
  **not testable**, not violated; this is a scope condition on the method, not a finding.

#### 2.5.4 Research agenda

Because a construct is only useful if it generates a research program beyond the platform that
introduced it, four directions are proposed as explicit next steps rather than as an unbounded
"future research" gesture. Direction 2 below is the one this repository is already actively
building toward — see [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md) for the concrete,
partially-executed follow-up study.

1. **Cross-platform SSI comparison.** Operationalize P1–P3 as measurable platform
   characteristics (share of decisions with human review; category-level auction depth) and test
   whether SSI strength covaries with them across platforms, turning this repository's
   single-platform result into a comparative framework.
2. **Temporal stability of SSI.** Track whether SSI persists across algorithm retrains or policy
   changes, or over time on an existing unit's lifecycle, or whether there are identifiable
   windows in which structural signals "re-enter." A first attempt at a temporal-axis
   replication (account maturity vs. a new ad group's growth trajectory) is documented in
   [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md); it was found too small-sample to
   support a confirmatory claim on its own and is reported there as a template for a better-
   powered follow-up rather than as evidence in this manuscript.
3. **SSI and distributive fairness, jointly modeled.** SSI (procedural) is compatible with
   resource-driven inequality in B itself (distributive) — a well-resourced participant can
   simply generate a stronger B. A formal model or simulation connecting SSI-consistent
   allocation rules to long-run market concentration would connect this repository's procedural
   finding to the distributive question it explicitly does not resolve (§7).
4. **A general-purpose SSI audit protocol.** Document the mediation-decomposition design used
   here (structural attribute → legitimate behavioral mediator → outcome, tested for a null
   direct path net of the mediator) as a portable audit template for other algorithmically
   mediated markets (gig-work assignment, credit scoring, marketplace ranking) where sock-puppet
   or field-experimental audits are infeasible.

> **Additional references for §2.5:** Barocas, S., & Selbst, A. D. (2016). Big data's disparate
> impact. *California Law Review*. Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017).
> Inherent trade-offs in the fair determination of risk scores. *ITCS*. Corbett-Davies, S., &
> Goel, S. (2018). The measure and mismeasure of fairness. *arXiv*. Gillespie, T. (2014). The
> relevance of algorithms. In *Media Technologies*.

---

## 3. Data & Setting

| Table | Contents | Rows | Coverage |
|---|---|---|---|
| Ad performance log | Daily/hourly impressions, clicks, cost, conversions, ad rank | 19,373,916 | 321 advertisers |
| Campaign dimension | Campaign-level metadata incl. `campaign_type` (ad-product code) | 1,504 | 263/321 |
| Ad group dimension (2026-07-22 snapshot) | Bid price, registration/deletion timestamps, on/off status | 9,823 | 263/321 |
| Keyword dimension | Brand type, `inspect_status` (review code), bid price | 1,503,289 | 256/321 |

**Limitations:**
- Single agency (SearchM), single platform (Naver search ads) — cannot be resolved with this
  data. See §2.5.4's cross-platform research agenda for how this constraint is meant to be
  lifted in follow-up work.
- `adgroup_dim` is a **current snapshot** (2026-07-22). Deleted ad groups drop out of the table
  entirely, so any account-history measure derived from it (all-time ad group count, account
  age) is always a **lower bound**.

### 3.1 Construct validity: why Conversion/ROAS variables are excluded (methodological decision, not a data gap)

Conversion and ROAS variables are excluded from this study **by design, prior to any modeling**,
for a reason that goes beyond routine data availability and bears directly on the mediation-
audit design behind H1c ([§2.4](#24-formal-hypotheses)), and is a direct instance of the P4
measurability boundary condition on SSI stated in §2.5.3.

Naver's conversion-tracking API backfills conversion records **per account**, on a delayed and
inconsistent schedule. This is not classical missing-data noise: the degree of backfill lag is a
property of *which account* is being observed, and there is no basis in the data-generating
process to assume that lag is uncorrelated with the structural attribute under test. A larger or
more established advertiser is plausibly more likely to have a fully integrated, low-latency
conversion pipeline (dedicated account management, more mature tracking-tag implementation) than
a smaller one — which means backfill completeness would be systematically confounded with
exactly the independent variable (H1c's `size`) whose residual, direct association with outcomes
is the object of the audit test.

Including conversion/ROAS as an outcome under these conditions would not simply add noise; it
risks **manufacturing the very c′ pattern the test is designed to detect, as a measurement
artifact of differential data completeness rather than a genuine algorithmic pattern** — this
would produce an apparent SSI *violation* that is actually unmeasurability, not a finding
(§2.5.3, P4). This is structurally the same concern that motivated the CPC-vs-`bid_amount`
mechanical-artifact check in [§4.5](#45-robustness-checks) (method 7): outcome measures that
share a data-generating dependency with the variable under test are excluded, or substituted
with a cost-independent alternative, wherever the shared dependency cannot be ruled out.
Conversion/ROAS could not be substituted with an equally valid cost-independent proxy the way
CPC was substituted with `bid_amount`, so it is excluded from the audit design entirely, and no
revenue- or profitability-linked claim is made anywhere in this repository. This decision was
made at the data-preparation stage, **before any outcome model was estimated** — it is a
pre-specified construct-validity safeguard, reported here as methodology rather than as a
post-hoc limitation. (Listed again briefly in [§8](#8-limitations) with a pointer back here.)

---

## 4. Central Analysis — Advertiser-Size Fairness

### 4.1 Question

Does advertiser size directly, statistically associate with algorithmic outcomes — approval
rate, cost efficiency, ad rank — independent of how much the advertiser actually spends? This
is the audit test of H1c ([§2.4](#24-formal-hypotheses)).

### 4.2 Where would a size advantage even live?

Before testing anything about size, a 3-level unconditional variance-component model (MixedLM,
REML) located *where* performance variation sits.

![Figure 1 | Multilevel variance decomposition of advertising performance](figures/Figure1_variance_decomposition.png)

**Figure 1.** Across ~663K observations, log ad spend is dominated by unexplained residual
variance (ICC = 0.825), not by who the customer is (ICC = 0.050). Click-through rate
concentrates at the *ad group* level (ICC = 0.301), not the customer level (ICC = 0.200). Both
patterns hold with or without month fixed effects, ruling out seasonality — a preliminary
signal, prior to any audit test, that "who the customer is" (the statistical-discrimination
account's structural proxy) explains comparatively little.

### 4.3 The raw gap, and why it doesn't survive clustering

Splitting advertisers into four spend-based size tiers, Kruskal–Wallis shows significant raw
differences in all three outcomes (p < .001 for CPC and ad rank, p = .0006 for approval rate;
ε² = 0.002–0.079 — significant but small). A customer-level cluster permutation test (2,000
iterations) shows most of this "significance" evaporates once same-customer non-independence is
accounted for — the exact failure mode the spend-controlled design below is built to correct.

### 4.4 The central audit test (H1c)

![Figure 2 | Advertiser-size effect on approval, cost efficiency, and ad rank, controlling for spend](figures/Figure2_fairness_forest_plot.png)

**Figure 2.** Controlling for log spend in a cluster-robust regression, **all six outcome ×
sample combinations return non-significant direct-path coefficients for size** (cluster-robust
p > .07). Every 95% bootstrap CI sits inside, or at the edge of, its own minimum-detectable-effect
(MDE) band at 80% power — the sample is well-powered to detect an effect smaller than what the
raw comparison suggests is "the effect." Approximate Bayes factors favor the null in 5 of 6
tests. **This is the pattern that satisfies structural signal irrelevance for advertiser size
([§2.5](#25-structural-signal-irrelevance-construct-definition-and-research-agenda)), and is
the pattern predicted by the behavioral-meritocracy account
([§2.3](#23-competing-account-ii--algorithmic-behavioral-meritocracy)) rather than the
statistical-discrimination account
([§2.2](#22-competing-account-i--statistical-discrimination-and-structural-entrenchment)).**

### 4.5 Robustness checks

1. **Specification curve** — 48 defensible analytic choices (tier definition × covariate set);
   0/48 reach significance for any outcome.
2. **Placebo test** — device-type share (which size *shouldn't* predict) is significant under
   the raw distributional test but null under the spend-controlled regression, showing the
   regression measures the right thing.

![Figure 3 | Multiverse specification curve and placebo test](figures/Figure3_specification_curve_placebo.png)

**Figure 3.** Panel A: none of 48 specification choices reach significance for any outcome.
Panel B: the raw distributional test is significant for *both* the real outcome and the
device-share placebo, proving a distributional test alone is not a clean placebo here. The
informative comparison is the spend-controlled regression, where real and placebo outcomes are
equally, indistinguishably null.

3. Customer-and-month fixed-effects panel regression.
4. **2SLS with lagged spend as instrument** — first-stage F-statistic could not be recovered
   (code exception, [transparency log #2](#9-transparency-log--known-codedesign-issues));
   excluded from any conclusion rather than silently dropped. As stated in §5, this attempt to
   move beyond the mediation-audit design into causal identification is a supplementary probe,
   not a requirement of the core design — its incompleteness is why a further supplementary
   strategy (RDD, policy-change event studies) was separately screened, see
   [§4.5.9](#459-alternative-identification-screening--rdd--policy-change-supplementary-robustness-only).
5. Temporal split-sample replication (era1 vs era2).
6. Benjamini–Hochberg FDR correction across the primary hypotheses — raw KW tests remain
   significant after correction, spend-controlled regressions remain null after correction (the
   contrast survives multiple-testing correction).
7. **Mechanical-artifact isolation in CPC** — since CPC = cost/click and spend is built from
   cost, a customer-level permutation procedure shows the observed spend→log(CPC) coefficient
   falls *below* the purely-mechanical null distribution's lower bound; a lagged replication
   (day t spend → CPC at t+1, t+7, immune to same-day cost-sharing) confirms a same-signed,
   significant association at both lags. This is the same construct-validity logic applied to
   Conversion/ROAS in [§3.1](#31-construct-validity-why-conversionroas-variables-are-excluded-methodological-decision-not-a-data-gap):
   where a shared data-generating dependency between treatment and outcome cannot be ruled out,
   either substitute a clean outcome (done here) or exclude the outcome entirely (done for
   Conversion/ROAS).
8. **Alternative-outcome replication on `bid_amount`** (shares no cost/click term with spend, so
   it carries none of method 7's artifact).

![Figure 7 | Spend-mediation b-path: CPC-based vs. cost-independent outcome](figures/Figure7_mediation_forest.png)

**Figure 7.** The spend–outcome coefficient shrinks from +1.277 (CPC-based, partly mechanical)
to +0.150 (bid_amount-based, cost-independent) once the shared cost term is removed — direction
survives, magnitude does not. At the customer level (n=263): the indirect (spend-linked)
association is significant (bootstrap 95% CI [0.008, 0.159], permutation p<.001) while the
direct association of size, net of spend, is not (p=.634) — the same qualitative pattern, now
on an artifact-free outcome.

#### 4.5.9 Alternative-identification screening — RDD & policy-change (supplementary robustness only)

**This entry supplements method 4 above; it does not replace it, and it is not part of the core
mediation-audit design (§5).** Because 2SLS could not be completed, a further, more ambitious
strategy was screened purely as a supplementary robustness angle: (1) regression discontinuity
(RDD) on the running variables `size` and `total spend`, screened across candidate cutoffs, and
(2) policy-change event-study DiD around dates flagged by an automated structural-break scan of
the size–CPC relationship. **Neither strategy is adopted as an identification design; both are
reported here as null robustness checks that are consistent with, but not required by, the H1c
mediation-audit result.** Full method and all candidates:
[`supplementary_identification/SCREENING_SUMMARY.md`](supplementary_identification/SCREENING_SUMMARY.md).

**RDD (summary).** 40 candidate cutoffs were scanned; 5 survived an initial bandwidth-sensitivity
filter. A three-round screen (bandwidth filter → donut-hole robustness → decisive customer-level
re-analysis) found **0 of 5 candidates survive** as a usable design: two fail a customer-level
density test outright (manipulation cannot be ruled out); two lose significance once
re-estimated at the customer level (the panel-level result was a density artifact of
higher-spend customers simply having more active days); the remaining candidate is only
marginally significant, fragile under donut-hole perturbation, and has no independent
institutional justification.

**Policy-change event studies (summary).** Five candidate dates from an automated CUSUM scan
produced uniformly non-significant DiD coefficients (p = .16–.58), statistically
indistinguishable from 500 randomly chosen placebo dates.

**Why this is reported rather than omitted.** Under the mediation-audit framing of §5, this
null result is not "a causal identification attempt that failed" — it is a supplementary
robustness angle whose null outcome is directionally consistent with the H1c mediation-audit
result: no detectable discontinuity in the size–CPC relationship at any scanned threshold or
auto-detected date. Full detail, all candidates, and the three-round screening process are
archived in [`supplementary_identification/`](supplementary_identification/SCREENING_SUMMARY.md);
the summary visual is [Figure 11](#10-figure-gallery).

### 4.6 Is the null homogeneous across contexts? (H2)

![Figure 8 | Campaign product-type heterogeneity](figures/Figure8_boundary_condition_forest.png)

**Figure 8.** Stratifying the spend-controlled CPC model by `campaign_type`, a joint Wald test
on the size × product-type interaction gives **p = .023**. No individual stratum is significant
alone (Website n=184: −0.279, p=.052; Local business n=27: +0.312, p=.211; Shopping n=17:
+0.245, p=.151), but the joint test is — treated here as a real, if narrow, exception rather
than noise, and as a candidate empirical instance of proposition P3 in §2.5.3 (discretionary
review re-entry). A plausible mechanism is that shopping campaigns route through a
product-feed validation pipeline that standard search campaigns do not, which could reintroduce
an account-level channel elsewhere in the approval process; this is offered as a hypothesis for
future work, not a demonstrated mechanism. Local-business and shopping strata are small (n=27,
n=17); this joint-test result should be read as a boundary-condition *candidate* per H2
([§2.4](#24-formal-hypotheses)), not an established theory, until it can be tested on a larger,
better-powered sample.

### 4.7 Exploratory appendix — churn-prediction benchmarking

Not part of the confirmatory hypothesis family; reported for practical reference only.

![Figure 4 | Churn-prediction benchmarking](figures/Figure4_churn_benchmark.png)

**Figure 4.** Nested-CV ROC-AUC across three models on a small, severely imbalanced labeled
sample (n=213 accounts, 2.35% churn rate). Gradient boosting nominally leads (0.79 [0.63, 0.97])
but all pairwise Wilcoxon comparisons return p=0.0625 — the statistical floor at n=5
repeat-pairs, not a real tie ([transparency log #4](#9-transparency-log--known-codedesign-issues)).
Not treated as a confirmatory finding.

### 4.8 Verdict

> Raw size-tier gaps are statistically detectable but fragile once clustering is accounted for.
> The spend-controlled test — replicated on a cost-independent outcome — returns a clean,
> well-powered null for the direct association of size (H1c), backed by eight independent
> robustness checks, with one precisely characterized exception (H2, ad-product heterogeneity).
> A supplementary robustness screening (RDD, policy-change event studies) found no usable design
> capable of upgrading this to a causal claim, and its null result is directionally consistent
> with the same conclusion — as expected under the mediation-audit boundary stated in §5.
> **Read against [§2](#2-theoretical-framework--two-competing-accounts-and-a-new-construct):
> advertiser size exhibits structural signal irrelevance (§2.5), consistent with the algorithmic
> behavioral-meritocracy account over the statistical-discrimination account.** The apparent
> advantage of being a large advertiser is, to first order, consistent with being fully
> accounted for by spending more rather than by size itself.

---

## 5. Methodological Positioning — This Study as a Mediation Audit

### 5.1 Why this section replaces a hedge with a design statement

This study is not a causal-inference study that fell short of identification. It is designed
and reported, from the outset, as a **mediation audit**: a method for evaluating procedural
fairness in an algorithmically-mediated market using observational panel data, without claiming
or requiring causal identification. Framing the study this way changes how the 2SLS/RDD/
policy-change screenings (§4.5, method 4; §4.5.9) should be read — not as failed attempts at the
study's actual goal, but as supplementary probes of whether a stronger identification tier was
*available*, run and reported honestly regardless of outcome.

### 5.2 Positioning within the algorithm-audit literature

Algorithm-audit methodology (Sandvig et al., 2014; Metaxa et al., 2021; Raji et al., 2020)
distinguishes several audit designs by what access to the platform they require and what they
can conclude:

| Audit type | Method | Requires platform access / intervention? | Targets causal identification? |
|---|---|---|---|
| Correlation audit | Raw outcome-attribute association in observational data | No | No |
| Sock-puppet / scraping audit | Controlled synthetic accounts probe the live system | Yes (simulated interaction) | Partially, within the synthetic-account frame |
| **Mediation audit (this study)** | Decompose a structural attribute's association with outcomes into a legitimate-mediator path and a direct residual path, in observational panel data | No | **No — by design** |

Sock-puppet audits are the gold standard for causal claims about a live algorithm, but require
platform access this repository does not have (no ability to create or manipulate real
advertiser accounts on a production ad platform). The mediation-audit design is the appropriate
alternative under that constraint: it cannot support a causal claim, but it can support a
sharper procedural-fairness claim than a raw correlation audit, because it isolates the direct
association from the association explained by a legitimate behavioral channel.

### 5.3 What follows from this framing

1. **The 2SLS/RDD/policy-change screenings are reframed, not re-run.** Their statistical results
   are unchanged; only their status in the argument changes — from "failed identification
   strategy" to "supplementary robustness angle whose null result is consistent with, but not
   required by, the mediation-audit conclusion" (§4.5.9).
2. **Every "path," "mediation," and "effect" statement in this repository** describes conditional
   statistical (in)dependence in observational panel data — Y ⊥ S | (B, X) in the notation of
   §2.5.2 — not an identified causal effect. This vocabulary is standard in the mediation-audit
   and platform-economics literatures and is used deliberately, not as a hedge added after the
   fact.
3. **What the combined robustness battery supports** is a materially stronger form of mediation-
   audit evidence than any single coefficient: the same qualitative pattern replicates across
   contaminated and artifact-free outcomes, across dozens of specifications, against placebos,
   across time splits, and — via the null RDD/policy-change screening — across two additional
   threshold/date axes that would have been expected to show a discontinuity if the structural
   attribute genuinely mattered independently.
4. **The reusable contribution of this repository is the audit protocol itself** (formalized as
   the SSI test in §2.5.2 and proposed as a portable template in §2.5.4), independent of which
   way any single platform's answer points.

> **References for §5:** Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014).
> Auditing algorithms: Research methods for detecting discrimination on internet platforms.
> *ICA Preconference on Data and Discrimination*. Metaxa, D., Park, J. S., Robertson, R. E.,
> Karahalios, K., Wilson, C., Hancock, J., & Sandvig, C. (2021). Auditing algorithms: Understanding
> algorithmic systems from the outside in. *Foundations and Trends in Human-Computer Interaction*.
> Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J.,
> Theron, D., & Barnes, P. (2020). Closing the AI accountability gap. *FAccT*.

---

## 6. Synthesis

![Figure 11 | Alternative-identification screening — RDD & policy-change event studies](figures/Figure11_identification_screening.png)

**Figure 11.** A supplementary robustness angle (not part of the core mediation-audit design,
§5): two causal-identification strategies (RDD across 5 size/spend cutoff candidates;
policy-change event-study DiD across 5 auto-detected dates) were screened. Neither survived
decisive customer-level re-analysis — 0/5 RDD candidates hold up, and all 5 event-study DiD
coefficients are statistically indistinguishable from a randomly chosen date. Consistent with
§5's positioning, this is reported as a null supplementary robustness check whose pattern is
directionally consistent with H1c, not as an adopted identification result.

### 6.1 Evidence summary

| | Advertiser size (H1c) |
|---|---|
| **Evidence grade** | **Confirmatory** |
| Robustness convergence | 8/8 independent methods null |
| Power against pre-registered SESOI | High across all six outcome×sample combinations |
| How it should be cited | As an independently interpretable mediation-audit result |

### 6.2 What this study establishes, and what it doesn't

This study tests one underlying question, framed theoretically in §2 and formalized as
**structural signal irrelevance** in §2.5 — *does a structural, account-level attribute directly
explain a unit-level algorithmic outcome (as the statistical-discrimination account predicts),
or is it fully absorbed by a legitimate behavioral channel (as the behavioral-meritocracy
account predicts)* — on a single, well-powered sample, using multiple independent robustness
methods and, in the supplementary screening, independent threshold/date axes. Per §5, no causal
identification is claimed anywhere in this repository, and none was required by the design; the
honest claim is **convergent mediation-audit evidence favoring behavioral meritocracy over
structural entrenchment on this sample**, not a proven causal mechanism, and not (yet) a
cross-sample or cross-time-axis replication. See [§7](#7-boundary-conditions--generalizability)
for the explicit boundary between this *procedural* finding and any *distributive*-fairness
claim, which this repository does not make, §2.5.4 for the research agenda that follows from
naming this pattern as a portable construct, and
[`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md) for a planned longitudinal replication
of this same design on an independent sample and time axis.

---

## 7. Boundary Conditions & Generalizability

**Within-platform heterogeneity.**
- Campaign product type (H2, Figure 8): joint Wald p = .023 — not perfectly homogeneous,
  plausibly because different product types route through different approval pipelines (e.g.,
  shopping campaigns undergo product-feed validation that standard search doesn't) — a candidate
  instance of proposition P3 (§2.5.3). Reported as a candidate boundary condition warranting
  further study, not an established theory — the individual product-type strata are small
  (n=27, n=17) and none is significant alone.
- Keyword review status (exploratory): only 0.5% of keywords carry a non-standard
  `inspect_status`, so this check is under-powered by construction; the one significant
  interaction (restricted-approval definition, p=.016) is one signal probed three ways, not
  three independent confirmations.
- Industry classification was piloted (multilingual embeddings + LLM ensemble against KSIC
  categories) but inter-rater reliability (Randolph's free-marginal κ = 0.557) and
  cross-validation against a rule-based classifier (Cohen's κ = 0.363) both indicate
  moderate-at-best label reliability — industry-stratified results are not reported as findings.

**Cross-platform generalizability.** The documented pattern — real-time, auction-based serving
whose outcomes track a unit's own current signal — is a property of the serving architecture,
not this platform's brand specifically (§2.5's proposition P1), and is consistent with the
behavioral-meritocracy account of §2.3 as a *property of the auction mechanism* rather than a
claim unique to Naver/SearchM. Direction is expected to generalize to other real-time bidding
platforms with comparable architecture; magnitude is not claimed to generalize. §2.5.4 proposes
the comparative study needed to test this directly. The pattern would plausibly **weaken**
under: mandatory human review (P3 — account-level trust could re-enter through reviewer
discretion), new categories without established auction liquidity (P2 — the platform may fall
back on account-level heuristics), or platforms whose ranking algorithm explicitly incorporates
account tenure/verification as a feature.

**Procedural vs. distributive fairness — an explicit boundary.** This repository's finding is
about **procedural** fairness: whether the algorithm conditions outcomes on structural status
net of current behavior — precisely the scope of the SSI construct defined in §2.5.2. It is
deliberately silent on **distributive** fairness: whether behavior-only allocation is itself
equitable across advertisers who start with unequal resources. A system that satisfies SSI can
still reproduce or amplify pre-existing resource asymmetries, since a well-resourced advertiser
can simply generate a stronger current behavioral signal — a concern raised in the broader
algorithmic-fairness literature's distinction between attribute-level non-discrimination and
structural injustice operating through correlated social determinants (Barocas & Selbst, 2016).
Nothing in this repository resolves that second, distributive question; §2.5.4 proposes it as
the natural next research direction rather than folding it into the present null result.

---

## 8. Limitations

| # | Limitation |
|---|---|
| 1 | Single agency, single platform — external generalizability is architecturally scoped, not empirically tested across platforms; §2.5.4 proposes the comparative design needed to test it |
| 2 | This is a mediation audit (§5), not a causal-inference study, by design. A supplementary attempt to reach a stronger identification tier (2SLS; RDD/policy-change event studies) found no usable design — an expected boundary of the method, not a deficiency of it |
| 3 | H2 strata are unevenly sized (n=184/27/17) — interpret the joint interaction test accordingly, and treat it as a boundary-condition candidate (§2.5.3, P3), not an established theory |
| 4 | Keyword-review-status boundary check is under-powered (0.5% of keywords carry non-standard status) |
| 5 | Conversion/ROAS variables excluded entirely as a pre-specified construct-validity safeguard (§3.1) — a direct instance of the P4 measurability boundary condition (§2.5.3) — no revenue/profitability conclusions can be drawn |
| 6 | RDD and policy-change screening candidates were found by scanning the same variables under audit test (`size`, `spend`) rather than an externally validated policy threshold or date; no candidate has independent institutional confirmation, which is an additional reason (beyond the statistical non-survival reported in §4.5.9) that neither is treated as an identification design |
| 7 | This repository establishes procedural fairness (SSI, §2.5.2) only; it does not adjudicate distributive fairness across advertisers with unequal starting resources (§7, §2.5.4) |
| 8 | This is a single-sample, single-time-axis result. A conceptual replication on an independent sample and a longitudinal time axis was attempted at small scale and is reported separately, as future work, in [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md) rather than as corroborating evidence in this document |

---

## 9. Transparency Log — Known Code/Design Issues

*Logged in full for reproducibility review. Reported plainly, not minimized. Full narrative log
lives in [`docs/METHODOLOGY_NOTES.md`](docs/METHODOLOGY_NOTES.md).*

| # | Location | Issue | Status | How it's handled |
|---|---|---|---|---|
| 1 | Central analysis | Spike-account exclusion produces identical results before/after in the FE and 2SLS robustness axes (likely because a `min_days` filter already excludes spike accounts from these subsamples) | Root cause inferred, not confirmed | Flagged as providing no additional robustness information on this axis — not counted as an independent confirmation |
| 2 | Central analysis | 2SLS first-stage F-statistic silently returns `None` due to an uncaught exception in a `try/except` block | Root cause unidentified | 2SLS coefficients excluded from all confirmatory conclusions; retained only as an unverified reference value |
| 3 | Central analysis | The core audit test (H1c, spend-controlled regression) was not re-run under the temporal split — only the raw KW test was | Design gap | Noted explicitly as a limitation, not silently left implicit |
| 4 | Exploratory churn appendix | Wilcoxon signed-rank p-values are identical (.0625) across all three model-pair comparisons — the floor value achievable at n=5 repeat-pairs, not a real tie in performance | Confirmed statistical artifact | No significance stars used; footnoted explicitly |
| 5 | Alt-ID screening | Initial RDD panel-level left/right sample-count imbalance flags conflated genuine running-variable manipulation with panel-density variation (higher-spend customers simply have more active days, hence more panel rows) | Confirmed methodological ambiguity | Resolved by re-running the density test and RDD at the customer level (one row per customer), which removes panel-density variation entirely — see `supplementary_identification/step11c_customer_level_reanalysis.py` |
| 6 | Alt-ID screening | Auto-detected structural-break dates (CUSUM scan) cluster within a 2-month window at ~15-day spacing, more consistent with one gradual coefficient drift than 5 discrete breaks | Confirmed pattern, not resolvable without external policy documentation | Reported as a limitation of the auto-detection approach; all 5 dates were still tested individually and none produced a significant DiD, so this ambiguity does not affect the (null) conclusion |
| 7 | Repository-wide | Earlier drafts framed §4.5.9's RDD/policy-change screening as a "failed causal identification attempt" | Framing issue, not a statistical one | Reframed under §5's mediation-audit positioning as a supplementary robustness angle whose null result is consistent with, not required by, the core conclusion — see `docs/METHODOLOGY_NOTES.md` |

---

## 10. Figure Gallery

All figures render inline below and also live as standalone PNGs in [`figures/`](figures/) for
direct download or embedding elsewhere.

<a id="figure-1"></a>
### Figure 1 — Multilevel variance decomposition of advertising performance
*[used in §4.2](#42-where-would-a-size-advantage-even-live)*

![Figure 1](figures/Figure1_variance_decomposition.png)

---

<a id="figure-2"></a>
### Figure 2 — Advertiser-size effect on approval, cost efficiency, and ad rank, controlling for spend
*[used in §4.4](#44-the-central-audit-test-h1c)*

![Figure 2](figures/Figure2_fairness_forest_plot.png)

---

<a id="figure-3"></a>
### Figure 3 — Multiverse specification curve and placebo test
*[used in §4.5](#45-robustness-checks)*

![Figure 3](figures/Figure3_specification_curve_placebo.png)

---

<a id="figure-4"></a>
### Figure 4 — Churn-prediction benchmarking (exploratory appendix)
*Appendix D · [used in §4.7](#47-exploratory-appendix--churn-prediction-benchmarking)*

![Figure 4](figures/Figure4_churn_benchmark.png)

---

<a id="figure-7"></a>
### Figure 7 — Spend-mediation b-path: CPC-based vs. cost-independent outcome
*[used in §4.5](#45-robustness-checks)*

![Figure 7](figures/Figure7_mediation_forest.png)

---

<a id="figure-8"></a>
### Figure 8 — Campaign product-type heterogeneity
*[used in §4.6](#46-is-the-null-homogeneous-across-contexts-h2)*

![Figure 8](figures/Figure8_boundary_condition_forest.png)

---

<a id="figure-11"></a>
### Figure 11 — Alternative-identification screening: RDD & policy-change event studies (null, supplementary)
*[used in §4.5.9](#459-alternative-identification-screening--rdd--policy-change-supplementary-robustness-only) and [§6](#6-synthesis)*

![Figure 11](figures/Figure11_identification_screening.png)

| # | Title | Script |
|---|---|---|
| [1](#figure-1) | Multilevel variance decomposition | `make_figure1_variance_decomposition.py` |
| [2](#figure-2) | Advertiser-size effect, controlling for spend | `make_figure2_fairness_forest_plot.py` |
| [3](#figure-3) | Multiverse specification curve + placebo | `make_figure3_specification_curve_placebo.py` |
| [4](#figure-4) | Churn-prediction benchmarking | `make_figure4_churn_benchmark.py` |
| [7](#figure-7) | Spend-mediation b-path | `make_figure7_mediation_forest.py` |
| [8](#figure-8) | Product-type heterogeneity | `make_figure8_boundary_condition_forest.py` |
| [**11**](#figure-11) | **Alternative-identification screening (RDD + policy-change, null)** | `make_figure11_identification_screening.py` |

> Figures 5, 6, 9, and 10 from an earlier version of this repository belonged to the descoped
> longitudinal study and have moved to
> [`FUTURE_RESEARCH_STUDY2.md`](FUTURE_RESEARCH_STUDY2.md).

---

## 11. Repository Structure

```
structural-signal-irrelevance/
├── README.md                          <- you are here (§2.5 SSI construct, §5 mediation-audit positioning)
├── FUTURE_RESEARCH_STUDY2.md          <- descoped longitudinal study (account maturity), reported as future work
├── LICENSE
├── requirements.txt
│
├── config/
│   └── config.yaml                    <- all paths, thresholds, sample-definition rules
│
├── data/
│   └── README.md                      <- expected schema + how to request access (no data files committed)
│
│
├── src/
│   ├── utils/
│   │   ├── io.py
│   │   └── identifiers.py
│   │
│   └── pipeline_v4/                   <- advertiser-size mediation-audit pipeline
│       ├── step0_data_prep_v4.py      <- includes conversion/ROAS exclusion logic (§3.1)
│       ├── step1_variance_decomposition_v4.py
│       ├── step2_advertiser_size_fairness_v4.py
│       ├── step3_churn_appendix_v4.py
│       └── step4_synthesis_v4.py
│
├── supplementary_robustness/           <- supplementary robustness scripts
│   ├── supplementary_robustness_README.md
│   ├── 01_alternative_outcome_mediation.md / .py
│   ├── 02_boundary_conditions.md / .py
│   └── 03_equivalence_and_sensitivity_notes.md / .py
│
├── supplementary_identification/       <- RDD + policy-change screening (§4.5.9); supplementary
│   │                                       robustness only per §5, not the core audit design
│   ├── SCREENING_SUMMARY.md            <- full narrative + results tables, framed per §5
│   ├── step11_alt_identification_RDD_policy.py       <- Round 1: cutoff/date scan
│   ├── step11b_donut_hole_full_scan.py               <- Round 2: donut-hole robustness
│   └── step11c_customer_level_reanalysis.py          <- Round 3 (decisive): customer-level re-analysis
│
├── figures/                            <- one script per figure; reads results JSON/CSV, writes PNG
│   ├── make_figure1_variance_decomposition.py        -> Figure1_variance_decomposition.png
│   ├── make_figure2_fairness_forest_plot.py          -> Figure2_fairness_forest_plot.png
│   ├── make_figure3_specification_curve_placebo.py   -> Figure3_specification_curve_placebo.png
│   ├── make_figure4_churn_benchmark.py               -> Figure4_churn_benchmark.png
│   ├── make_figure7_mediation_forest.py              -> Figure7_mediation_forest.png
│   ├── make_figure8_boundary_condition_forest.py     -> Figure8_boundary_condition_forest.png
│   ├── make_figure11_identification_screening.py     -> Figure11_identification_screening.png
│   └── Figure*.png                                   <- the 7 rendered figures used above
│
├── appendix/
│   ├── churn_prediction_rq4.md                <- Appendix D — exploratory churn prediction
│   ├── exploratory_industry_classification.md <- §7 industry-classification pilot
│   └── hypothesis_id_legacy_mapping.md        <- figure-title / hypothesis-ID reconciliation
│
├── docs/
│   ├── METHODOLOGY_NOTES.md            <- estimator-selection derivation log, incl. SSI formalization
│   │                                       and mediation-audit reframing
│   ├── RESULTS_SUMMARY.md              <- canonical statistics table + alt-ID screening
│   └── DESIGN_ARTIFACT.md              <- redirect stub: the flagging-rule artifact was grounded in
│                                            the descoped longitudinal study; see FUTURE_RESEARCH_STUDY2.md
│
├── run_pipeline_v4.sh                  <- runs the v4 pipeline end-to-end
├── run_supplementary_robustness.sh     <- runs all supplementary_robustness/*.py scripts
└── run_supplementary_identification.sh <- runs the three supplementary_identification/*.py scripts
```

---

## 12. How to Reproduce

1. Request a schema-compatible data extract (`data/README.md` documents the expected schema;
   data are proprietary and not included in this repository).
2. `bash run_pipeline_v4.sh` — variance decomposition, advertiser-size mediation-audit battery,
   churn appendix.
3. `bash run_supplementary_robustness.sh` — the independently runnable robustness analyses.
4. `bash run_supplementary_identification.sh` — the RDD + policy-change supplementary robustness
   screening (Rounds 1–3); this reproduces the null result summarized in §4.5.9 and Figure 11.
5. Regenerate Figures 1–4, 7, 8 with `figures/make_figure*.py` (each reads a results JSON/CSV and
   writes a PNG to `figures/`).
6. Regenerate Figure 11 with `figures/make_figure11_identification_screening.py` — requires no
   external data, pulling static values directly from `docs/RESULTS_SUMMARY.md`.

Every pipeline step writes its own diagnostic JSON/CSV artifact; nothing is silently overwritten,
and each script can be re-run independently as long as its upstream artifact exists.

---

*This repository is maintained as a living analysis log. Numbers here are pulled directly from
execution logs and are not rounded beyond what's shown — adjust significant figures to
target-venue convention only at manuscript-preparation time. Theoretical framing in §2, the SSI
construct in §2.5, and the mediation-audit positioning in §5 are repository-level additions
intended to make the empirical tests legible as hypothesis tests against named literatures and
as a coherent, portable audit method; they do not alter any reported statistic.*

**References (to be expanded into full manuscript bibliography at write-up stage):**
- Arrow, K. J. (1973). The theory of discrimination. In *Discrimination in Labor Markets*.
- Barocas, S., & Selbst, A. D. (2016). Big data's disparate impact. *California Law Review*, 104(3).
- Corbett-Davies, S., & Goel, S. (2018). The measure and mismeasure of fairness. *arXiv:1808.00023*.
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R. (2012). Fairness through awareness. *ITCS*.
- Gillespie, T. (2014). The relevance of algorithms. In *Media Technologies*.
- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2017). Inherent trade-offs in the fair determination of risk scores. *ITCS*.
- Metaxa, D., Park, J. S., Robertson, R. E., Karahalios, K., Wilson, C., Hancock, J., & Sandvig, C. (2021). Auditing algorithms: Understanding algorithmic systems from the outside in. *Foundations and Trends in Human-Computer Interaction*, 14(4).
- Phelps, E. S. (1972). The statistical theory of racism and sexism. *American Economic Review*.
- Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020). Closing the AI accountability gap. *FAccT*.
- Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014). Auditing algorithms: Research methods for detecting discrimination on internet platforms. *ICA Preconference on Data and Discrimination*.
- Spence, M. (1973). Job market signaling. *Quarterly Journal of Economics*.
