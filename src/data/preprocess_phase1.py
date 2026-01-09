import pandas as pd
import glob
import os

RAW_BASE = "Dataset/raw"
PROC_BASE = "Dataset/processed"


def load_chunks(subfolder):
    path = os.path.join(RAW_BASE, subfolder)
    files = sorted(glob.glob(os.path.join(path, "*.csv")))
    
    if len(files) == 0:
        raise ValueError(f"No files found in {path}")

    dfs = []

    print(f"[INFO] Found {len(files)} chunks in {subfolder}")
    for f in files:
        print(f"[LOAD] {os.path.basename(f)}")
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    return df


def preprocess(df, prefix):
    # Date conversion
    df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y", errors='coerce')

    # Normalize identifiers
    df['state'] = df['state'].astype(str).str.upper().str.strip()
    df['district'] = df['district'].astype(str).str.upper().str.strip()

    # Composite key
    df['district_key'] = df['state'] + "_" + df['district']

    # Pincode as string
    df['pincode'] = df['pincode'].astype(str)

    # Downcast numeric cohort fields
    for col in df.columns:
        if col.lower().startswith(prefix):
            df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

    # Convert to category for memory efficiency
    df['state'] = df['state'].astype('category')
    df['district'] = df['district'].astype('category')
    df['district_key'] = df['district_key'].astype('category')

    return df


def save_parquet(df, name):
    os.makedirs(PROC_BASE, exist_ok=True)
    out_path = os.path.join(PROC_BASE, f"{name}.parquet")
    df.to_parquet(out_path, index=False)
    print(f"[SAVED] {name} → {out_path}")


def run_phase1():

    print("\n=== PHASE-1: LOADING DATA ===")
    df_enrol = load_chunks("api_data_aadhar_enrolment")
    df_demo = load_chunks("api_data_aadhar_demographic")
    df_bio = load_chunks("api_data_aadhar_biometric")

    print("\n=== PREPROCESSING ===")
    df_enrol = preprocess(df_enrol, prefix="age")
    df_demo = preprocess(df_demo, prefix="demo")
    df_bio = preprocess(df_bio, prefix="bio")

    print("\n=== SAVING TO PROCESSED ===")
    save_parquet(df_enrol, "enrolment")
    save_parquet(df_demo, "demographic")
    save_parquet(df_bio, "biometric")

    print("\n=== SANITY CHECKS ===")

    print(f"Enrol Rows: {df_enrol.shape}")
    print(f"Demo Rows:  {df_demo.shape}")
    print(f"Bio Rows:   {df_bio.shape}")

    print("\nDate Ranges:")
    print("Enrol:", df_enrol['date'].min(), "→", df_enrol['date'].max())
    print("Demo: ", df_demo['date'].min(),  "→", df_demo['date'].max())
    print("Bio:  ", df_bio['date'].min(),   "→", df_bio['date'].max())

    print("\nDistrict Counts:")
    print("Enrol:", df_enrol['district_key'].nunique())
    print("Demo: ", df_demo['district_key'].nunique())
    print("Bio:  ", df_bio['district_key'].nunique())

    print("\nStates:")
    print("Enrol:", df_enrol['state'].nunique())
    print("Demo: ", df_demo['state'].nunique())
    print("Bio:  ", df_bio['state'].nunique())

    print("\nPHASE-1 completed successfully!\n")


if __name__ == "__main__":
    run_phase1()
