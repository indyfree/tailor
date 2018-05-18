# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import pysftp
import os
import os.path

from dotenv import find_dotenv, load_dotenv

import tailor
from tailor import data
from tailor import features

RAW_DATA_FILE = tailor.PROJECT_DIR + '/data/raw/data.csv'
PROCESSED_DATA_PATH = tailor.PROJECT_DIR + '/data/processed/'


@click.command()
def main():
    """ Runs data processing scripts to download data and turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    process_data(logger)


def download_data(logger):
    host = os.getenv("TAILORIT_SERVER_ADDRESS")
    username = os.getenv("TAILORIT_USER")
    password = os.getenv("TAILORIT_PW")

    HOST_DIR = 'incoming'
    HOST_FILE = 'courseData.csv'

    # Don't require server to be in ~/.ssh/known_hosts
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    logger.info('downloading data')
    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        with sftp.cd(HOST_DIR):                   # temporarily chdir to public
            sftp.get(HOST_FILE, RAW_DATA_FILE)        # get a remote file

    logger.info("successfully downloaded data")


def process_data(df):
    if os.path.isfile(RAW_DATA_FILE) is False:
        download_data()

    df = data.load_csv()
    df = data.transform_datatypes(df)
    df = features.build(df)

    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH)

    pd.to_pickle(df, PROCESSED_DATA_PATH + '/data.pkl')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
