import io
import logging
import zipfile
from datetime import datetime, timezone

import boto3
import psycopg2

logger = logging.getLogger(__name__)


def get_s3_client(region: str = "us-west-2") -> boto3.client:
    """Create and return an S3 client.

    Args:
        region: AWS region name

    Returns:
        Boto3 S3 client
    """
    session = boto3.session.Session()
    return session.client(service_name="s3", region_name=region)


def list_zip_files_in_bucket(s3_client: boto3.client, bucket_name: str) -> list[str]:
    """List all zip files in the S3 bucket.

    Args:
        s3_client: Boto3 S3 client
        bucket_name: Name of the S3 bucket

    Returns:
        List of zip file keys
    """
    try:
        response = s3_client.list_objects(Bucket=bucket_name)
        if "Contents" not in response:
            logger.warning(f"No objects found in bucket {bucket_name}")
            return []

        zip_files = [
            obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".zip")
        ]
        logger.info(f"Found {len(zip_files)} zip file(s) in bucket")
        return zip_files
    except Exception as e:
        logger.error(f"Error listing objects in bucket: {e}")
        return []


def extract_field_value(lines: list[str], field_name: str) -> str | None:
    """Extract a field value from TDM file lines.

    Args:
        lines: List of file lines
        field_name: Name of the field to extract (e.g., "CREATION_DATE")

    Returns:
        Field value if found, None otherwise
    """
    for line in lines:
        if field_name in line and "=" in line:
            return line.split("=", 1)[1].strip()
    return None


def parse_data_points_from_range(
    lines: list[str], start_idx: int, end_idx: int | None
) -> list[tuple[str, float, float, float | None]]:
    """Parse data points from a specific range of TDM file lines.

    Args:
        lines: List of file lines
        start_idx: Starting index (after DATA_START)
        end_idx: Ending index (before DATA_STOP), or None for end of file

    Returns:
        List of tuples: (timestamp, ra, dec, mag)
        Points are sorted by timestamp
    """
    if end_idx is None:
        end_idx = len(lines)

    # Group data by timestamp
    # Format: ANGLE_1 = timestamp ra, ANGLE_2 = timestamp dec, MAG = timestamp mag
    points_by_timestamp: dict[str, dict[str, float | None]] = {}

    for line in lines[start_idx:end_idx]:
        if "DATA_STOP" in line or "DATA_END" in line:
            break
        if "=" not in line:
            continue

        try:
            key, value = line.split("=", 1)
            key = key.strip()
            values = value.strip().split()
            if len(values) < 2:
                continue

            timestamp = values[0]
            numeric_value = float(values[1])

            # Initialize timestamp entry if needed
            if timestamp not in points_by_timestamp:
                points_by_timestamp[timestamp] = {"ra": None, "dec": None, "mag": None}

            # Store values by type
            if key == "ANGLE_1":
                points_by_timestamp[timestamp]["ra"] = numeric_value
            elif key == "ANGLE_2":
                points_by_timestamp[timestamp]["dec"] = numeric_value
            elif key == "MAG":
                points_by_timestamp[timestamp]["mag"] = numeric_value

        except (ValueError, IndexError) as e:
            logger.warning(f"Error parsing data line '{line}': {e}")
            continue

    # Convert to list of tuples, filtering incomplete points (need at least ra and dec)
    data_points = [
        (ts, data["ra"], data["dec"], data["mag"])
        for ts, data in sorted(points_by_timestamp.items())
        if data["ra"] is not None and data["dec"] is not None
    ]

    return data_points


def parse_tdm_file(file_content: bytes) -> list[dict]:
    """Parse a TDM file and return a list of data blocks.

    TDM files can contain multiple META_START/DATA_START/DATA_STOP blocks,
    each with its own metadata and data points.

    Args:
        file_content: The content of the TDM file as bytes

    Returns:
        List of dictionaries, each containing parsed TDM block data with keys:
        - creation_date: Creation date string (optional, from file header)
        - site_name: Site name (PARTICIPANT_1)
        - norad_id: NORAD ID (PARTICIPANT_2)
        - reference_frame: Reference frame
        - data_points: List of (timestamp, ra, dec, mag) tuples
        - first_timestamp: First timestamp in this block
        - last_timestamp: Last timestamp in this block

    Raises:
        ValueError: If required fields are missing
    """
    text_content = file_content.decode("utf-8")
    lines = text_content.splitlines()

    # Extract file-level metadata (appears once at the top)
    creation_date = extract_field_value(lines, "CREATION_DATE")

    # Find all META_START blocks
    blocks = []
    i = 0
    while i < len(lines):
        if "META_START" in lines[i]:
            # Extract metadata for this block
            meta_start_idx = i
            meta_end_idx = None
            data_start_idx = None
            data_end_idx = None

            # Find META_STOP
            for j in range(meta_start_idx + 1, len(lines)):
                if "META_STOP" in lines[j]:
                    meta_end_idx = j
                    break

            # Find DATA_START
            start_idx = meta_end_idx + 1 if meta_end_idx else meta_start_idx
            for j in range(start_idx, len(lines)):
                if "DATA_START" in lines[j]:
                    data_start_idx = j + 1
                    break

            # Find DATA_STOP
            if data_start_idx:
                for j in range(data_start_idx, len(lines)):
                    if "DATA_STOP" in lines[j] or "DATA_END" in lines[j]:
                        data_end_idx = j
                        break
                if data_end_idx is None:
                    data_end_idx = len(lines)

            # Extract metadata from this block
            if meta_end_idx and data_start_idx:
                block_lines = lines[meta_start_idx : meta_end_idx + 1]
                site_name = extract_field_value(block_lines, "PARTICIPANT_1")
                norad_id = extract_field_value(block_lines, "PARTICIPANT_2")
                reference_frame = extract_field_value(block_lines, "REFERENCE_FRAME")
                track_id = extract_field_value(block_lines, "TRACK_ID")

                # Validate required fields
                if not site_name or not norad_id or not reference_frame:
                    logger.warning(
                        f"Block starting at line {meta_start_idx} missing required "
                        f"fields, skipping"
                    )
                    i = data_end_idx + 1 if data_end_idx else len(lines)
                    continue

                # Parse data points for this block
                data_points = parse_data_points_from_range(
                    lines, data_start_idx, data_end_idx
                )

                first_timestamp = data_points[0][0] if data_points else None
                last_timestamp = data_points[-1][0] if data_points else None

                blocks.append(
                    {
                        "creation_date": creation_date,
                        "site_name": site_name,
                        "norad_id": norad_id,
                        "reference_frame": reference_frame,
                        "data_points": data_points,
                        "first_timestamp": first_timestamp,
                        "last_timestamp": last_timestamp,
                        "track_id": track_id,
                    }
                )

                logger.info(
                    f"Parsed block - Site: {site_name}, NORAD ID: {norad_id}, "
                    f"Points: {len(data_points)}, "
                    f"Time range: {first_timestamp} to {last_timestamp}"
                )

                i = data_end_idx + 1 if data_end_idx else len(lines)
            else:
                i += 1
        else:
            i += 1

    if not blocks:
        raise ValueError("No valid data blocks found in TDM file")

    logger.info(f"Parsed {len(blocks)} data block(s) from TDM file")
    return blocks


def process_zip_file(
    s3_client: boto3.client,
    bucket_name: str,
    zip_key: str,
    cursor: psycopg2.extensions.cursor,
    connection: psycopg2.extensions.connection,
) -> None:
    """Process a single zip file from S3.

    Args:
        s3_client: Boto3 S3 client
        bucket_name: Name of the S3 bucket
        zip_key: Key of the zip file in S3
        cursor: Database cursor for checking/inserting data
        connection: Database connection for transaction management
    """
    folder_name = zip_key.replace(".zip", "")

    # Check if already processed
    cursor.execute(
        "SELECT 1 FROM tdm_predictions WHERE folder_name = %s LIMIT 1", (folder_name,)
    )
    already_processed = bool(cursor.fetchone())

    if already_processed:
        logger.info(f"Skipping {zip_key} - already processed")
        return

    logger.info(f"Processing {zip_key}")

    try:
        # Download zip file from S3
        zip_obj = s3_client.get_object(Bucket=bucket_name, Key=zip_key)
        zip_content = zip_obj["Body"].read()

        # Process each file in the zip
        with zipfile.ZipFile(io.BytesIO(zip_content), "r") as zip_ref:
            for file_name in zip_ref.namelist():
                logger.info(f"  Processing file: {file_name}")
                file_content = zip_ref.read(file_name)

                try:
                    parsed_blocks = parse_tdm_file(file_content)
                    # parsed_blocks is a list of blocks of position data,
                    # each with its own metadata, since a file can contain multiple
                    # blocks like these

                    for _block_idx, block_data in enumerate(parsed_blocks):
                        cursor.execute(
                            "INSERT INTO tdm_predictions (creation_date, site_name, "
                            "norad_id, reference_frame, time_range_start, "
                            "time_range_end, track_id, folder_name, date_added) VALUES "
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                            (
                                block_data["creation_date"],
                                block_data["site_name"],
                                block_data["norad_id"],
                                block_data["reference_frame"],
                                block_data["first_timestamp"],
                                block_data["last_timestamp"],
                                block_data["track_id"],
                                folder_name,
                                datetime.now(timezone.utc),
                            ),
                        )
                        result = cursor.fetchone()
                        if result is None:
                            raise ValueError("Failed to get inserted row ID")
                        row_id = result[0]
                        logger.debug(f"    Inserted TDM prediction with ID: {row_id}")
                        for point in block_data["data_points"]:
                            cursor.execute(
                                "INSERT INTO tdm_prediction_points (tdm_prediction_id, "
                                "timestamp, right_ascension, declination, "
                                "apparent_magnitude) VALUES "
                                "(%s, %s, %s, %s, %s)",
                                (row_id, point[0], point[1], point[2], point[3]),
                            )

                except ValueError as e:
                    # If there is a failure for one file, rollback at the folder
                    # level so as not to let the check for already processed folders
                    # pass when it shouldn't
                    logger.warning(f"    Failed to parse {file_name}: {e}")
                    connection.rollback()
                    raise

        connection.commit()

    except Exception as e:
        logger.error(f"Error processing {zip_key}: {e}", exc_info=True)
        connection.rollback()
        raise


def get_tdm_data(
    cursor: psycopg2.extensions.cursor,
    connection: psycopg2.extensions.connection,
) -> None:
    """Process all TDM zip files from S3 bucket and insert into database.

    Args:
        cursor: Database cursor for executing queries
        connection: Database connection for transaction management
    """
    try:
        # Setup S3 client
        s3_client = get_s3_client()
        bucket_name = "bucket-name"

        # Get list of zip files
        zip_files = list_zip_files_in_bucket(s3_client, bucket_name)
        if not zip_files:
            logger.info("No files to process")
            return

        # Process each zip file
        for zip_key in zip_files:
            process_zip_file(s3_client, bucket_name, zip_key, cursor, connection)

    except Exception as err:
        log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        logger.error(f"{log_time}\tdatabase ERROR: {err}")
        connection.rollback()
