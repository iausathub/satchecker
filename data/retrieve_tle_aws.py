#!/usr/bin/env python

"""
This script retrieves TLEs from celestrak.com and saves them to a PostgreSQL database. It can be run in one of two modes: 
either once per day to retrieve the daily TLEs, or once per hour to retrieve the supplemental TLEs. 
The script should be run with the following command line arguments:
    -m, --mode: Determines which TLEs to download and save: use "gp" for daily TLEs, "sup" for supplemental TLEs.
    -h, --help: Show help message including the above info and exit.
"""

import json
import requests
import datetime
import os
import logging
import sys
import argparse
import psycopg2
import boto3
from botocore.exceptions import ClientError
from psycopg2 import connect, OperationalError, errorcodes, errors
from skyfield.api import EarthSatellite, load

def main():

    #define the logging file
    logging.basicConfig(filename=os.path.join(os.getcwd(),'SAVE_TLE_LOGFILE.txt'), encoding='utf-8', level=logging.INFO)    

    parser = argparse.ArgumentParser(description='Retrieve TLEs from celestrak.com')
    parser.add_argument('-m', '--mode', 
                        type=str, 
                        help='Determines which TLEs to download and save: use "gp" for daily TLEs, "sup" for supplemental TLEs. Daily TLEs are meant to be retreived once per day, supplemental TLEs are meant to be retreived hourly.', 
                        required=True)
    args = parser.parse_args()
    log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(log_time + '\t' + "Mode: " + args.mode) 
    
    #check if the server is up
    #response = os.system("ping -c 1 celestrak.com")
    #log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    #if response == 1: logging.error(log_time+'\t'+"Server not pingable. Exiting..."); sys.exit()
    
    #else: logging.info(log_time + '\t' + "Server ping successful.")

    # get database login info
    db_login = get_db_login()
    # connect to postgresql database
    try:
        connection = psycopg2.connect(host=db_login[2], 
                                    port=db_login[3], 
                                    database=db_login[4], 
                                    user=db_login[0]    , 
                                    password=db_login[1])
    except OperationalError as err:
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(log_time + '\t' + "Database ERROR: %s", err)
        sys.exit()
    
    cursor = connection.cursor()
    
    # Download and save the daily TLEs
    if args.mode.upper() == 'GP':
        files = {}
        files['oneweb'] = requests.get('https://celestrak.com/NORAD/elements/oneweb.txt')
        files['starlink'] = requests.get('https://celestrak.org/NORAD/elements/starlink.txt')
        files['AC'] = requests.get('https://celestrak.com/NORAD/elements/active.txt')
        files['GEO'] = requests.get('https://celestrak.com/NORAD/elements/geo.txt')

        # go through each TLE file and save info to the database

        #open each response and read in 3 lines at a time
        for category in files:
            log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(log_time + '\t' + "Loading %s TLEs..." %category)
            constellation = category if (category == 'starlink' or category == 'oneweb') else 'other'
            try:
                add_tle_to_db(files[category], constellation, cursor, "false")
            except Exception as err:
                log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(log_time + '\t' + "database ERROR:", err)
                connection.rollback()

        connection.commit()
        cursor.close()
        connection.close()
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(log_time + '\t' + "Daily GP save successful.")

    # Download and save the supplemental TLEs if any new ones have been added since the last check
    if args.mode.upper() == 'SUP':
        constellations = ['starlink', 'oneweb']
        for constellation in constellations: 
            TLE = requests.get('https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=%s&FORMAT=tle' %constellation)
            
            try:
                add_tle_to_db(TLE, constellation, cursor, "true")
            except Exception as err:
                log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(log_time + '\t' + "database ERROR:", err)
                connection.rollback()

        connection.commit()
        cursor.close()
        connection.close()
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(log_time + '\t' + "Hourly SUP save successful.")


# Parse TLE text file and add entries to database if they don't exist
def add_tle_to_db(tle, constellation, cursor, is_supplemental):
    lines = tle.text.splitlines()
    counter = 0 
    textEnd = len(lines)
    ts = load.timescale()

    while counter < textEnd - 2:
        name = lines[counter].strip()
        tleLine1 = lines[counter+1]
        tleLine2 = lines[counter+2]

        satellite = EarthSatellite(tleLine1,tleLine2,name = name, ts = ts)

        # add satellite to database if it doesn't already exist
        sat_to_insert = (satellite.model.satnum, name, constellation, str(satellite.model.satnum))
        satellite_insert_query = """ WITH e AS( INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION) VALUES (%s,%s,%s) ON CONFLICT (SAT_NUMBER) DO NOTHING RETURNING id) 
        SELECT * FROM e UNION SELECT id FROM satellites WHERE SAT_NUMBER=%s;"""
        cursor.execute(satellite_insert_query, sat_to_insert)
        sat_id = cursor.fetchone()[0]

        # add TLE to database
        current_date_time = datetime.datetime.now(datetime.timezone.utc)
        tle_insert_query = """ INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2, EPOCH, IS_SUPPLEMENTAL) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (SAT_ID, EPOCH) DO NOTHING;"""
        record_to_insert = (sat_id, current_date_time, tleLine1, tleLine2, satellite.epoch.utc_datetime(), is_supplemental)
        cursor.execute(tle_insert_query, record_to_insert)

        counter += 3

def get_db_login():

    secret_name = "satchecker-prod-db-cred"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    if(get_secret_value_response is None):
        raise Exception("No secret value response")
    
    secrets = json.loads(get_secret_value_response['SecretString'])
    # Decrypts secret using the associated KMS key.
    username = secrets['username']
    password = secrets['password']
    host = secrets['host']
    port = secrets['port']
    dbname = secrets['dbname']

    return[username, password, host, port, dbname]
    
if __name__=='__main__':
    main()