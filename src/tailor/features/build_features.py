def group(dataframe, attribute, mean=False):
    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()


def get_performance_measures(dataframe, column, characteristic):
    '''Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic'''

    filtered_dataframe = dataframe[dataframe[column] == characteristic]
    grouped_dataframe = group(filtered_dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]
