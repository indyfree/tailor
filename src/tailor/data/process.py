import pandas as pd


def drop_invalid_rows(df):

    # Negative sells price does not make sense, drop them
    invalid = df[df.sells_price < 0].index
    df.drop(invalid, inplace=True)

    print("Dropped", len(invalid), "invalid rows")

    return df


def fill_missing_values(df):
    '''
    Not all articles have values defined for the whole time_on_sale range.
    Fill the missing values with 0 values.
    '''

    print("Add missing time_on_sale values")

    # Save categorical values per article_id beforehand
    groupers = df.select_dtypes(['category']).columns.tolist()
    article_cats = df.groupby(by=groupers, as_index=False, observed=True).mean()
    article_cats = article_cats.select_dtypes(['category'])

    df.set_index(['article_id', 'time_on_sale'], inplace=True)

    # Create MultiIndex with all article_ids and all 26 time on sale values
    ids = df.index.levels[0].tolist()
    tos = pd.RangeIndex(26).tolist()  # Week 0 - Week 25
    idx = pd.MultiIndex.from_product([ids, tos], names=['article_id', 'time_on_sale'])

    # Reindex and fill values for previously indefined time_on_sale rows with 0
    df = df.reindex(idx, fill_value=0).reset_index()
    df = df.select_dtypes(exclude=['category'])
    df['article_id'] = df['article_id'].astype('category')

    return df.merge(article_cats, on='article_id', how='inner')


def normalize(df):
    '''
    Normalize the target features by using the standardized moment, that is by
    diving by the standard deviation. This is particulary useful at comparing
    different time series, as e.g. the sells of different articles over time.
    '''

    print("Normalize data with standard deviation")

    for a in df['article_id'].unique():
        df.loc[df.article_id == a, 'norm_article_count'] = df.loc[df.article_id == a, 'article_count'] / df.loc[df.article_id == a, 'article_count'].std()
        df.loc[df.article_id == a, 'norm_avq'] = df.loc[df.article_id == a, 'avq'] / df.loc[df.article_id == a, 'avq'].std()
        df.loc[df.article_id == a, 'norm_revenue'] = df.loc[df.article_id == a, 'revenue'] / df.loc[df.article_id == a, 'revenue'].std()

    return df


def order_columns(df):
    # Bring columns in senseful order
    columns = ['article_id', 'time_on_sale', 'original_price', 'discount', 'markdown', 'sells_price', 'stock_total', 'avq',
               'norm_avq', 'article_count', 'norm_article_count', 'revenue', 'norm_revenue', 'brand', 'color', 'Abteilung',
               'WHG', 'WUG', 'month', 'season']
    df = df[columns]
    return df


def transform_datatypes(df):
    '''Transform the raw data and returns a dataframe with correct dataypes'''

    print("Transforming datatypes")
    # Set article_id as category despite it's beeing a number
    df['article_id'] = df['article_id'].astype('category')

    # Set dates as type datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['markdown_start_date'] = pd.to_datetime(df['markdown_start_date'])
    # Replace 'infity' date with computable date in the future
    df.loc[df.markdown_end_date == '9999-12-31', 'markdown_end_date'] = '2018-12-31'
    df['markdown_end_date'] = pd.to_datetime(df['markdown_end_date'])

    # Set all other types as categories
    df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).apply(lambda x: x.astype('category'))

    return df
