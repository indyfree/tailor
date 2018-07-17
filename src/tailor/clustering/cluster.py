import pandas as pd
import sys
from tailor import data
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


def merge_min_clusters(df, feature, min_cluster_size, distance_measure, distance_target):

    c = pd.DataFrame()
    c['num_articles'] = df.groupby(['cluster']).apply(lambda x: len(x['article_id'].unique()))

    while c['num_articles'].min() < min_cluster_size:
        c.sort_values(by=['num_articles'], ascending=True, inplace=True)
        min_cluster = c.index[0]
        df = merge_closest_cluster(df, feature, min_cluster, distance_measure, distance_target)

        c = pd.DataFrame()
        c['num_articles'] = df.groupby(['cluster']).apply(lambda x: len(x['article_id'].unique()))

    return df


def merge_closest_cluster(df, feature, cluster, distance_measure, distance_target):
    df_cluster = data.group_by.feature(df, feature)

    clusters = df_cluster.cluster.unique()
    distance = sys.maxsize
    target_cluster = cluster

    cluster_curve = df_cluster.loc[df_cluster.cluster == cluster].set_index('time_on_sale')
    # Loop over each cluster c and find out distance to the observed cluster
    for i, c in enumerate(clusters):
        # No need to compare to itself
        if cluster == c:
            continue

        c_curve = df_cluster.loc[df_cluster.cluster == c].set_index('time_on_sale')
        d = distance_measure(cluster_curve[distance_target], c_curve[distance_target])
        if d < distance:
            distance = d
            target_cluster = int(c)

    if target_cluster is not cluster:
        # Merge the two clusters together
        df.loc[df.cluster == cluster, 'cluster'] = target_cluster

    return df
