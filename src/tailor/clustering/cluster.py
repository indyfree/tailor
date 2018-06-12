import tailor
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
    df_grouped = build_clusters(df, cluster_feat, distance_measure, distance_target)

    return df_grouped


def build_clusters(df, feature, distance_measure, distance_target):
    df_grouped = data.group_by.feature(df, feature)
    df_grouped['cluster'] = df_grouped[feature].cat.codes  # each characteristic forms a cluster


    distances = cluster_distances(df_grouped, distance_measure, distance_target)
    a, b = closest_clusters(distances)
    df_grouped.loc[df_grouped.cluster == a, 'cluster'] = b

    return df_grouped


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
    threshold = distances.cluster_distance.mean() / 2
    distances = distances.loc[distances.cluster_distance < threshold]
    min_distance = distances.loc[distances.cluster_distance == distances.cluster_distance.min()]

    return min_distance['to'].values[0], min_distance['from'].values[0]


def main():
    df = tailor.load_data()
    df_cluster = cluster(df, clustering.euclidean, 'article_count')
    print(df_cluster)


if __name__ == '__main__':
    main()
