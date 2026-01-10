import pandas as pd

def apply_balanced_filters(df):
    """
    Balanced filtering for clustering:
    - remove low population / dummy districts
    - require consistent monthly coverage
    - remove numeric-only states/districts
    """
    # POPULATION FILTER
    df = df[df['pop_adult'] >= 5000]

    # COVERAGE FILTER
    month_counts = df.groupby('district_key')['month'].nunique()
    valid_keys = month_counts[month_counts >= 8].index
    df = df[df['district_key'].isin(valid_keys)]

    # TEXT FILTER
    def is_text(x):
        return not str(x).isdigit()

    df = df[df['state'].apply(is_text)]
    df = df[df['district'].apply(is_text)]

    return df
