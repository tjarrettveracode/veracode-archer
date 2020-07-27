import sys
import requests
import argparse
import logging
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from helpers import api

def main():
    parser = argparse.ArgumentParser(
        description='This script adds the Security Labs User role for existing users. It can operate on one user '
                    'or all users in the account.')
    """ parser.add_argument('-u', '--user_id', required=False, help='User ID (GUID) to update. Ignored if --all is specified.')
    parser.add_argument('-l', '--all', required=False, help='Set to TRUE to update all users.', default=False)
    args = parser.parse_args() """

    logging.basicConfig(filename='vcarcher.log',
                        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S%p',
                        level=logging.INFO)

    count=0

    # parse arguments

    # if all

    # if last-day, last-week, last month

    # if range

    # handle analysis type

    # construct arguments

    # call generatearcherreport.do

    # cache token 

    # wait

    # call downloadarcherreport.do

    print("Downloaded Archer report")

if __name__ == '__main__':
    main()