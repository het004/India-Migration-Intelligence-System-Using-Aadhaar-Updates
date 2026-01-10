from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

def compute_pca(df, feature_cols, n_components=2):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    emb = pd.DataFrame(X_pca, columns=[f'pca_{i+1}' for i in range(n_components)])
    emb['district_key'] = df['district_key']

    return emb, scaler, pca
