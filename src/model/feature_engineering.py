import pandas as pd
from src.model.utils_trends import compute_slope


def engineer_features(month_df):
    """
    Aggregates structural, volatility and trend features per district
    """
    feats = month_df.groupby('district_key').agg(
        mean_total_demo=('total_demo','mean'),
        mean_student_ratio=('student_ratio','mean'),
        mean_adult_ratio=('adult_ratio','mean'),
        mean_movement_index=('movement_index','mean'),
        mean_bio_student=('bio_student','mean'),
        mean_bio_adult=('bio_adult','mean'),
        mean_pop_adult=('pop_adult','mean'),
        std_total_demo=('total_demo','std'),
        std_student_ratio=('student_ratio','std'),
        std_movement_index=('movement_index','std'),
        state=('state','first'),
        district=('district','first')
    )

    # TREND FEATURES
    slope_student = compute_slope(month_df, 'district_key', 'month_index', 'student_ratio', 'slope_student_ratio')
    slope_mov = compute_slope(month_df, 'district_key', 'month_index', 'movement_index', 'slope_movement_index')

    feats = feats.join(slope_student).join(slope_mov)

    return feats.reset_index()
