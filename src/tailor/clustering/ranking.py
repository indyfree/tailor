import pandas as pd
import time

import tailor
from tailor.clustering import distance


def rank_features(df, distance_measure, feats):
    '''Returns a list of features, sorted by their variance score'''

    return None


def inter_feat_variance(df, distance_measure, feat):
    '''Determines the variance of the given feature in respect to the grouped characteristics'''

    return None


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


def main():
    df = tailor.load_data()

    start_time = time.time()
    df_test = intra_feat_variance(df, distance.euclidean, 'color', 'article_count')
    end_time = time.time() - start_time
    print(df_test)
    print(end_time)


if __name__ == '__main__':
    main()
