from pathlib import Path
import pandas as pd


def load_raw_dataframe():
    PROJECT_DIR = str(Path(__file__).resolve().parents[3])
    RAW_DATA_DIR = '/data/raw/'
    RAW_DATA_FILE = 'data.csv'
    raw_dataframe = load_dataframe(PROJECT_DIR + RAW_DATA_DIR + RAW_DATA_FILE)

    return raw_dataframe


def load_dataframe(FILE_PATH):
    dataframe = pd.read_csv(FILE_PATH, encoding='iso-8859-1')

    return dataframe


def main():
    return

if __name__ == '__main__':
    main()
