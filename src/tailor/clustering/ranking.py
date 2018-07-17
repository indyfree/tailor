import pandas as pd

from tailor import data


def rank_features(df, distance_measure, feats, distance_target):
    '''Returns a list of features, sorted by their variance score'''

    variances = pd.DataFrame(columns=['feature', 'variance', 'num_characteristics'])

    for f in feats:
        v = inter_feat_variance(df, distance_measure, f, distance_target)
        variances = variances.append({'feature': f, 'variance': v, 'num_characteristics': len(df[f].unique())}, ignore_index=True)

    ranked_features = variances.sort_values(by=['variance'], ascending=False)

    return ranked_features


def inter_feat_variance(df, distance_measure, feat, distance_target):
    '''
    Determines the variance of the given feature in respect to the grouped characteristics

    Formular variance with discret variables: https://en.wikipedia.org/wiki/Variance#Discrete_random_variable

    SUM_i( (x_i - u)^2 * p_i )

    '''
    inter_feat_variance = 0.0
    num_articles = len(df['article_id'].unique())

    df_f = data.group_by.feature(df, feat)
    mean_curve = df_f.groupby('time_on_sale').mean()[distance_target]

    characteristics = df_f[feat].unique()
    for c in characteristics:
        num_c_articles = len(df[df[feat] == c].article_id.unique())

        characteristic_curve = df_f[df_f[feat] == c].set_index('time_on_sale')[distance_target]
        distance = distance_measure(mean_curve, characteristic_curve)

        probability = num_c_articles / num_articles
        inter_feat_variance += (distance**2) * probability

    return inter_feat_variance

def cluster_variance(df, cluster, distance_measure, distance_target):
    cluster_variance = 0.0

    df_c = df[df.cluster == cluster]
    mean_curve = df_c.groupby('time_on_sale').mean()[distance_target]

    articles = df_c['article_id'].unique()
    for a in articles:
        article_curve = df_c[df_c.article_id == a].set_index('time_on_sale')[distance_target]
        distance = distance_measure(mean_curve, article_curve)
        cluster_variance += (distance**2)

    return (cluster_variance / len(df_c['article_id'].unique()))



def intra_feat_variance(df, distance_measure, feat, distance_target):
    '''Determines the intra feature variances of all characteristics for the given feature'''

    intra_feat_variance = pd.Series()

    characteristics = df[feat].unique()
    for c in characteristics:
        df_c = df[df[feat] == c]
        mean_curve = df_c.groupby('time_on_sale')[distance_target].mean()

        variances = []
        for a in df_c.article_id.unique():
            article_curve = df_c[df_c.article_id == a].set_index('time_on_sale')[distance_target]
            distance = distance_measure(mean_curve, article_curve)
            variances.append(distance**2)

        intra_feat_variance[c] = pd.Series(variances).mean()

    return intra_feat_variance
