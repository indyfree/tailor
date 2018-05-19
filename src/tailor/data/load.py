import os
import pandas as pd

from tailor import data


def load_data():
    if os.path.isfile(data.PROCESSED_DATA_FILE) is False:
        try:
            data.process_data()
        except ValueError as error:
            print(error)
            return

    return pd.read_pickle(data.PROCESSED_DATA_FILE)


def load_csv():
    if os.path.isfile(data.RAW_DATA_FILE) is False:
        try:
            data.download_data()
        except ValueError as error:
            print(error)
            return

    return pd.read_csv(data.RAW_DATA_FILE, encoding='iso-8859-1')
