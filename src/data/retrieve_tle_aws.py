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
import logging
import sys

import psycopg2
from connections import get_db_login
from psycopg2 import OperationalError
from satellite_utils import (
    get_decayed_satellites,
    get_ephemeris_data_from_spacetrack,
    get_starlink_generations,
)
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
            logging.info(log_time + "\t" + "Daily GP save successful.")

        # Download and save the supplemental TLEs if any new ones have been added
        # since the last check
        if args.mode.upper() == "SUP":
            get_celestrak_supplemental_tles(cursor, connection)

            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(log_time + "\t" + "Hourly SUP save successful.")

        connection.commit()
        cursor.close()
        connection.close()

    ######################
    # SPACE-TRACK
    ######################
    elif args.source.upper() == "SPACETRACK":
        get_spacetrack_tles(cursor, connection)
        get_decayed_satellites(cursor, connection)
        get_starlink_generations(cursor, connection)

        get_ephemeris_data_from_spacetrack(cursor, connection)

        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
