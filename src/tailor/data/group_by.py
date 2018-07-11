import numpy as np
from pandas.core.groupby import DataFrameGroupBy


def weeks_on_sale(df):
    ''' Return dataframe which is grouped by weeks_on_sale'''

    if 'weeks_on_sale' not in df.columns:
        raise ValueError("Cannot group on 'weeks_on_sale', not a column")

    print("Group time_on_sale to weeks and recalculate values")

    # Select groupers (include categorical features to not drop them)
    groupers = df.select_dtypes(['category']).columns.tolist()
    groupers.append('weeks_on_sale')

    # Group dataframe and aggreagate with respective measures
    grouped = df.groupby(by=groupers, as_index=False, sort=False, observed=True)

    df = grouped.agg({'original_price': np.mean,
                      'markdown': np.mean,
                      'stock_total': np.max,
                      'article_count': np.sum,
                      'revenue': np.sum,
                      'avq': np.mean})

    # Recalculate the sells price from revenue and article_count
    df['sells_price'] = df.apply(lambda x: x.revenue / x.article_count, axis=1).round(decimals=2)

    # Recalculate discount according to formular for consistency
    df['discount'] = df.apply(lambda x: x.original_price - x.markdown - x.sells_price, axis=1)

    # Round avq
    df['avq'] = df.avq.round(decimals=2)

    # Weeks_on_sale is the new time_on_sale
    df = df.rename({'weeks_on_sale': 'time_on_sale'}, axis=1)

    # Bring columns in correct order again
    columns = ['article_id', 'time_on_sale', 'original_price', 'discount', 'markdown', 'sells_price', 'stock_total', 'avq',
               'article_count', 'revenue', 'brand', 'color', 'Abteilung', 'WHG', 'WUG', 'month', 'season']
    df = df[columns]

    return df


def feature(df, feature, aggregation_function=DataFrameGroupBy.mean):
    ''' Groups dataframe by the characteristic of a given feature'''

    if feature not in df.columns:
        raise ValueError("Cannot group on '{0}', not a column".format(feature))

    groups = df.groupby(by=[feature, 'time_on_sale'], as_index=False, sort=True, observed=True)

    return aggregation_function(groups)
