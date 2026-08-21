# Appendix: Hypothesis-ID and Figure-Label Reconciliation

The figure files referenced throughout the root [`README.md`](../README.md) were generated
across multiple rounds of internal labeling ("RQ1," "RQ3," "H3," and so on) baked into
image titles and script variable names before the current hypothesis/research-question
scheme (H1a/b/c, H1, H2, RQ2a/RQ2b/RQ2c) was finalized. This table is the permanent
cross-reference, so any given figure or legacy label can be traced unambiguously to what
it currently means. A superseded label is never deleted or silently dropped — it remains
here with a pointer to what replaced it, so any revision to the naming stays auditable.

**Scope of this file.** This table maps legacy pipeline/script labels ("RQ1"–"RQ4," "H3")
to this repository's current H1/H2/RQ2a–c naming, per the repository structure note in the
root README (§14). It does **not** cover the separately-numbered RQ1–RQ3 scheme used
internally by the descoped longitudinal companion study ("Study 2") — see the note at the
bottom of this file for why those entries were removed.

| Current ID (root README) | Legacy label(s) in figure titles / script names | What it claims | Status |
|---|---|---|---|
| P0 (preliminary, §5.1) | Figure 1's embedded "(RQ1)" — an `Ad_Advance` v4 pipeline stage number, unrelated to this README's H1/H2/RQ2a–c scheme | Performance variance sits mostly at ad-group/residual level, not customer level | Descriptive; motivates but does not test H1 [CONFIRMATORY, preliminary] |
| H1a | — (no individually legacy-labeled figure title; reported within Figure 2's forest plot) | Size → total spend | Confirmed, p < .001 [CONFIRMATORY] |
| H1b | — | Spend → outcome, controlling for size | Confirmed, p = .032 (bid_amount-based, primary) [CONFIRMATORY] |
| H1c | — (reported across Figures 2, 3, 7; see §5.2–5.4) | Size → outcome, controlling for spend | Confirmed null; 8/8 robustness methods + core-model influence diagnostic (see `docs/METHODOLOGY_NOTES.md` entry A4) [CONFIRMATORY] |
| H1 (composite) | — | Indirect association accounts for the entire size–outcome relationship | Supported [CONFIRMATORY] |
| H2 | Figure 8's embedded "(joint Wald test)" | H1c's null is homogeneous across `campaign_type` strata | Rejected, p = .023 (heterogeneous); this is the pre-specified result that motivated RQ2a–RQ2c [CONFIRMATORY] |
| RQ2a | Internal script naming under the retracted single-"H3" scheme; see B7 below | Where does H2's heterogeneity concentrate? (continuous-share re-specification) | Post-hoc; local business is the only term with majority (3/5) robustness-method agreement [POST-HOC / EXPLORATORY] |
| RQ2b | Internal script naming under the retracted single-"H3" scheme; see B7 below | Why might local business differ? (serving-structure / mechanism comparison, Figure 13) | Post-hoc, mixed; 3/4 mechanism-chain statistical signatures detected [POST-HOC / EXPLORATORY] |
| RQ2c | Figure 12's legend text "H3"; Figure 14's legend text "H3"; the script function name `h3_leave_one_out` in `localbiz_core_analysis.py` | Does H1c's null depend on local-business inclusion, beyond sample-size effects alone? | Post-hoc, partially supported on the *corrected* leave-one-type-out comparison only; the initial, uncorrected pass did not support it (see `docs/METHODOLOGY_NOTES.md` entries B6, B7) [POST-HOC / EXPLORATORY] |
| RQ4 | Figure 4's legacy "(RQ3, exploratory appendix)" label; `step3_churn_appendix_v4.py` | Can churn be predicted from approval/cost/efficiency features? | Exploratory, moved to [`appendix/churn_prediction_rq4.md`](churn_prediction_rq4.md), outside the H1 family |
| P5 (boundary condition, §3.3) | Derived post-hoc from RQ2b's Figure 13 findings; no legacy figure label of its own | SSI's audit design presupposes an auction/bidding serving mechanism; where this premise does not hold (local-business campaigns), the SSI test may fall outside its own scope rather than being violated | Post-hoc candidate proposition, not established; pending a preregistered confirmatory test in `FUTURE_RESEARCH_STUDY3.md` [POST-HOC / EXPLORATORY] |

**A note on the retracted "H3" label (see `docs/METHODOLOGY_NOTES.md`, entry B7).** Earlier
drafts numbered the entire post-hoc investigation into H2's heterogeneity as a single
"H3." That label has been retracted: numbering a post-hoc question alongside pre-specified
"H1" and "H2" risked implying it had been set out in advance. The investigation is now
three explicitly-named research questions — RQ2a (where), RQ2b (why), RQ2c (does it matter
for H1) — each with its own evidentiary bar. No underlying statistic changed; every number
previously reported under "H3" is reported identically today, split across RQ2a/RQ2b/RQ2c
depending on which question it answers. The old "H3" text still surfaces in two places that
were not worth regenerating purely for a label change: Figure 12's and Figure 14's embedded
legends, and the `h3_leave_one_out` function name inside `localbiz_core_analysis.py`. Both
are cosmetic remnants — see this table's RQ2c row for the mapping.

**A note on a dropped label.** An earlier internal draft also carried a formal ID "RQ3" for
a piloted advertiser-industry stratification. That check was dropped from the confirmatory
hypothesis family entirely due to unusable label reliability (see
[`exploratory_industry_classification.md`](exploratory_industry_classification.md)) and does
not appear in the table above. This dropped "RQ3" is unrelated to **both** of the two other
"RQ3"s that appear elsewhere in this repository's artifacts: (a) Figure 4's legacy
"RQ3" pipeline-title text, which this table's RQ4 row clarifies is really the churn
appendix; and (b) the descoped Study 2 companion's own internal "RQ3" (intervention-timing
simulation), which belongs to a different numbering scheme entirely (see the note below).

**A note on removed entries (Study 2 scope).** Earlier versions of this table also carried
entries §7.1-Maturity, §7.2-EarlySignal, §7.2-MaturityAdd, and §7.2-Flagging, mapped from
Figures 5 and 6's legacy "RQ1"/"RQ2"/"H2a"/"H2b"/"RQ3" titles. **Those entries have been
removed from this table.** Figures 5, 6, 9, and 10 belong to the descoped longitudinal
companion study ("Study 2" — account maturity vs. a new ad group's early growth
trajectory, n=29 customers), which is explicitly out of scope for this repository's
evidence base (root README, Appendix B and §11 Limitation 10). Study 2 uses its own
separate RQ1–RQ3 numbering, unrelated to this document's H1/H2/RQ2a–c scheme. The design
artifact once built on that study (`docs/DESIGN_ARTIFACT.md`) is now a redirect stub
pointing to `FUTURE_RESEARCH_STUDY2.md`. Any legacy-label mapping for Study 2's own figures
belongs in `FUTURE_RESEARCH_STUDY2.md`, not in this file.

**A note on a removed section ID.** Earlier versions of this table also carried an entry
"§9.1-review" (discretionary review leaking account attributes into outcomes). That
section number no longer exists in the current README. Its substance survives as
**proposition P3** in the SSI boundary-condition framework (root README §3.3:
"discretionary review re-entry — sub-processes with human discretionary review are
SSI-violation candidates even within an otherwise SSI-consistent system"), which this
table now lists in place of the old section reference.

**Naming convention.** `Hx` = a formally testable, pre-specified hypothesis with a
directional or point-null prediction (H1a, H1b, H1c, H1, H2). `RQ2x` = a post-hoc,
non-preregistered research question formulated after H2's result was observed (RQ2a,
RQ2b, RQ2c); the word "hypothesis" is deliberately reserved for the Hx family. `P0` = a
preliminary/descriptive analysis that motivates a hypothesis but does not itself test one.
`Px` (P1–P5) = a boundary condition on the SSI construct, not itself a tested claim; P1–P4
were derived pre-data-collection, P5 is post-hoc (derived from RQ2b's findings).
