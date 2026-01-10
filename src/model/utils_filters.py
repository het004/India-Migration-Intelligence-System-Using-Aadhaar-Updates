def filter_features(feats):

    feats = feats[
        (feats['mean_pop_adult'] >= 1000) |
        (feats['mean_total_demo'] >= 20)
    ]

    # remove numeric-only admin artifacts
    feats = feats[~feats['state'].str.isnumeric()]
    feats = feats[~feats['district'].str.isnumeric()]

    return feats
