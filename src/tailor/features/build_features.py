import calendar
import pandas as pd
from tailor.data import group_by


def build(df):
    '''Build new features'''
    df = weeks_on_sale(df)
    df = date_info(df)
    df = accurate_season(df)
    return df


def get_performance_measures(dataframe, column, characteristic):
    '''Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic'''

    filtered_dataframe = dataframe[dataframe[column] == characteristic]
    grouped_dataframe = group_by.attribute(filtered_dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]


def weeks_on_sale(df):
    '''Calculate weeks an article has been on sale'''

    df['weeks_on_sale'] = df.apply(lambda row: days_to_week(row['time_on_sale']), axis=1)
    print("finished building weeks_on_sale")

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


def date_info(df):
    '''Calculate the weekday, month and actual season'''

    seasons = list()
    weekdays = list()
    months = list()

    for i in df.transaction_date:
        month = i.month
        seasons.append(meteor_season(month))
        months.append(calendar.month_abbr[month])
        weekdays.append(calendar.day_abbr[i.weekday()])

    df['season_buy'] = pd.Series(seasons, index=df.index).astype('category')
    print("finished building season_buy")
    df['month'] = pd.Series(months, index=df.index).astype('category')
    print("finished building month")
    df['weekday'] = pd.Series(weekdays, index=df.index).astype('category')
    print("finished building weekday")

    return df


def accurate_season(df):
    '''Rebuild the season column with season of first transaction'''

    # build dictionary with first season per article_id
    new_season = df.groupby('article_id').apply(lambda x: meteor_season(x.transaction_date.min().month))
    # apply dictionary to season column
    df['season'] = df['article_id'].apply(lambda x: new_season[x]).astype('category')
    print("finished rebuilding season")

    return df
