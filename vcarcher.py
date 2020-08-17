import sys
import requests
import argparse
import logging
from lxml import etree
import json
import time
import datetime
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

from helpers import api

def creds_expire_days_warning():
    creds = api.VeracodeAPI().get_creds()
    exp = datetime.datetime.strptime(creds['expiration_ts'], "%Y-%m-%dT%H:%M:%S.%f%z")
    delta = exp - datetime.datetime.now().astimezone() #we get a datetime with timezone...
    if (delta.days < 7):
        print('These API credentials expire ', creds['expiration_ts'])

def generate(period,from_date, to_date,scan_type):
    params = {}

    # parse args
    if period == 'last-day':
        period = 'yesterday'
    elif period == 'last-week':
        period = 'last_week'
    elif period == 'last-month':
        period = 'last_month'
    elif period == 'all-time':
        period = None
        
    if period == 'range':
        period = None
        if not(from_date==None):
            params['from_date'] = from_date
        if not(to_date==None):
            params['to_date'] = to_date

    if not(period==None):
        params['period'] = period

    if not(scan_type==None):
        params['scan_type'] = scan_type

    if params=={}:
        paramsobject = None
    else:
        paramsobject = params

    # Initiate the Archer report generation job with provided parameters, returns a token
    requestdata = api.VeracodeAPI().generate_archer(payload=paramsobject)

    return gettoken(requestdata)

def gettoken(requestdata):
    # processes the response to generatearcherreport.do to identify the token to retrieve the archer job
    archerroot = etree.fromstring(requestdata)
    attribs = archerroot.attrib
    return archerroot.get('token')
    

def downloadreport(token):
    # this will retry until the report is ready, with a 15 second wait between retries
    response = api.VeracodeAPI().download_archer(token)

    # handle case where response is empty
    if (reportlength(response) == 0):
        return None

    return response

def cleanup(report):
    # selectively manually urldecode some stuff in the header; we don't want to urldecode the whole payload
    report = report.replace("http&#x3a;&#x2f;&#x2f;","http://")
    report = report.replace("https&#x3a;&#x2f;&#x2f;","https://")
    report = report.replace("com&#x2f;","com/")
    report = report.replace("&#x2f;2001&#x2f;","/2001/")
    report = report.replace("schema&#x2f;2.0&#x2f;","schema/2.0/")
    report = report.replace("resource&#x2f;2.0&#x2f;","resource/2.0/")
    return report

def reportlength(response):
    responseroot = etree.fromstring(response)
    numentries = len(responseroot)
    return numentries

def writereportfile(report):
    f = open("archerreport.xml","w")
    f.write(report)
    f.close()
    print("Wrote report to archerreport.xml containing",reportlength(report.encode()),"entries")
    return 

def main():
    parser = argparse.ArgumentParser(
        description='This script adds the Security Labs User role for existing users. It can operate on one user '
                    'or all users in the account.')
    parser.add_argument('-i', '--interval', required=False, help='Interval over which to import data. Options: last-day (default), last-week, last-month, all-time, range.',default='last-week')
    parser.add_argument('-f', '--from_date', required=False, help='The date (mm-dd-yyyy) on which to begin the import range. Required if -i is "range."')
    parser.add_argument('-t', '--to_date', required=False, help='The date (mm-dd-yyyy) on which to end the import range. Required if -i is "range."')
    parser.add_argument('-s', '--scan_type', required=False, help='The scan type to import. Options: static, dynamic, manual.')
    args = parser.parse_args()

    period = args.interval
    from_date = args.from_date
    to_date = args.to_date
    scan_type = args.scan_type

    logging.basicConfig(filename='vcarcher.log',
                        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S%p',
                        level=logging.INFO)

    # CHECK FOR CREDENTIALS EXPIRATION
    creds_expire_days_warning()

    token=None

    # cache token 
    print("Generating the Archer report")
    token = generate(period, from_date, to_date, scan_type)

    if token == 0:
        logging.error("Error generating report. Got a 0 token\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n"
                        .format(period,from_date,to_date,scan_type))
        return

    logging.debug("Got token:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n{}\r\n"
                        .format(token,period,from_date,to_date,scan_type))

    # wait
    time.sleep(5)

    # call downloadarcherreport.do
    print("Downloading the Archer report for token",token)
    report = downloadreport(token)

    if report == None:
        logging.warning("No entries in Archer report for this time period:\r\n{}\r\n{}\r\n{}\r\n\r\n{}\r\n"
                        .format(period,from_date,to_date,scan_type))
        return
    else:
        # clean up report - urldecode header
        reportdecode = cleanup(report.decode('utf-8'))
        # write to file
        writereportfile(reportdecode)

if __name__ == '__main__':
    main()