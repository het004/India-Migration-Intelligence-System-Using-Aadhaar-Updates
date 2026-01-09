import pandas as pd
import glob
import os

def load_chunks(path):
    files = glob.glob(os.path.join(path, "*.csv"))
    dfs = []
    for f in files:
        df = pd.read_csv(f, low_memory=False)
        dfs.append(df)
    out = pd.concat(dfs, ignore_index=True)
    return out


def load_all(base="Dataset/raw"):
    df_enrol = load_chunks(os.path.join(base, "enrolment"))
    df_demo = load_chunks(os.path.join(base, "demographic"))
    df_bio = load_chunks(os.path.join(base, "biometric"))
    return df_enrol, df_demo, df_bio
