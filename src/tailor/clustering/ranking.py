import pandas as pd

from tailor import data


def rank_features(df, distance_measure, feats, distance_target):
    '''Returns a list of features, sorted by their variance score'''

    feature_variances = pd.Series()

    for f in feats:
        feature_variance = inter_feat_variance(df, distance_measure, f, distance_target).mean()
        feature_variances[f] = feature_variance

    ranked_features = feature_variances.sort_values(ascending=False)

    return ranked_features


def inter_feat_variance(df, distance_measure, feat, distance_target):
    '''Determines the variance of the given feature in respect to the grouped characteristics'''

    inter_feat_variance = pd.Series()
    df_f = data.group_by.feature(df, feat)

    # NOTE: grouped on mean of characteristics not all articles
    # Is is different because of missing values at some ToS values
    mean_curve = df_f.groupby('time_on_sale').mean()[distance_target]

    characteristics = df_f[feat].unique()
    for c in characteristics:
        characteristic_curve = df_f[df_f[feat] == c].set_index('time_on_sale')[distance_target]
        distance = distance_measure(mean_curve, characteristic_curve)
        inter_feat_variance[c] = distance**2

    return inter_feat_variance


def intra_feat_variance(df, distance_measure, feat, distance_target):
    '''Determines the intra feature variances of all characteristics for the given feature'''

    intra_feat_variance = pd.Series()

    characteristics = df[feat].unique()
    for c in characteristics:
        df_c = df[df[feat] == c]
        mean_curve = df_c.groupby('time_on_sale')[distance_target].mean()

        variances = []
        for a in df_c.article_id.unique():
            article_curve = df_c[df_c.article_id == a].set_index('time_on_sale')[distance_target]
            distance = distance_measure(mean_curve, article_curve)
            variances.append(distance**2)

        intra_feat_variance[c] = pd.Series(variances).mean()

    return intra_feat_variance
