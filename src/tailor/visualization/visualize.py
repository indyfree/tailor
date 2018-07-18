import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import tailor
from tailor.data import group_by


def plot_articles(df, articles, measure, legend=True):
    plt = _setup_plot('time on sale', measure)

    for a in articles:
        x = df.loc[df.article_id == a, 'time_on_sale']
        y = df.loc[df.article_id == a, measure]
        plt.plot(x, y, label=str(a))

    if legend is True:
        plt.legend()

    return plt


def plot_cluster_articles(df, cluster, distance_target, legend=True):
    cluster_articles = df.loc[df.cluster == cluster]
    ids = cluster_articles.article_id.unique()
    return plot_articles(df, ids, distance_target, legend)


def plot_cluster_characteristics(df, cluster, feature, distance_target, legend=True):
    df_cluster = df.loc[df['cluster'] == cluster]
    return plot_feature_characteristics(df_cluster, feature, distance_target, legend)


def plot_feature_characteristics(df, feature, measure, legend=True):
    plt = _setup_plot('time on sale', measure)
    df = group_by.feature(df, feature)

    for characteristic in df[feature].unique():
        x = df.loc[df[feature] == characteristic, 'time_on_sale']
        y = df.loc[df[feature] == characteristic, measure]
        plt.plot(x, y, label=str(characteristic))

    if legend is True:
        plt.legend()

    return plt


def plot_cluster_pca(df, clusters, distance_target, legend=True):
    pca = PCA(n_components=2)
    X = _pivot_dataset(df, distance_target)
    X_r = pca.fit(X).transform(X)
    F = pd.DataFrame(X_r)
    F['cluster'] = df.loc[:, ['article_id', 'cluster']].groupby('article_id').first().reset_index().cluster

    plt.figure(num=None, figsize=(6, 4), dpi=600, facecolor='w', edgecolor='k')
    ax = plt.axes()

    for i in clusters:
        plt.scatter(x=F.loc[F.cluster == i, 1], y=F.loc[F.cluster == i, 0], alpha=.4, lw=0.5,
                    label=F.loc[F.cluster == i, 'cluster'].unique())

    if legend is True:
        plt.legend(loc='best', shadow=False, scatterpoints=1)

    plt.title('Principal Component Analysis')

    ax.set_ylabel('PC 1 (variance explained: %s)' % str(round(pca.explained_variance_ratio_[0], 2)), fontsize=12)
    ax.set_xlabel('PC 2 (variance explained: %s)' % str(round(pca.explained_variance_ratio_[1], 2)), fontsize=12)

    return plt


def _setup_plot(xlabel, ylabel):
    plt.figure(num=None, figsize=(10, 4), dpi=600, facecolor='w', edgecolor='k')
    ax = plt.axes()
    ax.set_xlabel(xlabel.replace("_", " "), fontsize=12)
    ax.set_ylabel(ylabel.replace("_", " "), fontsize=12)
    return plt


def _pivot_dataset(df, distance_target):
    X = df.pivot(index='article_id', columns='time_on_sale', values=distance_target).reset_index()
    X.index = pd.Int64Index(X.article_id)
    X = X.drop('article_id', axis=1)
    X.columns.name = ''
    return X


def main():
    OUTPUT_DIR = tailor.PROJECT_DIR + '/reports/figures'
    df = tailor.load_data()
    plt = plot_articles(df, [900001, 900002], 'revenue')
    plt.savefig(OUTPUT_DIR + '/weekly_article_history.png')
    print("Plots have been saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
