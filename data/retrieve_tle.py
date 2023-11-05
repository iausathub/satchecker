#!/usr/bin/env python

"""This script retrieves TLEs from celestrak.com and saves them to a PostgreSQL
database. It can be run in one of two modes: either once per day to retrieve the daily
TLEs, or once per hour to retrieve the supplemental TLEs. The script should be run
with the following command line arguments:
    -m, --mode: Determines which TLEs to download and save: use "gp" for daily TLEs,
                "sup" for supplemental TLEs.
    -s, --server: Host name of the PostgreSQL server to connect to.
    -p, --port: Port number of the PostgreSQL server to connect to.
    -d, --database: Name of the PostgreSQL database to save the TLEs to.
    -u, --user: PostgreSQL username with rights to make changes to the database.
    -pw, --password: PostgreSQL password.
    -h, --help: Show help message including the above info and exit.
"""

import argparse
import datetime
import logging
import os
import sys

import psycopg2
import requests
from psycopg2 import OperationalError
from skyfield.api import EarthSatellite, load


def main():
    # define the logging file
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), "SAVE_TLE_LOGFILE.txt"),
        encoding="utf-8",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="Retrieve TLEs from celestrak.com")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help='Determines which TLEs to download and save: use "gp" for daily TLEs, \
                "sup" for supplemental TLEs. Daily TLEs are meant to be retreived once \
                per day, supplemental TLEs are meant to be retreived hourly.',
        required=True,
    )
    parser.add_argument(
        "-s",
        "--server",
        type=str,
        help="Host name of the PostgreSQL server to connect to",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        help="Port number of the PostgreSQL server to connect to",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--database",
        type=str,
        help="Name of the PostgreSQL database to save the TLEs to",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        help="PostgreSQL username with rights to make changes to the database",
        required=True,
    )
    parser.add_argument(
        "-pw", "--password", type=str, help="PostgreSQL password", required=True
    )
    args = parser.parse_args()
    log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(log_time + "\t" + "Mode: " + args.mode)

    # check if the server is up
    response = os.system("ping -c 1 celestrak.com")  # noqa: S605, S607
    log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if response == 1:
        logging.error(log_time + "\t" + "Server not pingable. Exiting...")
        sys.exit()

    else:
        logging.info(log_time + "\t" + "Server ping successful.")

    # connect to postgresql database
    try:
        connection = psycopg2.connect(
            host=args.server,
            port=args.port,
            database=args.database,
            user=args.user,
            password=args.password,
        )
    except OperationalError as err:
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(log_time + "\t" + "Database ERROR: %s", err)
        sys.exit()

    cursor = connection.cursor()

    # Download and save the daily TLEs
    if args.mode.upper() == "GP":
        files = {}
        files["oneweb"] = requests.get(
            "https://celestrak.com/NORAD/elements/oneweb.txt", timeout=10
        )
        files["starlink"] = requests.get(
            "https://celestrak.org/NORAD/elements/starlink.txt", timeout=10
        )
        files["AC"] = requests.get(
            "https://celestrak.com/NORAD/elements/active.txt", timeout=10
        )
        files["GEO"] = requests.get(
            "https://celestrak.com/NORAD/elements/geo.txt", timeout=10
        )

        # go through each TLE file and save info to the database

        # open each response and read in 3 lines at a time
        for category in files:
            log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(log_time + "\t" + "Loading %s TLEs..." % category)
            constellation = (
                category
                if (category == "starlink" or category == "oneweb")
                else "other"
            )
            try:
                add_tle_to_db(files[category], constellation, cursor, "false")
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

    # Download and save the supplemental TLEs if any new ones have been added since the
    # last check
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

        # add satellite to database if it doesn't already exist
        sat_to_insert = (
            satellite.model.satnum,
            name,
            constellation,
            str(satellite.model.satnum),
        )
        satellite_insert_query = """ WITH e AS(
        INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION) VALUES (%s,%s,%s)
        ON CONFLICT (SAT_NUMBER) DO NOTHING RETURNING id)
        SELECT * FROM e UNION SELECT id FROM satellites WHERE SAT_NUMBER=%s;"""
        cursor.execute(satellite_insert_query, sat_to_insert)
        sat_id = cursor.fetchone()[0]

        # add TLE to database
        current_date_time = datetime.datetime.now(datetime.timezone.utc)
        tle_insert_query = """
        INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2, \
            EPOCH, IS_SUPPLEMENTAL) VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (SAT_ID, EPOCH) DO NOTHING;"""
        record_to_insert = (
            sat_id,
            current_date_time,
            tle_line_1,
            tle_line_2,
            satellite.epoch.utc_datetime(),
            is_supplemental,
        )
        cursor.execute(tle_insert_query, record_to_insert)

        counter += 3


if __name__ == "__main__":
    main()
