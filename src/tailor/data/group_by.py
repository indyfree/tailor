def weeks_on_sale(df):
    ''' Return dataframe which is grouped by weeks_on_sale'''

    # Select groupers
    groupers = df.select_dtypes(['category']).columns.tolist()
    groupers.append('weeks_on_sale')

    # Group dataframe by categories, which are all the same for an article, and weeks on sale
    grouped = df.groupby(by=groupers,as_index=False, sort=False, observed=True)

    # Aggregate numeric values by mean and drop meaningless time on sale
    df = grouped.mean().drop(columns=['time_on_sale'])
    return df
