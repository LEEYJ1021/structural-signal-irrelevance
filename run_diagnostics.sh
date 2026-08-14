#!/usr/bin/env bash
# Runs the coldstart_v5 diagnostic pipeline (Steps A-M) in order.
# Each step is independently re-runnable as long as its upstream
# artifact exists; running them in this order from a clean outputs/
# directory reproduces the full diagnostic evidence base that the
# confirmatory design in src/analysis/ relies on.
#
# Usage: bash run_diagnostics.sh [path/to/config.yaml]

set -euo pipefail

CONFIG="${1:-config/config.yaml}"

echo "=== coldstart_v5 diagnostic pipeline (config: ${CONFIG}) ==="

STEPS=(
  "src.coldstart_v5.step_a_period_and_spike_check"
  "src.coldstart_v5.step_b_true_coldstart_sample"
  "src.coldstart_v5.step_c_right_censoring_flags"
  "src.coldstart_v5.step_d_customer_clustering_density"
  "src.coldstart_v5.step_e_class_count_identifiability_sim"
  "src.coldstart_v5.step_f_registration_cutoff_sensitivity"
  "src.coldstart_v5.step_g_fixed_window_coverage"
  "src.coldstart_v5.step_h_top_customer_profiling"
  "src.coldstart_v5.step_i_account_maturity_distribution"
  "src.coldstart_v5.step_j_regtm_artifact_check"
  "src.coldstart_v5.step_k_power_simulation"
  "src.coldstart_v5.step_l_rq2_feature_engineering"
  "src.coldstart_v5.step_m_intervention_timing_simulation"
)

for step in "${STEPS[@]}"; do
  echo ""
  echo "--- running ${step} ---"
  python -m "${step}" --config "${CONFIG}"
done

echo ""
echo "=== diagnostic pipeline complete -- see outputs/coldstart_v5/ ==="
