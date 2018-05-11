def group_dataframe_by_attribute(dataframe, attribute, mean=False):
    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()


'''
Summarize sells, revenue and avq for every time_on_sale value for any feature characteristic
'''


def summarize_performance_measures_for_feature_characteristic(dataframe, column_name_of_feature, feature_characteristic):
    dataframe = dataframe[dataframe[column_name_of_feature] == feature_characteristic]
    grouped_dataframe = group_dataframe_by_attribute(dataframe, 'time_on_sale')

    return grouped_dataframe[['time_on_sale', 'revenue', 'avq', 'article_count']]
