#!/usr/bin/env python

"""This script retrieves TLEs from celestrak.com and saves them to a PostgreSQL
database. It can be run in one of two modes: either once per day to retrieve the daily
TLEs, or once per hour to retrieve the supplemental TLEs.The script should be run with
the following command line arguments:
    -m, --mode: Determines which TLEs to download and save: use "gp" for daily TLEs,
                "sup" for supplemental TLEs.
    -h, --help: Show help message including the above info and exit.
"""

import argparse
import datetime
import json
import logging
import sys

import boto3
import psycopg2
import requests
from botocore.exceptions import ClientError
from psycopg2 import OperationalError
from skyfield.api import EarthSatellite, load


def main():
    # define the logging file
    parser = argparse.ArgumentParser(description="Retrieve TLEs from celestrak.com")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help='Determines which TLEs to download and save: use "gp" for daily TLEs, \
        "sup" for supplemental TLEs. Daily TLEs are meant to be retreived once per \
        day, supplemental TLEs are meant to be retreived hourly.',
        required=True,
    )
    args = parser.parse_args()
    log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(log_time + "\t" + "Mode: " + args.mode)

    # get database login info
    db_login = get_db_login()
    # connect to postgresql database
    try:
        connection = psycopg2.connect(
            host=db_login[2],
            port=db_login[3],
            database=db_login[4],
            user=db_login[0],
            password=db_login[1],
        )
    except OperationalError as err:
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(log_time + "\t" + "Database ERROR: %s", err)
        sys.exit()

    cursor = connection.cursor()

    # Download and save the daily TLEs
    if args.mode.upper() == "GP":
        # open each response and read in 3 lines at a time
        groups = ["starlink", "oneweb", "geo", "active"]
        for group in groups:
            tle = requests.get(
                "https://celestrak.org/NORAD/elements/gp.php?GROUP=%s&FORMAT=tle"
                % group,
                timeout=10,
            )
            try:
                constellation = (
                    group if (group == "starlink" or group == "oneweb") else "other"
                )
                add_tle_to_db(tle, constellation, cursor, "false")
            except Exception as err:
                log_time = (
                    datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
                )
                logging.error(log_time + "\t" + "database ERROR:", err)
                connection.rollback()

        connection.commit()
        cursor.close()
        connection.close()
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(log_time + "\t" + "Daily GP save successful.")

    # Download and save the supplemental TLEs if any new ones have been added
    # since the last check
    if args.mode.upper() == "SUP":
        constellations = ["starlink", "oneweb"]
        for constellation in constellations:
            tle = requests.get(
                "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=%s&FORMAT=tle"
                % constellation,
                timeout=10,
            )

            try:
                add_tle_to_db(tle, constellation, cursor, "true")
            except Exception as err:
                log_time = (
                    datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
                )
                logging.error(log_time + "\t" + "database ERROR:", err)
                connection.rollback()

        connection.commit()
        cursor.close()
        connection.close()
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(log_time + "\t" + "Hourly SUP save successful.")


# Parse TLE text file and add entries to database if they don't exist
def add_tle_to_db(tle, constellation, cursor, is_supplemental):
    lines = tle.text.splitlines()
    counter = 0
    text_end = len(lines)
    ts = load.timescale()

    while counter < text_end - 2:
        name = lines[counter].strip()
        tle_line_1 = lines[counter + 1]
        tle_line_2 = lines[counter + 2]

        satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=ts)
        current_date_time = datetime.datetime.now(datetime.timezone.utc)

        # add satellite to database if it doesn't already exist
        sat_to_insert = (
            satellite.model.satnum,
            name,
            constellation,
            current_date_time,
            current_date_time,
            str(satellite.model.satnum),
        )
        satellite_insert_query = """ WITH e AS(
        INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION,
        DATE_ADDED, DATE_MODIFIED) VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (SAT_NUMBER, SAT_NAME) DO NOTHING RETURNING id)
        SELECT * FROM e UNION SELECT id FROM satellites WHERE SAT_NUMBER=%s;"""
        cursor.execute(satellite_insert_query, sat_to_insert)
        sat_id = cursor.fetchone()[0]

        # add TLE to database
        tle_insert_query = """
        INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2, \
            EPOCH, IS_SUPPLEMENTAL, DATA_SOURCE) VALUES (%s,%s,%s,%s,%s,%s,%s) \
            ON CONFLICT (SAT_ID, EPOCH) DO NOTHING;"""
        record_to_insert = (
            sat_id,
            current_date_time,
            tle_line_1,
            tle_line_2,
            satellite.epoch.utc_datetime(),
            is_supplemental,
            "celestrak",
        )
        cursor.execute(tle_insert_query, record_to_insert)

        counter += 3


def get_db_login():
    secret_name = "satchecker-prod-db-cred"  # noqa: S105
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    if get_secret_value_response is None:
        raise Exception("No secret value response")

    secrets = json.loads(get_secret_value_response["SecretString"])
    # Decrypts secret using the associated KMS key.
    username = secrets["username"]
    password = secrets["password"]
    host = secrets["host"]
    port = secrets["port"]
    dbname = secrets["dbname"]

    return [username, password, host, port, dbname]


if __name__ == "__main__":
    main()
