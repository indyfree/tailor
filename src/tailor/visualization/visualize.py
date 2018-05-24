import tailor
from tailor.data import group_by

import matplotlib
# Do not use X-Server backend, we only want to output png
matplotlib.use('Agg')
import matplotlib.pyplot as plt # noqa

OUTPUT_DIR = tailor.PROJECT_DIR + '/reports/figures/'


def plot_line_chart(x_axis, y_axis, filename, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.plot(x_axis, y_axis)
    plt.savefig(OUTPUT_DIR + filename)


def plot_bar_chart(x_axis, y_axis, filename, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.bar(x_axis, y_axis)
    plt.savefig(OUTPUT_DIR + filename)


def plot_scatter_plot(x_axis, y_axis, filename, x_axis_label='', y_axis_label=''):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(y_axis_label, fontsize=12)
    ax.set_xlabel(x_axis_label, fontsize=12)
    plt.scatter(x_axis, y_axis, alpha=0.3, cmap='viridis', s=1.5)
    plt.savefig(OUTPUT_DIR + filename)


def main():
    raw_dataframe = tailor.load_data()
    grouped_dataframe = group_by.attribute(raw_dataframe, 'article_id', mean=True)

    plot_bar_chart(grouped_dataframe['article_id'], grouped_dataframe['revenue'], 'barchart_mean_revenue.png')

    plot_bar_chart(grouped_dataframe['article_id'], grouped_dataframe['avq'], 'barchart_mean_avq.png')

    plot_bar_chart(grouped_dataframe['article_id'], grouped_dataframe['article_count'], 'barchart_mean_article_count.png')


if __name__ == '__main__':
    main()
