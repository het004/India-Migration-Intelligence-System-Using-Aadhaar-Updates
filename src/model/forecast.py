import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

PROC = "Dataset/processed"
OUT = f"{PROC}/forecast"
HORIZON = 3   # predict 3 months ahead


# ============================
# SUPERVISED LEARNING TRANSFORM
# ============================

def create_forecast_pairs(df):
    """
    Convert monthly panel to supervised dataset:
    X_t  ->  y_(t+HORIZON)
    """
    df = df.sort_values(['district_key', 'month_index'])

    df['movement_target'] = df.groupby('district_key')['movement_index'].shift(-HORIZON)
    df['student_target'] = df.groupby('district_key')['student_ratio'].shift(-HORIZON)

    # remove last horizon months
    df = df.dropna(subset=['movement_target','student_target'])
    return df


# ============================
# MAIN PIPELINE
# ============================

def run_phase4():
    print("\n=== PHASE-4: DISTRICT FORECASTING (RandomForest, +3 month) ===")

    df = pd.read_parquet(f"{PROC}/monthly.parquet")

    # build supervised pair
    df = create_forecast_pairs(df)

    # features for X(t)
    feature_cols = [
        'movement_index',
        'student_ratio',
        'bio_student',
        'bio_adult',
        'total_demo',
        'pop_adult',
        'month_index',
        'quarter'
    ]

    X = df[feature_cols]
    y_mov = df['movement_target']
    y_std = df['student_target']

    # ============================
    # TRAIN MODELS
    # ============================

    model_mov = RandomForestRegressor(
        n_estimators=400,
        max_depth=12,
        min_samples_split=5,
        n_jobs=-1,
        random_state=42
    )
    model_mov.fit(X, y_mov)

    model_std = RandomForestRegressor(
        n_estimators=400,
        max_depth=12,
        min_samples_split=5,
        n_jobs=-1,
        random_state=42
    )
    model_std.fit(X, y_std)

    # ============================
    # IN-SAMPLE EVALUATION
    # ============================

    pred_mov_hist = model_mov.predict(X)
    pred_std_hist = model_std.predict(X)

    rmse_mov = mean_squared_error(y_mov, pred_mov_hist) ** 0.5
    rmse_std = mean_squared_error(y_std, pred_std_hist) ** 0.5


    print(f"[RMSE] movement_index(t+3m): {rmse_mov:.4f}")
    print(f"[RMSE] student_ratio(t+3m): {rmse_std:.4f}")

    # ============================
    # FEATURE IMPORTANCE
    # ============================

    print("\n[Feature Importance] movement_index +3m")
    for c, imp in sorted(zip(feature_cols, model_mov.feature_importances_), key=lambda x: -x[1]):
        print(f"{c:20s} : {imp:.4f}")

    print("\n[Feature Importance] student_ratio +3m")
    for c, imp in sorted(zip(feature_cols, model_std.feature_importances_), key=lambda x: -x[1]):
        print(f"{c:20s} : {imp:.4f}")

    # ============================
    # SAVE HISTORICAL PREDICTIONS
    # ============================

    df_hist = df.copy()
    df_hist['pred_mov'] = pred_mov_hist
    df_hist['pred_std'] = pred_std_hist

    # ============================
    # FUTURE FORECAST (LATEST MONTH → +3 month)
    # ============================

    df_future = df.groupby('district_key').tail(1).copy()
    X_final = df_future[feature_cols]

    df_future['pred_mov_3m'] = model_mov.predict(X_final)
    df_future['pred_std_3m'] = model_std.predict(X_final)

    # ============================
    # SAVE ARTIFACTS
    # ============================

    os.makedirs(OUT, exist_ok=True)

    df_hist.to_parquet(f"{OUT}/historical_predictions.parquet", index=False)
    df_future.to_parquet(f"{OUT}/future_forecast.parquet", index=False)

    print(f"[SAVED] historical_predictions → {OUT}/historical_predictions.parquet")
    print(f"[SAVED] future_forecast → {OUT}/future_forecast.parquet")

    print("\n=== PHASE-4 COMPLETED ===")


if __name__ == "__main__":
    run_phase4()
