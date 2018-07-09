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
                      # TODO: calculate discount price, data is inconsistent now
                      'discount': np.max,
                      'markdown': np.max,
                      'sells_price': lambda x: np.min(x[x > 0]),
                      'stock_total': np.max,
                      'article_count': np.sum,
                      'revenue': np.sum,
                      'avq': lambda x: np.mean(x[x > 0])})

    # Weeks_on_sale is the new time_on_sale
    df = df.rename({'weeks_on_sale': 'time_on_sale'}, axis=1)

    return df


def feature(df, feature, aggregation_function=DataFrameGroupBy.mean):
    ''' Groups dataframe by the characteristic of a given feature'''

    if feature not in df.columns:
        raise ValueError("Cannot group on '{0}', not a column".format(feature))

    groups = df.groupby(by=[feature, 'time_on_sale'], as_index=False, sort=True, observed=True)

    return aggregation_function(groups)
