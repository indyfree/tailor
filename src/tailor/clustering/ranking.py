import pandas as pd
import time

import tailor
from tailor.data import group_by


def rank_features(df, distance_measure, feats):
    '''Returns a list of features, sorted by their variance score'''

    return None


def inter_feat_variance(df, distance_measure, feat):
    '''Determines the variance of the given feature in respect to the grouped characteristics'''

    return None


def intra_feat_variance(df, distance_maesure, feat):
    '''Determines the intra feature variances of all characteristics for the given feature'''

    intra_feat_variance = pd.Series()
    all_characteristics = df[feat].unique()

    for characteristic in all_characteristics:
        df_characteristic = df[df[feat] == characteristic]
        df_mean = group_by.attribute(df_characteristic, 'time_on_sale', mean=True)

        mean_article_count = df_mean['article_count'].reset_index()
        variances = pd.Series()
        all_articles = df_characteristic['article_id'].unique()

        for article in all_articles:
            article_count_of_article = df_characteristic[df_characteristic['article_id'] == article]['article_count'].reset_index()
            distance = distance_maesure(mean_article_count, article_count_of_article)
            variances = variances.append(distance)

        variance = variances.mean()
        intra_feat_variance[characteristic] = variance

    return intra_feat_variance


def distance_measure(series_a, series_b):
    distances = (series_a - series_b)**2**0.5
    distance = distances.mean()
    return distance


def main():
    df = tailor.load_data()
    df = group_by.weeks_on_sale(df)

    start_time = time.time()
    df_test = intra_feat_variance(df, distance_measure, 'color')
    end_time = time.time() - start_time
    print(df_test)
    print(end_time)


if __name__ == '__main__':
    main()
