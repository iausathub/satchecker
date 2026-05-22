import logging
import re
import time
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
from astropy.time import Time
from psycopg2.extras import execute_values
from scipy.optimize import least_squares
from sgp4.api import WGS84, Satrec
from sgp4.exporter import export_tle
from skyfield.api import EarthSatellite, load
from skyfield.elementslib import osculating_elements_of

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)

# How much of each ephemeris file we keep in the database. Anything beyond this
# horizon from ``ephemeris_start`` is dropped in ``parse_ephemeris_file``.
EPHEMERIS_DB_SPAN_HOURS = 26.0

# Subset of the stored ephemeris that ``create_tle_from_ephemeris`` actually
# uses to fit a TLE. Must be ``<= EPHEMERIS_DB_SPAN_HOURS``; chosen empirically
# (20 h gave the lowest XYZ RMS over the 26 h DB span without overfitting the
# first few hours), but this can be changed later if needed.
TLE_FIT_WINDOW_HOURS = 20.0

# When picking a seed TLE from the catalog, prefer rows whose epoch falls in
# ``[ephemeris_start, ephemeris_start + this many hours]`` (used by
# ``get_closest_tle``). Falls back to the globally closest TLE otherwise.
TLE_SEED_PREFERENCE_WINDOW_HOURS = 8.0

# Penalty magnitude returned by ``residuals`` when SGP4 propagation fails or
# produces non-finite outputs. Large enough that least_squares (LM) will treat
# the step as a bad direction and back off via its damping parameter, but
# finite so it never raises and never produces NaN cost.
LARGE_RESIDUAL = 1.0e6

# ``sgp4init`` epoch argument: days since 1949-12-31 00:00 UT (JD 2433281.5).
SGP4_EPOCH_REFERENCE_JD = 2433281.5


def insert_ephemeris_data(
    parsed_data, cursor, connection
) -> tuple[InterpolableEphemeris, int] | None:
    """
    Insert ephemeris data into the database efficiently using batch inserts.

    Args:
        parsed_data (dict): Dictionary containing parsed ephemeris data
        cursor: Database cursor
        connection: Database connection

    Returns:
        InterpolableEphemeris: The created ephemeris object if successful,
        None if duplicate
    """
    try:
        # TODO: fix usage of has_current_sat_number
        # Get the satellite data to create a proper Satellite object
        cursor.execute(
            "SELECT id, sat_number, sat_name, constellation, generation, "
            "rcs_size, launch_date, decay_date, object_id, object_type, "
            "has_current_sat_number FROM satellites "
            "WHERE sat_name = %s "
            "AND has_current_sat_number = true",
            (parsed_data["satellite_name"],),
        )
        satellite_result = cursor.fetchone()
        if satellite_result is None:
            logging.error("Satellite not found: %s", parsed_data["satellite_name"])
            return None

        satellite_id = satellite_result[0]

        date_collected = datetime.now(timezone.utc)
        data_source = "starlink"

        ephemeris_insert = """
            INSERT INTO interpolable_ephemeris (
                satellite,
                date_collected,
                generated_at,
                data_source,
                file_reference,
                ephemeris_start,
                ephemeris_stop,
                frame
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (satellite, generated_at, data_source) DO NOTHING
            RETURNING id
        """

        cursor.execute(
            ephemeris_insert,
            (
                satellite_id,
                date_collected,
                parsed_data["generated_at"],
                data_source,
                parsed_data["filename"],
                parsed_data["ephemeris_start"],
                parsed_data["ephemeris_stop"],
                parsed_data["frame"],
            ),
        )
        ephemeris_result = cursor.fetchone()
        if ephemeris_result is None:
            logging.warning(
                "Likely duplicate ephemeris data for %s",
                parsed_data["satellite_name"],
            )
            return None
        ephemeris_id = ephemeris_result[0]

        # Prepare the points data for batch insert
        timestamps = parsed_data["timestamps"]
        positions = parsed_data["positions"]
        velocities = parsed_data["velocities"]
        covariances = parsed_data["covariances"]

        # Create a list of tuples for batch insert
        points = []
        for i in range(len(timestamps)):
            # Position and velocity are 3D arrays (x,y,z)
            pos_array = [float(x) for x in positions[i]]
            vel_array = [float(x) for x in velocities[i]]
            # Covariance is a 6x6 matrix flattened to 1D array of 36 elements
            cov_array = [float(x) for x in covariances[i].flatten()]

            points.append(
                (ephemeris_id, timestamps[i], pos_array, vel_array, cov_array)
            )

        # Batch insert the points with ON CONFLICT DO NOTHING
        points_insert = """
            INSERT INTO ephemeris_points (
                ephemeris_id,
                timestamp,
                position,
                velocity,
                covariance
            ) VALUES %s
            ON CONFLICT (ephemeris_id, timestamp) DO NOTHING
        """
        execute_values(cursor, points_insert, points)

        # Commit the transaction
        connection.commit()

        logging.info(
            "Successfully inserted %d points for ephemeris_id %s",
            len(points),
            ephemeris_id,
        )

        # Create EphemerisPoint objects from the data
        ephemeris_points = []
        for i in range(len(timestamps)):
            point = EphemerisPoint(
                timestamp=timestamps[i],
                position=np.array(positions[i]),
                velocity=np.array(velocities[i]),
                covariance=np.array(covariances[i]),
            )
            ephemeris_points.append(point)

        # Create and return the InterpolableEphemeris object
        ephemeris = InterpolableEphemeris(
            sat_id=satellite_id,
            generated_at=parsed_data["generated_at"],
            data_source=data_source,
            frame=parsed_data["frame"],
            points=ephemeris_points,
            ephemeris_start=parsed_data["ephemeris_start"],
            ephemeris_stop=parsed_data["ephemeris_stop"],
            file_reference=parsed_data["filename"],
            date_collected=date_collected,
        )

        return ephemeris, ephemeris_id

    except Exception as e:
        connection.rollback()
        logging.error("Error inserting ephemeris data: %s", e)
        raise


def parse_ephemeris_file(file_content: str, filename: str) -> dict:
    """
    Parse a satellite ephemeris file in UVW frame format.

    Args:
        file_content (str): Content of the ephemeris file
        filename (str): Name of the file, used to extract satellite name

    Returns:
        dict: A dictionary containing:
            - headers (dict): Key-value pairs from the file header
            - timestamps (np.ndarray): Array of datetime objects
            - positions (np.ndarray): Array of position vectors
            - velocities (np.ndarray): Array of velocity vectors
            - covariances (np.ndarray): Array of 6x6 covariance matrices
            - frame (str): Coordinate frame (UVW)
            - ephemeris_start (datetime): Start time of the ephemeris
            - ephemeris_stop (datetime): End time of the ephemeris
            - generated_at (datetime): When the ephemeris was created
            - satellite_name (str): Name of the satellite extracted from filename
    """
    lines = file_content.splitlines()

    # Parse headers
    headers = {}
    for i in range(3):
        line = lines[i].strip()

        if "ephemeris_start:" in line and "ephemeris_stop:" in line:

            # everything after "ephemeris_start:" until "ephemeris_stop:"
            start_match = re.search(
                r"ephemeris_start:([^e]+?)(?=ephemeris_stop:)", line
            )
            if start_match:
                headers["ephemeris_start"] = start_match.group(1).strip()

            # everything after "ephemeris_stop:" until "step_size:"
            stop_match = re.search(r"ephemeris_stop:([^s]+?)(?=step_size:)", line)
            if stop_match:
                headers["ephemeris_stop"] = stop_match.group(1).strip()

            # everything after "step_size:"
            step_match = re.search(r"step_size:(.+)", line)
            if step_match:
                headers["step_size"] = step_match.group(1).strip()
        else:
            if ":" in line:
                colon_pos = line.find(":")
                key = line[:colon_pos]
                value = line[colon_pos + 1 :].strip()
                headers[key] = value

    if lines[3].strip() != "UVW":
        raise ValueError("Expected UVW frame specification")

    # Extract satellite name from filename
    # Format: MEME_57851_STARLINK-30405_1490204_Operational_1432778700_UNCLASSIFIED
    satellite_name = None
    try:
        # Find STARLINK- pattern and extract the full satellite name
        if "STARLINK-" in filename:
            start_idx = filename.find("STARLINK-")
            end_idx = filename.find("_", start_idx)
            if end_idx == -1:
                end_idx = len(filename)
            satellite_name = filename[start_idx:end_idx]
    except Exception as e:
        logging.warning(
            "Could not parse satellite name from filename %s: %s", filename, e
        )

    # Parse creation time
    generated_at = None
    if "created" in headers:
        try:
            time_str = headers["created"].replace(" UTC", "")
            # Try parsing with time first, then fall back to date only
            try:
                generated_at = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                generated_at = datetime.strptime(time_str, "%Y-%m-%d")
            generated_at = generated_at.replace(tzinfo=timezone.utc)
        except ValueError:
            logging.warning("Could not parse creation time: %s", headers["created"])

    # Parse ephemeris start and stop times
    ephemeris_start = None
    ephemeris_stop = None
    if "ephemeris_start" in headers and "ephemeris_stop" in headers:
        try:
            start_str = headers["ephemeris_start"].replace(" UTC", "")
            stop_str = headers["ephemeris_stop"].replace(" UTC", "")
            # Try parsing with time first, then fall back to date only
            try:
                ephemeris_start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                ephemeris_stop = datetime.strptime(stop_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                ephemeris_start = datetime.strptime(start_str, "%Y-%m-%d")
                ephemeris_stop = datetime.strptime(stop_str, "%Y-%m-%d")
            ephemeris_start = ephemeris_start.replace(tzinfo=timezone.utc)
            ephemeris_stop = ephemeris_stop.replace(tzinfo=timezone.utc)
        except ValueError:
            logging.warning(
                "Could not parse ephemeris times: %s - %s",
                headers["ephemeris_start"],
                headers["ephemeris_stop"],
            )

    timestamps = []
    positions = []
    velocities = []
    covariances = []

    i = 4
    while i < len(lines):
        state_parts = lines[i].strip().split()

        # Parse timestamp
        timestamp_str = state_parts[0]
        year = int(timestamp_str[:4])
        day_of_year = int(timestamp_str[4:7])
        hour = int(timestamp_str[7:9])
        minute = int(timestamp_str[9:11])
        second = int(timestamp_str[11:13])
        # Handle decimal seconds
        millisec = int(
            float(timestamp_str[13:]) * 1000
        )  # Convert decimal seconds to milliseconds

        timestamp = datetime(year, 1, 1, tzinfo=timezone.utc).replace(
            hour=hour, minute=minute, second=second, microsecond=millisec * 1000
        ) + timedelta(days=day_of_year - 1)

        # Parse position and velocity
        pos = np.array([np.float64(x) for x in state_parts[1:4]])
        vel = np.array([np.float64(x) for x in state_parts[4:7]])

        # Parse covariance
        cov_values = []
        for j in range(3):
            cov_values.extend([np.float64(x) for x in lines[i + 1 + j].strip().split()])

        cov_matrix = np.zeros((6, 6), dtype=np.float64)
        idx = 0
        for row in range(6):
            for col in range(row + 1):
                cov_matrix[row, col] = cov_values[idx]
                cov_matrix[col, row] = cov_values[idx]
                idx += 1

        # Store arrays
        timestamps.append(timestamp)
        positions.append(pos)
        velocities.append(vel)
        covariances.append(cov_matrix)

        i += 4

    # If we couldn't parse from headers, use first and last timestamps
    if ephemeris_start is None:
        ephemeris_start = timestamps[0]
    if ephemeris_stop is None:
        ephemeris_stop = timestamps[-1]
    if generated_at is None:
        generated_at = ephemeris_start

    # Restrict to ``EPHEMERIS_DB_SPAN_HOURS`` worth of samples from the start.
    # Everything beyond that horizon is dropped from the DB to bound storage.
    timestamps_array = np.array(timestamps)
    positions_array = np.array(positions, dtype=np.float64)
    velocities_array = np.array(velocities, dtype=np.float64)
    covariances_array = np.array(covariances, dtype=np.float64)

    cutoff_time = ephemeris_start + timedelta(hours=EPHEMERIS_DB_SPAN_HOURS)

    time_mask = timestamps_array <= cutoff_time

    # Filter all arrays using the mask
    filtered_timestamps = timestamps_array[time_mask]
    filtered_positions = positions_array[time_mask]
    filtered_velocities = velocities_array[time_mask]
    filtered_covariances = covariances_array[time_mask]

    # Update ephemeris_stop to reflect the actual end time of filtered data
    if len(filtered_timestamps) > 0:
        actual_ephemeris_stop = filtered_timestamps[-1]
        ephemeris_stop = min(cutoff_time, actual_ephemeris_stop)
    else:
        ephemeris_stop = cutoff_time

    original_count = len(timestamps)
    filtered_count = len(filtered_timestamps)
    logging.info("Original data points: %d", original_count)
    logging.info(
        "Filtered data points (%g hours): %d",
        EPHEMERIS_DB_SPAN_HOURS,
        filtered_count,
    )
    logging.info("Data reduction: %d points removed", original_count - filtered_count)
    logging.info("Parsed %d timestamps", filtered_count)
    logging.info("Parsed %d positions", len(filtered_positions))
    logging.info("Parsed %d velocities", len(filtered_velocities))
    logging.info("Parsed %d covariances", len(filtered_covariances))
    logging.info("Ephemeris start: %s", ephemeris_start)
    logging.info("Ephemeris stop: %s", ephemeris_stop)
    logging.info("Generated at: %s", generated_at)
    logging.info("Satellite name: %s", satellite_name)
    logging.info("Filename: %s", filename)

    return {
        "timestamps": filtered_timestamps,
        "positions": filtered_positions,
        "velocities": filtered_velocities,
        "covariances": filtered_covariances,
        "frame": "UVW",
        "ephemeris_start": ephemeris_start,
        "ephemeris_stop": ephemeris_stop,
        "generated_at": generated_at,
        "satellite_name": satellite_name,
        "filename": filename,
    }


def get_starlink_ephemeris_data(cursor, connection):
    """
    Fetch and process ephemeris data for Starlink satellites.

    This function:
    1. Downloads each ephemeris file referenced in the Starlink public manifest
       (``https://api.starlink.com/public-files/ephemerides``).
    2. Parses each file (``parse_ephemeris_file``), inserts the points into
       ``ephemeris_points`` (``insert_ephemeris_data``), and fits a generated
       TLE from the first ``TLE_FIT_WINDOW_HOURS`` of stored data
       (``create_tle_from_ephemeris``).
    3. After the loop, logs mean/median/p95/min/max for both TLE-fit timing
       and residuals across every ephemeris that was successfully processed.

    Files are named like
    ``MEME_57851_STARLINK-30405_1490204_Operational_1432778700_UNCLASSIFIED``.
    Each file contains position, velocity, and covariance state vectors.

    Args:
        cursor: Database cursor used to execute SQL.
        connection: Database connection for transaction management.

    Raises:
        requests.HTTPError: If the manifest itself cannot be downloaded.
            Per-file HTTP errors are caught and logged, and the loop
            continues with the next file.

    Note:
        - Per-file failures (download, parse, insert, fit) are logged,
          the transaction is rolled back, and processing continues with the
          next file. Only a failure to fetch the manifest is fatal.
        - Uses ``ON CONFLICT DO NOTHING`` for both ephemeris and TLE inserts
          so duplicate runs are idempotent.
    """
    with requests.Session() as session:
        # Retrieve list of ephemeris files
        manifest_response = session.get(
            "https://api.starlink.com/public-files/ephemerides/MANIFEST.txt",
            timeout=60,
        )
        manifest_response.raise_for_status()

        # Parse the manifest to get file names
        ephemeris_files = [
            line.strip() for line in manifest_response.text.splitlines() if line.strip()
        ]

        # Get today's date in UTC
        today = datetime.now(timezone.utc).date()
        logging.info("Today's date: %s", today)
        logging.info("Found %d files in manifest", len(ephemeris_files))

        stats: list[dict[str, float]] = []
        files_processed = 0
        total_data_points = 0

        # Process each file individually
        for file_name in ephemeris_files:
            try:
                # Check if file has already been processed
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM interpolable_ephemeris
                    WHERE file_reference = %s
                    """,
                    (file_name,),
                )
                if cursor.fetchone()[0] > 0:
                    logging.info("Skipping already processed file: %s", file_name)
                    continue

                # Download the file
                file_url = (
                    f"https://api.starlink.com/public-files/ephemerides/{file_name}"
                )
                response = session.get(file_url, timeout=120)
                response.raise_for_status()
                logging.info("Processing file: %s", file_name)

                parsed_data = parse_ephemeris_file(
                    response.content.decode("utf-8"), file_name
                )
                insert_result = insert_ephemeris_data(parsed_data, cursor, connection)
                if insert_result is None:
                    logging.warning(
                        "Skipping TLE generation for %s: ephemeris insert "
                        "returned None (duplicate, missing satellite, etc.)",
                        file_name,
                    )
                    continue
                ephemeris, _ephemeris_id = insert_result

                t0 = time.perf_counter()
                fit_xyz_rms, fit_ang_rms = create_tle_from_ephemeris(
                    ephemeris, cursor, connection
                )
                stats.append(
                    {
                        "tle_generation_s": time.perf_counter() - t0,
                        "fit_xyz_rms_km": fit_xyz_rms,
                        "fit_ang_rms_arcsec": fit_ang_rms,
                    }
                )
                total_data_points += len(ephemeris.points)
                files_processed += 1
            except Exception as e:
                logging.error("Error processing file %s: %s", file_name, e)
                try:
                    connection.rollback()
                except Exception as rollback_err:
                    logging.warning(
                        "Rollback failed for %s: %s", file_name, rollback_err
                    )
                cursor = connection.cursor()
                continue

        logging.info("Total data points: %d", total_data_points)
        logging.info("Files processed: %d", files_processed)
        _log_tle_generation_stats(stats)


def _log_tle_generation_stats(stats: list[dict[str, float]]) -> None:
    """Log mean/median/p95/min/max for timing and RMS across a batch."""
    if not stats:
        return

    times = np.array([s["tle_generation_s"] for s in stats], dtype=float)
    xyz_rms = np.array([s["fit_xyz_rms_km"] for s in stats], dtype=float)
    ang_rms = np.array([s["fit_ang_rms_arcsec"] for s in stats], dtype=float)

    def _summary(values: np.ndarray) -> tuple[float, float, float, float, float]:
        return (
            float(np.mean(values)),
            float(np.median(values)),
            float(np.percentile(values, 95)),
            float(np.min(values)),
            float(np.max(values)),
        )

    logging.info("TLE generation aggregate stats for %d ephemerides:", len(stats))
    logging.info(
        "  Time (s):           mean=%.3f median=%.3f p95=%.3f min=%.3f max=%.3f",
        *_summary(times),
    )
    logging.info(
        "  XYZ RMS (km):       mean=%.6f median=%.6f p95=%.6f min=%.6f max=%.6f",
        *_summary(xyz_rms),
    )
    logging.info(
        "  Angle RMS (arcsec): mean=%.6f median=%.6f p95=%.6f min=%.6f max=%.6f",
        *_summary(ang_rms),
    )


def propagate_teme_positions_km(
    satrec: Satrec,
    julian_dates: np.ndarray,
) -> np.ndarray:
    """
    Propagate a satellite state to TEME position vectors in kilometers.

    Args:
        satrec (Satrec): SGP4 satellite record initialized from a TLE
        julian_dates (np.ndarray): Julian dates at which to evaluate the state

    Returns:
        np.ndarray: Position vectors with shape (N, 3) in TEME frame (km)

    Raises:
        RuntimeError: If SGP4 returns a non-zero error code for any epoch
    """
    out = np.empty((len(julian_dates), 3), dtype=float)
    for i, jd in enumerate(julian_dates):
        jd_int = int(jd)
        jd_frac = float(jd - jd_int)
        err, r, _v = satrec.sgp4(jd_int, jd_frac)
        if err != 0:
            raise RuntimeError(f"SGP4 propagation error code {err} at JD={jd}")
        out[i] = np.array(r, dtype=float)
    return out


def get_closest_tle(
    ephemeris_start_time: datetime, sat_id: int, cursor
) -> tuple[str, str] | None:
    """
    Retrieve a catalog TLE to seed fitting, aligned with ephemeris start time.

    Rows whose ``epoch`` falls in
    ``[ephemeris_start_time, ephemeris_start_time + TLE_SEED_PREFERENCE_WINDOW_HOURS]``
    are sorted first. Within each group, the row with ``epoch`` closest to
    ``ephemeris_start_time + TLE_SEED_PREFERENCE_WINDOW_HOURS`` (absolute time
    difference) wins. If the window is empty, this falls back to the globally
    closest ``epoch`` to that same target — same idea as
    ``TleRepository._get_closest_by_satellite_number``, but with ``sat_id`` and
    a soft preference for the seed window (no ``data_source`` filter).

    Args:
        ephemeris_start_time (datetime): Ephemeris segment start.
        sat_id (int): Satellite primary key
        cursor: Database cursor used to execute SQL.

    Returns:
        TLE line 1 and line 2, or ``None`` if no row matches ``sat_id``.
    """

    target_time = ephemeris_start_time + timedelta(
        hours=TLE_SEED_PREFERENCE_WINDOW_HOURS
    )

    cursor.execute(
        "SELECT t.id, t.tle_line1, t.tle_line2 FROM tle t "
        "WHERE t.sat_id = %s "
        "ORDER BY CASE "
        "WHEN t.epoch >= %s::timestamptz "
        "AND t.epoch <= %s::timestamptz THEN 0 ELSE 1 END, "
        "ABS(EXTRACT(EPOCH FROM t.epoch) - "
        "EXTRACT(EPOCH FROM %s::timestamptz)) "
        "LIMIT 1",
        (sat_id, ephemeris_start_time, target_time, target_time),
    )
    tle_result = cursor.fetchone()
    if tle_result is None:
        logging.error("TLE not found: %s", ephemeris_start_time)
        return None

    tle_line1 = tle_result[1]
    tle_line2 = tle_result[2]
    return tle_line1, tle_line2


def ut1_jd_from_datetime(dt: datetime) -> float:
    """UT1 Julian date for an aware or naive UTC ``datetime``."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return float(Time(dt, format="datetime", scale="utc").ut1.jd)


def sgp4_epoch_days_from_ut1_jd(jd_ut1: float) -> float:
    """Convert UT1 JD to the ``sgp4init`` epoch offset (days since 1949-12-31)."""
    return float(jd_ut1) - SGP4_EPOCH_REFERENCE_JD


def fit_window_epoch_datetime(window_start: datetime) -> datetime:
    """Midpoint of the TLE fit window (``window_start + TLE_FIT_WINDOW_HOURS / 2``)."""
    if window_start.tzinfo is None:
        window_start = window_start.replace(tzinfo=timezone.utc)
    else:
        window_start = window_start.astimezone(timezone.utc)
    return window_start + timedelta(hours=TLE_FIT_WINDOW_HOURS / 2.0)


def fit_epoch_jd_from_fit_jds(jd_fit: np.ndarray) -> float:
    """Midpoint epoch (UT1 JD) from the first and last sample in the fit window."""
    if len(jd_fit) < 1:
        raise ValueError("jd_fit must contain at least one epoch")
    return float(0.5 * (float(jd_fit[0]) + float(jd_fit[-1])))


def seed_params_at_epoch(
    line1: str,
    line2: str,
    fit_epoch_dt: datetime,
) -> np.ndarray:
    """
    Physical SGP4 parameters at ``fit_epoch_dt`` for LM initialization.

    Propagates the seed TLE to ``fit_epoch_dt`` and maps osculating elements
    (Skyfield) to the ``get_fit_params_from_satrec`` vector order. ``ndot`` and
    ``bstar`` stay from the seed catalog TLE.
    """
    if fit_epoch_dt.tzinfo is None:
        fit_epoch_dt = fit_epoch_dt.replace(tzinfo=timezone.utc)
    else:
        fit_epoch_dt = fit_epoch_dt.astimezone(timezone.utc)

    seed_sat = Satrec.twoline2rv(line1, line2)
    ts = load.timescale()
    elements = osculating_elements_of(
        EarthSatellite(line1, line2, "SAT", ts).at(ts.from_datetime(fit_epoch_dt))
    )
    no_kozai = elements.mean_motion_per_day.radians / (24.0 * 60.0)
    return np.array(
        [
            elements.inclination.radians,
            elements.longitude_of_ascending_node.radians,
            float(elements.eccentricity),
            elements.argument_of_periapsis.radians,
            elements.mean_anomaly.radians,
            no_kozai,
            float(seed_sat.ndot),
            float(seed_sat.bstar),
        ],
        dtype=np.float64,
    )


def get_fit_params_from_satrec(satrec: Satrec) -> np.ndarray:
    """
    Convert a `Satrec` object to the least-squares fit parameter vector.

    Args:
        satrec (Satrec): SGP4 satellite record used as the optimization seed

    Returns:
        np.ndarray: Parameter vector in the order
        [inclo, nodeo, ecco, argpo, mo, no_kozai, ndot, bstar]
    """
    vals = [
        satrec.inclo,
        satrec.nodeo,
        satrec.ecco,
        satrec.argpo,
        satrec.mo,
        satrec.no_kozai,
        satrec.ndot,
        satrec.bstar,
    ]
    return np.array(vals, dtype=float)


def wrap_angle_rad(x: float) -> float:
    return float(x % (2.0 * np.pi))


def angular_rms_arcsec(model_pos: np.ndarray, obs_pos: np.ndarray) -> float:
    """
    Compute the RMS angular separation between modeled and observed vectors.

    Args:
        model_pos (np.ndarray): Modeled Cartesian position vectors with shape (N, 3)
        obs_pos (np.ndarray): Observed Cartesian position vectors with shape (N, 3)

    Returns:
        float: Root-mean-square separation in arcseconds

    Raises:
        ValueError: If input shapes differ, are not `(N, 3)`, or any vector norm is zero
    """
    if model_pos.shape != obs_pos.shape:
        raise ValueError("model_pos and obs_pos must have the same shape")
    if model_pos.ndim != 2 or model_pos.shape[1] != 3:
        raise ValueError("model_pos and obs_pos must have shape (N, 3)")

    # Compute vector magnitudes for normalization.
    model_norm = np.linalg.norm(model_pos, axis=1, keepdims=True)
    obs_norm = np.linalg.norm(obs_pos, axis=1, keepdims=True)
    if np.any(model_norm == 0.0) or np.any(obs_norm == 0.0):
        raise ValueError("Cannot compute angular separation for zero-length vectors")

    # Normalize vectors to compare direction only (not magnitude).
    model_unit = model_pos / model_norm
    obs_unit = obs_pos / obs_norm
    dots = np.sum(model_unit * obs_unit, axis=1)
    dots = np.clip(dots, -1.0, 1.0)

    # Convert angular separation from radians to arcseconds.
    sep_rad = np.arccos(dots)
    sep_arcsec = np.rad2deg(sep_rad) * 3600.0
    return float(np.sqrt(np.mean(sep_arcsec**2)))


def xyz_rms_km(model_pos: np.ndarray, obs_pos: np.ndarray) -> float:
    """
    Compute RMS 3D position error between modeled and observed vectors.

    Args:
        model_pos (np.ndarray): Modeled Cartesian position vectors with shape (N, 3)
        obs_pos (np.ndarray): Observed Cartesian position vectors with shape (N, 3)

    Returns:
        float: Root-mean-square 3D position residual in kilometers

    Raises:
        ValueError: If input shapes differ or are not `(N, 3)`
    """
    # Ensure both arrays represent the same sampled points.
    if model_pos.shape != obs_pos.shape:
        raise ValueError("model_pos and obs_pos must have the same shape")

    # Expect one 3D Cartesian position per sample.
    if model_pos.ndim != 2 or model_pos.shape[1] != 3:
        raise ValueError("model_pos and obs_pos must have shape (N, 3)")

    # Compute per-sample squared 3D distance, then return RMS in km.
    return float(np.sqrt(np.mean(np.sum((model_pos - obs_pos) ** 2, axis=1))))


def build_satrec_from_params(
    template: Satrec,
    x: np.ndarray,
    *,
    epoch_ut1_jd: float | None = None,
) -> Satrec:
    """
    Build a new `Satrec` from an optimized TLE parameter vector.

    Args:
        template (Satrec): Seed satellite record providing metadata
        x (np.ndarray): Fit vector ordered as
        [inclo, nodeo, ecco, argpo, mo, no_kozai, ndot, bstar]
        epoch_ut1_jd: UT1 Julian date for ``sgp4init``; defaults to the seed
            TLE epoch when omitted.

    Returns:
        Satrec: Re-initialized SGP4 satellite record with fitted elements

    Raises:
        ValueError: If `x` does not contain at least 8 parameters
    """
    if x.shape[0] < 8:
        raise ValueError("Expected at least 8 fit parameters in x")

    sat = Satrec()
    ndot = float(x[6])
    bstar = float(x[7])

    if epoch_ut1_jd is None:
        epoch_days = (
            template.jdsatepoch + template.jdsatepochF - SGP4_EPOCH_REFERENCE_JD
        )
    else:
        epoch_days = sgp4_epoch_days_from_ut1_jd(epoch_ut1_jd)

    sat.sgp4init(
        WGS84,
        template.operationmode,
        template.satnum,
        epoch_days,
        bstar,
        ndot,
        template.nddot,
        float(x[2]),
        wrap_angle_rad(float(x[3])),
        float(x[0]),
        wrap_angle_rad(float(x[4])),
        float(x[5]),
        wrap_angle_rad(float(x[1])),
    )

    # Preserve catalog/export metadata required by export_tle().
    for attr in (
        "satnum_str",
        "classification",
        "intldesg",
        "ephtype",
        "elnum",
        "revnum",
    ):
        if hasattr(template, attr):
            setattr(sat, attr, getattr(template, attr))
    return sat


def build_unconstrained_tle_param_transform(
    seed_params: np.ndarray,
) -> tuple[Callable[[np.ndarray], np.ndarray], np.ndarray]:
    """
    Build an unconstrained LM parameterization for ``ecco``, ``no_kozai``, and
    ``bstar``.

    Levenberg–Marquardt does not support bounds. Three elements use the same map:
    ``physical[i] = center + half_width * tanh(u_i)`` so each unconstrained
    ``u_i`` can roam while staying in a finite interval. Indices ``0``, ``1``,
    ``3``, ``4``, ``6`` (``inclo``, ``nodeo``, ``argpo``, ``mo``, ``ndot``) copy
    through unchanged.

    **ecco** (index ``2``): Band is an absolute eccentricity interval
    ``[ecc_min, ecc_max]`` with center at the midpoint (not the seed). Keeps ecc
    off the negative / hyperbolic ``sgp4init`` failures and bounded for a sane
    LEO regime; see the implementation for ``ecc_min`` / ``ecc_max``. Starting
    ``unconstrained_seed[2]`` is set from ``arctanh`` so the seed eccentricity is
    reproduced.

    **no_kozai** (index ``5``): Band is relative to the seed mean motion (about
    ±5% of the seed), trimmed so the upper edge stays safely below ~0.074 rad/min
    (below the regime where ``sgp4init`` returns err=1, ``a < 0.95 ER``).

    **bstar** (index ``7``): Band is centered on the seed drag term with
    half-width ``max(0.5 * |bstar_seed|, 1e-7)``. ``no_kozai`` and ``bstar`` both
    use ``u=0`` at the seed so ``unconstrained_seed[5] ==
    unconstrained_seed[7] == 0`` recovers seed mean motion and BSTAR.

    Args:
        seed_params (np.ndarray): Physical seed parameter vector in the order
            ``[inclo, nodeo, ecco, argpo, mo, no_kozai, ndot, bstar]``.

    Returns:
        tuple[Callable[[np.ndarray], np.ndarray], np.ndarray]:
            ``(unconstrained_to_physical, unconstrained_seed)`` where
            ``unconstrained_to_physical(unconstrained)`` yields a physical
            parameter vector in the same order as ``get_fit_params_from_satrec``,
            and ``unconstrained_seed`` reproduces ``seed_params``.
    """
    if seed_params.shape[0] < 8:
        raise ValueError("Expected at least 8 seed parameters in seed_params")

    seed_params = np.asarray(seed_params, dtype=np.float64)

    # Eccentricity band: lower bound avoids sgp4init ecc < 0 branch; upper cap
    # keeps the fit in a sensible LEO regime.
    ecc_min = 1e-8
    ecc_seed = float(np.clip(seed_params[2], ecc_min + 1e-15, None))
    ecc_max = max(5e-3, min(0.25, max(ecc_seed * 5.0, ecc_seed * 1.001 + 1e-12)))
    if ecc_max <= ecc_min + 1e-15:
        ecc_max = ecc_min + 1e-6
    ecc_center = 0.5 * (ecc_min + ecc_max)
    ecc_half_width = 0.5 * (ecc_max - ecc_min)

    no_kozai_seed = float(seed_params[5])
    if no_kozai_seed <= 0.0:
        raise ValueError(f"Seed no_kozai must be > 0, got {no_kozai_seed}")

    # Mean-motion half-width: ±5% of seed, but never so large that the upper
    # bound approaches the ~0.0764 rad/min regime where sgp4init returns err=1
    # (a < 0.95 Earth radii). Use 0.074 as a conservative ceiling.
    no_kozai_safe_max = 0.074
    no_kozai_relative_band = 0.05 * no_kozai_seed
    no_kozai_ceiling_margin = no_kozai_safe_max - no_kozai_seed
    if no_kozai_ceiling_margin > 1e-12:
        no_kozai_half_width = min(
            no_kozai_relative_band, 0.95 * no_kozai_ceiling_margin
        )
    else:
        no_kozai_half_width = min(no_kozai_relative_band, 0.01 * no_kozai_seed)
    no_kozai_half_width = max(float(no_kozai_half_width), 1e-12)

    bstar_seed = float(seed_params[7])
    bstar_center = bstar_seed
    bstar_half_width = max(abs(bstar_seed) * 0.5, 1e-7)

    def unconstrained_to_physical(unconstrained: np.ndarray) -> np.ndarray:
        unconstrained = np.asarray(unconstrained, dtype=np.float64)
        physical = unconstrained.copy()
        physical[2] = ecc_center + ecc_half_width * np.tanh(float(unconstrained[2]))
        physical[5] = no_kozai_seed + no_kozai_half_width * np.tanh(
            float(unconstrained[5])
        )
        physical[7] = bstar_center + bstar_half_width * np.tanh(float(unconstrained[7]))
        return physical

    unconstrained_seed = seed_params.copy()
    ecc_normalized = (ecc_seed - ecc_center) / ecc_half_width
    ecc_normalized = float(np.clip(ecc_normalized, -0.999999, 0.999999))
    unconstrained_seed[2] = float(np.arctanh(ecc_normalized))
    unconstrained_seed[5] = 0.0
    if bstar_half_width > 0:
        bstar_norm = (bstar_seed - bstar_center) / bstar_half_width
        bstar_norm = float(np.clip(bstar_norm, -0.999999, 0.999999))
        unconstrained_seed[7] = float(np.arctanh(bstar_norm))

    return unconstrained_to_physical, unconstrained_seed


def residuals_from_unconstrained_params(
    unconstrained_params: np.ndarray,
    unconstrained_to_physical: Callable[[np.ndarray], np.ndarray],
    template_satrec: Satrec,
    jd: np.ndarray,
    pos_obs_km: np.ndarray,
    km_scale: float,
    epoch_ut1_jd: float,
) -> np.ndarray:
    """
    Evaluate ``residuals`` after mapping unconstrained params to physical ones.

    Args:
        unconstrained_params (np.ndarray): Unconstrained iterate driven by LM.
        unconstrained_to_physical (Callable): Mapping built by
            ``build_unconstrained_tle_param_transform``.
        template_satrec (Satrec): Template satellite record used for metadata
            in ``build_satrec_from_params``.
        jd (np.ndarray): Julian dates for propagation, shape ``(N,)``.
        pos_obs_km (np.ndarray): Observed TEME positions in km, shape ``(N, 3)``.
        km_scale (float): Residual scaling factor in kilometers.
        epoch_ut1_jd (float): UT1 Julian date anchored at the fit-window midpoint.

    Returns:
        np.ndarray: Flattened residual vector with shape ``(3N,)``.
    """
    physical_params = unconstrained_to_physical(unconstrained_params)
    return residuals(
        physical_params,
        template_satrec,
        jd,
        pos_obs_km,
        km_scale,
        epoch_ut1_jd,
    )


def residuals(
    x: np.ndarray,
    template_satrec: Satrec,
    jd: np.ndarray,
    pos_obs_km: np.ndarray,
    km_scale: float,
    epoch_ut1_jd: float,
) -> np.ndarray:
    """
    Build scaled residuals for least-squares fitting of TLE parameters.

    Any SGP4 propagation failure or non-finite output is converted to a large
    finite residual vector (``LARGE_RESIDUAL`` per element). This lets
    ``least_squares`` (method='lm') back off via its damping parameter when the
    optimizer wanders into a region that produces an invalid TLE
    (e.g. ``ecc < 0``, ``ecc >= 1``, ``a < 0.95 ER``) instead of raising and
    aborting the whole fit.

    Args:
        x (np.ndarray): Fit parameter vector
        template_satrec (Satrec): Template satellite record used for metadata
        jd (np.ndarray): Julian dates for propagation, shape `(N,)`
        pos_obs_km (np.ndarray): Observed TEME positions in km, shape `(N, 3)`
        km_scale (float): Residual scaling factor in kilometers
        epoch_ut1_jd (float): UT1 Julian date for ``sgp4init`` (fit-window midpoint)

    Returns:
        np.ndarray: Flattened residual vector with shape `(3N,)`

    Raises:
        ValueError: If `km_scale <= 0` or `pos_obs_km` is not shape `(N, 3)`
    """
    if km_scale <= 0:
        raise ValueError("km_scale must be > 0")
    if pos_obs_km.ndim != 2 or pos_obs_km.shape[1] != 3:
        raise ValueError("pos_obs_km must have shape (N, 3)")

    penalty_vec = np.full(pos_obs_km.size, LARGE_RESIDUAL, dtype=float)

    try:
        satrec = build_satrec_from_params(template_satrec, x, epoch_ut1_jd=epoch_ut1_jd)
        pos_model_km = propagate_teme_positions_km(satrec, jd)
    except (RuntimeError, ValueError, OverflowError, FloatingPointError):
        return penalty_vec

    if pos_model_km.shape != pos_obs_km.shape:
        return penalty_vec
    if not np.all(np.isfinite(pos_model_km)):
        return penalty_vec

    # least_squares expects a 1D residual vector; flatten [N,3] -> [3N].
    return ((pos_model_km - pos_obs_km) / km_scale).ravel()


def create_tle_from_ephemeris(
    ephemeris: InterpolableEphemeris,
    cursor,
    connection,
) -> tuple[float, float]:
    """
    Fit a TLE to ephemeris position samples using nonlinear least squares.

    Only the first ``TLE_FIT_WINDOW_HOURS`` of ``ephemeris.points`` are used
    for the fit. The returned XYZ / angular RMS are computed against **that
    same subset** -- they are in-sample residuals over the fit window, not
    over the full ``EPHEMERIS_DB_SPAN_HOURS`` retained in the database.

    Before saving, the fitted TLE is also propagated across **every stored
    ephemeris point** (the full ``EPHEMERIS_DB_SPAN_HOURS``). If SGP4 fails
    anywhere in that span the TLE is rejected -- the propagation exception
    propagates and ``save_tle_to_db`` is never called. When propagation
    succeeds, fit-window, full-ephemeris, and out-of-window RMS values are
    logged together in a single ``INFO`` message (not used for validation yet.)

    Args:
        ephemeris (InterpolableEphemeris): Ephemeris object with timestamped
            position vectors used as fit targets.

    Returns:
        tuple[float, float]: XYZ RMS (km) and angular RMS (arcsec) of the
            fitted TLE versus the ephemeris samples **inside the fit window**.

    Raises:
        ValueError: If ephemeris has fewer than two points (overall or in the
            fit window), if no seed TLE exists in the database, or if the
            least-squares fit does not converge.
        RuntimeError: If SGP4 fails to propagate the fitted TLE at any
            stored ephemeris epoch after the optimizer converged (whether
            inside or outside the fit window). The TLE is not saved.
    """
    if len(ephemeris.points) < 2:
        raise ValueError("At least two ephemeris points are required to fit a TLE")

    # Residual scaling (km) to keep least-squares numerics well-conditioned.
    km_scale = 10.0
    max_nfev = 600

    # Query a nearby catalog TLE to seed the optimizer.
    seed_lines = get_closest_tle(ephemeris.ephemeris_start, ephemeris.sat_id, cursor)
    if seed_lines is None:
        raise ValueError(
            f"No catalog TLE found for sat_id={ephemeris.sat_id} "
            f"near ephemeris_start={ephemeris.ephemeris_start}"
        )
    line1, line2 = seed_lines

    seed_sat = Satrec.twoline2rv(line1, line2)

    # Limit the fit to the first ``TLE_FIT_WINDOW_HOURS`` of the ephemeris.
    # The DB stores up to ``EPHEMERIS_DB_SPAN_HOURS``; the fit window is a
    # strict subset chosen for accuracy over the full stored span.
    timestamped = [
        (
            (
                p.timestamp.replace(tzinfo=timezone.utc)
                if p.timestamp.tzinfo is None
                else p.timestamp.astimezone(timezone.utc)
            ),
            p,
        )
        for p in ephemeris.points
    ]
    timestamped.sort(key=lambda kv: kv[0])
    sorted_points = [p for _, p in timestamped]
    window_start = timestamped[0][0]
    window_end = window_start + timedelta(hours=TLE_FIT_WINDOW_HOURS)
    fit_window_points = [p for ts, p in timestamped if ts <= window_end]

    if len(fit_window_points) < 2:
        raise ValueError(
            f"Only {len(fit_window_points)} ephemeris point(s) in the first "
            f"{TLE_FIT_WINDOW_HOURS:g} h window; need at least 2 to fit a TLE"
        )

    logging.info(
        "Restricting fit to %d of %d points in [%s, %s] (first %g h of ephemeris)",
        len(fit_window_points),
        len(sorted_points),
        window_start.isoformat(),
        fit_window_points[-1].timestamp.isoformat(),
        TLE_FIT_WINDOW_HOURS,
    )

    # Convert point timestamps to UT1 Julian dates for SGP4 calls. Build two
    # parallel arrays:
    #   * ``jd_fit`` / ``pos_fit`` -- the fit-window subset used by the
    #     optimizer (and reported as in-sample RMS).
    #   * ``jd_full`` / ``pos_full`` -- every stored point (up to
    #     ``EPHEMERIS_DB_SPAN_HOURS``) used for the post-fit generalization
    #     check below.
    def _to_jd(points: list[EphemerisPoint]) -> np.ndarray:
        return np.array(
            [
                float(Time(p.timestamp, format="datetime", scale="utc").ut1.jd)
                for p in points
            ],
            dtype=np.float64,
        )

    def _to_pos_km(points: list[EphemerisPoint]) -> np.ndarray:
        return np.vstack([np.asarray(p.position, dtype=np.float64) for p in points])

    jd_fit = _to_jd(fit_window_points)
    pos_fit = _to_pos_km(fit_window_points)
    jd_full = _to_jd(sorted_points)
    pos_full = _to_pos_km(sorted_points)

    fit_epoch_dt = fit_window_epoch_datetime(window_start)
    fit_epoch_jd = ut1_jd_from_datetime(fit_epoch_dt)
    x0 = seed_params_at_epoch(line1, line2, fit_epoch_dt)
    logging.info(
        "TLE fit epoch at fit-window midpoint: %s (UT1 JD %.8f)",
        fit_epoch_dt.isoformat(),
        fit_epoch_jd,
    )

    # Baseline error from the seed TLE on the fit window only.
    seed_pos = propagate_teme_positions_km(seed_sat, jd_fit)
    seed_xyz_rms = xyz_rms_km(seed_pos, pos_fit)
    seed_ang_rms = angular_rms_arcsec(seed_pos, pos_fit)
    logging.info(
        "Seed TLE vs fit window (%d epochs): XYZ RMS %.3f km, angular RMS %.3f arcsec",
        len(jd_fit),
        seed_xyz_rms,
        seed_ang_rms,
    )

    # Reparameterize ecco (absolute safe band), no_kozai (relative + SGP4
    # ceiling), and bstar (relative drag band) via tanh so LM stays in
    # physically safe ranges without TRF bounds.
    unconstrained_to_physical, unconstrained_seed = (
        build_unconstrained_tle_param_transform(x0)
    )

    # Optimize fit parameters to minimize scaled position residuals.
    result = least_squares(
        residuals_from_unconstrained_params,
        unconstrained_seed,
        args=(
            unconstrained_to_physical,
            seed_sat,
            jd_fit,
            pos_fit,
            km_scale,
            fit_epoch_jd,
        ),
        method="lm",
        max_nfev=max_nfev,
    )

    if not result.success:
        logging.error(
            "least_squares did not converge: %s (nfev=%s); TLE not saved",
            result.message,
            result.nfev,
        )
        raise ValueError(f"Least-squares TLE fit did not converge: {result.message}")

    fitted_params = unconstrained_to_physical(result.x)

    # Evaluate final fit quality on the fit window (in-sample residuals).
    fitted = build_satrec_from_params(
        seed_sat, fitted_params, epoch_ut1_jd=fit_epoch_jd
    )
    fit_pos = propagate_teme_positions_km(fitted, jd_fit)
    fit_xyz_rms = xyz_rms_km(fit_pos, pos_fit)
    fit_ang_rms = angular_rms_arcsec(fit_pos, pos_fit)

    # Validation: the fitted TLE must also propagate over every stored
    # ephemeris point (the full ``EPHEMERIS_DB_SPAN_HOURS``).
    full_pos = propagate_teme_positions_km(fitted, jd_full)
    full_xyz = xyz_rms_km(full_pos, pos_full)
    full_ang = angular_rms_arcsec(full_pos, pos_full)

    # Out-of-window slice: every stored point after the last fit-window epoch.
    out_mask = jd_full > float(jd_fit[-1])
    out_xyz = xyz_rms_km(full_pos[out_mask], pos_full[out_mask])
    out_ang = angular_rms_arcsec(full_pos[out_mask], pos_full[out_mask])

    logging.info(
        "Fitted TLE residuals (same TLE, three spans):\n"
        "  fit window (%d pts): XYZ RMS %.3f km, angular RMS %.3f arcsec\n"
        "  full ephemeris (%d pts): XYZ RMS %.3f km, angular RMS %.3f arcsec\n"
        "  out-of-window (%d pts): XYZ RMS %.3f km, angular RMS %.3f arcsec\n"
        "  least_squares: cost=%.6g, nfev=%d",
        len(jd_fit),
        fit_xyz_rms,
        fit_ang_rms,
        len(jd_full),
        full_xyz,
        full_ang,
        int(np.count_nonzero(out_mask)),
        out_xyz,
        out_ang,
        result.cost,
        result.nfev,
    )

    date_collected = datetime.now(timezone.utc)
    save_tle_to_db(fitted, date_collected, ephemeris.sat_id, cursor, connection)

    return fit_xyz_rms, fit_ang_rms


def save_tle_to_db(
    satrec: Satrec,
    date_collected: datetime,
    sat_id: int,
    cursor,
    connection,
) -> None:
    """
    Export ``satrec`` to TLE text and insert it into the ``tle`` table.

    The TLE epoch is taken from ``satrec`` (converted from its internal Julian
    date to a UTC ``datetime``); ``data_source`` is fixed to ``"generated"`` and
    ``is_supplemental`` to ``False`` because this path only stores TLEs that
    were fitted by ``create_tle_from_ephemeris``. Inserts use
    ``ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING`` so duplicate runs
    are idempotent; a conflict logs a warning but does not raise.

    The two TLE lines are also logged at ``INFO`` for verification in logs.

    Args:
        satrec (Satrec): Fitted SGP4 satellite record to export.
        date_collected (datetime): When this TLE was produced (UTC).
        sat_id (int): Satellites table primary key the TLE belongs to.
        cursor: Database cursor used to execute SQL.
        connection: Database connection; ``commit()`` is called on success.
    """
    tle_line1, tle_line2 = export_tle(satrec)
    logging.info("Fitted TLE (verify before operational use):")
    logging.info(tle_line1)
    logging.info(tle_line2)

    epoch = Time(
        satrec.jdsatepoch + satrec.jdsatepochF,
        format="jd",
        scale="utc",
    ).to_datetime(timezone.utc)

    is_supplemental = False
    data_source = "generated"

    tle_insert_query = """
        INSERT INTO tle (SAT_ID, DATE_COLLECTED, TLE_LINE1, TLE_LINE2,
            EPOCH, IS_SUPPLEMENTAL, DATA_SOURCE)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (SAT_ID, EPOCH, DATA_SOURCE) DO NOTHING"""

    cursor.execute(
        tle_insert_query,
        (
            sat_id,
            date_collected,
            tle_line1,
            tle_line2,
            epoch,
            is_supplemental,
            data_source,
        ),
    )
    if cursor.rowcount == 0:
        logging.warning(
            "TLE not inserted (ON CONFLICT): sat_id=%s epoch=%s data_source=%s",
            sat_id,
            epoch,
            data_source,
        )
    connection.commit()
