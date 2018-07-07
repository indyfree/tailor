import pandas as pd


def fill_missing_values(df):
    '''
    Not all articels have values defines for the whole time_on_sale range.
    Fill the missing values with 0 values.
    '''

    # Groupby time_on_sale to get NaN for article values that does not exists
    filled = df.groupby(by=['article_id', 'time_on_sale'], as_index=True).mean()
    # Fill NaN values with zeros
    filled = filled.fillna(0).reset_index()

    # Re-add lost categorical columns if previous step
    groupers = df.select_dtypes(['category']).columns.tolist()
    # Find out categorical values per article_id
    article_cats = df.groupby(by=groupers, as_index=False, observed=True).mean()
    article_cats = article_cats.select_dtypes(['category'])

    return filled.merge(article_cats, on='article_id', how='inner')


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
