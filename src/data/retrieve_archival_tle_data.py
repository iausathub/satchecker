import argparse
import datetime
import logging
import sys
import time
from datetime import timezone

import psycopg2
import requests
from psycopg2 import OperationalError
from tle_utils import add_tle_list_to_db, get_db_login, get_spacetrack_login


def main():
    # define the logging info
    logging.basicConfig(
        level=logging.INFO,
    )
    parser = argparse.ArgumentParser(description="add archival TLEs to database")
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    end_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")

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
        log_time = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(log_time + "\t" + "Database ERROR: %s", err)
        sys.exit()

    cursor = connection.cursor()

    with requests.Session() as session:
        username, password = get_spacetrack_login()
        site_cred = {
            "identity": username,
            "password": password,
        }
        base_uri = "https://www.space-track.org"
        resp = session.post(base_uri + "/ajaxauth/login", data=site_cred)
        session.auth = (username, password)
        if resp.status_code != 200:
            raise requests.HTTPError(resp, "failed on login")

        start_date = end_date - datetime.timedelta(days=2)

        for i in range(50):
            url = f"https://www.space-track.org/basicspacedata/query/class/gp_history/EPOCH/>{start_date.strftime('%Y-%m-%d')}%2C<{end_date.strftime('%Y-%m-%d')}/OBJECT_TYPE/<>DEBRIS/orderby/EPOCH%20asc/emptyresult/show"

            print(url)
            try:
                tle = session.get(url, timeout=60)
                tle.raise_for_status()
                pass
            except Exception as err:
                log_time = datetime.datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logging.error(
                    log_time + "\t" + "Failed to get TLEs from spacetrack.org:", err
                )
                sys.exit()

            print(tle.status_code)
            if tle.status_code != 200:
                log_time = datetime.datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logging.error(
                    "%s\tFailed to get TLEs from spacetrack.org: %s",
                    log_time,
                    tle.content,
                )
                sys.exit()
            try:
                log_time = datetime.datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                add_tle_list_to_db(tle, "", cursor, "false", "spacetrack", False)
            except Exception as err:
                log_time = datetime.datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logging.error("%s\tdatabase ERROR: %s", log_time, err)
                connection.rollback()
            # Increment the dates by 3 days
            start_date -= datetime.timedelta(days=2)
            end_date -= datetime.timedelta(days=2)

            # Sleep for 2 seconds after every request to ensure no
            # more than 30 requests are made per minute
            if i % 30 == 0 and i != 0:
                time.sleep(60)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
