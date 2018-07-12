from . import group_by # noqa
from .load import load_data # noqa
from .load import load_csv # noqa
from .make_dataset import process_data # noqa
from .make_dataset import download_data # noqa
from .process import drop_invalid_rows # noqa
from .process import fill_missing_values # noqa
from .process import normalize # noqa
from .process import order_columns # noqa
from .process import transform_datatypes # noqa

from pathlib import Path

# Constants
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
RAW_DATA_PATH = PROJECT_DIR + '/data/raw'
RAW_DATA_FILE = RAW_DATA_PATH + '/data.csv'
PROCESSED_DATA_PATH = PROJECT_DIR + '/data/processed'
PROCESSED_DATA_FILE = PROCESSED_DATA_PATH + '/data.pkl'
