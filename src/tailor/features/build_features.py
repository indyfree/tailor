import calendar
import pandas as pd
from tailor.data import group_by


def build(df):
    '''Build new features'''
    df = weeks_on_sale(df)
    df = accurate_season(df)
    return df


def get_performance_measures(dataframe, column, characteristic):
    '''Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic'''

    filtered_dataframe = dataframe[dataframe[column] == characteristic]
    grouped_dataframe = group_by.attribute(filtered_dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]


def weeks_on_sale(df):
    '''Calculate weeks an article has been on sale'''

    print("Building weeks_on_sale")
    df['weeks_on_sale'] = df.apply(lambda row: days_to_week(row['time_on_sale']), axis=1)

    return df


def days_to_week(days):
    return days // 7


def meteor_season(month):
    '''return meteorological season'''

    # spring is months 3 to 5
    if 2 < month < 6:
        return 'Spring'
    # summer is months 6 to 8
    elif 5 < month < 9:
        return 'Summer'
    # fall is months 9 to 11
    elif 8 < month < 12:
        return 'Fall'
    # winter is months 12, 1, 2
    else:
        return 'Winter'


def day_to_month(day):
    return day.month


def accurate_season(df):
    '''Rebuild the season column with season of first transaction'''

    feats = pd.DataFrame()
    df_id = df.groupby('article_id')
    print("Calculate starting month")
    # Add month of first transaction 
    feats['month'] = df_id.apply(lambda row: day_to_month(row.transaction_date.min()))
    print("Calculate starting season")
    # Add season of first transaction
    feats['season'] = df_id.apply(lambda row: meteor_season(row.transaction_date.min().month)).astype('category')
    
    return df.drop('season', axis=1).merge(feats, on='article_id')
