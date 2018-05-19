# -*- coding: utf-8 -*-
import click
import pandas as pd
import pysftp
import os
import os.path

from dotenv import find_dotenv, load_dotenv

from tailor import data
from tailor import features


@click.command()
def main():
    """ Runs data processing scripts to download data and turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    process_data()


def download_data():
    host = os.getenv("TAILORIT_SERVER_ADDRESS")
    username = os.getenv("TAILORIT_USER")
    password = os.getenv("TAILORIT_PW")

    HOST_DIR = 'incoming'
    HOST_FILE = 'courseData.csv'

    # Don't require server to be in ~/.ssh/known_hosts
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    if not os.path.exists(data.RAW_DATA_PATH):
        os.makedirs(data.RAW_DATA_PATH)

    print('Downloading data...')
    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        with sftp.cd(HOST_DIR):                        # temporarily chdir to public
            sftp.get(HOST_FILE, data.RAW_DATA_FILE)    # get a remote file

    print('Successfully downloaded data to', data.RAW_DATA_FILE)


def process_data():
    if os.path.isfile(data.RAW_DATA_FILE) is False:
        download_data()

    print('Processing data...')
    df = data.load_csv()
    df = data.transform_datatypes(df)
    df = features.build(df)

    if not os.path.exists(data.PROCESSED_DATA_PATH):
        os.makedirs(data.PROCESSED_DATA_PATH)

    pd.to_pickle(df, data.PROCESSED_DATA_FILE)
    print('Sucessfully processed data and written to', data.PROCESSED_DATA_FILE)


if __name__ == '__main__':
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
