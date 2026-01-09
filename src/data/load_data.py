import pandas as pd
import glob
import os

BASE_DIR = "Dataset/raw"

def load_chunks(subfolder):
    path = os.path.join(BASE_DIR, subfolder)
    files = glob.glob(os.path.join(path, "*.csv"))

    print(f"[INFO] Found {len(files)} chunks for {subfolder}")

    dfs = []
    for f in files:
        print(f"[LOAD] → {os.path.basename(f)}")
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    return df


def load_all():
    df_enrol = load_chunks("api_data_aadhar_enrolment")
    df_demo = load_chunks("api_data_aadhar_demographic")
    df_bio  = load_chunks("api_data_aadhar_biometric")
    return df_enrol, df_demo, df_bio
