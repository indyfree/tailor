from pathlib import Path
import pandas as pd

PROJECT_DIR = str(Path(__file__).resolve().parents[2])
RAW_DATA_DIR = '/data/raw/'
RAW_DATA_FILE = 'data.csv'


def load_raw_dataframe(RAW_DATA_PATH):
    raw_dataframe = pd.read_csv(RAW_DATA_PATH, encoding='iso-8859-1')

    return raw_dataframe


def main():
    raw_dataframe = load_raw_dataframe(PROJECT_DIR + RAW_DATA_DIR + RAW_DATA_FILE)


if __name__ == '__main__':
    main()
