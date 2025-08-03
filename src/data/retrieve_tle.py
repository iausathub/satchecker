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
import sys

import psycopg2
from psycopg2 import OperationalError
from satellite_utils import get_decayed_satellites
from tle_utils import (
    get_celestrak_general_tles,
    get_celestrak_supplemental_tles,
    get_spacetrack_tles,
)


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
    log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
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
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(log_time + "\t" + "Database ERROR: %s", err)
        sys.exit()
    cursor = connection.cursor()

    ######################
    # CELESTRAK
    ######################
    if args.source.upper() == "CELESTRAK":
        # Download and save the daily TLEs
        if args.mode.upper() == "GP":
            get_celestrak_general_tles(cursor, connection)

            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(
                log_time + "\t" + "Celestrak general TLE data saved successfully."
            )

        # Download and save the supplemental TLEs if any new ones have been added since
        # the last check
        if args.mode.upper() == "SUP":
            get_celestrak_supplemental_tles(cursor, connection)

            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(
                log_time + "\t" + "Celestrak supplemental TLE data saved successfully."
            )

        connection.commit()
        cursor.close()
        connection.close()

    ######################
    # SPACE-TRACK
    ######################
    elif args.source.upper() == "SPACETRACK":
        get_spacetrack_tles(cursor, connection)
        get_decayed_satellites(cursor, connection)

        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
