import datetime
import logging

import requests
from connections import get_spacetrack_login
from psycopg2.extras import execute_values
from skyfield.api import EarthSatellite, load


def insert_records(
    record,
    timescale,
    cursor,
    constellation,
    is_supplemental,
    source,
    is_current_number,
):
    name = record["OBJECT_NAME"]
    tle_line_1 = record["TLE_LINE1"]
    tle_line_2 = record["TLE_LINE2"]

    rcs_size = record.get("RCS_SIZE", None)
    launch_date = record.get("LAUNCH_DATE", None)
    decay_date = record.get("DECAY_DATE", None)
    object_id = record.get("OBJECT_ID", None)
    object_type = record.get("OBJECT_TYPE", None)

    satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=timescale)
    current_date_time = datetime.datetime.now(datetime.timezone.utc)
    # add satellite to database if it doesn't already exist
    sat_to_insert = (
        satellite.model.satnum,
        name,
        constellation,
        current_date_time,
        current_date_time,
        rcs_size,
        launch_date,
        decay_date,
        object_id,
        object_type,
        is_current_number,
        str(satellite.model.satnum),
        name,
    )

    satellite_insert_query = """ WITH e AS(
    INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION,
    DATE_ADDED, DATE_MODIFIED, RCS_SIZE, LAUNCH_DATE, DECAY_DATE, OBJECT_ID,
    OBJECT_TYPE, HAS_CURRENT_SAT_NUMBER)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (SAT_NUMBER, SAT_NAME) DO UPDATE SET
        DECAY_DATE = EXCLUDED.DECAY_DATE,
        OBJECT_ID = EXCLUDED.OBJECT_ID,
        OBJECT_TYPE = EXCLUDED.OBJECT_TYPE,
        RCS_SIZE = EXCLUDED.RCS_SIZE,
        LAUNCH_DATE = EXCLUDED.LAUNCH_DATE,
        DATE_MODIFIED = EXCLUDED.DATE_MODIFIED
    RETURNING id)
    SELECT * FROM e
    UNION ALL
    (SELECT id FROM satellites WHERE SAT_NUMBER=%s AND SAT_NAME=%s);"""
    cursor.execute(satellite_insert_query, sat_to_insert)
    sat_id = cursor.fetchone()[0]

    # update all other satellites with the same sat_number
    update_query = """
        UPDATE satellites
        SET HAS_CURRENT_SAT_NUMBER = FALSE,
            DATE_MODIFIED = %s
        WHERE SAT_NUMBER = %s
        AND id != %s
        """

    params = (current_date_time, satellite.model.satnum, sat_id)
    cursor.execute(update_query, params)

    if cursor.rowcount == 0:
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tnew satellite: {satellite.model.satnum}")

    # make sure this satellite has the correct has_current_sat_number value
    # only allow data from space-track to update this value, celestrak has
    # had a few instances of name changes outside of preliminary names
    if is_current_number and source == "spacetrack":
        update_query = """
            UPDATE satellites
            SET HAS_CURRENT_SAT_NUMBER = TRUE,
            DATE_MODIFIED = %s
        WHERE id = %s
        """
        params = (current_date_time, sat_id)
        cursor.execute(update_query, params)

    # add TLE to database
    tle_insert_query = """
    INSERT INTO tle_partitioned (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2, \
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


def insert_archival_tles(
    records, timescale, cursor, connection, constellation, is_supplemental, source
):
    batch_size = 1000
    tle_values = []
    for i, record in enumerate(records):

        name = record["OBJECT_NAME"]
        tle_line_1 = record["TLE_LINE1"]
        tle_line_2 = record["TLE_LINE2"]

        rcs_size = record.get("RCS_SIZE", None)
        launch_date = record.get("LAUNCH_DATE", None)
        decay_date = record.get("DECAY_DATE", None)
        object_id = record.get("OBJECT_ID", None)
        object_type = record.get("OBJECT_TYPE", None)

        satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=timescale)
        current_date_time = datetime.datetime.now(datetime.timezone.utc)

        check_query = """
         SELECT EXISTS (
            SELECT 1 FROM satellites
            WHERE sat_number = %s OR sat_name = %s
            ) as exists_either;
        """
        cursor.execute(check_query, (satellite.model.satnum, name))
        exists_either = cursor.fetchone()[0]
        is_current_number = (
            not exists_either
        )  # can be true only if completely new satellite

        sat_to_insert = (
            satellite.model.satnum,
            name,
            constellation,
            current_date_time,
            current_date_time,
            rcs_size,
            launch_date,
            decay_date,
            object_id,
            object_type,
            is_current_number,
            str(satellite.model.satnum),
            name,
        )

        satellite_insert_query = """ WITH e AS(
        INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION,
        DATE_ADDED, DATE_MODIFIED, RCS_SIZE, LAUNCH_DATE, DECAY_DATE, OBJECT_ID,
        OBJECT_TYPE, HAS_CURRENT_SAT_NUMBER)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (SAT_NUMBER, SAT_NAME) DO NOTHING
        RETURNING id)
        SELECT * FROM e
        UNION ALL
        (SELECT id FROM satellites WHERE SAT_NUMBER=%s AND SAT_NAME=%s);"""
        cursor.execute(satellite_insert_query, sat_to_insert)
        sat_id = cursor.fetchone()[0]

        if cursor.rowcount == 0:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{log_time}\tnew satellite: {satellite.model.satnum}")

        # make sure this satellite gets committed to the database
        connection.commit()

        tle_values.append(
            (
                sat_id,
                current_date_time,
                tle_line_1,
                tle_line_2,
                satellite.epoch.utc_datetime(),
                is_supplemental,
                source,
            )
        )

        if len(tle_values) >= batch_size:
            execute_values(
                cursor,
                """
                INSERT INTO tle_partitioned (sat_id, date_collected,
                tle_line1, tle_line2,cepoch, is_supplemental, data_source)
                VALUES %s
                ON CONFLICT (sat_id, epoch, data_source) DO NOTHING
                """,
                tle_values,
            )
            tle_values = []
            print(f"TLEs added: {i}")
            connection.commit()

    if len(tle_values) > 0:
        execute_values(
            cursor,
            """
            INSERT INTO tle_partitioned (sat_id, date_collected, tle_line1, tle_line2,
                            epoch, is_supplemental, data_source)
            VALUES %s
            ON CONFLICT (sat_id, epoch, data_source) DO NOTHING
            """,
            tle_values,
        )
        print(f"Final TLEs added: {len(tle_values)}")
        connection.commit()


# Parse TLE list and add entries to database if they don't exist
def add_tle_list_to_db(
    tle,
    constellation,
    cursor,
    connection,
    is_supplemental,
    source,
    is_current_number,
    is_archival,
):
    tle_count = 0
    if source == "celestrak":
        lines = tle.text.splitlines()
        counter = 0
        text_end = len(lines)
        ts = load.timescale()

        while counter < text_end - 2:
            record = {}

            record["OBJECT_NAME"] = lines[counter].strip()
            record["TLE_LINE1"] = lines[counter + 1]
            record["TLE_LINE2"] = lines[counter + 2]

            insert_records(
                record,
                ts,
                cursor,
                constellation,
                is_supplemental,
                source,
                is_current_number,
            )
            counter += 3
            tle_count += 1
    elif source == "spacetrack":
        tle_json = tle.json()
        ts = load.timescale()
        if is_archival:
            insert_archival_tles(
                tle_json,
                ts,
                cursor,
                connection,
                constellation,
                is_supplemental,
                source,
            )
            tle_count += len(tle_json)
        else:
            for record in tle_json:
                insert_records(
                    record,
                    ts,
                    cursor,
                    constellation,
                    is_supplemental,
                    source,
                    is_current_number,
                )
                tle_count += 1

    log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{log_time}\tTLE source: {source}")
    logging.info(f"{log_time}\tConstellation: {constellation}")
    logging.info(f"{log_time}\tSupplemental: {is_supplemental}")
    logging.info(f"{log_time}\tTLEs added: {tle_count}")


def get_celestrak_general_tles(cursor, connection):
    # open each response and read in 3 lines at a time
    groups = ["starlink", "oneweb", "geo", "active"]
    for group in groups:
        tle = requests.get(
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=%s&FORMAT=tle"  # noqa: UP031
            % group,
            timeout=10,
        )
        tle.raise_for_status()
        try:
            constellation = (
                group if (group == "starlink" or group == "oneweb") else "other"
            )
            add_tle_list_to_db(tle, constellation, cursor, "false", "celestrak", True)
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()


def get_celestrak_supplemental_tles(cursor, connection):
    constellations = ["starlink", "oneweb"]
    for constellation in constellations:
        tle = requests.get(
            "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php"  # noqa: UP031
            "?FILE=%s&FORMAT=tle" % constellation,
            timeout=10,
        )
        tle.raise_for_status()
        try:
            add_tle_list_to_db(tle, constellation, cursor, "true", "celestrak", True)
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()


def get_spacetrack_tles(cursor, connection):
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
        tle = session.get(
            "https://www.space-track.org/basicspacedata/query/class/gp/decay_date/null-val/epoch/%3Enow-30/orderby/norad_cat_id/format/json",
            timeout=60,
        )
        try:
            add_tle_list_to_db(tle, "", cursor, "false", "spacetrack", True)
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()
