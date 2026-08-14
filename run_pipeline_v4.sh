#!/usr/bin/env bash
# Runs the earlier-generation v4 pipeline end-to-end: data prep and
# spike-account detection, variance decomposition, advertiser-size
# fairness suite (multiverse + placebo), churn-prediction appendix,
# and synthesis into outputs/_v4_synthesis/summary.json.
#
# Independent of run_diagnostics.sh / src/analysis/ -- only shares the
# spike_account_ids.json artifact and config.yaml.
#
# Usage: bash run_pipeline_v4.sh [path/to/config.yaml]

set -euo pipefail

CONFIG="${1:-config/config.yaml}"

echo "=== pipeline_v4 (config: ${CONFIG}) ==="

STEPS=(
  "src.pipeline_v4.step0_data_prep_v4"
  "src.pipeline_v4.step1_variance_decomposition_v4"
  "src.pipeline_v4.step2_advertiser_size_fairness_v4"
  "src.pipeline_v4.step3_churn_appendix_v4"
  "src.pipeline_v4.step4_synthesis_v4"
)

for step in "${STEPS[@]}"; do
  echo ""
  echo "--- running ${step} ---"
  python -m "${step}" --config "${CONFIG}"
done

echo ""
echo "=== pipeline_v4 complete -- see outputs/_v4_synthesis/summary.json ==="
