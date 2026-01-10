import numpy as np
import pandas as pd

def compute_slope(df, group_col, x_col, y_col, out_col):
    """
    Computes slope of y over x per group using np.polyfit
    """
    slopes = {}

    for key, sub in df.groupby(group_col):
        if sub[y_col].notna().sum() >= 2:
            x = sub[x_col].values
            y = sub[y_col].values
            slope = np.polyfit(x, y, 1)[0]
        else:
            slope = 0
        slopes[key] = slope

    return pd.Series(slopes, name=out_col)
