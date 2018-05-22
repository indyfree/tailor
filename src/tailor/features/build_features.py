import pandas as pd
from tailor.data import group_by


def build(df):
    '''Build new features'''

    df = weeks_on_sale(df)
    df = expand_date_info(df)
    return df


def get_performance_measures(dataframe, column, characteristic):
    '''Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic'''

    filtered_dataframe = dataframe[dataframe[column] == characteristic]
    grouped_dataframe = group_by.attribute(filtered_dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]


def weeks_on_sale(df):
    '''Calculate weeks an article has been on sale'''

    df['weeks_on_sale'] = df.apply(lambda row: days_to_week(row['time_on_sale']), axis=1)
    return df


def days_to_week(days):
    return days // 7


def meteor_season(month):
    '''return meteorological season'''

    if 2 < month < 6:
        return 'spring'
    elif 5 < month < 9:
        return 'summer'
    elif 8 < month < 12:
        return 'fall'
    else:
        return 'winter'


def expand_date_info(df):
    '''Calculate the weekday, month and actual season'''

    season = list()
    weekday = list()
    months = list()

    # three different functions therefore faster than three separate .apply()
    for i in df.transaction_date:
        month = i.month
        season.append(meteor_season(month))
        months.append(month)
        weekday.append(i.weekday())

    df['season_buy'] = pd.Series(season, index=df.index)
    df['month'] = pd.Series(months, index=df.index)
    df['weekday'] = pd.Series(weekday, index=df.index)
    return df
