# ============================================================
# rq3_confirm_v2_campaign_stratified_full.py
#
#   [POST-HOC ON POST-HOC / TERTIARY, RQ3 -> M4] -- root README §16.3.1,
#   docs/METHODOLOGY_NOTES.md entry B10/B11 참조.
#
#   목적: M2/M3가 Size-blind 전략에 적용했던 것과 완전히 동일한 프로토콜
#   (4개 모델 클래스 x 200-rep customer-cluster bootstrap x 고객 단위
#   5-fold out-of-fold 예측)을 S9_Campaign_stratified(및 참고용 결합 전략
#   S9_plus_S1)에 적용한다.
#
#   [실행 후 수정 이력 - entry B11] 최초 버전은 각 부트스트랩 표본 안에서
#   in-sample 예측(학습에 쓴 데이터로 그대로 predict)을 썼다. 이는 M2/M3
#   (및 v3/v4의 fit_predict_oof)가 쓴 out-of-fold 예측과 다른 방법론이며,
#   특히 S9_Campaign_stratified처럼 표본을 그룹별로 쪼개 학습하는 전략에서
#   표본이 작아진 만큼 과적합이 쉬워져 "성능이 좋아진 것처럼" 보이는
#   아티팩트를 만들 수 있다는 문제가 실제 실행 결과(전 모델에서 균일하게
#   RMSE가 개선되는 패턴)로 드러났다. 이번 버전은 각 부트스트랩 표본
#   내부에서 고객 단위 5-fold OOF로 다시 예측하도록 수정했다 -- in-sample
#   버전의 실행 결과는 폐기하고 이 버전으로 재실행한 결과만 인용할 것.
#
#   본 스크립트는 근-상수 열(near-constant column) 문제를 아직 처리하지
#   않는다 -- 그 처리는 rq3_confirm_v2_patch_ols_stratified.py에서
#   OLS x stratified 두 조합만 골라 별도로 수행한다(전체 재실행보다 훨씬
#   빠르기 때문). 이 스크립트의 출력(rq3_confirm_v2_bootstrap_raw.csv)이
#   그 패치 스크립트의 입력이 된다.
# ============================================================

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore")
pd.set_option("display.width", 200)

# ---------------------------------------------------------------
# CONFIG (경로는 기존 v3/v4/Confirm-v1 스크립트와 동일하게 맞춰주세요)
# ---------------------------------------------------------------
AD_DATA_DIR = Path("/home/yjlee/Research/Ad_Advance/AD_Data")
ADGROUP_DIM_PATH = AD_DATA_DIR / "adgroup_dim_20260722.tsv"
PERF_PANEL_PATH  = AD_DATA_DIR / "ad_performance_17col_20260722.tsv"
CAMPAIGN_DIM_PATH = AD_DATA_DIR / "campaign_dim_20260722.tsv"
OUT_DIR = AD_DATA_DIR.parent

RQ3CONFIRM2_VERDICT_PATH = OUT_DIR / "rq3_confirm_v2_verdict.csv"
RQ3CONFIRM2_RAW_PATH     = OUT_DIR / "rq3_confirm_v2_bootstrap_raw.csv"

RANDOM_STATE = 42
LOCALBIZ_TYPE = 6
MIN_CLICKS_FOR_CPC = 1
MIN_GROUP_N_FOR_GAP = 10
MIN_GROUP_N_FOR_STRAT = 15
TARGET_COL = "log_cpc"
N_BOOT = 200          # M2/M3와 동일한 반복 수 (사전 고정, 결과 보고 바꾸지 않음)
RMSE_NEUTRAL_THRESHOLD = 0.02   # v3/v4의 "정확도 손실 없음" 기준과 동일하게 고정
N_INNER_FOLDS = 5     # M2/M3 및 v3/v4의 fit_predict_oof와 동일하게 5-fold OOF 사용

# 부트스트랩(200) x 모델(4) x 전략(baseline+3, 그 중 stratified 2개는 그룹별
# 5-fold라 fold 수가 2배)이 중첩되므로 in-sample 버전보다 훨씬 느립니다. 코드가
# 끝까지 도는지, 결과 형태가 맞는지만 먼저 확인하려면 PILOT_MODE=True로 짧게
# 돌려보고, 실제 보고에 쓸 결과는 반드시 PILOT_MODE=False(N_BOOT=200)로
# 재실행하세요. PILOT_MODE 결과는 논문/보고서 어디에도 인용하지 말 것.
PILOT_MODE = False
if PILOT_MODE:
    N_BOOT = 10
    print("[경고] PILOT_MODE=True -- 이 실행 결과는 코드 동작 확인용이며 보고에 쓸 수 없습니다.")


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
# STEP 1-3. 패널 재구성 (H1/H2/RQ3 v3·v4·Confirm-v1과 완전히 동일한 정의)
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
# STEP 4. 전략 정의
#   - S0_Baseline           : size_z + spend_z + campaign shares (pooled, 구분 없음)
#   - S1_Size_blind         : M2/M3에서 이미 검증된 전략 (참고용으로 재수록)
#   - S9_Campaign_stratified: local-biz(share_6>0) 여부로 완전히 분리된 두 서브모델
#                             -- 자문 피드백이 요청한 "캠페인 유형을 구분한 모델링"에 해당
#   - S9_plus_S1            : 위 두 전략의 결합 (서브모델 학습 시 size_z 자체를 제외)
#                             -- M1 스캔에 없던 조합이므로 참고용 exploratory 취급
# =====================================================================
_FEATURE_SETS = {
    "S0_Baseline":   ["size_z", "spend_z"] + non_ref_share_cols,
    "S1_Size_blind": ["spend_z"] + non_ref_share_cols,
}
STRATIFIED_STRATEGIES = {
    "S9_Campaign_stratified": ["size_z", "spend_z"] + non_ref_share_cols,
    "S9_plus_S1":             ["spend_z"] + non_ref_share_cols,  # 서브모델 내에서도 size_z 제외
}
ALL_STRATEGIES = ["S1_Size_blind", "S9_Campaign_stratified", "S9_plus_S1"]

# M2/M3와 완전히 동일한 4개 모델 클래스 (선형 / 부스팅 / 배깅 / 커널)
# -- 이번 스캔 결과를 보고 고른 것이 아니라, M2/M3의 사전 고정 목록을 그대로 재사용 (entry B9 원칙)
CONFIRM_MODELS = {
    "OLS":          lambda: LinearRegression(),
    "HistGB":       lambda: HistGradientBoostingRegressor(
        max_depth=4, learning_rate=0.05, max_iter=300, random_state=RANDOM_STATE),
    "RandomForest": lambda: RandomForestRegressor(
        n_estimators=300, max_depth=6, min_samples_leaf=10,
        random_state=RANDOM_STATE, n_jobs=-1),
    "SVR_rbf":      lambda: SVR(kernel="rbf", C=1.0, epsilon=0.1),
}
NEEDS_SCALING_CONFIRM = {"OLS", "SVR_rbf"}


def _confirm_build_pipeline(model_name, model_factory):
    if model_name in NEEDS_SCALING_CONFIRM:
        return Pipeline([("scaler", StandardScaler()), ("model", model_factory())])
    return Pipeline([("model", model_factory())])


def _confirm_compute_metrics(y_true, y_pred, size_tercile, share6, min_n=MIN_GROUP_N_FOR_GAP):
    """M2/M3와 동일하게 overall RMSE, size_gap, localbiz_gap 세 지표를 모두 계산."""
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


def _make_fold_assignment(customer_ids_array, n_splits, seed):
    """v3/v4의 make_fold_assignment와 동일 로직: 고객 단위로 fold를 나눠
    같은 고객의 행이 train/test에 동시에 들어가지 않도록 한다."""
    rng_local = np.random.RandomState(seed)
    unique_ids = np.unique(customer_ids_array)
    shuffled = unique_ids.copy()
    rng_local.shuffle(shuffled)
    folds = np.array_split(shuffled, n_splits)
    fold_id = np.full(len(customer_ids_array), -1)
    for k, test_ids in enumerate(folds):
        fold_id[np.isin(customer_ids_array, test_ids)] = k
    return fold_id


def _fit_predict_pooled(strategy, model_name, model_factory, data, seed):
    """S0_Baseline, S1_Size_blind: 5-fold out-of-fold(OOF) 예측.
    M2/M3·v3/v4와 동일하게, 각 fold의 테스트 구간은 그 fold를 학습에 쓰지 않은
    모델로만 예측한다 -- in-sample 예측이 아니다."""
    X = data[_FEATURE_SETS[strategy]].copy()
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
        pipe = _confirm_build_pipeline(model_name, model_factory)
        pipe.fit(X.iloc[train_idx], y[train_idx])
        pred[test_idx] = pipe.predict(X.iloc[test_idx])

    return _confirm_compute_metrics(y, pred, data["size_tercile"].values, data[localbiz_share_col].values)


def _fit_predict_stratified(strategy, model_name, model_factory, data, seed):
    """S9_Campaign_stratified, S9_plus_S1: local-biz(share_6>0) 여부로 완전히
    분리된 두 서브모델을 각각 5-fold OOF로 학습·예측한다 (그룹은 사전 고정된
    share_6>0 기준만 사용). 그룹 내 fold도 고객 단위로 나눠 그룹 안에서도
    train/test 고객이 겹치지 않게 한다. 이렇게 해야 그룹을 쪼개서 생기는
    표본 축소가 과적합으로 이어져 in-sample RMSE만 낮아지는 아티팩트를
    피할 수 있다."""
    feats = STRATIFIED_STRATEGIES[strategy]
    y_full = data[TARGET_COL].values
    cust_ids = data["customer_id"].values
    pred_full = np.full(len(data), np.nan)
    mask_arr = data["is_localbiz_primary"].values.astype(bool)

    for grp_val in (0, 1):
        grp_idx = np.where(mask_arr == bool(grp_val))[0]
        grp_n_customers = len(np.unique(cust_ids[grp_idx]))

        if len(grp_idx) < MIN_GROUP_N_FOR_STRAT or grp_n_customers < N_INNER_FOLDS:
            # 그룹 표본(또는 그룹 내 고객 수)이 fold를 나누기에 너무 작으면
            # 전체 데이터로 학습한 모델로 이 그룹을 예측 (v4의 폴백 규칙과 동일
            # 원칙, 단 여기서도 그룹 자신의 fold는 학습에서 제외해 누수를 막는다)
            X_all = data[feats]
            other_idx = np.where(~np.isin(np.arange(len(data)), grp_idx))[0]
            if len(other_idx) == 0:
                continue
            pipe = _confirm_build_pipeline(model_name, model_factory)
            pipe.fit(X_all.iloc[other_idx], y_full[other_idx])
            pred_full[grp_idx] = pipe.predict(X_all.iloc[grp_idx])
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
            pipe = _confirm_build_pipeline(model_name, model_factory)
            pipe.fit(X_grp.iloc[train_idx], y_grp[train_idx])
            local_pred = pipe.predict(X_grp.iloc[test_idx])
            pred_full[grp_idx[test_idx]] = local_pred

    return _confirm_compute_metrics(y_full, pred_full, data["size_tercile"].values, data[localbiz_share_col].values)


def _confirm_fit_predict(strategy, model_name, model_factory, data, seed):
    if strategy in STRATIFIED_STRATEGIES:
        return _fit_predict_stratified(strategy, model_name, model_factory, data, seed)
    return _fit_predict_pooled(strategy, model_name, model_factory, data, seed)


# =====================================================================
# STEP 5. 고객 단위 bootstrap 재검증 (M2/M3와 동일: 200 reps, customer-cluster)
# =====================================================================
unique_customers = df["customer_id"].unique()
rng = np.random.RandomState(RANDOM_STATE)
idx_map = {c: df.index[df["customer_id"] == c].to_numpy() for c in unique_customers}

print(f"\nSTEP 5. Bootstrap 재검증 시작 ({N_BOOT}회 x 전략 {len(ALL_STRATEGIES)} x 모델 {len(CONFIRM_MODELS)})")
boot_records = []
for b in range(N_BOOT):
    sampled_customers = rng.choice(unique_customers, size=len(unique_customers), replace=True)
    boot_idx = np.concatenate([idx_map[c] for c in sampled_customers])
    boot_df = df.loc[boot_idx].reset_index(drop=True)

    oof_seed = RANDOM_STATE + b   # bootstrap마다 다른 fold 분할 (재현 가능하게 고정된 시드)
    for model_name, model_factory in CONFIRM_MODELS.items():
        base_metrics = _confirm_fit_predict("S0_Baseline", model_name, model_factory, boot_df, oof_seed)
        for strategy in ALL_STRATEGIES:
            alt_metrics = _confirm_fit_predict(strategy, model_name, model_factory, boot_df, oof_seed)
            boot_records.append({
                "boot": b, "model": model_name, "strategy": strategy,
                "rmse_overall_diff": alt_metrics["rmse_overall"] - base_metrics["rmse_overall"],
                "size_gap_diff":     alt_metrics["rmse_gap_size"] - base_metrics["rmse_gap_size"],
                "localbiz_gap_diff": alt_metrics["rmse_gap_localbiz"] - base_metrics["rmse_gap_localbiz"],
            })
    if (b + 1) % 50 == 0:
        print(f"  bootstrap {b+1}/{N_BOOT} 완료")

boot_df_result = pd.DataFrame(boot_records)
boot_df_result.to_csv(RQ3CONFIRM2_RAW_PATH, index=False, encoding="utf-8-sig")

# =====================================================================
# STEP 6. 판정 -- M2/M3와 완전히 동일한 규칙
#   "세 지표(ΔRMSE, Δsize_gap, Δlocalbiz_gap) 모두 95% CI가 완전히 음수(개선)"
#   일 때만 verdict="ALL_THREE_IMPROVED". 그 외는 어느 지표가 어떻게
#   움직였는지 그대로 보고한다 -- 결과를 좋아 보이게 재분류하지 않는다.
# =====================================================================
print("\n" + "=" * 74); print("STEP 6. 판정 (M2/M3와 동일 기준)"); print("=" * 74)

verdicts = []
for (strategy, model_name), g in boot_df_result.groupby(["strategy", "model"]):
    rmse_lo, rmse_hi = np.percentile(g["rmse_overall_diff"], [2.5, 97.5])
    size_lo, size_hi = np.percentile(g["size_gap_diff"], [2.5, 97.5])
    lb_lo, lb_hi = np.percentile(g["localbiz_gap_diff"], [2.5, 97.5])

    rmse_neutral_or_better = rmse_hi < RMSE_NEUTRAL_THRESHOLD  # 소폭 악화까지는 "손실 없음"으로 허용(v3/v4 기준과 동일)
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

print(verdict_df.to_string(index=False))
verdict_df.to_csv(RQ3CONFIRM2_VERDICT_PATH, index=False, encoding="utf-8-sig")

print(f"\n[6] 원본 부트스트랩 저장: {RQ3CONFIRM2_RAW_PATH}")
print(f"[6] 판정 결과 저장: {RQ3CONFIRM2_VERDICT_PATH}")
print("\n[주의] OLS x S9_Campaign_stratified / S9_plus_S1의 CI 상단이 비정상적으로")
print("       넓게 나올 수 있습니다(근-상수 열로 인한 수치 불안정, entry B11).")
print("       이 두 조합만 rq3_confirm_v2_patch_ols_stratified.py로 재계산하세요.")
