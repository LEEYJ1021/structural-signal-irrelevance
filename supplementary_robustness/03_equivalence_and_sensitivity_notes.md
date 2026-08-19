# Equivalence Testing and Omitted-Variable Sensitivity

**Supports:** root README §3.2, §6

A non-significant p-value does not, by itself, establish that an effect is genuinely absent — it establishes that this sample could not distinguish the observed effect from zero at conventional confidence. Where a null result is central to this repository's argument, that distinction is made explicit rather than glossed over.

## 1. TOST equivalence tests

Two one-sided tests (TOST) assess whether an effect can be bounded within a pre-specified equivalence margin, rather than merely failing to reject a point-null.

### RQ1 (account maturity → initial growth slope, §3.2)

- **Equivalence margin:** ±0.20 standardized effect size (SESOI)
- **Observed standardized coefficient:** β = 0.085 (customer-level, n=29)
- **TOST result:** p = .197 — equivalence is **not established**

### RQ2 / H2b (does adding account maturity improve ad-group-level growth prediction?)

- **Equivalence margin:** ±0.05 Spearman ρ (SESOI)
- **Observed mean improvement:** Δρ = +0.023 across 100 group-shuffled splits
- **TOST result:** p = .290 — equivalence is **not established**

### How this is reported in the main text

Both results are reported in the root README as *non-significant, well-powered associations for which formal equivalence is inconclusive* — not as confirmed nulls. The pre-registered power simulations (root README §3.1, point 5; §7) establish that the samples are well-powered against *large* effects; the TOST results add the complementary information that the samples cannot rule out a small-to-moderate effect existing but falling below detection. Both statements are true simultaneously and are not in tension: "this sample would have detected a large effect and did not" and "this sample cannot formally confirm the complete absence of a small effect" describe the same evidence from two different, equally valid angles.

## 2. Oster's delta: omitted-variable-bias sensitivity for the bid_amount b-path

The bid_amount-based mediation result ([`01_alternative_outcome_mediation.md`](01_alternative_outcome_mediation.md)) is the primary replication for Study 1's efficiency finding. Oster's delta (Oster, 2019) quantifies how much stronger an unobserved confounder would need to be, relative to the observed controls, to fully explain away the spend → bid_amount coefficient.

| Quantity | Value |
|---|---|
| Restricted model (spend only): coefficient | +0.170 |
| Restricted model: R² | 0.0273 |
| Full model (spend + size): coefficient | +0.150 |
| Full model: R² | 0.0282 |
| R² increment from adding size | 0.0009 |
| Rmax (1.3 × R²_full, capped at 1.0) | 0.0367 |
| δ* (Oster's delta) | +71.4 |

**Why this number is not reported as evidence of robustness.** Oster's delta is defined with the R² increment from the additional control in its denominator. Here that increment is 0.0009 — effectively zero — which places the calculation in a numerically unstable region where δ* diverges regardless of the underlying relationship's true robustness. A large |δ*| driven by a near-zero denominator is not interpretable as "this result would survive a confounder 71 times stronger than the observed controls"; it is an artifact of `size_z` adding almost no explanatory power to this particular model. We therefore report δ* here for transparency but explicitly do not use it to support a robustness claim. The R² increment itself — size adding essentially no explanatory power to bid_amount beyond spend — is the more interpretable and more conservative takeaway, and is consistent with (not contrary to) the paper's central claim that size operates only through spend.

**Recommended minimum threshold.** Based on this experience, we treat Oster's delta as interpretable only when the R² increment from the additional control exceeds 0.01; below that, we report the R² increment itself rather than the derived δ* as the substantive sensitivity statistic.

## Reference

Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *Journal of Business & Economic Statistics*, 37(2), 187–204.
