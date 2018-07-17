import pandas as pd
from tailor.clustering import ranking
from tailor.clustering import multi_feature_cluster
from tailor.clustering import single_feature_cluster


def multi_feature(data, distance_measure, clustering_feature, min_cluster_size, max_cluster_count):
    '''cluster the dataframe using all categorical columns and the target feature'''

    split_results = multi_feature_cluster.split(data, distance_measure, min_cluster_size)
    merge_results = multi_feature_cluster.merge(data, split_results, distance_measure, clustering_feature, min_cluster_size, max_cluster_count)

    return (split_results, merge_results)


def single_feature(df, distance_measure, distance_target):
    '''
    Takes a dataframe, a distance measure (e.g. dynamic_time_warp)
    and a target variable (e.g. 'article_count') as inputs and retuns
    a dataframe where each article is assinged a cluster.
    '''

    feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
    ranked_features = ranking.rank_features(df, distance_measure, feats, distance_target)
    first_feat = ranked_features.loc[0].feature
    df = single_feature_cluster.build_clusters(df, first_feat, distance_measure, distance_target)

    return df
