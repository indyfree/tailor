import os
import pandas as pd

from tailor import data


def load_data():
    if os.path.isfile(data.PROCESSED_DATA_FILE) is False:
        data.process_data()

    return pd.read_pickle(data.PROCESSED_DATA_FILE)


def load_csv():
    if os.path.isfile(data.RAW_DATA_FILE) is False:
        data.download_data()

    return pd.read_csv(data.RAW_DATA_FILE, encoding='iso-8859-1')
