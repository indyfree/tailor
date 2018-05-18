import pandas as pd

import tailor
from tailor import features


def load_data():
    '''Loads the raw data and returns a dataframe with formatted columns'''

    df = load_csv()

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

    # Build new features
    df = features.build(df)

    return df


def load_csv():
    RAW_DATA_FILE = tailor.PROJECT_DIR + '/data/raw/data.csv'

    return pd.read_csv(RAW_DATA_FILE, encoding='iso-8859-1')
