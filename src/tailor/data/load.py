import pandas as pd

import tailor


# PROCESSED_DATA_FILE = tailor.PROJECT_DIR + '/data/processed/data.pkl'
def load_data():
    return null

    
#     # if os.path.isfile(PROCESSED_DATA_FILE) is False:


def load_csv():
    RAW_DATA_FILE = tailor.PROJECT_DIR + '/data/raw/data.csv'

    return pd.read_csv(RAW_DATA_FILE, encoding='iso-8859-1')
