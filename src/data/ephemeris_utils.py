import logging
import os
import re
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import boto3
import numpy as np
import psycopg2
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from frame_transforms import operator_position_frame_from_filename
from orbital_data_generation import (
    create_orbital_elements_from_ephemeris,
    # create_tle_from_ephemeris,
)
from psycopg2.extras import execute_values

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)

# How much of each ephemeris file we keep in the database. Anything beyond this
# horizon from ``ephemeris_start`` is dropped in ``parse_ephemeris_file``.
EPHEMERIS_DB_SPAN_HOURS = 26.0

DEFAULT_ARCHIVE_SHARD_BYTES = 256 * 1024 * 1024
DEFAULT_ARCHIVE_WRITE_BATCH_ROWS = 50_000
DEFAULT_ARCHIVE_DB_UPDATE_CHUNK = 5_000

EPHEMERIS_POINTS_S3_BUCKET = os.environ.get("EPHEMERIS_POINTS_S3_BUCKET", "bucket-name")
EPHEMERIS_POINTS_S3_REGION = "us-west-2"
EPHEMERIS_POINTS_S3_PREFIX = "starlink-ephemeris-data/ephemeris-shards"

_POINTS_FOR_ARCHIVE_SQL = """
    SELECT
        ep.ephemeris_id,
        ep.timestamp,
        ep.position,
        ep.velocity,
        ep.covariance
    FROM ephemeris_points ep
    WHERE ep.ephemeris_id = %s
    ORDER BY ep.timestamp
"""


def insert_ephemeris_data(
    parsed_data, cursor, connection, run_id
) -> tuple[InterpolableEphemeris, int] | None:
    """
    Insert ephemeris data into the database efficiently using batch inserts.

    Args:
        parsed_data (dict): Dictionary containing parsed ephemeris data
        cursor: Database cursor
        connection: Database connection
        run_id: Run ID for the ephemeris data set collection
    Returns:
        tuple[InterpolableEphemeris, int]: The created ephemeris and its DB id if
        successful, None if duplicate
    """
    try:
        # TODO: fix usage of has_current_sat_number
        cursor.execute(
            "SELECT id FROM satellites "
            "WHERE sat_name = %s "
            "AND has_current_sat_number = true",
            (parsed_data["satellite_name"],),
        )
        satellite_result = cursor.fetchone()
        if satellite_result is None:
            logging.info("Satellite not found: %s", parsed_data["satellite_name"])
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
                frame,
                run_id
            ) VALUES (
                %s,
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
                run_id,
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
            - frame (str): Position frame (``MEME`` for Starlink operator files
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
        "frame": operator_position_frame_from_filename(filename),
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
       OMM element set from the first ``ORBITAL_DATA_FIT_WINDOW_HOURS`` of stored data
       (````).
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

        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

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
                insert_result = insert_ephemeris_data(
                    parsed_data, cursor, connection, run_id
                )
                if insert_result is None:
                    logging.warning(
                        "Skipping TLE generation for %s: ephemeris insert "
                        "returned None (duplicate, missing satellite, etc.)",
                        file_name,
                    )
                    continue
                ephemeris, _ephemeris_id = insert_result

                t0 = time.perf_counter()
                try:
                    omm_xyz_rms, omm_ang_rms = create_orbital_elements_from_ephemeris(
                        ephemeris, cursor, connection
                    )
                    if not (omm_xyz_rms == -1 and omm_ang_rms == -1):
                        stats.append(
                            {
                                "orbital_data_generation_s": time.perf_counter() - t0,
                                "fit_xyz_rms_km": omm_xyz_rms,
                                "fit_ang_rms_arcsec": omm_ang_rms,
                            }
                        )
                        total_data_points += len(ephemeris.points)
                        files_processed += 1
                except Exception as omm_err:
                    logging.warning(
                        "OMM generation failed for %s: %s", file_name, omm_err
                    )
                    try:
                        connection.rollback()
                    except Exception as rollback_err:
                        logging.warning(
                            "Rollback failed for %s: %s", file_name, rollback_err
                        )
                    cursor = connection.cursor()

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
        _log_orbital_data_generation_stats(stats, label="OMM")


def _log_orbital_data_generation_stats(
    stats: list[dict[str, float]], label: str = "OMM"
) -> None:
    """Log mean/median/p95/min/max for timing and RMS across a batch."""
    if not stats:
        return

    times = np.array([s["orbital_data_generation_s"] for s in stats], dtype=float)
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

    logging.info("%s generation aggregate stats for %d ephemerides:", label, len(stats))
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


def _parquet_tmp_path(local_path: Path) -> Path:
    return local_path.with_name(local_path.name + ".tmp")


def _append_batch_to_parquet(
    batch: list[dict], tmp_path: Path, writer: pq.ParquetWriter | None
) -> pq.ParquetWriter | None:
    """Append rows to a single open shard file; create writer on first batch."""
    if not batch:
        return writer
    table = pa.Table.from_pylist(batch)
    if writer is None:
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        writer = pq.ParquetWriter(tmp_path, table.schema, compression="zstd")
    writer.write_table(table)
    return writer


def _s3_client():
    return boto3.client("s3", region_name=EPHEMERIS_POINTS_S3_REGION)


def _upload_file_to_s3(local_path: Path, key: str) -> None:
    logging.info(
        "Uploading %s → s3://%s/%s",
        local_path,
        EPHEMERIS_POINTS_S3_BUCKET,
        key,
    )
    _s3_client().upload_file(str(local_path), EPHEMERIS_POINTS_S3_BUCKET, key)


def _delete_s3_object(key: str) -> None:
    logging.warning(
        "Deleting S3 object s3://%s/%s",
        EPHEMERIS_POINTS_S3_BUCKET,
        key,
    )
    _s3_client().delete_object(Bucket=EPHEMERIS_POINTS_S3_BUCKET, Key=key)


def _fetch_points_for_ephemeris(cursor, ephemeris_id: int) -> list[dict]:
    """Load all points for one interpolable_ephemeris row (one file per query)."""
    cursor.execute(_POINTS_FOR_ARCHIVE_SQL, (ephemeris_id,))
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]


def _select_ephemeris_ids_for_archive(cursor) -> list[int]:
    """
    Ephemeris primary keys to copy to S3 on this cron run.

    Requires ``interpolable_ephemeris.run_id``. Archives ephemerides in the oldest
    ``run_id`` batch that still have ``parquet_points_file`` unset (skips rows
    already archived in a partial run). Only rows with ``generated_at`` older than
    one week are eligible.
    """
    cursor.execute("""
        SELECT id FROM interpolable_ephemeris
        WHERE run_id = (
            SELECT run_id FROM interpolable_ephemeris
            WHERE (parquet_points_file IS NULL OR parquet_points_file = '')
              AND generated_at < NOW() - INTERVAL '7 days'
            ORDER BY generated_at ASC
            LIMIT 1
        )
          AND (parquet_points_file IS NULL OR parquet_points_file = '')
          AND generated_at < NOW() - INTERVAL '7 days'
        ORDER BY id
        """)
    return [int(row[0]) for row in cursor.fetchall()]


def _archive_batch_run_id(cursor) -> str:
    """
    Folder name under S3 for this archive (same ``run_id`` as selection query).

    Must match the subquery logic in ``_select_ephemeris_ids_for_archive``.
    """
    cursor.execute("""
        SELECT run_id FROM interpolable_ephemeris
        WHERE (parquet_points_file IS NULL OR parquet_points_file = '')
          AND generated_at < NOW() - INTERVAL '7 days'
        ORDER BY generated_at ASC
        LIMIT 1
        """)
    row = cursor.fetchone()
    if row is None or row[0] is None:
        raise RuntimeError("No archivable run_id found (parquet_points_file IS NULL)")
    return str(row[0])


def _update_parquet_points_file(
    cursor,
    connection,
    ephemeris_ids: list[int],
    s3_key: str,
    *,
    chunk_size: int = DEFAULT_ARCHIVE_DB_UPDATE_CHUNK,
) -> None:
    """
    Point every ephemeris in this shard at the same S3 object key.

    All ids in one Parquet shard share one ``parquet_points_file`` value. Commits
    immediately so a later shard failure does not roll back earlier shards.
    """
    if not ephemeris_ids:
        return
    sql = """
        UPDATE interpolable_ephemeris
        SET parquet_points_file = %s
        WHERE id = ANY(%s)
    """
    for start in range(0, len(ephemeris_ids), chunk_size):
        chunk = ephemeris_ids[start : start + chunk_size]
        cursor.execute(sql, (s3_key, chunk))
    connection.commit()


class _RunParquetArchiver:
    """
    Build one or more Parquet shards under ``work_dir``, then upload each to S3.

    Rotation is by compressed ``.tmp`` size (``target_bytes``), not ephemeris count,
    because points per ephemeris vary. Whole ephemeris rows are kept in one shard
    before rotate is checked (an ephemeris is not split across files).
    """

    def __init__(
        self,
        *,
        cursor,
        connection,
        work_dir: Path,
        s3_prefix: str,
        target_bytes: int = DEFAULT_ARCHIVE_SHARD_BYTES,
        write_batch_size: int = DEFAULT_ARCHIVE_WRITE_BATCH_ROWS,
    ) -> None:
        self._cursor = cursor
        self._connection = connection
        self._work_dir = work_dir
        self._s3_prefix = s3_prefix.strip("/")
        self._target_bytes = target_bytes
        self._write_batch_size = write_batch_size

        self._shard_index = -1
        self._local_path: Path | None = None
        self._tmp_path: Path | None = None
        self._writer: pq.ParquetWriter | None = None
        self._batch: list[dict] = []
        self._row_count = 0
        self._ephemeris_ids: list[int] = []
        self._published_shards = 0
        self._published_rows = 0

    def _s3_key(self) -> str:
        return f"{self._s3_prefix}/part-{self._shard_index:03d}.parquet"

    def _tmp_size_bytes(self) -> int:
        if self._tmp_path and self._tmp_path.is_file():
            return self._tmp_path.stat().st_size
        return 0

    def _open_next_shard(self) -> None:
        self._shard_index += 1
        name = f"part-{self._shard_index:03d}.parquet"
        self._local_path = self._work_dir / name
        self._tmp_path = _parquet_tmp_path(self._local_path)
        if self._tmp_path.exists():
            self._tmp_path.unlink()
        self._writer = None
        self._batch = []
        self._row_count = 0
        self._ephemeris_ids = []
        logging.info("Opening archive shard %03d", self._shard_index)

    def _flush_batch(self) -> None:
        if not self._batch or self._tmp_path is None:
            return
        self._writer = _append_batch_to_parquet(
            self._batch, self._tmp_path, self._writer
        )
        self._batch = []

    def _publish_current_shard(self) -> None:
        """
        Finalize Parquet, upload, record S3 key in Postgres, remove local copy.

        If DB update fails after S3 upload, delete the new object so we do not
        leave an orphan; ``parquet_points_file`` stays unset for retry.
        """
        if self._shard_index < 0 or self._row_count == 0:
            return

        if self._writer is not None:
            self._writer.close()
            self._writer = None
        self._flush_batch()

        if self._tmp_path is None or self._local_path is None:
            raise RuntimeError("No open archive shard when publishing")
        if not self._tmp_path.is_file():
            raise RuntimeError(f"Missing temporary Parquet file: {self._tmp_path}")
        if self._local_path.exists():
            self._local_path.unlink()
        self._tmp_path.replace(self._local_path)

        size_bytes = self._local_path.stat().st_size
        s3_key = self._s3_key()
        ephemeris_ids = list(self._ephemeris_ids)

        try:
            _upload_file_to_s3(self._local_path, s3_key)
            _update_parquet_points_file(
                self._cursor, self._connection, ephemeris_ids, s3_key
            )
        except Exception:
            try:
                _delete_s3_object(s3_key)
            except Exception as cleanup_exc:
                logging.error(
                    "Could not delete S3 object after failed publish %s: %s",
                    s3_key,
                    cleanup_exc,
                )
            raise
        finally:
            for path in (self._local_path, _parquet_tmp_path(self._local_path)):
                if path.is_file():
                    path.unlink()

        self._published_shards += 1
        self._published_rows += self._row_count
        logging.info(
            "Published shard %03d: %d ephemerides, %d rows, %.2f MiB → %s",
            self._shard_index,
            len(ephemeris_ids),
            self._row_count,
            size_bytes / (1024 * 1024),
            s3_key,
        )

        self._row_count = 0
        self._ephemeris_ids = []
        self._local_path = None
        self._tmp_path = None

    def _close_shard_if_full(self) -> None:
        """Start a new part-NNN file when the current compressed tmp reaches the cap."""
        if self._tmp_size_bytes() >= self._target_bytes:
            self._publish_current_shard()
            self._open_next_shard()

    def append_ephemeris(self, ephemeris_id: int, rows: list[dict]) -> int:
        """Add one ephemeris worth of points; rotate shard if tmp file is full."""
        if not rows:
            return 0
        if self._shard_index < 0:
            self._open_next_shard()

        n_added = 0
        for row in rows:
            self._batch.append(row)
            n_added += 1
            if len(self._batch) >= self._write_batch_size:
                self._flush_batch()

        self._flush_batch()
        self._row_count += n_added
        self._ephemeris_ids.append(ephemeris_id)
        self._close_shard_if_full()
        return n_added

    def close(self) -> tuple[int, int]:
        """Publish the last open shard if it has any rows."""
        if self._shard_index >= 0 and self._row_count > 0:
            self._publish_current_shard()
        return self._published_shards, self._published_rows


def archive_starlink_ephemeris_data(
    cursor,
    connection,
    *,
    target_shard_bytes: int = DEFAULT_ARCHIVE_SHARD_BYTES,
    write_batch_size: int = DEFAULT_ARCHIVE_WRITE_BATCH_ROWS,
) -> None:
    """
    Archive one ``run_id`` batch from Postgres to S3 (ZSTD Parquet, ~256 MiB shards).

    Called from ``retrieve_tle_aws`` after ``get_starlink_ephemeris_data``. Ingest
    and archive are separate: this function only processes rows chosen by
    ``_select_ephemeris_ids_for_archive`` (oldest pending ``run_id``, at least one
    week old).

    S3 layout: ``{prefix}/{run_id}/part-000.parquet``, etc.

    Uses a process temp directory; does not delete ``ephemeris_points`` rows after
    upload (retention is separate).

    Partial failure: shards already committed keep their S3 key; retry only
    processes rows still missing parquet_points_file (see SQL comments below).
    """
    if not EPHEMERIS_POINTS_S3_BUCKET or EPHEMERIS_POINTS_S3_BUCKET == "bucket-name":
        logging.error(
            "EPHEMERIS_POINTS_S3_BUCKET is not configured; skipping ephemeris archive"
        )
        return

    to_archive = _select_ephemeris_ids_for_archive(cursor)
    if not to_archive:
        logging.info("No ephemerides to archive for selected batch")
        return

    run_id = _archive_batch_run_id(cursor)
    s3_prefix = f"{EPHEMERIS_POINTS_S3_PREFIX}/{run_id}"
    logging.info(
        "Archiving run_id=%s: %d ephemerides → s3://%s/%s/ (shard target %.0f MiB)",
        run_id,
        len(to_archive),
        EPHEMERIS_POINTS_S3_BUCKET,
        s3_prefix,
        target_shard_bytes / (1024 * 1024),
    )

    total_rows = 0
    t0 = time.perf_counter()

    # Temp dir: only holds the current shard on disk; removed when context exits.
    with tempfile.TemporaryDirectory(prefix="starlink-ephemeris-archive-") as tmp:
        work_dir = Path(tmp)
        archiver = _RunParquetArchiver(
            cursor=cursor,
            connection=connection,
            work_dir=work_dir,
            s3_prefix=s3_prefix,
            target_bytes=target_shard_bytes,
            write_batch_size=write_batch_size,
        )

        for idx, ephemeris_id in enumerate(to_archive, start=1):
            try:
                rows = _fetch_points_for_ephemeris(cursor, ephemeris_id)
            except psycopg2.Error as exc:
                raise RuntimeError(
                    f"Error reading ephemeris_id={ephemeris_id} "
                    f"({idx}/{len(to_archive)})"
                ) from exc

            # Leaves parquet_points_file NULL; will be retried unless handled elsewhere.
            if not rows:
                logging.warning("ephemeris_id=%s has no points; skipping", ephemeris_id)
                continue

            total_rows += archiver.append_ephemeris(ephemeris_id, rows)

            if idx % 500 == 0:
                logging.info(
                    "Archive progress: %d/%d ephemerides, %d rows (%.1fs)",
                    idx,
                    len(to_archive),
                    total_rows,
                    time.perf_counter() - t0,
                )

        n_shards, published_rows = archiver.close()

    logging.info(
        "Archive complete: %d shards, %d ephemerides, %d rows, %.1fs → %s",
        n_shards,
        len(to_archive),
        published_rows,
        time.perf_counter() - t0,
        s3_prefix,
    )
