import logging
import re
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import requests
from astropy.time import Time
from psycopg2.extras import execute_values
from scipy.optimize import least_squares
from sgp4.api import WGS84, Satrec
from sgp4.exporter import export_tle

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)


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
            logging.error(f"Satellite not found: {parsed_data['satellite_name']}")
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
            logging.error(
                f"Likely duplicate ephemeris data for {parsed_data['satellite_name']}"
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
            f"Successfully inserted {len(points)} "
            f"points for ephemeris_id {ephemeris_id}"
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
        logging.error(f"Error inserting ephemeris data: {e}")
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
        logging.warning(f"Could not parse satellite name from filename {filename}: {e}")

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
            logging.warning(f"Could not parse creation time: {headers['created']}")

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
                f"Could not parse ephemeris times: "
                f"{headers['ephemeris_start']} - "
                f"{headers['ephemeris_stop']}"
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

    # Filter data to only include 26 hours (1 day + 2 hours) from start
    timestamps_array = np.array(timestamps)
    positions_array = np.array(positions, dtype=np.float64)
    velocities_array = np.array(velocities, dtype=np.float64)
    covariances_array = np.array(covariances, dtype=np.float64)

    # Calculate cutoff time (26 hours from ephemeris start)
    cutoff_time = ephemeris_start + timedelta(hours=26)

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
    logging.info(f"Original data points: {original_count}")
    logging.info(f"Filtered data points (26 hours): {filtered_count}")
    logging.info(f"Data reduction: {original_count - filtered_count} points removed")
    logging.info(f"Parsed {filtered_count} timestamps")
    logging.info(f"Parsed {len(filtered_positions)} positions")
    logging.info(f"Parsed {len(filtered_velocities)} velocities")
    logging.info(f"Parsed {len(filtered_covariances)} covariances")
    logging.info(f"Ephemeris start: {ephemeris_start}")
    logging.info(f"Ephemeris stop: {ephemeris_stop}")
    logging.info(f"Generated at: {generated_at}")
    logging.info(f"Satellite name: {satellite_name}")
    logging.info(f"Filename: {filename}")

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


def insert_interpolated_splines(interpolated_splines, cursor, connection):
    """
    Insert interpolated splines into the database.
    """


def get_starlink_ephemeris_data(cursor, connection):
    """
    Fetch and process ephemeris data for Starlink satellites.

    This function:
    1. Downloads and processes each ephemeris data file
    2. Parses ephemeris data and inserts it into the database

    The function processes files in the following format:
    - Each ephemeris file contains satellite position, velocity, and covariance data
    - Files are named in format:
        MEME_57851_STARLINK-30405_1490204_Operational_1432778700_UNCLASSIFIED

    Args:
        cursor: Database cursor used to execute SQL.
        connection: Database connection for transaction management

    Raises:
        requests.HTTPError: If login to Space-Track fails
        Exception: For other errors during processing

    Note:
        - Uses ON CONFLICT DO NOTHING for database inserts to handle duplicates
    """
    try:
        with requests.Session() as session:
            # Retrieve list of ephemeris files
            ephemeris_response = session.get(
                "https://api.starlink.com/public-files/ephemerides/MANIFEST.txt",
                timeout=60,
            )
            ephemeris_response.raise_for_status()

            # Parse the manifest to get file names
            manifest_content = ephemeris_response.text
            ephemeris_files = [
                line.strip() for line in manifest_content.splitlines() if line.strip()
            ]

            files_processed = 0
            total_data_points = 0

            # Get today's date in UTC
            today = datetime.now(timezone.utc).date()

            logging.info(f"Today's date: {today}")
            logging.info(f"Found {len(ephemeris_files)} files in manifest")

            stats = []
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
                        logging.info(f"Skipping already processed file: {file_name}")
                        continue

                    # Download the file
                    file_url = (
                        f"https://api.starlink.com/public-files/ephemerides/{file_name}"
                    )
                    response = session.get(file_url, timeout=120)
                    response.raise_for_status()

                    logging.info(f"Processing file: {file_name}")

                    try:
                        file_content = response.content.decode("utf-8")
                        parsed_data = parse_ephemeris_file(file_content, file_name)
                        insert_result = insert_ephemeris_data(
                            parsed_data, cursor, connection
                        )
                        if insert_result is None:
                            logging.warning(
                                "Skipping TLE generation for %s: ephemeris insert "
                                "returned None (duplicate, missing satellite, etc.)",
                                file_name,
                            )
                            continue

                        ephemeris, ephemeris_id = insert_result

                        start_time = time.perf_counter()
                        fit_xyz_rms, fit_ang_rms = create_tle_from_ephemeris(
                            ephemeris, cursor, connection
                        )

                        end_time = time.perf_counter()
                        tle_generation_s = end_time - start_time

                        stats.append(
                            {
                                "tle_generation_s": tle_generation_s,
                                "fit_xyz_rms_km": fit_xyz_rms,
                                "fit_ang_rms_arcsec": fit_ang_rms,
                            }
                        )

                        num_points = len(ephemeris.points)

                    except Exception as e:
                        logging.error(
                            "Error parsing/inserting ephemeris data for file %s: %s",
                            file_name,
                            e,
                        )
                        try:
                            connection.rollback()
                        except Exception as rollback_err:
                            logging.warning(
                                "Rollback failed after insert error for %s: %s",
                                file_name,
                                rollback_err,
                            )
                        cursor = connection.cursor()
                        continue

                except Exception as e:
                    logging.error(f"Error processing file {file_name}: {e}")
                    try:
                        connection.rollback()
                    except Exception as rollback_err:
                        logging.warning(
                            "Rollback failed after processing error for %s: %s",
                            file_name,
                            rollback_err,
                        )
                    cursor = connection.cursor()
                    continue

                total_data_points += num_points
                files_processed += 1

            logging.info(f"Total data points: {total_data_points}")
            logging.info(f"Files processed: {files_processed}")
            if stats:
                times = np.array([s["tle_generation_s"] for s in stats], dtype=float)
                xyz_rms = np.array([s["fit_xyz_rms_km"] for s in stats], dtype=float)
                ang_rms = np.array(
                    [s["fit_ang_rms_arcsec"] for s in stats], dtype=float
                )

                logging.info(
                    "TLE generation aggregate stats for %d ephemerides:",
                    len(stats),
                )
                logging.info(
                    "  Time (s): mean=%.3f median=%.3f p95=%.3f min=%.3f max=%.3f",
                    float(np.mean(times)),
                    float(np.median(times)),
                    float(np.percentile(times, 95)),
                    float(np.min(times)),
                    float(np.max(times)),
                )
                logging.info(
                    "  XYZ RMS (km): mean=%.6f median=%.6f p95=%.6f min=%.6f max=%.6f",
                    float(np.mean(xyz_rms)),
                    float(np.median(xyz_rms)),
                    float(np.percentile(xyz_rms, 95)),
                    float(np.min(xyz_rms)),
                    float(np.max(xyz_rms)),
                )
                logging.info(
                    (
                        "  Angle RMS (arcsec): mean=%.6f median=%.6f "
                        "p95=%.6f min=%.6f max=%.6f"
                    ),
                    float(np.mean(ang_rms)),
                    float(np.median(ang_rms)),
                    float(np.percentile(ang_rms, 95)),
                    float(np.min(ang_rms)),
                    float(np.max(ang_rms)),
                )
    except Exception as err:
        logging.error(f"Error getting ephemeris data for Starlink satellites: {err}")
        raise


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

    Rows whose ``epoch`` falls in ``[ephemeris_start_time,
    ephemeris_start_time + 8h]`` are sorted first. Within each group, the row
    with ``epoch`` closest to ``ephemeris_start_time + 8h`` (absolute time
    difference) wins. If the window is empty, this falls back to the globally
    closest ``epoch`` to that same target — same idea as
    ``TleRepository._get_closest_by_satellite_number``, but with ``sat_id`` and
    a soft preference for that 8h window (no ``data_source`` filter).

    Args:
        ephemeris_start_time (datetime): Ephemeris segment start.
        sat_id (int): Satellite primary key
        cursor: Database cursor used to execute SQL.

    Returns:
        TLE line 1 and line 2, or ``None`` if no row matches ``sat_id``.
    """

    target_time = ephemeris_start_time + timedelta(hours=8)

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
        logging.error(f"TLE not found: {ephemeris_start_time}")
        return None

    tle_line1 = tle_result[1]
    tle_line2 = tle_result[2]
    return tle_line1, tle_line2


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
) -> Satrec:
    """
    Build a new `Satrec` from an optimized TLE parameter vector.

    Args:
        template (Satrec): Seed satellite record providing metadata and epoch
        x (np.ndarray): Fit vector ordered as
        [inclo, nodeo, ecco, argpo, mo, no_kozai, ndot, bstar]

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

    # sgp4init() expects epoch as days since 1949-12-31 00:00 UT
    # (JD 2433281.5), so convert absolute JD by subtracting that reference epoch.
    sat.sgp4init(
        WGS84,
        template.operationmode,
        template.satnum,
        template.jdsatepoch + template.jdsatepochF - 2433281.5,
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


def residuals(
    x: np.ndarray,
    template_satrec: Satrec,
    jd: np.ndarray,
    pos_obs_km: np.ndarray,
    km_scale: float,
) -> np.ndarray:
    """
    Build scaled residuals for least-squares fitting of TLE parameters.

    Args:
        x (np.ndarray): Fit parameter vector
        template_satrec (Satrec): Template satellite record used for metadata/epoch
        jd (np.ndarray): Julian dates for propagation, shape `(N,)`
        pos_obs_km (np.ndarray): Observed TEME positions in km, shape `(N, 3)`
        km_scale (float): Residual scaling factor in kilometers

    Returns:
        np.ndarray: Flattened residual vector with shape `(3N,)`

    Raises:
        ValueError: If `km_scale <= 0` or propagated/observed shapes differ
    """
    if km_scale <= 0:
        raise ValueError("km_scale must be > 0")

    satrec = build_satrec_from_params(template_satrec, x)
    pos_model_km = propagate_teme_positions_km(satrec, jd)
    if pos_model_km.shape != pos_obs_km.shape:
        raise ValueError("Propagated and observed positions must have the same shape")

    # least_squares expects a 1D residual vector; flatten [N,3] -> [3N].
    return ((pos_model_km - pos_obs_km) / km_scale).ravel()


def create_tle_from_ephemeris(
    ephemeris: InterpolableEphemeris,
    cursor,
    connection,
) -> tuple[float, float]:
    """
    Fit a TLE to ephemeris position samples using nonlinear least squares.

    Args:
        ephemeris (InterpolableEphemeris): Ephemeris object with timestamped
            position vectors used as fit targets

    Returns:
        tuple[float, float]: XYZ RMS and angular RMS (arcsec) of the fitted TLE
            vs the ephemeris samples.

    Raises:
        ValueError: If ephemeris has fewer than two points, if no seed TLE exists
            in the database, or if the least-squares fit does not converge.
    """
    if len(ephemeris.points) < 2:
        raise ValueError("At least two ephemeris points are required to fit a TLE")

    # Residual scaling (km) to keep least-squares numerics well-conditioned.
    km_scale = 10.0
    max_nfev = 300

    # Query a nearby catalog TLE to seed the optimizer.
    seed_lines = get_closest_tle(ephemeris.ephemeris_start, ephemeris.sat_id, cursor)
    if seed_lines is None:
        raise ValueError(
            f"No catalog TLE found for sat_id={ephemeris.sat_id} "
            f"near ephemeris_start={ephemeris.ephemeris_start}"
        )
    line1, line2 = seed_lines

    seed_sat = Satrec.twoline2rv(line1, line2)
    x0 = get_fit_params_from_satrec(seed_sat)

    ephemeris_points = ephemeris.points
    # Convert point timestamps to UT1 Julian dates for SGP4 calls.
    jd = np.array(
        [
            float(Time(p.timestamp, format="datetime", scale="utc").ut1.jd)
            for p in ephemeris_points
        ],
        dtype=np.float64,
    )
    # Stack observed positions into an (N, 3) array in kilometers.
    pos_km = np.vstack(
        [np.asarray(p.position, dtype=np.float64) for p in ephemeris_points]
    )

    # Baseline error from the seed TLE before optimization.
    seed_pos = propagate_teme_positions_km(seed_sat, jd)
    seed_xyz_rms = xyz_rms_km(seed_pos, pos_km)
    seed_ang_rms = angular_rms_arcsec(seed_pos, pos_km)
    logging.info(f"Seed TLE vs ephemeris: {len(jd)} epochs")
    logging.info(f"  XYZ RMS: {seed_xyz_rms:.3f} km")
    logging.info(f"  Angle RMS: {seed_ang_rms:.3f} arcsec")

    # Optimize fit parameters to minimize scaled position residuals.
    result = least_squares(
        residuals,
        x0,
        args=(
            seed_sat,
            jd,
            pos_km,
            km_scale,
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

    # Evaluate final fit quality and export TLE text.
    fitted = build_satrec_from_params(seed_sat, result.x)
    fit_pos = propagate_teme_positions_km(fitted, jd)
    fit_xyz_rms = xyz_rms_km(fit_pos, pos_km)
    fit_ang_rms = angular_rms_arcsec(fit_pos, pos_km)

    logging.info(
        f"After fit: XYZ RMS={fit_xyz_rms:.3f} km, "
        f"Angle RMS={fit_ang_rms:.3f} arcsec "
        f"(cost={result.cost:.6g}, nfev={result.nfev})"
    )

    date_collected = datetime.now(timezone.utc)
    save_tle_to_db(fitted, date_collected, ephemeris.sat_id, cursor, connection)

    return fit_xyz_rms, fit_ang_rms


def save_tle_to_db(
    satrec: Satrec, date_collected: datetime, sat_id: int, cursor, connection
):

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
