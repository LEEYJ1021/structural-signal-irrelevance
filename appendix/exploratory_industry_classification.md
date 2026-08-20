# Appendix: Exploratory Industry-Classification Pipeline

**Status: exploratory. Not used as evidence for any claim in the root [`README.md`](../README.md).** This pipeline is retained for transparency and as a candidate direction for future work with a higher-reliability label source — see root README §9.2 for the two-sentence summary that is safe to cite.

---

## 1. Why this was attempted

`campaign_type` (used in root README §5.5 / §9.1) is a platform-defined **ad-product code** (website / shopping / brand-new-product / local-business), not an industry classification. No industry field exists natively in the platform's schema (`data/README.md` documents this explicitly: "category name (industry, top-level) — not included — not a platform API field → requires a manually constructed mapping per account"). An attempt was made to construct an industry proxy from free-text campaign and ad-group names, as a third boundary-condition candidate alongside `campaign_type` and keyword review status.

Two non-text candidate columns were ruled out first:
- `campaign_type`: confirmed, from the platform's own documentation, to be a product-code field, not an industry field.
- `business_channel_id`: a per-account channel identifier (median 2 per customer, max 26) corresponding to individual websites/stores/blogs an advertiser operates — a business-unit identifier, not an industry taxonomy.

Free-text `campaign_name` / `ad_group_name` fields do contain clear industry signal on manual inspection (e.g., dental clinics, dermatology, real estate brokers, travel agencies), motivating a text-based classification pipeline.

## 2. Pipeline

| Stage | Method |
|---|---|
| Text source | `campaign_name` + `ad_group_name` (9,390 unique strings, 263 customers) |
| Embedding | `intfloat/multilingual-e5-large`, `passage:` prefix per model convention |
| Dimensionality reduction | UMAP (10 components, 15 neighbors, cosine metric) |
| Clustering | HDBSCAN (min cluster size 12, min samples 5) + soft-clustering reassignment of noise points to reach ≥50% coverage |
| Cluster labeling | 4 local LLMs (qwen2.5:14b, llama3.1:8b, mistral:7b-instruct, qwen2.5:7b-instruct) × 3 repeats = 12 votes per cluster, each forced to select one of the 21 Korean Standard Industrial Classification (KSIC) top-level categories or "unclassifiable" |
| Representative terms | c-TF-IDF (cluster-as-document) with a within-cluster minimum document-frequency filter (≥15%), to prevent a single outlier document from dominating a cluster's representative terms |
| Consensus | Majority vote per cluster (≥34% plurality threshold); customer-level label = plurality of that customer's cluster labels |

## 3. Results

- **Clustering:** 227 clusters from 9,390 unique text strings; 78% final coverage after noise reassignment (22% initial HDBSCAN noise rate).
- **LLM labeling:** 2,724 total LLM calls; 0.4% parse failures.
- **Inter-rater reliability:** because the number of valid votes per cluster varies (due to occasional parse failures), standard Fleiss' kappa is not well-defined across the full cluster set. Randolph's free-marginal multirater kappa (Randolph, 2005), which tolerates a variable number of raters per subject, was used as the primary reliability statistic: **κ = 0.557** (227 clusters) — conventionally "moderate" agreement. As a secondary check restricted to the 220 clusters with all 12 votes valid, standard Fleiss' kappa gives **κ = 0.497**, consistent with the primary estimate.
- **21 KSIC categories → 6 supergroups** (to secure adequate stratum sizes): RETAIL_LOGISTICS (n=92 customers), REALESTATE_PROF (n=66), IT_COMM (n=34), MANUF_CONSTRUCTION (n=32), HEALTHCARE (n=17), OTHER_SMALL (n=10, categories below the n=15 stratification floor merged in).
- **Cross-validation against an independent method:** a keyword-rule-based classifier (built independently of the embedding/LLM pipeline, using hand-specified Korean industry keyword lists) was run on the same customers. Comparable-customer agreement: 50.0% simple agreement, **Cohen's κ = 0.363** (n = 128 customers with a non-"unclassifiable" label from both methods) — "fair" agreement by conventional benchmarks, below the threshold at which a label would typically be trusted for a confirmatory stratified test.

## 4. Why this is not used as a confirmatory result

Both reliability statistics (Randolph's κ = 0.557 across the LLM ensemble; Cohen's κ = 0.363 against an independent rule-based method) fall in the "moderate-at-best" range. Given this, any industry-stratified finding built on these labels would be a statement about label noise as much as about the underlying phenomenon, and is not reported as evidence for or against any hypothesis in the root README.

## 5. A directional observation, reported without confirmatory weight

Under this low-reliability labeling, the MANUF_CONSTRUCTION supergroup (n = 27 customers) showed a significant negative direct effect of size, net of spend, on the CPC-based outcome (c′ = −0.728, p < .001), stable in direction across split-half resampling (91% sign agreement across 200 replications, 95% range [−1.665, +0.210]). This is noted here **for transparency only** — it is not reported as a finding in the root README, given the label-reliability ceiling documented in §3 above. A higher-reliability industry classification (e.g., a validated commercial industry-tagging service, or a larger human-annotated gold-standard sample for supervised fine-tuning) would be required before this observation could be treated as evidence.

## 6. Reference

Randolph, J. J. (2005). Free-marginal multirater kappa: An alternative to Fleiss' fixed-marginal multirater kappa. *Joensuu Learning and Instruction Symposium.*
