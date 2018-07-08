import pandas as pd


def fill_missing_values(df):
    '''
    Not all articels have values defines for the whole time_on_sale range.
    Fill the missing values with 0 values.
    '''

    print("Add missing time_on_sale values")

    # Save categorical values per article_id beforehand
    groupers = df.select_dtypes(['category']).columns.tolist()
    article_cats = df.groupby(by=groupers, as_index=False, observed=True).mean()
    article_cats = article_cats.select_dtypes(['category'])

    df.set_index(['article_id', 'time_on_sale'], inplace=True)

    # Create MultiIndex with all article_ids and all 182 time on sale values
    ids = df.index.levels[0].tolist()
    tos = pd.RangeIndex(182).tolist()
    idx = pd.MultiIndex.from_product([ids,tos], names=['article_id', 'time_on_sale'])

    # Reindex and fill values for previously indefined time_on_sale rows with 0
    df = df.reindex(idx, fill_value=0).reset_index()
    df = df.select_dtypes(exclude=['category'])
    df["article_id"] = df["article_id"].astype('category')

    return df.merge(article_cats, on='article_id', how='inner')


def transform_datatypes(df):
    '''Transform the raw data and returns a dataframe with correct dataypes'''

    print("Transforming datatypes")
    # Set article_id as category despite it's beeing a number
    df["article_id"] = df["article_id"].astype('category')

    # Set dates as type datetime
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["markdown_start_date"] = pd.to_datetime(df["markdown_start_date"])
    # Replace 'infity' date with computable date in the future
    df.loc[df.markdown_end_date == "9999-12-31", "markdown_end_date"] = "2018-12-31"
    df["markdown_end_date"] = pd.to_datetime(df["markdown_end_date"])

    # Set all other types as categories
    df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).apply(lambda x: x.astype('category'))

    return df
