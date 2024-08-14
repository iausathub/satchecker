import datetime
import logging

import requests
from connections import get_spacetrack_login


def get_decayed_satellites(cursor, connection):
    with requests.Session() as session:
        username, password = get_spacetrack_login()
        site_cred = {
            "identity": username,
            "password": password,
        }
        base_uri = "https://www.space-track.org"
        resp = session.post(base_uri + "/ajaxauth/login", data=site_cred)
        if resp.status_code != 200:
            raise requests.HTTPError(resp, "failed on login")

        decayed_satellites = session.get(
            "https://www.space-track.org/basicspacedata/query/class/satcat_change/PREVIOUS_DECAY/null-val/CURRENT_DECAY/%3C%3Enull-val/orderby/CHANGE_MADE%20desc/format/json",
            timeout=60,
        )

        try:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{log_time}\tUpdating decayed satellites...")
            update_decayed_satellites(decayed_satellites, cursor)
            connection.commit()
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()


def update_decayed_satellites(decayed_satellites, cursor):
    decayed_satellites = decayed_satellites.json()
    for sat in decayed_satellites:
        try:
            current_date_time = datetime.datetime.now(datetime.timezone.utc)

            decay_date = sat.get("CURRENT_DECAY", None)
            sat_name = sat.get("CURRENT_NAME", None)
            sat_number = int(sat.get("NORAD_CAT_ID", None))
            query = """
                UPDATE satellites SET DECAY_DATE = %s, DATE_MODIFIED = %s
                WHERE SAT_NAME = %s AND SAT_NUMBER = %s;
                """

            cursor.execute(query, (decay_date, current_date_time, sat_name, sat_number))
            logging.info(f"Query: {cursor.query}")
            if cursor.rowcount == 0:
                logging.warning(
                    f"Unable to update decay date for {sat_name} ({sat_number})"
                )  # noqa: E501
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            raise
