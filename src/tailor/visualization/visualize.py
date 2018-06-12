import matplotlib.pyplot as plt

import tailor
from tailor.data import group_by


def plot_articles(df, articles, measure, legend=True):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(measure, fontsize=12)
    ax.set_xlabel('time on sale', fontsize=12)

    for a in articles:
        x = df.loc[df.article_id == a, 'time_on_sale']
        y = df.loc[df.article_id == a, measure]
        plt.plot(x, y, label=str(a))

    if legend is True:
        plt.legend()

    return plt


def plot_feature_characteristics(df, feature, measure, legend=True):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(measure, fontsize=12)
    ax.set_xlabel('time on sale', fontsize=12)

    df = group_by.feature(df, feature)

    for characteristic in df[feature].unique():
        x = df.loc[df[feature] == characteristic, 'time_on_sale']
        y = df.loc[df[feature] == characteristic, measure]
        plt.plot(x, y, label=str(characteristic))

    if legend is True:
        plt.legend()

    return plt

def plot_cluster_articles(df, cluster, distance_target, legend=True):
    cluster_articles = df.loc[df.cluster == cluster]
    ids = cluster_articles.article_id.unique()
    return plot_articles(df, ids, distance_target, legend)


def plot_line_chart(x_axis, y_axis, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.plot(x_axis, y_axis)
    return plt


def plot_bar_chart(x_axis, y_axis, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.bar(x_axis, y_axis)
    return plt


def plot_scatter_plot(x_axis, y_axis, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.scatter(x_axis, y_axis, alpha=0.3, cmap='viridis', s=1.5)
    return plt


def main():
    OUTPUT_DIR = tailor.PROJECT_DIR + '/reports/figures'
    df = tailor.load_data()
    plt = plot_articles(df, [900001, 900002], 'revenue')
    plt.savefig(OUTPUT_DIR + '/weekly_article_history.png')
    print("Plots have been saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
