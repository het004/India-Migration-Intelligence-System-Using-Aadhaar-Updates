import os
import pandas as pd
from sklearn.cluster import KMeans

from .feature_engineering import engineer_features
from .utils_filters import filter_features
from .utils_pca import compute_pca
from .utils_labels import semantic_label

PROC = "Dataset/processed"
OUT = f"{PROC}/clustering"


def run_phase3():
    print("\n=== PHASE-3: CLUSTERING & ARCHETYPES ===")

    # Load monthly table
    df_month = pd.read_parquet(f"{PROC}/monthly.parquet")

    # Feature Engineering (district-level)
    feats = engineer_features(df_month)

    # Balanced Filters applied on features
    feats = filter_features(feats)

    # Feature cols for clustering
    feature_cols = [c for c in feats.columns if c.startswith(('mean','std','slope'))]
    assert len(feature_cols) > 0, "No features selected for clustering"

    # NaN fix for PCA & clustering
    feats[feature_cols] = feats[feature_cols].fillna(0)

    # PCA Embedding (2D)
    emb, scaler, pca = compute_pca(feats, feature_cols)

    # Clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    feats['cluster'] = kmeans.fit_predict(feats[feature_cols])

    # Semantic labeling
    feats['cluster_label'] = feats['cluster'].apply(semantic_label)

    # Build hierarchy (State → Cluster → District)
    hierarchy = feats.groupby(['state','cluster_label'])['district'].apply(list).reset_index()

    # Ensure output dir exists
    os.makedirs(OUT, exist_ok=True)

    # Save outputs
    feats.to_parquet(f"{OUT}/district_features.parquet", index=False)
    emb.to_parquet(f"{OUT}/pca_embedding.parquet", index=False)
    hierarchy.to_parquet(f"{OUT}/hierarchy.parquet", index=False)

    print("\n=== PHASE-3 COMPLETED ===")
    print("[INFO] Districts:", len(feats))
    print("[INFO] States:", feats['state'].nunique())
    print("[INFO] Clusters:", feats['cluster'].nunique())
    print(hierarchy.head(10))


if __name__ == "__main__":
    run_phase3()
