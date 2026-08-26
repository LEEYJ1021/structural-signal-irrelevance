# ============================================================
# rq3_confirm_v2_robust_summary_postprocess.py
#
#   [POST-HOC ON POST-HOC / TERTIARY, RQ3 -> M5 numerical-stability
#   diagnostic] root README §16.3.1, docs/METHODOLOGY_NOTES.md entry B11
#   참조.
#
#   목적: rq3_confirm_v2_patch_ols_stratified.py가 만든
#   rq3_confirm_v2_bootstrap_raw_patched.csv를 읽어, 각 (strategy, model)
#   조합·각 지표(ΔRMSE, Δsize_gap, Δlocalbiz_gap)에 대해
#     - 평균 기반 95% percentile CI (기존 M2/M3 보고 방식)
#     - median + IQR(25/75%ile) 강건 통계
#   를 나란히 계산하고, 우측 꼬리가 비대칭으로 불안정한 조합을 자동으로
#   플래그한다.
#
#   불안정 판정 규칙 (사전 고정, 결과를 보고 바꾸지 않음):
#     우측 꼬리 길이 = CI_hi - median
#     좌측 꼬리 길이 = median - CI_lo
#     tail_ratio = 우측 꼬리 길이 / max(좌측 꼬리 길이, EPS)
#     tail_ratio > TAIL_RATIO_THRESHOLD(=3.0) 이면 *_right_tail_unstable = True
#
#   플래그된 조합은 README/RESULTS_SUMMARY 본문 및 Figure 19에서 평균 기반
#   CI 대신 median [IQR]으로 보고한다 (entry B11) — 이는 M2/M3의 원래 보고
#   관행과 다르다는 점을 disclosure로 남긴다.
#
#   이 스크립트는 모델을 다시 학습하지 않는다 — 이미 계산된 CSV만 읽는다.
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

AD_DATA_DIR = Path("/home/yjlee/Research/Ad_Advance/AD_Data")
OUT_DIR = AD_DATA_DIR.parent

RAW_PATCHED_PATH = OUT_DIR / "rq3_confirm_v2_bootstrap_raw_patched.csv"
ROBUST_SUMMARY_PATH = OUT_DIR / "rq3_confirm_v2_robust_summary.csv"

TAIL_RATIO_THRESHOLD = 3.0
EPS = 1e-9

METRICS = [
    ("rmse_overall_diff", "rmse_overall"),
    ("size_gap_diff", "size_gap"),
    ("localbiz_gap_diff", "localbiz_gap"),
]

if not RAW_PATCHED_PATH.exists():
    raise FileNotFoundError(
        f"{RAW_PATCHED_PATH} 가 없습니다. 먼저 rq3_confirm_v2_patch_ols_stratified.py를 "
        "실행해 병합된 raw를 만들어야 합니다."
    )

raw = pd.read_csv(RAW_PATCHED_PATH)

rows = []
for (strategy, model), g in raw.groupby(["strategy", "model"]):
    row = {"strategy": strategy, "model": model}
    for col, prefix in METRICS:
        vals = g[col].dropna().values
        if len(vals) == 0:
            continue

        mean_val = np.mean(vals)
        ci_lo, ci_hi = np.percentile(vals, [2.5, 97.5])
        median_val = np.median(vals)
        iqr_lo, iqr_hi = np.percentile(vals, [25, 75])

        right_tail = ci_hi - median_val
        left_tail = median_val - ci_lo
        tail_ratio = right_tail / max(left_tail, EPS)
        is_unstable = bool(tail_ratio > TAIL_RATIO_THRESHOLD)

        # median 기준 방향성 판정 (IQR이 전부 한쪽 부호일 때만 "방향이 있다"고 봄)
        if iqr_lo > 0:
            median_direction = "worsened"       # 값이 클수록 악화(diff 정의상 양수=악화)
        elif iqr_hi < 0:
            median_direction = "improved"
        else:
            median_direction = "inconclusive"   # IQR이 0을 포함

        row[f"{prefix}_mean"] = mean_val
        row[f"{prefix}_ci_lo"] = ci_lo
        row[f"{prefix}_ci_hi"] = ci_hi
        row[f"{prefix}_median"] = median_val
        row[f"{prefix}_iqr_lo"] = iqr_lo
        row[f"{prefix}_iqr_hi"] = iqr_hi
        row[f"{prefix}_tail_ratio"] = tail_ratio
        row[f"{prefix}_right_tail_unstable"] = is_unstable
        row[f"{prefix}_median_direction"] = median_direction

    rows.append(row)

summary_df = pd.DataFrame(rows)
model_order = {"OLS": 0, "HistGB": 1, "RandomForest": 2, "SVR_rbf": 3}
summary_df["_order"] = summary_df["model"].map(model_order)
summary_df = summary_df.sort_values(["strategy", "_order"]).drop(columns="_order")

summary_df.to_csv(ROBUST_SUMMARY_PATH, index=False, encoding="utf-8-sig")

print("=" * 90)
print("Robust summary (mean/CI vs median/IQR, tail-instability flag)")
print("=" * 90)
display_cols = ["strategy", "model"]
for _, prefix in METRICS:
    display_cols += [f"{prefix}_tail_ratio", f"{prefix}_right_tail_unstable", f"{prefix}_median_direction"]
print(summary_df[display_cols].to_string(index=False))

n_unstable = sum(
    summary_df[f"{prefix}_right_tail_unstable"].sum() for _, prefix in METRICS
)
print(f"\n총 {n_unstable}개 (조합 x 지표) 셀에서 우측 꼬리 불안정 플래그 발생"
      f"(tail_ratio > {TAIL_RATIO_THRESHOLD}).")
print(f"저장 완료: {ROBUST_SUMMARY_PATH}")
print("\n[해석 지침] *_right_tail_unstable=True인 셀은 README/RESULTS_SUMMARY 및")
print("            Figure 19에서 평균 기반 95% CI 대신 median [IQR]로 보고할 것")
print("            (entry B11). 나머지 셀은 기존처럼 mean/95% CI로 보고.")
