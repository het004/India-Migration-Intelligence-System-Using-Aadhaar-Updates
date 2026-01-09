import pandas as pd
import glob
import os

RAW = "Dataset/raw"
PROC = "Dataset/processed"
CHUNK = 300_000   # safe for 16GB


def stream_monthly(path, value_cols, rename_map=None):
    files = glob.glob(os.path.join(path, "*.csv"))
    agg = None

    print(f"[STREAM] {path} ({len(files)} chunks)")

    for f in files:
        print(f"[CHUNK] {os.path.basename(f)}")
        for chunk in pd.read_csv(f, chunksize=CHUNK, low_memory=False):
            # Date → month
            chunk['date'] = pd.to_datetime(chunk['date'], format="%d-%m-%Y", errors='coerce')
            chunk['month'] = chunk['date'].dt.to_period("M")

            # Normalize identifiers
            chunk['state'] = chunk['state'].astype(str).str.upper().str.strip()
            chunk['district'] = chunk['district'].astype(str).str.upper().str.strip()
            chunk['district_key'] = chunk['state'] + "_" + chunk['district']

            # Monthly aggregation on district
            grouped = chunk.groupby(
                ['district_key', 'state', 'district', 'month']
            )[value_cols].sum()

            agg = grouped if agg is None else agg.add(grouped, fill_value=0)

    df = agg.reset_index()

    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def run_phase2():

    print("\n=== PHASE-2: MONTHLY AGGREGATION + MIGRATION SIGNALS ===")

    # DEMOGRAPHIC (primary migration signal)
    df_demo = stream_monthly(
        f"{RAW}/api_data_aadhar_demographic",
        value_cols=['demo_age_5_17','demo_age_17_'],
        rename_map={
            'demo_age_5_17': 'student_updates',
            'demo_age_17_': 'adult_updates'
        }
    )

    df_demo['total_demo'] = df_demo['student_updates'] + df_demo['adult_updates']
    df_demo['student_ratio'] = df_demo['student_updates'] / df_demo['total_demo']
    df_demo['adult_ratio']   = df_demo['adult_updates']   / df_demo['total_demo']


    # BIOMETRIC (lifecycle signal)
    df_bio = stream_monthly(
        f"{RAW}/api_data_aadhar_biometric",
        value_cols=['bio_age_5_17','bio_age_17_'],
        rename_map={
            'bio_age_5_17': 'bio_student',
            'bio_age_17_': 'bio_adult'
        }
    )

    # ENROLMENT (population proxy)
    df_enrol = stream_monthly(
        f"{RAW}/api_data_aadhar_enrolment",
        value_cols=['age_0_5','age_5_17','age_18_greater'],
        rename_map={'age_18_greater': 'pop_adult'}
    )

    # MERGE (small table, cheap)
    df_month = df_demo \
        .merge(df_bio,   on=['district_key','state','district','month'], how='left') \
        .merge(df_enrol, on=['district_key','state','district','month'], how='left')

    # MIGRATION PROXY
    df_month['movement_index'] = df_month['total_demo'] / df_month['pop_adult'].replace(0, pd.NA)
    df_month['movement_index'] = df_month['movement_index'].fillna(df_month['total_demo'])

    # TIME FEATURES
    df_month['month_num'] = df_month['month'].dt.month
    df_month['quarter'] = df_month['month'].dt.quarter

    df_month['month_index'] = (
        df_month['month'].dt.to_timestamp()
        .rank(method="dense")
        .astype(int) - 1
    )

    # SORT (optional but useful for forecasting & viz)
    df_month = df_month.sort_values(['state','district','month'])

    # SAVE OUTPUT
    out_path = f"{PROC}/monthly.parquet"
    df_month.to_parquet(out_path, index=False)
    print(f"[SAVED] → {out_path}")

    # SANITY OUTPUT
    print("\n=== SANITY ===")
    print("Date Range:", df_month['month'].min(), "→", df_month['month'].max())
    print("Districts:", df_month['district_key'].nunique())
    print("States:", df_month['state'].nunique())
    print(df_month.head(10))
    print("\nPHASE-2 completed successfully!\n")


if __name__ == "__main__":
    run_phase2()
