import itertools
import multiprocessing as mp
import numpy as np
import pandas as pd
from tailor import data
from tailor.clustering import ranking


def get_cluster_names(clusters, reversed_sort = False):
    '''retrieves all names of the given clusters'''
    names = list()
    for cluster in clusters:
        name = cluster['Name']
        names.append(name)
    # sort by underscore count
    names.sort(key = lambda s: s.count("_"), reverse=reversed_sort)
    return names


def show_cluster_characteristics(data, merge_results, layer, threshold=0.0):
    '''prints values and percentages of cluster defining feature characteristics'''
    for i, df in enumerate(merge_results['DataFrames'][str(layer)]):
        found_something = False
        for col in df.select_dtypes(include=['category']):
            if "article_id" not in col:
                for characteristic in df[col].unique():
                    query_string = str(col) + " == " + '"' + str(characteristic) + '"'
                    temp_df = df.query(query_string)
                    temp_nunique = temp_df['article_id'].nunique()
                    temp_percentage = temp_nunique / data.query(query_string)['article_id'].nunique()
                    if temp_percentage > threshold:
                        found_something = True
                        print(str(i) + ": " + str(characteristic) + ": " + str(temp_nunique) + " " + "{0:.0%}".format(temp_percentage))
        if not found_something:
            print(str(i) + ": " + "outlier collection cluster")
        print("")


def multi_feature(data, distance_measure, clustering_feature, min_cluster_size, max_cluster_count):
    '''cluster the dataframe using all categorical columns and the target feature'''
    split_results = multi_feature_split(data, distance_measure, min_cluster_size)
    merge_results = multi_feature_merge(data, split_results, distance_measure, clustering_feature, min_cluster_size, max_cluster_count)
    return (split_results, merge_results)


def multi_feature_merge(data, split_results, distance_measure, clustering_feature, min_cluster_size, max_cluster_count):
    '''this method merges the split_results until both min_cluster_size and max_clustercount are satisfied'''

    def get_cluster_parent_name(cluster):
        '''generates the name of the parent cluster'''
        name = cluster['Name']
        # remove last character until name is the parent cluster's name
        terminate = False
        while not terminate:
            character = name[-1:]
            if ((character == "_") or (character == "")):
                terminate = True
            name = name[:-1]
        return name


    def get_leaves(split_results):
        '''retrieves all the unsplit clusters / the leaves of the split tree'''
        leaves = list()
        # iterate through all layers of the clustering
        for layer in split_results['Clusters'].index:
            # add all layer leaves and remove leaf parents
            for add_cluster in split_results['Clusters'][layer]:
                check_name = get_cluster_parent_name(add_cluster)
                # iterate until parent cluster is found then remove it
                for index, check_cluster in enumerate(leaves):
                    if check_cluster['Name'] == check_name:
                        # parent cluster found, remove it
                        del leaves[index]
                        # no more than one parent cluster, therefore exit for loop
                        break
                leaves.append(add_cluster)
        return leaves


    def get_distance_matrix(targets):
        # calculate distance matrix
        length = len(targets)
        distances = pd.DataFrame(index=range(length),columns=range(length))
        for i, a in enumerate(targets):
            for k, b in enumerate(reversed(targets)):
                j = length - 1 - k
                if j <= i:
                    break
                else:
                    d = distance_measure(a.values,b.values)
                    distances[i][j] = d
                    distances[j][i] = d
        return distances

    def merge_all(distances):
        # get the closest cluster for each cluster
        # generates a Series with pointer lists
        closest_clusters = pd.Series(index=range(len(distances)), dtype='object')
        for i in distances.index:
            target_index = np.nanargmin(distances[i]).item()
            # only one value now, but we will add values later
            closest_clusters[i] = list()
            closest_clusters[i].append(target_index)

        cluster_groups = closest_clusters

        # generate initial groups by adding the index to the target
        for i, group in cluster_groups.iteritems():
            # first value is the initial closest cluster
            target = group[0]
            cluster_groups[target].append(i)

        # merge until there are only loners and groups with a pointer loop
        # a pointer loop is when two cluster point towards each other, even over multiple cluster between
        finished = False
        while not finished:
            finished = True

            # merge dependencies
            for i, group in cluster_groups.iteritems():
                # loner check
                if len(group) > 1:
                    # first value is the initial closest cluster
                    target = group[0]
                    # rest of the values are pointers added by dependent groups
                    pointers = group[1:]
                    try:
                        # check whether this is a dependent group without a pointer loop
                        if (target not in pointers):
                            # still dependent groups left, we need to iterate at least one more time
                            finished = False
                            # add own index to target
                            cluster_groups[target].append(i)
                            # sanity check whether looping is required
                            if (type(pointers) is list):
                                # multiple entries we can loop
                                for x in pointers:
                                    if (x not in cluster_groups[target]):
                                        cluster_groups[target].append(x)
                            else:
                                print(pointers)
                                cluster_groups[target].append(pointers[0])
                            # dependent group is spent, create loner
                            cluster_groups[i] = list()
                            cluster_groups[i].append(target)
                    except:
                        print("shit's on fire, yo")
                        print(str(i) + " " + str(group) + " " + str(target) + " " + str(pointers))

        # clear loners
        for i, group in cluster_groups.iteritems():
            if (len(group) <= 1):
                target = group[0]
                if target in cluster_groups.index:
                    cluster_groups[target].append(i)
                    cluster_groups = cluster_groups.drop(i)

        # dress up the group list
        merged_groups = list()
        for i, group in cluster_groups.iteritems():
            # replace target with own index
            temp = group
            temp.append(i)
            temp = sorted(list(set(temp)))
            merged_groups.append(temp)
        merged_groups = sorted(merged_groups)

        # merge connected groups and remove duplicates
        for i, group_a in enumerate(merged_groups):
            for k, group_b in enumerate(merged_groups):
                if k is not i:
                    for x in group_a:
                        if x in set(group_b):
                            merged_groups[i] = list(set(group_a).union(set(group_b)))
                            # both will point to the same list
                            merged_groups[k] = merged_groups[i]

        clean = list()
        for group in merged_groups:
            sgroup = sorted(group)
            if sgroup not in clean:
                clean.append(sgroup)
        clean = sorted(clean)

        print(len(list(set(list(itertools.chain.from_iterable(clean))))))
        print(len(clean))

        return clean

    print("merge layer 0")
    # initialize layer 0
    merge_results = pd.Series()
    merge_results['Groups'] = pd.Series()
    merge_results['Indexes'] = pd.Series()
    merge_results['DataFrames'] = pd.Series()

    clusters = get_leaves(split_results)

    length = len(clusters)
    targets = list()

    # dress the clusters for better distance performance
    for i, cluster in enumerate(clusters):
        # only select the distance relevant slice of the Dataframe
        target = cluster['DataFrame'].groupby(['time_on_sale']).mean()[clustering_feature]
        if (len(target) < 26):
            # fill with 0 until index 25 so all comparison arrays are the same length
            # this improves performance dramatically
            target = target.reindex(pd.RangeIndex(26)).fillna(0)
        targets.append(target)

    distances = get_distance_matrix(targets)

    grouped_clusters = merge_all(distances)

    merge_results['Indexes']['0'] = grouped_clusters
    merge_results['Groups']['0'] = list()
    merge_results['DataFrames']['0'] = list()
    for i, pointers in enumerate(merge_results['Indexes']['0']):
        group = list()
        dfs = list()
        for pointer in pointers:
            cluster = clusters[pointer]
            group.append(cluster)
            # retrieving the relevant part of the original dataframe since the cluster dataframe has missing columns
            query_string = ""
            # building the query string
            # e.g. '(Abteilung == "Abteilung001") & (WHG == "WHG003")'
            for feature, characteristic in cluster['Features'].iteritems():
                query_string = query_string + " & " + "(" + feature + " == " + '"' + characteristic + '"' + ")"
            # remove first " & "
            query_string = query_string[3:]
            # select the dataframe part
            df_temp = data.query(query_string)
            dfs.append(df_temp)
        merge_results['Groups']['0'].append(group)
        # merge the clusters' dataframes to one and add it
        merge_results['DataFrames']['0'].append(pd.concat(dfs, sort=True))

    print("get clusters above min_size")
    # generate new layers
    merge_number = 1

    # get all clusters above min_cluster_size
    above_min_size = False
    while not above_min_size:
        above_min_size = True
        # check whether all clusters are above min_cluster_size
        too_small = list()
        for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
            group_size = merge_results['DataFrames'][str(merge_number - 1)][i]['article_id'].nunique()
            if group_size < min_cluster_size:
                above_min_size = False
                too_small.append(i)
        print(len(too_small))

        if not above_min_size:
            # distance matrix generation
            length = len(merge_results['Groups'][str(merge_number - 1)])
            targets = list()
            # dress the clusters for better distance performance
            for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
                # only select the distance relevant slice of the Dataframe
                target = merge_results['DataFrames'][str(merge_number - 1)][i].groupby(['time_on_sale']).mean()[clustering_feature]
                if (len(target) < 26):
                    # fill with 0 until index 25 so all comparison arrays are the same length
                    # this improves performance dramatically
                    target = target.reindex(pd.RangeIndex(26)).fillna(0)
                targets.append(target)
            distances = get_distance_matrix(targets)

            # get the closest group for each group that is too small
            # generates a Series with pointer lists
            closest_groups = pd.Series(index=range(length), dtype='object')
            for i in too_small:
                target_index = np.nanargmin(distances[i]).item()
                # only one value now, but we will add values later
                closest_groups[i] = list()
                closest_groups[i].append(target_index)

            relevant_groups = closest_groups
            relevant_groups = relevant_groups.dropna()

            # generate initial groups by adding the index to the target
            for i, group in relevant_groups.iteritems():
                if group is not np.nan:
                    # first value is the initial closest group
                    target = group[0]
                    # sanity check
                    if target in relevant_groups.index:
                        relevant_groups[target].append(i)
                    else:
                        # targeting group outside of too_small
                        # add own index to own group to not be a loner
                        group.append(i)

            # merge until there are only loners and groups with a pointer loop
            # a pointer loop is when two groups point towards each other, even over multiple groups in between
            finished = False
            while not finished:
                finished = True

                # merge dependencies
                for i, group in relevant_groups.iteritems():
                    # ignore loners
                    if len(group) > 1:
                        # first value is the initial closest cluster
                        target = group[0]
                        # sanity check
                        if target in relevant_groups.index:
                            # rest of the values are pointers added by dependent groups
                            pointers = group[1:]
                            try:
                                # check whether this is a dependent group without a pointer loop
                                if (target not in pointers):
                                    # still dependent groups left, we need to iterate at least one more time
                                    finished = False
                                    # add own index to target
                                    relevant_groups[target].append(i)
                                    # sanity check whether looping is required
                                    if type(pointers) is list:
                                        # multiple entries we can loop
                                        for x in pointers:
                                            if (x not in relevant_groups[target]):
                                                relevant_groups[target].append(x)
                                    else:
                                        print(pointers)
                                        relevant_groups[target].append(pointers[0])
                                    # dependent group is spent, create loner
                                    relevant_groups[i] = list()
                                    relevant_groups[i].append(target)
                            except:
                                print("shit's on fire, yo")
                                print(str(i) + " " + str(group) + " " + str(target) + " " + str(pointers))

            # clear loners
            for i, group in relevant_groups.iteritems():
                if (len(group) <= 1):
                    target = group[0]
                    if target in relevant_groups.index:
                        relevant_groups[target].append(i)
                        relevant_groups = relevant_groups.drop(i)

            # dress up the group list
            sorted_groups = list()
            for i, group in relevant_groups.iteritems():
                # replace target with own index
                temp = group
                temp.append(i)
                temp = sorted(list(set(temp)))
                sorted_groups.append(temp)
            sorted_groups = sorted(sorted_groups)

            # merge connected groups and remove duplicates
            for i, group_a in enumerate(sorted_groups):
                for k, group_b in enumerate(sorted_groups):
                    if k is not i:
                        for x in group_a:
                            if x in set(group_b):
                                sorted_groups[i] = list(set(group_a).union(set(group_b)))
                                # both will point to the same list
                                sorted_groups[k] = sorted_groups[i]
            clean = list()
            for group in sorted_groups:
                sgroup = sorted(group)
                if sgroup not in clean:
                    clean.append(sgroup)
            clean = sorted(clean)

            print(len(list(set(list(itertools.chain.from_iterable(clean))))))

            new_groups = pd.Series(index=range(length), dtype='object')

            # initialize with own index
            for i in new_groups.index:
                if i not in too_small:
                    new_groups[i] = list()
                    new_groups[i].append(i)

            # include the newly generated groups
            for i, group in enumerate(clean):
                found = False
                for x in group:
                    if x not in too_small:
                        # found target group that already was big enough
                        found = True
                        try:
                            # merge groups
                            temp = list()
                            temp.extend(group)
                            temp.extend(new_groups[x])
                            temp = sorted(list(set(temp)))
                            new_groups[x] = temp
                        except:
                            print(x)
                            print(new_groups[x])
                            print(group)
                        break
                if not found:
                    # add new group only made of merged too_small groups
                    new_groups[group[0]] = group

            new_groups = new_groups.dropna()

            clean = list()
            for i, group in new_groups.iteritems():
                sgroup = sorted(group)
                if sgroup not in clean:
                    clean.append(sgroup)
            clean = sorted(clean)

            print(len(list(set(list(itertools.chain.from_iterable(clean))))))

            merge_results['Indexes'][str(merge_number)] = clean
            merge_results['Groups'][str(merge_number)] = list()
            merge_results['DataFrames'][str(merge_number)] = list()
            for i, pointers in enumerate(merge_results['Indexes'][str(merge_number)]):
                group = list()
                dfs = list()
                for pointer in pointers:
                    df_temp = merge_results['DataFrames'][str(merge_number-1)][pointer]
                    dfs.append(df_temp)
                    for cluster in merge_results['Groups'][str(merge_number-1)][pointer]:
                        group.append(cluster)
                merge_results['Groups'][str(merge_number)].append(group)
                # merge the clusters' dataframes to one and add it
                merge_results['DataFrames'][str(merge_number)].append(pd.concat(dfs, sort=True))
            merge_number += 1

    print("merge until below max_cluster_count")
    # merge until below max_cluster_count
    while len(merge_results['Groups'][str(merge_number - 1)]) > max_cluster_count:
        # distance matrix generation
        length = len(merge_results['Groups'][str(merge_number - 1)])
        targets = list()
        # dress the clusters for better distance performance
        for i, group in enumerate(merge_results['Groups'][str(merge_number - 1)]):
            # only select the distance relevant slice of the Dataframe
            target = merge_results['DataFrames'][str(merge_number - 1)][i].groupby(['time_on_sale']).mean()[clustering_feature]
            if (len(target) < 26):
                # fill with 0 until index 25 so all comparison arrays are the same length
                # this improves performance dramatically
                target = target.reindex(pd.RangeIndex(26)).fillna(0)
            targets.append(target)
        distances = get_distance_matrix(targets)
        clean = merge_all(distances)
        merge_results['Indexes'][str(merge_number)] = clean
        merge_results['Groups'][str(merge_number)] = list()
        merge_results['DataFrames'][str(merge_number)] = list()
        for i, pointers in enumerate(merge_results['Indexes'][str(merge_number)]):
            group = list()
            dfs = list()
            for pointer in pointers:
                df_temp = merge_results['DataFrames'][str(merge_number-1)][pointer]
                dfs.append(df_temp)
                for cluster in merge_results['Groups'][str(merge_number-1)][pointer]:
                    group.append(cluster)
            merge_results['Groups'][str(merge_number)].append(group)
            # merge the clusters' dataframes to one and add it
            merge_results['DataFrames'][str(merge_number)].append(pd.concat(dfs, sort=True))
        merge_number += 1

    return merge_results


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
