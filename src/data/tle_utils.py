import datetime
import logging
import traceback

import requests
from connections import get_spacetrack_login
from psycopg2.extras import execute_values
from skyfield.api import EarthSatellite, load


def _parse_omm_float(value):
    if value is None:
        return None
    return float(value)


def _parse_omm_int(value):
    if value is None:
        return None
    return int(float(value))


ORBITAL_ELEMENTS_REQUIRED_FIELDS = (
    "mean_motion",
    "eccentricity",
    "inclination",
    "ra_of_ascending_node",
    "arg_of_pericenter",
    "mean_anomaly",
    "ephemeris_type",
    "classification_type",
    "element_set_no",
    "rev_at_epoch",
    "bstar",
    "mean_motion_dot",
    "mean_motion_ddot",
)

TLE_REQUIRED_FIELDS = ("tle_line_1", "tle_line_2")


def _missing_fields(orbital_data, required_fields):
    return [field for field in required_fields if orbital_data.get(field) is None]


def insert_record(
    record,
    timescale,
    cursor,
    constellation,
    is_supplemental,
    source,
    is_current_number,
):
    # These fields are the same from the TLE format JSON
    name = record["OBJECT_NAME"]
    tle_line_1 = record.get("TLE_LINE1")
    tle_line_2 = record.get("TLE_LINE2")

    rcs_size = record.get("RCS_SIZE", None)
    launch_date = record.get("LAUNCH_DATE", None)
    decay_date = record.get("DECAY_DATE", None)
    object_id = record.get("OBJECT_ID", None)
    object_type = record.get("OBJECT_TYPE", None)

    # OMM only fields
    sat_number = record.get("NORAD_CAT_ID", None)
    epoch = record.get("EPOCH", None)
    mean_motion = _parse_omm_float(record.get("MEAN_MOTION"))
    eccentricity = _parse_omm_float(record.get("ECCENTRICITY"))
    inclination = _parse_omm_float(record.get("INCLINATION"))
    ra_of_ascending_node = _parse_omm_float(record.get("RA_OF_ASC_NODE"))
    arg_of_pericenter = _parse_omm_float(record.get("ARG_OF_PERICENTER"))
    mean_anomaly = _parse_omm_float(record.get("MEAN_ANOMALY"))
    ephemeris_type = _parse_omm_int(record.get("EPHEMERIS_TYPE"))
    classification_type = record.get("CLASSIFICATION_TYPE", None)
    element_set_no = _parse_omm_int(record.get("ELEMENT_SET_NO"))
    rev_at_epoch = _parse_omm_int(record.get("REV_AT_EPOCH"))
    bstar = _parse_omm_float(record.get("BSTAR"))
    mean_motion_dot = _parse_omm_float(record.get("MEAN_MOTION_DOT"))
    mean_motion_ddot = _parse_omm_float(record.get("MEAN_MOTION_DDOT"))

    # add all these fields to a dictionary
    orbital_data = {
        "name": name,
        "tle_line_1": tle_line_1,
        "tle_line_2": tle_line_2,
        "rcs_size": rcs_size,
        "launch_date": launch_date,
        "decay_date": decay_date,
        "object_id": object_id,
        "object_type": object_type,
        "epoch": epoch,
        "mean_motion": mean_motion,
        "eccentricity": eccentricity,
        "inclination": inclination,
        "ra_of_ascending_node": ra_of_ascending_node,
        "arg_of_pericenter": arg_of_pericenter,
        "mean_anomaly": mean_anomaly,
        "ephemeris_type": ephemeris_type,
        "classification_type": classification_type,
        "element_set_no": element_set_no,
        "rev_at_epoch": rev_at_epoch,
        "bstar": bstar,
        "mean_motion_dot": mean_motion_dot,
        "mean_motion_ddot": mean_motion_ddot,
    }

    satellite = None
    if tle_line_1 and tle_line_2:
        satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=timescale)
    if epoch is None:
        if satellite is not None:
            epoch = satellite.epoch.utc_datetime()
        else:
            raise ValueError(f"Record for {name} has no EPOCH and no TLE lines")
    elif isinstance(epoch, str):
        epoch = datetime.datetime.fromisoformat(epoch.replace("Z", "+00:00"))
    elif isinstance(epoch, datetime.datetime) and epoch.tzinfo is None:
        epoch = epoch.replace(tzinfo=datetime.timezone.utc)
    if sat_number is None:
        if satellite is not None:
            sat_number = int(satellite.model.satnum)
        elif record.get("NORAD_CAT_ID") is not None:
            sat_number = int(record["NORAD_CAT_ID"])
        else:
            raise ValueError(f"Record for {name} has no NORAD_CAT_ID and no TLE lines")
    else:
        sat_number = int(sat_number)

    current_date_time = datetime.datetime.now(datetime.timezone.utc)
    # add satellite to database if it doesn't already exist
    sat_to_insert = (
        sat_number,
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
        str(sat_number),
        name,
    )
    satellite_insert_query = """ WITH e AS(
    INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION,
    DATE_ADDED, DATE_MODIFIED, RCS_SIZE, LAUNCH_DATE, DECAY_DATE, OBJECT_ID,
    OBJECT_TYPE, HAS_CURRENT_SAT_NUMBER)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (SAT_NUMBER, SAT_NAME) DO UPDATE SET
        DECAY_DATE = EXCLUDED.DECAY_DATE,
        CONSTELLATION = EXCLUDED.CONSTELLATION,
        OBJECT_ID = EXCLUDED.OBJECT_ID,
        OBJECT_TYPE = EXCLUDED.OBJECT_TYPE,
        RCS_SIZE = EXCLUDED.RCS_SIZE,
        LAUNCH_DATE = EXCLUDED.LAUNCH_DATE,
        DATE_MODIFIED = EXCLUDED.DATE_MODIFIED
    WHERE
        satellites.DECAY_DATE IS DISTINCT FROM EXCLUDED.DECAY_DATE OR
        satellites.CONSTELLATION IS DISTINCT FROM EXCLUDED.CONSTELLATION OR
        satellites.OBJECT_ID IS DISTINCT FROM EXCLUDED.OBJECT_ID OR
        satellites.OBJECT_TYPE IS DISTINCT FROM EXCLUDED.OBJECT_TYPE OR
        satellites.RCS_SIZE IS DISTINCT FROM EXCLUDED.RCS_SIZE OR
        satellites.LAUNCH_DATE IS DISTINCT FROM EXCLUDED.LAUNCH_DATE
    RETURNING id, xmax = 0 as is_new)
    SELECT * FROM e
    UNION ALL
    (SELECT id, false as is_new FROM satellites WHERE SAT_NUMBER=%s AND SAT_NAME=%s);"""
    cursor.execute(satellite_insert_query, sat_to_insert)
    result = cursor.fetchone()

    sat_id = result[0] if result else None
    if sat_id is None:
        raise ValueError(f"No results returned for satellite {sat_number}")

    is_new = result[1]

    if is_new:
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tnew satellite: {sat_number}")

    # update all other satellites with the same sat_number
    update_query = """
        UPDATE satellites
        SET HAS_CURRENT_SAT_NUMBER = FALSE,
            DATE_MODIFIED = %s
        WHERE SAT_NUMBER = %s
        AND id != %s
        """

    params = (current_date_time, sat_number, sat_id)
    cursor.execute(update_query, params)

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

    return (
        sat_id,
        current_date_time,
        orbital_data,
        epoch,
        is_supplemental,
        source,
    )


def add_orbital_data_list_to_db(
    orbital_data,
    constellation,
    cursor,
    connection,
    is_supplemental,
    source,
    is_current_number,
):
    """
    This will add OMM format data to the database to replace retrieving TLEs in the
    original format. TLE functionaliy is kept for backwards compatibility and just in
    case it's needed later (SpaceTrack will still publish TLEs with alpha-5 numbering
    for now).
    """
    tle_count = 0
    orbital_elements_count = 0

    commit_batch_size = (
        100  # Commit satellite upserts + flush TLE batch every N records
    )
    tle_batch = []
    orbital_elements_batch = []

    tle_insert_query = """
        INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2,
            EPOCH, IS_SUPPLEMENTAL, DATA_SOURCE)
        VALUES %s
        ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING"""

    orbital_elements_insert_query = """
        INSERT INTO orbital_elements (SAT_ID, DATE_COLLECTED, EPOCH, DATA_SOURCE,
        MEAN_MOTION, ECCENTRICITY, INCLINATION, RA_OF_ASCENDING_NODE, ARG_OF_PERICENTER,
        MEAN_ANOMALY, EPHEMERIS_TYPE, CLASSIFICATION_TYPE, ELEMENT_SET_NO, REV_AT_EPOCH,
        BSTAR, MEAN_MOTION_DOT, MEAN_MOTION_DDOT)
        VALUES %s
        ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING"""

    def flush_tle_batch():
        if tle_batch:
            execute_values(cursor, tle_insert_query, tle_batch, page_size=500)
            tle_batch.clear()

    def flush_orbital_elements_batch():
        if orbital_elements_batch:
            execute_values(
                cursor,
                orbital_elements_insert_query,
                orbital_elements_batch,
                page_size=500,
            )
            orbital_elements_batch.clear()

    skipped_count = 0

    def _record_label(record):
        return (
            f"{record.get('OBJECT_NAME', '?')} "
            f"(NORAD {record.get('NORAD_CAT_ID', '?')})"
        )

    try:
        ts = load.timescale()
        for record in orbital_data.json():
            # Each record gets its own savepoint so a single bad record (a
            # parsing error, or a DB error on its satellite upsert) can be
            # rolled back and skipped without discarding already-processed
            # records still pending in this transaction.
            cursor.execute("SAVEPOINT record_savepoint")
            try:
                orbital_data_tuple = insert_record(
                    record,
                    ts,
                    cursor,
                    constellation,
                    is_supplemental,
                    source,
                    is_current_number,
                )
            except Exception as err:
                cursor.execute("ROLLBACK TO SAVEPOINT record_savepoint")
                skipped_count += 1
                logging.warning(f"Skipping record {_record_label(record)}: {err}")
                continue

            sat_id, date_collected, od, epoch, sup, data_source = orbital_data_tuple
            is_orbital_elements = source == "celestrak" or "CCSDS_OMM_VERS" in record
            required_fields = (
                ORBITAL_ELEMENTS_REQUIRED_FIELDS
                if is_orbital_elements
                else TLE_REQUIRED_FIELDS
            )
            missing = _missing_fields(od, required_fields)
            if missing:
                # Roll back the satellite upsert insert_record already made
                # for this record too -- a record we can't store orbital
                # data for shouldn't leave a dangling satellite behind.
                cursor.execute("ROLLBACK TO SAVEPOINT record_savepoint")
                skipped_count += 1
                logging.warning(
                    f"Skipping record {_record_label(record)}: "
                    f"missing required field(s) {missing}"
                )
                continue
            cursor.execute("RELEASE SAVEPOINT record_savepoint")

            if is_orbital_elements:
                orbital_elements_batch.append(
                    (
                        sat_id,
                        date_collected,
                        epoch,
                        data_source,
                        od["mean_motion"],
                        od["eccentricity"],
                        od["inclination"],
                        od["ra_of_ascending_node"],
                        od["arg_of_pericenter"],
                        od["mean_anomaly"],
                        od["ephemeris_type"],
                        od["classification_type"],
                        od["element_set_no"],
                        od["rev_at_epoch"],
                        od["bstar"],
                        od["mean_motion_dot"],
                        od["mean_motion_ddot"],
                    )
                )
                orbital_elements_count += 1
            else:
                tle_batch.append(
                    (
                        sat_id,
                        date_collected,
                        od["tle_line_1"],
                        od["tle_line_2"],
                        epoch,
                        sup,
                        data_source,
                    )
                )
                tle_count += 1

            if (tle_count + orbital_elements_count) % commit_batch_size == 0:
                flush_tle_batch()
                flush_orbital_elements_batch()
                connection.commit()
                log_time = datetime.datetime.now(datetime.UTC).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logging.info(
                    f"{log_time}\tCommitted batch of {commit_batch_size} "
                    f"TLEs. Total: {tle_count}. "
                    f"Orbital elements: {orbital_elements_count}. "
                    f"Last inserted: epoch: {record.get('EPOCH', epoch)}"
                )

        # Final flush and commit for any remaining records
        flush_tle_batch()
        flush_orbital_elements_batch()
        connection.commit()

        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tTLE source: {source}")
        logging.info(f"{log_time}\tConstellation: {constellation}")
        logging.info(f"{log_time}\tSupplemental: {is_supplemental}")
        logging.info(f"{log_time}\tTLEs added: {tle_count}")
        logging.info(f"{log_time}\tOrbital elements added: {orbital_elements_count}")
        logging.info(f"{log_time}\tRecords skipped: {skipped_count}")
        logging.info(
            f"{log_time}\tTotal records added: {tle_count + orbital_elements_count}"
        )

    except Exception as err:
        connection.rollback()
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{log_time}\tError processing TLEs: {err}")
        raise


def add_archival_spacetrack_tles_to_db(
    tle, constellation, cursor, connection, is_supplemental, source
):
    tle_count = 0
    tles_inserted = 0
    tle_batch = []
    step = "parse response"

    tle_insert_query = """
        INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2,
            EPOCH, IS_SUPPLEMENTAL, DATA_SOURCE)
        VALUES %s
        ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING
        RETURNING id"""

    satellite_insert_query = """
    INSERT INTO satellites (SAT_NUMBER, SAT_NAME, CONSTELLATION,
    DATE_ADDED, DATE_MODIFIED, RCS_SIZE, LAUNCH_DATE, DECAY_DATE, OBJECT_ID,
    OBJECT_TYPE, HAS_CURRENT_SAT_NUMBER)
    VALUES %s
    ON CONFLICT (SAT_NUMBER, SAT_NAME) DO UPDATE SET
        DECAY_DATE = EXCLUDED.DECAY_DATE,
        CONSTELLATION = EXCLUDED.CONSTELLATION,
        OBJECT_ID = EXCLUDED.OBJECT_ID,
        OBJECT_TYPE = EXCLUDED.OBJECT_TYPE,
        RCS_SIZE = EXCLUDED.RCS_SIZE,
        LAUNCH_DATE = EXCLUDED.LAUNCH_DATE,
        DATE_MODIFIED = EXCLUDED.DATE_MODIFIED
    WHERE
        satellites.DECAY_DATE IS DISTINCT FROM EXCLUDED.DECAY_DATE OR
        satellites.CONSTELLATION IS DISTINCT FROM EXCLUDED.CONSTELLATION OR
        satellites.OBJECT_ID IS DISTINCT FROM EXCLUDED.OBJECT_ID OR
        satellites.OBJECT_TYPE IS DISTINCT FROM EXCLUDED.OBJECT_TYPE OR
        satellites.RCS_SIZE IS DISTINCT FROM EXCLUDED.RCS_SIZE OR
        satellites.LAUNCH_DATE IS DISTINCT FROM EXCLUDED.LAUNCH_DATE"""

    try:
        tle_json = tle.json()
        ts = load.timescale()
        current_date_time = datetime.datetime.now(datetime.timezone.utc)
        sats_to_insert = {}
        tle_rows = []

        for record in tle_json:
            name = record["OBJECT_NAME"]
            tle_line_1 = record["TLE_LINE1"]
            tle_line_2 = record["TLE_LINE2"]

            rcs_size = record.get("RCS_SIZE", None)
            launch_date = record.get("LAUNCH_DATE", None)
            decay_date = record.get("DECAY_DATE", None)
            object_id = record.get("OBJECT_ID", None)
            object_type = record.get("OBJECT_TYPE", None)

            satellite = EarthSatellite(tle_line_1, tle_line_2, name=name, ts=ts)
            sat_number = int(satellite.model.satnum)
            sat_key = (sat_number, name)
            sats_to_insert[sat_key] = (
                sat_number,
                name,
                constellation,
                current_date_time,
                current_date_time,
                rcs_size,
                launch_date,
                decay_date,
                object_id,
                object_type,
            )
            tle_rows.append(
                (
                    sat_key,
                    tle_line_1,
                    tle_line_2,
                    satellite.epoch.utc_datetime(),
                )
            )
            tle_count += 1

        if sats_to_insert:
            sat_keys = list(sats_to_insert.keys())
            step = "lookup existing satellites"
            cursor.execute(
                "SELECT sat_number, sat_name FROM satellites "
                "WHERE (sat_number, sat_name) IN %s",
                (tuple(sat_keys),),
            )
            existing_sat_keys = set(cursor.fetchall())
            new_sat_keys = [
                sat_key for sat_key in sat_keys if sat_key not in existing_sat_keys
            ]

            # archival data is loaded backwards in time, so the first time we see an
            # object it is the latest epoch and should be the current sat number
            sat_rows_to_insert = []
            for sat_key in sat_keys:
                sat_row = sats_to_insert[sat_key]
                has_current_sat_number = sat_key in new_sat_keys
                sat_rows_to_insert.append(sat_row + (has_current_sat_number,))

            step = "upsert satellites"
            execute_values(
                cursor,
                satellite_insert_query,
                sat_rows_to_insert,
                page_size=500,
            )

            step = "lookup satellite ids"
            cursor.execute(
                "SELECT id, sat_number, sat_name FROM satellites "
                "WHERE (sat_number, sat_name) IN %s",
                (tuple(sat_keys),),
            )
            sat_id_by_key = {}
            for sat_id, sat_number, sat_name in cursor.fetchall():
                sat_id_by_key[(sat_number, sat_name)] = sat_id

            update_false_query = """
        UPDATE satellites
        SET HAS_CURRENT_SAT_NUMBER = FALSE,
            DATE_MODIFIED = %s
        WHERE SAT_NUMBER = %s
        AND id != %s
        """

            update_true_query = """
            UPDATE satellites
            SET HAS_CURRENT_SAT_NUMBER = TRUE,
            DATE_MODIFIED = %s
        WHERE id = %s
        """

            step = "update has_current_sat_number"
            if new_sat_keys:
                log_time = datetime.datetime.now(datetime.UTC).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                false_params = []
                for sat_key in new_sat_keys:
                    sat_id = sat_id_by_key.get(sat_key)
                    if sat_id is None:
                        raise ValueError(
                            f"No results returned for satellite {sat_key[0]}"
                        )
                    logging.info(f"{log_time}\tnew satellite: {sat_key[0]}")
                    false_params.append((current_date_time, sat_key[0], sat_id))

                cursor.executemany(update_false_query, false_params)

                # make sure this satellite has the correct has_current_sat_number value
                # only allow data from space-track to update this value, celestrak has
                # had a few instances of name changes outside of preliminary names
                if source == "spacetrack":
                    true_params = [
                        (current_date_time, sat_id_by_key[sat_key])
                        for sat_key in new_sat_keys
                    ]
                    cursor.executemany(update_true_query, true_params)

            step = "build tle batch"
            for sat_key, tle_line_1, tle_line_2, epoch in tle_rows:
                if sat_key not in sat_id_by_key:
                    raise ValueError(f"No results returned for satellite {sat_key[0]}")
                tle_batch.append(
                    (
                        sat_id_by_key[sat_key],
                        current_date_time,
                        tle_line_1,
                        tle_line_2,
                        epoch,
                        is_supplemental,
                        source,
                    )
                )

            step = "insert tles"
            inserted = execute_values(
                cursor,
                tle_insert_query,
                tle_batch,
                page_size=500,
                fetch=True,
            )
            tles_inserted = len(inserted) if inserted else 0

        step = "commit"
        connection.commit()
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{log_time}\tTLE source: {source}")
        logging.info(f"{log_time}\tConstellation: {constellation}")
        logging.info(f"{log_time}\tSupplemental: {is_supplemental}")
        logging.info(f"{log_time}\tTLEs retrieved: {tle_count}")
        logging.info(f"{log_time}\tTLEs inserted: {tles_inserted}")

    except Exception as err:
        connection.rollback()
        log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{log_time}\tError processing TLEs at step '{step}': {err}")
        logging.error(traceback.format_exc())
        raise


def get_celestrak_general_tles(cursor, connection):
    groups = ["starlink", "oneweb", "geo", "active"]
    for group in groups:
        tle = requests.get(
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=%s&FORMAT=json"  # noqa: UP031
            % group,
            timeout=120,
        )
        tle.raise_for_status()
        try:
            constellation = (
                group if (group == "starlink" or group == "oneweb") else "other"
            )
            add_orbital_data_list_to_db(
                tle, constellation, cursor, connection, "false", "celestrak", True
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
            "?FILE=%s&FORMAT=json" % constellation,
            timeout=120,
        )
        tle.raise_for_status()
        try:
            add_orbital_data_list_to_db(
                tle, constellation, cursor, connection, "true", "celestrak", True
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
            add_orbital_data_list_to_db(
                tle, "", cursor, connection, "false", "spacetrack", True
            )
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()
