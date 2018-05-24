import matplotlib.pyplot as plt

import tailor
from tailor.data import group_by


def plot_article_history(df, articles, measure):
    plt.figure()
    ax = plt.axes()
    ax.set_ylabel(measure, fontsize=12)
    ax.set_xlabel('weeks on sale', fontsize=12)

    for a in articles:
        x = df.loc[df.article_id == a, 'weeks_on_sale']
        y = df.loc[df.article_id == a, measure]
        plt.plot(x, y, label=str(a))

    plt.legend()
    return plt


def main():
    df = tailor.load_data()
    df = group_by.weeks_on_sale(df)
    plt = plot_article_history(df, [900001, 900002], 'revenue')
    plt.savefig(tailor.PROJECT_DIR + '/reports/figures/weekly_article_history.png')


if __name__ == '__main__':
    main()
