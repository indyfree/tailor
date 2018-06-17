import pandas as pd

from tailor import data

def davis_bouldin(df, distance_measure, distance_target):
    for c1 in sorted(df.cluster.unique()):
        s1 = cluster_scatter(df, c1, distance_measure, distance_target)

        for c2 in sorted(df.cluster.unique()):
            if c2 <= c1:
                continue

            s2 = cluster_scatter(df, c2, distance_measure, distance_target)


def cluster_scatter(df, cluster, distance_measure, distance_target):
    '''Returns the scatter value within a cluster 'S'

    The scatter value is defined as the average distance to the cluster centroid (mean)
    '''

    cluster = df.loc[df.cluster == cluster]
    mean_curve = cluster.groupby('time_on_sale').mean()[distance_target]
    scatter = []

    for a in cluster.article_id.unique():
        article_curve = cluster[cluster.article_id == a].set_index('time_on_sale')[distance_target]
        scatter.append(distance_measure(mean_curve, article_curve))

    return pd.Series(scatter).mean()

def cluster_separation(df, c1, c2, distance_measure, distance_target):
    '''Returns the cluster separation 'M'

    The cluster seperation is defined as the distance between two clusters centroids (means)
    '''

    cluster1 = df.loc[df.cluster == c1]
    mean_curve1 = cluster1.groupby('time_on_sale').mean()[distance_target]

    cluster2 = df.loc[df.cluster == c2]
    mean_curve2 = cluster2.groupby('time_on_sale').mean()[distance_target]

    return distance_measure(mean_curve1, mean_curve2)
