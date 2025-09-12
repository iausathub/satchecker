import datetime
import logging

import requests
from connections import get_spacetrack_login
from skyfield.api import EarthSatellite, load


def insert_record(
    record,
    timescale,
    cursor,
    constellation,
    is_supplemental,
    source,
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
    tle_epoch = satellite.epoch.utc_datetime()

    # check if satellite's object_id is 'UNKNOWN' - if so, set object_id to
    # 'UNKNOWN_' + sat_number
    if object_id == "UNKNOWN":
        object_id = f"UNKNOWN_{satellite.model.satnum}"

    # add satellite to database if it doesn't already exist
    sat_to_insert = (
        constellation,
        current_date_time,
        current_date_time,
        rcs_size,
        launch_date,
        decay_date,
        object_id,
        object_type,
        object_id,
    )
    satellite_insert_query = """ WITH e AS(
    INSERT INTO satellites (CONSTELLATION,
    DATE_ADDED, DATE_MODIFIED, RCS_SIZE, LAUNCH_DATE, DECAY_DATE, OBJECT_ID,
    OBJECT_TYPE)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (OBJECT_ID) DO UPDATE SET
        LAUNCH_DATE = CASE
            WHEN EXCLUDED.LAUNCH_DATE IS NOT NULL
                 AND satellites.LAUNCH_DATE IS DISTINCT FROM EXCLUDED.LAUNCH_DATE
            THEN EXCLUDED.LAUNCH_DATE
            ELSE satellites.LAUNCH_DATE
        END,
        DECAY_DATE = CASE
            WHEN EXCLUDED.DECAY_DATE IS NOT NULL
                 AND satellites.DECAY_DATE IS DISTINCT FROM EXCLUDED.DECAY_DATE
            THEN EXCLUDED.DECAY_DATE
            ELSE satellites.DECAY_DATE
        END,
        CONSTELLATION = CASE
            WHEN EXCLUDED.CONSTELLATION IS NOT NULL
                 AND satellites.CONSTELLATION IS DISTINCT FROM EXCLUDED.CONSTELLATION
            THEN EXCLUDED.CONSTELLATION
            ELSE satellites.CONSTELLATION
        END,
        OBJECT_TYPE = CASE
            WHEN EXCLUDED.OBJECT_TYPE IS NOT NULL
                 AND satellites.OBJECT_TYPE IS DISTINCT FROM EXCLUDED.OBJECT_TYPE
            THEN EXCLUDED.OBJECT_TYPE
            ELSE satellites.OBJECT_TYPE
        END,
        RCS_SIZE = CASE
            WHEN EXCLUDED.RCS_SIZE IS NOT NULL
                 AND satellites.RCS_SIZE IS DISTINCT FROM EXCLUDED.RCS_SIZE
            THEN EXCLUDED.RCS_SIZE
            ELSE satellites.RCS_SIZE
        END,
        DATE_MODIFIED = CASE
            WHEN (EXCLUDED.LAUNCH_DATE IS NOT NULL
                  AND satellites.LAUNCH_DATE IS DISTINCT FROM EXCLUDED.LAUNCH_DATE) OR
                 (EXCLUDED.DECAY_DATE IS NOT NULL
                  AND satellites.DECAY_DATE IS DISTINCT FROM EXCLUDED.DECAY_DATE) OR
                 (EXCLUDED.CONSTELLATION IS NOT NULL
                  AND satellites.CONSTELLATION IS DISTINCT FROM EXCLUDED.CONSTELLATION)
                  OR
                 (EXCLUDED.OBJECT_TYPE IS NOT NULL
                  AND satellites.OBJECT_TYPE IS DISTINCT FROM EXCLUDED.OBJECT_TYPE) OR
                 (EXCLUDED.RCS_SIZE IS NOT NULL
                  AND satellites.RCS_SIZE IS DISTINCT FROM EXCLUDED.RCS_SIZE)
            THEN EXCLUDED.DATE_MODIFIED
            ELSE satellites.DATE_MODIFIED
        END
    WHERE
        (EXCLUDED.LAUNCH_DATE IS NOT NULL
         AND satellites.LAUNCH_DATE IS DISTINCT FROM EXCLUDED.LAUNCH_DATE) OR
        (EXCLUDED.DECAY_DATE IS NOT NULL
         AND satellites.DECAY_DATE IS DISTINCT FROM EXCLUDED.DECAY_DATE) OR
        (EXCLUDED.CONSTELLATION IS NOT NULL
         AND satellites.CONSTELLATION IS DISTINCT FROM EXCLUDED.CONSTELLATION) OR
        (EXCLUDED.OBJECT_TYPE IS NOT NULL
         AND satellites.OBJECT_TYPE IS DISTINCT FROM EXCLUDED.OBJECT_TYPE) OR
        (EXCLUDED.RCS_SIZE IS NOT NULL
         AND satellites.RCS_SIZE IS DISTINCT FROM EXCLUDED.RCS_SIZE)
    RETURNING id, xmax = 0 as is_new)
    SELECT * FROM e
    UNION ALL
    (SELECT id, false as is_new FROM satellites WHERE OBJECT_ID=%s);
    """
    cursor.execute(satellite_insert_query, sat_to_insert)
    result = cursor.fetchone()

    sat_id = result[0] if result else None
    if sat_id is None:
        raise ValueError(f"No results returned for satellite {satellite.model.satnum}")

    is_new = result[1]

    if is_new:
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tnew satellite: {satellite.model.satnum}")

    # if the current designation (valid_to is null) has a different sat_number or
    # sat_name, set valid_to to the TLE epoch so it's no longer the current designation
    designation_update_query = """
    UPDATE satellite_designation
    SET valid_to = %s, date_modified = %s
    WHERE id = (
        SELECT id FROM satellite_designation
        WHERE sat_id = %s AND valid_to IS NULL
        AND (sat_number != %s OR sat_name != %s)
        ORDER BY valid_from DESC
        LIMIT 1
    );
    """
    designation_to_update = (
        tle_epoch,
        current_date_time,
        sat_id,
        satellite.model.satnum,
        name,
    )
    cursor.execute(designation_update_query, designation_to_update)
    designation_changed = cursor.rowcount > 0

    # add designation to database if it doesn't already exist
    # set valid_from to TLE epoch, valid_to to null (only if new, don't
    # edit otherwise)
    if designation_changed:
        designation_insert_query = """
        INSERT INTO satellite_designation (sat_id, sat_name, sat_number,
        valid_from, valid_to)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (sat_number, sat_name, sat_id, valid_from, valid_to) DO NOTHING
        RETURNING id;
        """
        designation_to_insert = (
            sat_id,
            name,
            satellite.model.satnum,
            tle_epoch,
            None,
        )
        cursor.execute(designation_insert_query, designation_to_insert)
        result = cursor.fetchone()
        if result:
            designation_id = result[0]
            logging.info(
                f"Created new designation {designation_id} for satellite {sat_id}"
            )

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


# Parse TLE list and add entries to database if they don't exist
def add_tle_list_to_db(tle, constellation, cursor, connection, is_supplemental, source):
    tle_count = 0
    commit_batch_size = 100  # Commit every 100 TLEs

    try:
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
                logging.info(f"TLE count before insert_record: {tle_count}")
                insert_record(
                    record,
                    ts,
                    cursor,
                    constellation,
                    is_supplemental,
                    source,
                )
                counter += 3
                tle_count += 1
                logging.info(f"TLE count before batch size check: {tle_count}")
                # Commit periodically
                if tle_count % commit_batch_size == 0:
                    try:
                        connection.commit()
                        log_time = datetime.datetime.now(datetime.UTC).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        logging.info(
                            f"{log_time}\tCommitted batch of {commit_batch_size} "
                            f"TLEs. Total: {tle_count}"
                        )

                    except Exception as err:
                        log_time = datetime.datetime.now(datetime.UTC).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        logging.error(log_time + "\t" + "database ERROR:", err)

        elif source == "spacetrack":
            tle_json = tle.json()
            ts = load.timescale()
            for record in tle_json:
                logging.info(f"TLE count before insert_record: {tle_count}")
                insert_record(
                    record,
                    ts,
                    cursor,
                    constellation,
                    is_supplemental,
                    source,
                )
                tle_count += 1
                logging.info(f"TLE count before batch size check: {tle_count}")

                # Commit periodically
                if tle_count % commit_batch_size == 0:
                    try:
                        connection.commit()
                        log_time = datetime.datetime.now(datetime.UTC).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        logging.info(
                            f"{log_time}\tCommitted batch of {commit_batch_size} "
                            f"TLEs. Total: {tle_count}"
                        )
                    except Exception as err:
                        log_time = datetime.datetime.now(datetime.UTC).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        logging.error(log_time + "\t" + "database ERROR:", err)

        # Final commit for any remaining records
        connection.commit()
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tTLE source: {source}")
        logging.info(f"{log_time}\tConstellation: {constellation}")
        logging.info(f"{log_time}\tSupplemental: {is_supplemental}")
        logging.info(f"{log_time}\tTLEs added: {tle_count}")

    except Exception as err:
        connection.rollback()
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{log_time}\tError processing TLEs: {err}")
        raise


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
            add_tle_list_to_db(
                tle, constellation, cursor, connection, "false", "celestrak"
            )
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()


def get_celestrak_supplemental_tles(cursor, connection):
    constellations = ["starlink", "oneweb", "ast", "kuiper", "planet"]
    for constellation in constellations:
        tle = requests.get(
            "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php"  # noqa: UP031
            "?FILE=%s&FORMAT=tle" % constellation,
            timeout=10,
        )
        tle.raise_for_status()
        try:
            add_tle_list_to_db(
                tle, constellation, cursor, connection, "true", "celestrak"
            )
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
            add_tle_list_to_db(tle, "", cursor, connection, "false", "spacetrack")
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()
