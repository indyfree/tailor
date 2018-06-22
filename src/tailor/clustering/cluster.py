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
    first_feat = ranked_features.index[0]
    df = build_clusters(df, first_feat, distance_measure, distance_target)

    return df


def build_clusters(df, feature, distance_measure, distance_target, min_cluster_size):
    ''' Build clusters from the features characteristics '''

    df_cluster = data.group_by.feature(df, feature)

    # Assign the initial clusters, where each characteristic forms a cluster
    df_cluster['cluster'] = df_cluster[feature].cat.codes

    # Merge closest clusters till there are no close clusters anymore
    while True:
        distances = cluster_distances(df_cluster, distance_measure, distance_target)
        print(distances)

        # Set the merging threshold as the values which fall below half of the average distance
        # NOTE: This is arbitrary and should be statistically proven
        threshold = distances.cluster_distance.mean() / 2

        a, b = closest_clusters(distances, threshold)
        if (a or b) is None:
            break

        # Merge the two closest clusters with a distance value below the threshold
        df_cluster.loc[df_cluster.cluster == a, 'cluster'] = b
        print(a, b)

    # Find out which feature characteristics are assigned to which cluster
    char_to_cluster_map = df_cluster[[feature, 'cluster']].groupby(feature).mean()
    # Add Cluster label to the original (article-level) dataframe
    df = df.merge(char_to_cluster_map, on=feature)

    return df


def cluster_distances(df_cluster, distance_measure, distance_target):
    '''
    Takes a grouped dataframe with cluster labels and return a dataframe
    with the distances between each pair of clusters.
    '''

    cluster = df_cluster.cluster.unique()
    distances = pd.DataFrame()

    # Loop over each cluster a and find out distance to every other cluster b
    for i, a in enumerate(cluster):
        distances = distances.append(cluster_distance(df_cluster, a, distance_measure, distance_target))

    return distances


def cluster_distance(df_cluster, cluster_id, distance_measure, distance_target):
    cluster = df_cluster.cluster.unique()
    distances = []

    # Loop over each cluster a and find out distance to every other cluster b
    a_curve = df_cluster.loc[df_cluster.cluster == cluster_id].set_index('time_on_sale')
    for k, b in enumerate(cluster):
        if cluster_id == b:
            continue

        b_curve = df_cluster.loc[df_cluster.cluster == b].set_index('time_on_sale')
        # Calculate distance between cluster a and b
        d = distance_measure(a_curve[distance_target], b_curve[distance_target])
        distances.append((cluster_id, b, d))

    return pd.DataFrame(distances, columns=['from', 'to', 'cluster_distance'])


def closest_clusters(distances, threshold):
    ''' Return the two closest clusters '''

    distances = distances.loc[distances.cluster_distance < threshold]
    min_distance = distances.loc[distances.cluster_distance == distances.cluster_distance.min()]

    if(not min_distance.empty):
        return min_distance['to'].values[0], min_distance['from'].values[0]
    else:
        return None, None


def cluster_characteristics(df, feat):
    ''' Returns a series with with a list of the feature characteristics assigned to a cluster '''
    c = df.groupby(['cluster', feat], observed=True, as_index=False).sum()
    return c.groupby('cluster')[feat].apply(lambda x: "%s" % ', '.join(x))
