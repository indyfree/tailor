import pandas as pd
import sys
from tailor import data


def build_clusters(df, feature, distance_measure, distance_target):
    ''' Build clusters from the features characteristics '''

    df_cluster = data.group_by.feature(df, feature)

    # Drop eventually existing cluster labels
    if 'cluster' in df_cluster.columns:
        df_cluster.drop(['cluster'], axis=1, inplace=True)

    # Assign the initial clusters, where each characteristic forms a cluster
    df_cluster['cluster'] = df_cluster[feature].cat.codes

    # Merge closest clusters till there are no close clusters anymore
    while True:
        distances = cluster_distances(df_cluster, distance_measure, distance_target)

        # Set the merging threshold as the values which fall below half of the average distance
        # NOTE: This is arbitrary and should be statistically proven
        threshold = distances.cluster_distance.mean() / 2

        a, b = closest_clusters(distances, threshold)
        if (a or b) is None:
            break

        # Merge the two closest clusters with a distance value below the threshold
        df_cluster.loc[df_cluster.cluster == a, 'cluster'] = b

    # Find out which feature characteristics are assigned to which cluster
    char_to_cluster_map = df_cluster[[feature, 'cluster']].groupby(feature).first()

    # Drop eventually existing cluster labels
    if 'cluster' in df.columns:
        df.drop(['cluster'], axis=1, inplace = True)
    # Add Cluster label to the original (article-level) dataframe
    df = df.merge(char_to_cluster_map, on=feature)

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
