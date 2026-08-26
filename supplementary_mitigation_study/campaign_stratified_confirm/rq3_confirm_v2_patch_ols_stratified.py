# ============================================================
# rq3_confirm_v2_patch_ols_stratified.py
#
#   [POST-HOC ON POST-HOC / TERTIARY, RQ3 -> M4/M5 numerical-stability patch]
#   root README §16.3.1, docs/METHODOLOGY_NOTES.md entry B11 참조.
#
#   목적: rq3_confirm_v2_campaign_stratified_full.py 실행 결과(raw)에서
#   OLS x {S9_Campaign_stratified, S9_plus_S1} 두 조합만 CI 상단이
#   비정상적으로 넓게(14~25) 나오는 문제를 해결한다.
#
#   원인 추정: local-business 서브그룹만 따로 떼어 학습할 때, 그 안에서는
#   share_2(쇼핑)·share_3(파워컨텐츠) 같은 열이 거의 0에 가깝게 상수화되어
#   있을 가능성이 높다(정의상 local-biz 비중이 큰 고객은 다른 유형 비중이
#   작으므로). 분산이 거의 없는 열이 있으면 OLS 설계행렬이 거의
#   특이(near-singular)해지고, 부트스트랩·fold를 반복하다 보면 가끔 계수가
#   폭발해서 극단적인 예측값이 나온다. RandomForest/HistGB/SVR은 정규화나
#   트리 분할 특성상 이런 폭발이 잘 안 생기므로 이 둘(순수 OLS x
#   stratified)에서만 나타난다.
#
#   해결: 각 fold에서 "학습 데이터 기준" 분산이 거의 0인 열을 train/test
#   양쪽에서 함께 제거한 뒤 학습한다. 어떤 열이 몇 번, 어느 맥락에서
#   제거됐는지 로그로 남겨 조용히 넘어가지 않게 한다.
#
#   재현성: 원본 스크립트와 동일한 rng 시퀀스를 유지하기 위해
#   rng = RandomState(42)를 만들고 b=0..199를 "순서대로" rng.choice(...)를
#   호출한다(중간을 건너뛰면 이후 시드가 어긋난다). 실제 모델 학습은
#   OLS 두 조합에 대해서만 수행하므로, RandomForest/SVR을 다시 돌리는
#   전체 재실행보다 훨씬 빠르다.
#
#   전제조건: rq3_confirm_v2_campaign_stratified_full.py를 먼저 1회
#   실행해 rq3_confirm_v2_bootstrap_raw.csv가 이미 존재해야 한다.
# ============================================================

import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore")
pd.set_option("display.width", 200)

# ---------------------------------------------------------------
# CONFIG (원본 스크립트와 완전히 동일하게 맞춰주세요)
# ---------------------------------------------------------------
AD_DATA_DIR = Path("/home/yjlee/Research/Ad_Advance/AD_Data")
ADGROUP_DIM_PATH = AD_DATA_DIR / "adgroup_dim_20260722.tsv"
PERF_PANEL_PATH  = AD_DATA_DIR / "ad_performance_17col_20260722.tsv"
CAMPAIGN_DIM_PATH = AD_DATA_DIR / "campaign_dim_20260722.tsv"
OUT_DIR = AD_DATA_DIR.parent

ORIGINAL_RAW_PATH   = OUT_DIR / "rq3_confirm_v2_bootstrap_raw.csv"       # 1단계 결과
PATCHED_RAW_PATH     = OUT_DIR / "rq3_confirm_v2_bootstrap_raw_patched.csv"
PATCHED_VERDICT_PATH = OUT_DIR / "rq3_confirm_v2_verdict_patched.csv"
DROPPED_COL_LOG_PATH = OUT_DIR / "rq3_confirm_v2_dropped_columns_log_patch.csv"

RANDOM_STATE = 42
LOCALBIZ_TYPE = 6
MIN_CLICKS_FOR_CPC = 1
MIN_GROUP_N_FOR_GAP = 10
MIN_GROUP_N_FOR_STRAT = 15
TARGET_COL = "log_cpc"
N_BOOT = 200            # 원본과 동일해야 rng 시퀀스가 맞음 -- 바꾸지 말 것
N_INNER_FOLDS = 5
NEAR_CONSTANT_VAR_THRESHOLD = 1e-8
RMSE_NEUTRAL_THRESHOLD = 0.02

# 재계산 대상: 이 2개 (strategy, model) 조합만 다시 계산한다.
PATCH_TARGETS = [
    ("S9_Campaign_stratified", "OLS"),
    ("S9_plus_S1", "OLS"),
]


def smart_read_table(path):
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(path, sep=sep, low_memory=False)


def find_column(df_, keywords):
    lower_map = {c.lower(): c for c in df_.columns}
    for kw in keywords:
        for lower_name, orig_name in lower_map.items():
            if kw in lower_name:
                return orig_name
    return None


def clean_id(series):
    return series.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


def to_naive(series):
    if isinstance(series.dtype, pd.DatetimeTZDtype):
        return series.dt.tz_localize(None)
    return series


# =====================================================================
# STEP 1-3. 패널 재구성 (원본과 완전히 동일)
# =====================================================================
print("=" * 74); print("STEP 1-3. 패널 재구성 (기존 정의와 동일)"); print("=" * 74)

adgroup_dim_raw = smart_read_table(ADGROUP_DIM_PATH)
panel_sep = "\t" if PERF_PANEL_PATH.suffix.lower() == ".tsv" else ","
panel_header = pd.read_csv(PERF_PANEL_PATH, sep=panel_sep, nrows=5, low_memory=False)

cust_col_adg     = find_column(adgroup_dim_raw, ["customer_id", "cust_id", "customer"])
adgid_col_adg    = find_column(adgroup_dim_raw, ["ad_group_id", "adgroup_id", "ad_group"])
campaign_col_adg = find_column(adgroup_dim_raw, ["campaign_id"])

date_col        = find_column(panel_header, ["date", "dt", "day"])
cust_col_panel  = find_column(panel_header, ["customer_id", "cust_id", "customer"])
adgid_col_panel = find_column(panel_header, ["ad_group_id", "adgroup_id", "ad_group"])
click_col       = find_column(panel_header, ["click"])
cost_col        = find_column(panel_header, ["cost"])

adgroup_dim = adgroup_dim_raw.rename(columns={cust_col_adg: "customer_id"})
adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
if adgid_col_adg:
    adgroup_dim = adgroup_dim.rename(columns={adgid_col_adg: "ad_group_id"})
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])
if campaign_col_adg:
    adgroup_dim = adgroup_dim.rename(columns={campaign_col_adg: "campaign_id"})
    adgroup_dim["campaign_id"] = clean_id(adgroup_dim["campaign_id"])

usecols_panel = [c for c in [date_col, cust_col_panel, adgid_col_panel, click_col, cost_col] if c]
panel = pd.read_csv(PERF_PANEL_PATH, sep=panel_sep, low_memory=False,
                     usecols=usecols_panel,
                     dtype={cust_col_panel: str, **({adgid_col_panel: str} if adgid_col_panel else {})})
rename_map = {date_col: "date", cust_col_panel: "customer_id", click_col: "click", cost_col: "cost"}
if adgid_col_panel:
    rename_map[adgid_col_panel] = "ad_group_id"
panel = panel.rename(columns=rename_map)
panel["date"] = to_naive(pd.to_datetime(panel["date"], errors="coerce")).dt.normalize()
panel["customer_id"] = clean_id(panel["customer_id"])
if "ad_group_id" in panel.columns:
    panel["ad_group_id"] = clean_id(panel["ad_group_id"])
panel["click"] = pd.to_numeric(panel["click"], errors="coerce").fillna(0)
panel["cost"]  = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
panel = panel.dropna(subset=["date"])

cust_day = panel.groupby(["customer_id", "date"], as_index=False).agg(
    click=("click", "sum"), cost=("cost", "sum"))

alltime_adgroup_count = adgroup_dim.groupby("customer_id").size().rename("all_time_ad_group_count")
size_df = alltime_adgroup_count.to_frame().reset_index()
size_df["log_size"] = np.log1p(size_df["all_time_ad_group_count"])
size_df["size_z"]   = (size_df["log_size"] - size_df["log_size"].mean()) / size_df["log_size"].std()
cust_day = cust_day.merge(size_df[["customer_id", "size_z"]], on="customer_id", how="inner")

cust_day["log_spend"] = np.log1p(cust_day["cost"])
cust_day["spend_z"]   = (cust_day["log_spend"] - cust_day["log_spend"].mean()) / cust_day["log_spend"].std()

cpc_sample = cust_day[cust_day["click"] >= MIN_CLICKS_FOR_CPC].copy()
cpc_sample["cpc"] = cpc_sample["cost"] / cpc_sample["click"]
cpc_sample = cpc_sample[cpc_sample["cpc"] > 0].copy()
cpc_sample["log_cpc"] = np.log(cpc_sample["cpc"])

campaign_dim = smart_read_table(CAMPAIGN_DIM_PATH)
camp_id_col   = find_column(campaign_dim, ["campaign_id"])
camp_type_col = find_column(campaign_dim, ["campaign_type", "camp_type"])
campaign_dim = campaign_dim.rename(columns={camp_id_col: "campaign_id", camp_type_col: "campaign_type"})
campaign_dim["campaign_id"] = clean_id(campaign_dim["campaign_id"])

adg_to_campaign = adgroup_dim[["ad_group_id", "campaign_id", "customer_id"]].dropna(subset=["campaign_id"])
adg_to_campaign = adg_to_campaign.merge(campaign_dim[["campaign_id", "campaign_type"]],
                                          on="campaign_id", how="left")

adg_cost = panel.groupby(["ad_group_id", "customer_id"], as_index=False)["cost"].sum()
adg_cost = adg_cost.merge(adg_to_campaign[["ad_group_id", "campaign_type"]], on="ad_group_id", how="left")
adg_cost = adg_cost.dropna(subset=["campaign_type"])
adg_cost["campaign_type"] = adg_cost["campaign_type"].astype(int)

detected_types = sorted(adg_cost["campaign_type"].unique())
cust_type_cost = adg_cost.groupby(["customer_id", "campaign_type"])["cost"].sum().reset_index()
pivot_cost = cust_type_cost.pivot(index="customer_id", columns="campaign_type", values="cost").fillna(0.0)
total_cost_row = pivot_cost.sum(axis=1)
valid_mask = total_cost_row > 0
pivot_cost = pivot_cost.loc[valid_mask]
total_cost_row = total_cost_row.loc[valid_mask]

share_cols = []
for t in detected_types:
    if t not in pivot_cost.columns:
        pivot_cost[t] = 0.0
    col_name = f"share_{t}"
    pivot_cost[col_name] = pivot_cost[t] / total_cost_row
    share_cols.append(col_name)

composition = pivot_cost[share_cols].reset_index()
localbiz_share_col = f"share_{LOCALBIZ_TYPE}"

panel_final = cpc_sample.merge(composition, on="customer_id", how="inner")
size_lookup = panel_final[["customer_id", "size_z"]].drop_duplicates("customer_id")
size_lookup["size_tercile"] = pd.qcut(size_lookup["size_z"], 3, labels=["소형", "중형", "대형"])
panel_final = panel_final.merge(size_lookup[["customer_id", "size_tercile"]], on="customer_id", how="left")

non_ref_share_cols = [c for c in share_cols if c != "share_1"]
df = panel_final.copy()
for c in non_ref_share_cols:
    if c not in df.columns:
        df[c] = 0.0

df["is_localbiz_primary"] = (df[localbiz_share_col] > 0.0).astype(int)
print(f"[1-3] 최종 패널: {len(df):,}행, 고객 {df['customer_id'].nunique()}명")

# =====================================================================
# STEP 4. 전략/모델 정의 -- OLS, 두 stratified 전략만 필요
# =====================================================================
_FEATURE_SETS = {
    "S0_Baseline": ["size_z", "spend_z"] + non_ref_share_cols,
}
STRATIFIED_STRATEGIES = {
    "S9_Campaign_stratified": ["size_z", "spend_z"] + non_ref_share_cols,
    "S9_plus_S1":             ["spend_z"] + non_ref_share_cols,
}


def _ols_pipeline():
    return Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])


def _make_fold_assignment(customer_ids_array, n_splits, seed):
    rng_local = np.random.RandomState(seed)
    unique_ids = np.unique(customer_ids_array)
    shuffled = unique_ids.copy()
    rng_local.shuffle(shuffled)
    folds = np.array_split(shuffled, n_splits)
    fold_id = np.full(len(customer_ids_array), -1)
    for k, test_ids in enumerate(folds):
        fold_id[np.isin(customer_ids_array, test_ids)] = k
    return fold_id


_dropped_col_log = []


def _drop_near_constant_columns(X_train, X_test, context_label):
    """학습 데이터 기준 분산이 거의 0인 열을 train/test 양쪽에서 함께
    제거한다. 어떤 맥락(전략|모델|그룹)에서 어떤 열이 빠졌는지 로그로
    남긴다 -- 조용히 넘어가지 않기 위함."""
    variances = X_train.var(axis=0)
    keep_cols = variances[variances > NEAR_CONSTANT_VAR_THRESHOLD].index.tolist()
    dropped = [c for c in X_train.columns if c not in keep_cols]
    if dropped:
        _dropped_col_log.append((context_label, tuple(dropped)))
    if not keep_cols:
        return X_train, X_test
    return X_train[keep_cols], X_test[keep_cols]


def _compute_metrics(y_true, y_pred, size_tercile, share6, min_n=MIN_GROUP_N_FOR_GAP):
    out = {"rmse_overall": np.sqrt(mean_squared_error(y_true, y_pred))}
    mask_l, mask_s = (size_tercile == "대형"), (size_tercile == "소형")
    if mask_l.sum() >= min_n and mask_s.sum() >= min_n:
        out["rmse_gap_size"] = abs(
            np.sqrt(mean_squared_error(y_true[mask_l], y_pred[mask_l])) -
            np.sqrt(mean_squared_error(y_true[mask_s], y_pred[mask_s])))
    else:
        out["rmse_gap_size"] = np.nan
    mask = share6 > 0
    other = ~mask
    if mask.sum() >= min_n and other.sum() >= min_n:
        rmse_in = np.sqrt(mean_squared_error(y_true[mask], y_pred[mask]))
        rmse_out = np.sqrt(mean_squared_error(y_true[other], y_pred[other]))
        out["rmse_gap_localbiz"] = abs(rmse_in - rmse_out)
    else:
        out["rmse_gap_localbiz"] = np.nan
    return out


def _fit_predict_baseline_ols(data, seed):
    """S0_Baseline x OLS: pooled 5-fold OOF (근-상수 문제 없음, 안전장치는
    형식적으로만 적용)."""
    X = data[_FEATURE_SETS["S0_Baseline"]].copy()
    y = data[TARGET_COL].values
    cust_ids = data["customer_id"].values
    fold_id = _make_fold_assignment(cust_ids, N_INNER_FOLDS, seed)
    pred = np.full(len(y), np.nan)
    for k in range(N_INNER_FOLDS):
        test_mask = fold_id == k
        train_idx = np.where(~test_mask)[0]
        test_idx = np.where(test_mask)[0]
        if len(test_idx) == 0 or len(train_idx) == 0:
            continue
        X_train, X_test = _drop_near_constant_columns(
            X.iloc[train_idx], X.iloc[test_idx], "S0_Baseline|OLS|pooled")
        pipe = _ols_pipeline()
        pipe.fit(X_train, y[train_idx])
        pred[test_idx] = pipe.predict(X_test)
    return _compute_metrics(y, pred, data["size_tercile"].values, data[localbiz_share_col].values)


def _fit_predict_stratified_ols(strategy, data, seed):
    """S9_Campaign_stratified / S9_plus_S1 x OLS: 그룹별 5-fold OOF +
    근-상수 열 제거."""
    feats = STRATIFIED_STRATEGIES[strategy]
    y_full = data[TARGET_COL].values
    cust_ids = data["customer_id"].values
    pred_full = np.full(len(data), np.nan)
    mask_arr = data["is_localbiz_primary"].values.astype(bool)

    for grp_val in (0, 1):
        grp_idx = np.where(mask_arr == bool(grp_val))[0]
        grp_n_customers = len(np.unique(cust_ids[grp_idx]))

        if len(grp_idx) < MIN_GROUP_N_FOR_STRAT or grp_n_customers < N_INNER_FOLDS:
            X_all = data[feats]
            other_idx = np.where(~np.isin(np.arange(len(data)), grp_idx))[0]
            if len(other_idx) == 0:
                continue
            X_train, X_test = _drop_near_constant_columns(
                X_all.iloc[other_idx], X_all.iloc[grp_idx], f"{strategy}|OLS|fallback_grp{grp_val}")
            pipe = _ols_pipeline()
            pipe.fit(X_train, y_full[other_idx])
            pred_full[grp_idx] = pipe.predict(X_test)
            continue

        X_grp = data.iloc[grp_idx][feats].reset_index(drop=True)
        y_grp = y_full[grp_idx]
        cust_grp = cust_ids[grp_idx]
        fold_id = _make_fold_assignment(cust_grp, N_INNER_FOLDS, seed)

        for k in range(N_INNER_FOLDS):
            test_mask = fold_id == k
            train_idx = np.where(~test_mask)[0]
            test_idx = np.where(test_mask)[0]
            if len(test_idx) == 0 or len(train_idx) == 0:
                continue
            X_train, X_test = _drop_near_constant_columns(
                X_grp.iloc[train_idx], X_grp.iloc[test_idx], f"{strategy}|OLS|grp{grp_val}")
            pipe = _ols_pipeline()
            pipe.fit(X_train, y_grp[train_idx])
            pred_full[grp_idx[test_idx]] = pipe.predict(X_test)

    return _compute_metrics(y_full, pred_full, data["size_tercile"].values, data[localbiz_share_col].values)


# =====================================================================
# STEP 5. 부트스트랩 -- 원본과 완전히 동일한 순서로 rng를 진행시키되,
#   실제 계산은 OLS x 두 stratified 전략만 수행한다.
# =====================================================================
unique_customers = df["customer_id"].unique()
rng = np.random.RandomState(RANDOM_STATE)   # 원본과 동일 -- 재현성 핵심
idx_map = {c: df.index[df["customer_id"] == c].to_numpy() for c in unique_customers}

print(f"\nSTEP 5. 패치 재계산 시작 ({N_BOOT}회 x OLS x 2개 전략만)")
patch_records = []
for b in range(N_BOOT):
    # 원본과 동일한 호출 순서 -- 반드시 매 b마다 호출해 rng 시퀀스를 맞춘다
    sampled_customers = rng.choice(unique_customers, size=len(unique_customers), replace=True)
    boot_idx = np.concatenate([idx_map[c] for c in sampled_customers])
    boot_df = df.loc[boot_idx].reset_index(drop=True)

    oof_seed = RANDOM_STATE + b  # 원본과 동일

    base_metrics = _fit_predict_baseline_ols(boot_df, oof_seed)
    for strategy in ["S9_Campaign_stratified", "S9_plus_S1"]:
        alt_metrics = _fit_predict_stratified_ols(strategy, boot_df, oof_seed)
        patch_records.append({
            "boot": b, "model": "OLS", "strategy": strategy,
            "rmse_overall_diff": alt_metrics["rmse_overall"] - base_metrics["rmse_overall"],
            "size_gap_diff":     alt_metrics["rmse_gap_size"] - base_metrics["rmse_gap_size"],
            "localbiz_gap_diff": alt_metrics["rmse_gap_localbiz"] - base_metrics["rmse_gap_localbiz"],
        })
    if (b + 1) % 50 == 0:
        print(f"  bootstrap {b+1}/{N_BOOT} 완료")

patch_df = pd.DataFrame(patch_records)

# =====================================================================
# STEP 6. 원본 raw와 병합 -- 문제였던 두 조합만 교체, 나머지 10개는 그대로 유지
# =====================================================================
if not ORIGINAL_RAW_PATH.exists():
    raise FileNotFoundError(
        f"{ORIGINAL_RAW_PATH} 가 없습니다. 먼저 "
        "rq3_confirm_v2_campaign_stratified_full.py를 1회 실행해야 합니다.")

original_raw = pd.read_csv(ORIGINAL_RAW_PATH)
is_broken = (
    (original_raw["model"] == "OLS") &
    (original_raw["strategy"].isin(["S9_Campaign_stratified", "S9_plus_S1"]))
)
kept = original_raw.loc[~is_broken].copy()
print(f"\n[6] 원본 raw {len(original_raw)}행 중 재사용 {len(kept)}행, 교체 대상 {is_broken.sum()}행")
print(f"[6] 패치로 새로 계산된 행: {len(patch_df)} (기대값: {N_BOOT * 2})")

merged = pd.concat([kept, patch_df], ignore_index=True)
merged.to_csv(PATCHED_RAW_PATH, index=False, encoding="utf-8-sig")
print(f"[6] 병합된 raw 저장: {PATCHED_RAW_PATH}")

# =====================================================================
# STEP 7. verdict 재계산 (직전 스크립트와 동일한 판정 기준)
# =====================================================================
verdicts = []
for (strategy, model_name), g in merged.groupby(["strategy", "model"]):
    rmse_lo, rmse_hi = np.percentile(g["rmse_overall_diff"], [2.5, 97.5])
    size_lo, size_hi = np.percentile(g["size_gap_diff"], [2.5, 97.5])
    lb_lo, lb_hi = np.percentile(g["localbiz_gap_diff"], [2.5, 97.5])

    rmse_neutral_or_better = rmse_hi < RMSE_NEUTRAL_THRESHOLD
    size_improved = size_hi < 0
    size_worsened = size_lo > 0
    lb_improved = lb_hi < 0
    lb_worsened = lb_lo > 0

    if rmse_neutral_or_better and size_improved and lb_improved:
        verdict = "ALL_THREE_IMPROVED"
    elif rmse_neutral_or_better and (size_improved or lb_improved) and not (size_worsened or lb_worsened):
        verdict = "PARTIAL_IMPROVEMENT"
    elif size_worsened or lb_worsened:
        verdict = "TRADE_OFF_OR_HARM"
    else:
        verdict = "NO_EFFECT"

    verdicts.append({
        "strategy": strategy, "model": model_name,
        "rmse_overall_diff_CI": f"[{rmse_lo:.4f}, {rmse_hi:.4f}]",
        "size_gap_diff_CI":     f"[{size_lo:.4f}, {size_hi:.4f}]",
        "localbiz_gap_diff_CI": f"[{lb_lo:.4f}, {lb_hi:.4f}]",
        "verdict": verdict,
    })

verdict_df = pd.DataFrame(verdicts)
model_order = {"OLS": 0, "HistGB": 1, "RandomForest": 2, "SVR_rbf": 3}
verdict_df["_order"] = verdict_df["model"].map(model_order)
verdict_df = verdict_df.sort_values(["strategy", "_order"]).drop(columns="_order")

print("\n" + "=" * 74); print("최종 verdict (병합, 12개 조합 전체)"); print("=" * 74)
print(verdict_df.to_string(index=False))
verdict_df.to_csv(PATCHED_VERDICT_PATH, index=False, encoding="utf-8-sig")
print(f"\n[7] 최종 판정 저장: {PATCHED_VERDICT_PATH}")

if _dropped_col_log:
    drop_counter = Counter(_dropped_col_log)
    print(f"\n[7] 근-상수 열 제거 발생: {len(drop_counter)}종 조합, 총 {sum(drop_counter.values())}회")
    for (ctx, cols), cnt in drop_counter.most_common(10):
        print(f"     {ctx} -- {cols}: {cnt}회")
    pd.DataFrame(
        [{"context": ctx, "dropped_columns": ",".join(cols), "count": cnt}
         for (ctx, cols), cnt in drop_counter.items()]
    ).to_csv(DROPPED_COL_LOG_PATH, index=False, encoding="utf-8-sig")
    print(f"[7] 로그 저장: {DROPPED_COL_LOG_PATH}")
else:
    print("\n[7] 근-상수 열 제거 없음 (예상과 다름 -- 원인 재확인 필요).")

print("\n[다음 단계] merged raw(rq3_confirm_v2_bootstrap_raw_patched.csv)의")
print("            OLS x stratified 두 조합은 여전히 우측 꼬리가 불안정할 수")
print("            있습니다. rq3_confirm_v2_robust_summary_postprocess.py로")
print("            median/IQR 강건 통계와 tail_ratio 불안정 플래그를 계산하세요.")
