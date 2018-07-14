import pandas as pd
from tailor import data
from tailor.clustering import ranking


def multi_feature_split(df, distance_measure, min_cluster_size):
    '''this is the top-down cluster split that returns all clusters of the process

    example of the result:

    accessing the first cluster of the second split
    split_results['Clusters']["2"][0]

    accessing the split feature for the next split of the first cluster of the second split
    split_results['Features']["2"][0]

    accessing the DataFrame of the first cluster of the second split
    split_results['Clusters']["2"][0]['DataFrame']

    accessing the cluster defining features
    cluster['Features']

    accessing the cluster name which contains the split hierarchy
    cluster['Name']
    e.g. 0_3_1_7 means that the cluster is the 7th split of the 1st split of the 3rd split of the starting cluster
    '''
    # retrieve the features relevant for clustering
    usable_features = df.select_dtypes(include=['category']).drop(columns=['article_id']).columns.values
    split_number = 0
    split_possible = True

    # this will contain the whole hierarchical top-down clustering
    split_results = pd.Series()
    # this will contain all the clusters in an array with the split_number as index
    split_results['Clusters'] = pd.Series()
    # this will contain all the clusters' split features in an array with the split_number as index
    split_results['Features'] = pd.Series()

    # this is the data structure used for all clusters
    first_cluster = pd.Series()
    # this only contains the cluster's articles, all split clusteres will use splines of this
    first_cluster['DataFrame'] = df.copy()
    # this contains the features and characteristics used for the cluster
    first_cluster['Features'] = pd.Series()
    # the name will be defined in a manner that the hierarchy of the clustering will become clear
    first_cluster['Name'] = "0"

    # initializing the 0 split
    # adding the base cluster
    split_results['Clusters'][str(split_number)] = list()
    split_results['Clusters'][str(split_number)].append(first_cluster)
    # determining the feature the cluster should be split by
    split_feature = ranking.rank_features(df, distance_measure, usable_features, 'article_count').index[0]
    # the split_feature is saved
    split_results['Features'][str(split_number)] = list()
    split_results['Features'][str(split_number)].append(split_feature)

    while (split_possible):
        split_possible = False
        # iterate through all split target clusters
        for position, cluster in enumerate(split_results['Clusters'][str(split_number)]):
            if (cluster['DataFrame']['article_id'].nunique() > min_cluster_size):
                # retrieving the feature to split the cluster
                split_feature = split_results['Features'][str(split_number)][position]
                # sanity check
                if (split_feature is not None):
                    # split initialization
                    if (split_possible is False):
                        split_possible = True
                        # generating the new split layer
                        new_layer = split_number + 1
                        split_results['Clusters'][str(new_layer)] = list()
                        split_results['Features'][str(new_layer)] = list()

                    # retrieving the values the cluster will be split into
                    feature_uniques = cluster['DataFrame'][split_feature].unique()
                    df_temp = cluster['DataFrame']

                    for position, characteristic in enumerate(feature_uniques):
                        # create new cluster
                        new_cluster = pd.Series()
                        # select the relevant part of the dataframe
                        new_cluster['DataFrame'] = df_temp[df_temp[split_feature] == characteristic].drop(columns=[split_feature])
                        # copy the features from the parent cluster
                        new_cluster['Features'] = cluster['Features'].copy()
                        # add the split feature to it
                        new_cluster['Features'][split_feature] = characteristic
                        # name the cluster
                        new_cluster['Name'] = cluster['Name'] + "_" + str(position + 1)
                        # retrieve the features relevant for clustering
                        usable_features = new_cluster['DataFrame'].select_dtypes(include=['category']).drop(columns=['article_id']).columns.values
                        if len(usable_features) > 0:
                            # determine the feature the new cluster will be split by
                            new_split_feature = ranking.rank_features(new_cluster['DataFrame'], distance_measure, usable_features, 'article_count').index[0]
                            # add the cluster to the split_results
                            split_results['Clusters'][str(new_layer)].append(new_cluster)
                            split_results['Features'][str(new_layer)].append(new_split_feature)
                        else:
                            # no categorical columns left
                            split_results['Clusters'][str(new_layer)].append(new_cluster)
                            split_results['Features'][str(new_layer)].append(None)
        split_number += 1

    return split_results


def single_feature(df, distance_measure, distance_target):
    '''The Tailor Clustering Algorithm

    Takes a dataframe, a distance measure (e.g. dynamic_time_warp)
    and a target variable (e.g. 'article_count') as inputs and retuns
    a dataframe where each article is assinged a cluster.

    '''

    feats = ['color', 'brand', 'Abteilung', 'WHG', 'WUG', 'season', 'month']
    ranked_features = ranking.rank_features(df, distance_measure, feats, distance_target)
    first_feat = ranked_features.index[0]
    df = build_clusters(df, first_feat, distance_measure, distance_target)

    return df


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
    ''' Returns a series with with a list of the feature characteristics assigned to a cluster '''
    c = df.groupby(['cluster', feat], observed=True, as_index=False).sum()
    return c.groupby('cluster')[feat].apply(lambda x: "%s" % ', '.join(x))
