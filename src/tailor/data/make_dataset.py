# -*- coding: utf-8 -*-
import click
from dotenv import find_dotenv, load_dotenv
import logging
import pysftp
import os

import tailor


@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    """ Runs data processing scripts to download data and turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('downloading raw data')
    download_data(logger)


def download_data(logger):
    host = os.getenv("TAILORIT_SERVER_ADDRESS")
    username = os.getenv("TAILORIT_USER")
    password = os.getenv("TAILORIT_PW")

    HOST_DIR = 'incoming'
    HOST_FILE = 'courseData.csv'
    LOCAL_DIR = tailor.PROJECT_DIR + '/data/raw/'
    LOCAL_FILE = 'data.csv'

    # Don't require server to be in ~/.ssh/known_hosts
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        with sftp.cd(HOST_DIR):                   # temporarily chdir to public
            sftp.get(HOST_FILE, LOCAL_DIR + LOCAL_FILE)        # get a remote file

    logger.info("successfully downloaded data")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
