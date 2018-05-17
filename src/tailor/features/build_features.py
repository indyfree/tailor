def build(df):
    '''Build new features'''
    df = weeks_on_sale(df)
    return df


def get_performance_measures(dataframe, column, characteristic):
    '''Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic'''

    filtered_dataframe = dataframe[dataframe[column] == characteristic]
    grouped_dataframe = group(filtered_dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]


def group(dataframe, attribute, mean=False):
    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()


def weeks_on_sale(df):
    '''Calculate weeks an article has been on sale'''

    df['weeks_on_sale'] = df.apply(lambda row: days_to_week(row['time_on_sale']), axis=1)
    return df


def days_to_week(days):
    return days // 7
