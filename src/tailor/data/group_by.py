def weeks_on_sale(df):
    ''' Return dataframe which is grouped by weeks_on_sale'''

    # Select groupers (include categorical features to not drop them)
    groupers = df.select_dtypes(['category']).columns.tolist()
    groupers.append('weeks_on_sale')

    # Don't group by date data
    groupers.remove('month')
    groupers.remove('weekday')
    groupers.remove('season_buy')

    # Group dataframe and aggreagate with mean
    df = df.groupby(by=groupers, as_index=False, sort=False, observed=True).mean()

    # Weeks_on_sale is the new time_on_sale
    df = df.drop('time_on_sale', axis=1).rename({'weeks_on_sale': 'time_on_sale'}, axis=1)

    return df


def attribute(dataframe, attribute, mean=False):
    if(mean):
        return dataframe.groupby(attribute, as_index=False).mean()
    else:
        return dataframe.groupby(attribute, as_index=False).sum()
