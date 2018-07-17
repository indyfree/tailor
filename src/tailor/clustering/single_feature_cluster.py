import pandas as pd
from tailor import data


def build_clusters(df, feature, distance_measure, distance_target):
    ''' Build clusters from the features characteristics '''

    df_cluster = data.group_by.feature(df, feature)
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
    distances = []
    # Loop over each cluster a and find out distance to every other cluster b
    for i, a in enumerate(cluster):
        a_curve = df_cluster.loc[df_cluster.cluster == a].set_index('time_on_sale')
        for k, b in enumerate(cluster):
            if k <= i:
                continue
            b_curve = df_cluster.loc[df_cluster.cluster == b].set_index('time_on_sale')
            # Calculate distance between cluster a and b
            d = distance_measure(a_curve[distance_target], b_curve[distance_target])
            distances.append((a, b, d))

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
    ''' Returns cluster information in a dataframe '''

    c = pd.DataFrame()
    c['num_articles'] = df.groupby(['cluster']).apply(lambda x: len(x['article_id'].unique()))
    c['num_characteristics'] = df.groupby(['cluster']).apply(lambda x: len(x[feat].unique()))
    c['characteristics'] = df.groupby(['cluster']).apply(lambda x: x[feat].unique().tolist())

    return c

