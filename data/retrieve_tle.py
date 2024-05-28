#!/usr/bin/env python

"""This script retrieves TLEs from celestrak.com and space-track.org and saves them
to a PostgreSQL database. It can be run in one of two modes: either once per day to
retrieve the daily TLEs, or once per hour to retrieve the supplemental TLEs. The script
should be run with the following command line arguments:
    -m, --mode: Determines which TLEs to download and save: use "gp" for daily TLEs,
                "sup" for supplemental TLEs.
    -s, --server: Host name of the PostgreSQL server to connect to.
    -p, --port: Port number of the PostgreSQL server to connect to.
    -d, --database: Name of the PostgreSQL database to save the TLEs to.
    -u, --user: PostgreSQL username with rights to make changes to the database.
    -pw, --password: PostgreSQL password.
    -sc, --source: Source of the TLEs: use "celestrak" for celestrak.com, "spacetrack"
                for space-track.org.
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
    # define the logging info
    logging.basicConfig(
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="Retrieve TLEs")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help='Determines which TLEs to download and save: use "gp" for daily TLEs, \
                "sup" for supplemental TLEs. Daily TLEs are meant to be retreived once \
                per day, supplemental TLEs are meant to be retreived hourly.',
        required=False,
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
    parser.add_argument(
        "-sc",
        "--source",
        type=str,
        help="Source of the TLEs: use 'celestrak'\
              for celestrak.com, 'spacetrack' for space-track.org.",
        required=True,
    )

    args = parser.parse_args()
    log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if args.mode:
        logging.info(log_time + "\t" + "Mode: " + args.mode)

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

    ######################
    # CELESTRAK
    ######################
    if args.source.upper() == "CELESTRAK":
        # check if the server is up
        response = os.system("ping -c 1 celestrak.com")  # noqa: S605, S607
        log_time = datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if response == 1:
            logging.error(log_time + "\t" + "Server not pingable. Exiting...")
            sys.exit()

        else:
            logging.info(log_time + "\t" + "Server ping successful.")

        # Download and save the daily TLEs
        if args.mode.upper() == "GP":
            # open each response and read in 3 lines at a time
            groups = ["starlink", "oneweb", "geo", "active"]
            for group in groups:
                tle = requests.get(
                    "https://celestrak.org/NORAD/elements/gp.php?GROUP=%s&FORMAT=tle"  # noqa: UP031
                    % group,
                    timeout=10,
                )
                try:
                    constellation = (
                        group if (group == "starlink" or group == "oneweb") else "other"
                    )
                    add_tle_to_db(tle, constellation, cursor, "false", "celestrak")
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

        # Download and save the supplemental TLEs if any new ones have been added since
        # the last check
        if args.mode.upper() == "SUP":
            constellations = ["starlink", "oneweb"]
            for constellation in constellations:
                tle = requests.get(
                    "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php"  # noqa: UP031
                    "?FILE=%s&FORMAT=tle" % constellation,
                    timeout=10,
                )
                print(tle.url)

                try:
                    add_tle_to_db(tle, constellation, cursor, "true", "celestrak")
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

    ######################
    # SPACE-TRACK
    ######################
    elif args.source.upper() == "SPACETRACK":
        with requests.Session() as session:
            site_cred = {"identity": "email", "password": "password"}
            base_uri = "https://www.space-track.org"
            resp = session.post(base_uri + "/ajaxauth/login", data=site_cred)
            if resp.status_code != 200:
                raise requests.HTTPError(resp, "failed on login")
            tle = session.get(
                "https://www.space-track.org/basicspacedata/query/class/gp/decay_date/null-val/epoch/%3Enow-30/orderby/norad_cat_id/format/json",
                timeout=60,
            )

            try:
                add_tle_to_db(tle, "", cursor, "false", "spacetrack")
            except Exception as err:
                log_time = (
                    datetime.datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S")
                )
                logging.error(log_time + "\t" + "database ERROR:", err)
                connection.rollback()

        connection.commit()
        cursor.close()
        connection.close()


# Parse TLE list and add entries to database if they don't exist
def add_tle_to_db(tle, constellation, cursor, is_supplemental, source):
    if source == "celestrak":
        lines = tle.text.splitlines()
        counter = 0
        text_end = len(lines)
        ts = load.timescale()

        while counter < text_end - 2:
            name = lines[counter].strip()
            tle_line_1 = lines[counter + 1]
            tle_line_2 = lines[counter + 2]
            insert_records(
                name,
                tle_line_1,
                tle_line_2,
                ts,
                cursor,
                constellation,
                is_supplemental,
                source,
            )
            counter += 3
    elif source == "spacetrack":
        tle_json = tle.json()
        ts = load.timescale()
        for record in tle_json:
            name = record["OBJECT_NAME"]
            tle_line_1 = record["TLE_LINE1"]
            tle_line_2 = record["TLE_LINE2"]
            insert_records(
                name,
                tle_line_1,
                tle_line_2,
                ts,
                cursor,
                constellation,
                is_supplemental,
                source,
            )


def insert_records(
    name,
    tle_line_1,
    tle_line_2,
    timescale,
    cursor,
    constellation,
    is_supplemental,
    source,
):
    satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=timescale)
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
    SELECT * FROM e
    UNION ALL
    (SELECT id FROM satellites WHERE SAT_NUMBER=%s order by date_added desc);"""
    cursor.execute(satellite_insert_query, sat_to_insert)
    sat_id = cursor.fetchone()[0]

    # add TLE to database
    tle_insert_query = """
    INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2, \
        EPOCH, IS_SUPPLEMENTAL, DATA_SOURCE) VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING;"""
    record_to_insert = (
        sat_id,
        current_date_time,
        tle_line_1,
        tle_line_2,
        satellite.epoch.utc_datetime(),
        is_supplemental,
        source,
    )

    cursor.execute(tle_insert_query, record_to_insert)


if __name__ == "__main__":
    main()
