from tailor import clustering
from tailor import data

import pandas as pd


def cluster(df, distance_measure, distance_target):
    '''The Tailor Clustering Algorithm

    Takes a dataframe, a distance measure (e.g. dynamic_time_warp)
    and a target variable (e.g. 'article_count') as inputs and retuns
    a dataframe where each article is assinged a cluster.

    '''

    feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
    ranked_features = clustering.rank_features(df, distance_measure, feats, distance_target)
    cluster_feat = ranked_features.index[0]
    df_clusters = build_clusters(df, cluster_feat, distance_measure, distance_target)

    return df_clusters


def build_clusters(df, feature, distance_measure, distance_target):
    ''' Build cluster for a specific feature '''

    df_cluster = data.group_by.feature(df, feature)
    df_cluster['cluster'] = df_cluster[feature].cat.codes  # each characteristic forms a cluster

    while(True):
        distances = cluster_distances(df_cluster, distance_measure, distance_target)
        a, b = closest_clusters(distances)

        if (a or b) is None:
            break

        # TODO: Print characteristics of clusters
        # print("Merging Cluster:", a, b)
        df_cluster.loc[df_cluster.cluster == a, 'cluster'] = b

    return df_cluster


def cluster_distances(df, distance_measure, distance_target):
    '''
    Takes the dataframe which is grouped by the feature that is currently used to cluster.
    Return the distances between the feature characteristics.
    '''

    cluster = df.cluster.unique()
    distances = []

    for i, x in enumerate(cluster):
        x_curve = df.loc[df.cluster == x].set_index('time_on_sale')

        for k, y in enumerate(cluster):
            if k <= i:
                continue

            y_curve = df.loc[df.cluster == y].set_index('time_on_sale')
            d = distance_measure(x_curve[distance_target], y_curve[distance_target])
            distances.append((x, y, d))

    return pd.DataFrame(distances, columns=['from', 'to', 'cluster_distance'])


def closest_clusters(distances):
    ''' Return the two closest clusters '''

    threshold = distances.cluster_distance.mean() / 2
    distances = distances.loc[distances.cluster_distance < threshold]
    min_distance = distances.loc[distances.cluster_distance == distances.cluster_distance.min()]

    if(not min_distance.empty):
        return min_distance['to'].values[0], min_distance['from'].values[0]
    else:
        return None, None
