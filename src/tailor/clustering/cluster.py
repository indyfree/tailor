def cluster(df, distance_measure, target):
    '''The Tailor Clustering Algorithm

    Takes a dataframe, a distance measure (e.g. dynamic_time_warp)
    and a target variable (e.g. 'article_count') as inputs and retuns
    a dataframe where each article is assinged a cluster.

    '''

    feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']

    ranked_feats = rank_features(df, distance_measure, feats)

    for f in ranked_feats:
        df = build_clusters(df, f)

    return df


def build_clusters(df, feature):

    return df
