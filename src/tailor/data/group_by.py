from pandas.core.groupby import DataFrameGroupBy


def weeks_on_sale(df):
    ''' Return dataframe which is grouped by weeks_on_sale'''

    if 'weeks_on_sale' not in df.columns:
        raise ValueError("Cannot group on 'weeks_on_sale', not a column")

    # Select groupers (include categorical features to not drop them)
    groupers = df.select_dtypes(['category']).columns.tolist()
    groupers.append('weeks_on_sale')

    # Don't group by date data
    groupers.remove('weekday')
    groupers.remove('season_buy')

    # Group dataframe and aggreagate with mean
    df = df.groupby(by=groupers, as_index=False, sort=False, observed=True).mean()

    # Weeks_on_sale is the new time_on_sale
    df = df.drop('time_on_sale', axis=1).rename({'weeks_on_sale': 'time_on_sale'}, axis=1)

    return df


def feature(df, feature, aggregation_function=DataFrameGroupBy.mean):
    ''' Groups dataframe by the characteristic of a given feature'''

    if feature not in df.columns:
        raise ValueError("Cannot group on '{0}', not a column".format(feature))

    groups = df.groupby(by=[feature, 'time_on_sale'], as_index=False, sort=False)

    return aggregation_function(groups)
