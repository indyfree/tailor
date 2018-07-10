import numpy as np
from pandas.core.groupby import DataFrameGroupBy


def weeks_on_sale(df):
    ''' Return dataframe which is grouped by weeks_on_sale'''

    if 'weeks_on_sale' not in df.columns:
        raise ValueError("Cannot group on 'weeks_on_sale', not a column")

    # Select groupers (include categorical features to not drop them)
    groupers = df.select_dtypes(['category']).columns.tolist()
    groupers.append('weeks_on_sale')

    # Group dataframe and aggreagate with respective measures
    grouped = df.groupby(by=groupers, as_index=False, sort=False, observed=True)
    df = grouped.agg({'original_price': np.max,
                      'discount': lambda x: np.mean(x[x > 0]),
                      'markdown': lambda x: np.mean(x[x > 0]),
                      'stock_total': np.max,
                      'article_count': np.sum,
                      'revenue': np.sum,
                      # avq is the mean of all (non-added, zero) values
                      'avq': lambda x: np.mean(x[x > 0])})

    # Recalculate the sales price according to formular to eliminate negative sales prices and establish data consistency
    df['sells_price'] = df.apply(lambda row: (row['original_price'] - row['discount'] - row['markdown']), axis=1)

    # Weeks_on_sale is the new time_on_sale
    df = df.rename({'weeks_on_sale': 'time_on_sale'}, axis=1)

    #
    # Aesthetics
    #

    # Reorder columns
    columns = ['article_id', 'time_on_sale', 'original_price', 'discount', 'markdown', 'sells_price', 'stock_total', 'avq',
               'article_count', 'revenue', 'brand', 'color', 'Abteilung', 'WHG', 'WUG', 'month', 'season']
    df = df[columns]

    # Round values
    df['avq'] = df.avq.round(decimals=2)
    df['revenue'] = df.revenue.round(decimals=0)

    return df


def feature(df, feature, aggregation_function=DataFrameGroupBy.mean):
    ''' Groups dataframe by the characteristic of a given feature'''

    if feature not in df.columns:
        raise ValueError("Cannot group on '{0}', not a column".format(feature))

    groups = df.groupby(by=[feature, 'time_on_sale'], as_index=False, sort=True, observed=True)

    return aggregation_function(groups)
