import logging
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
from connections import get_spacetrack_login
from psycopg2.extras import execute_values

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)
from api.domain.models.satellite import Satellite
from api.utils.interpolation_utils import (
    generate_and_propagate_sigma_points,
    interpolate_sigma_pointsKI,
)


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
            "https://www.space-track.org/basicspacedata/query/class/satcat_change/PREVIOUS_DECAY/null-val/CURRENT_DECAY/%3C%3Enull-val/orderby/CHANGE_MADE%20desc/format/json/change_made/%3Enow-1",
            timeout=60,
        )

        try:
            log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{log_time}\tUpdating decayed satellites...")
            update_decayed_satellites(decayed_satellites, cursor)
            connection.commit()
        except Exception as err:
            log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            connection.rollback()


def update_decayed_satellites(decayed_satellites, cursor):
    decayed_satellites = decayed_satellites.json()
    for sat in decayed_satellites:
        try:
            current_date_time = datetime.now(timezone.utc)

            decay_date = sat.get("CURRENT_DECAY", None)
            sat_name = sat.get("CURRENT_NAME", None)
            sat_number = int(sat.get("NORAD_CAT_ID", None))
            query = """
                UPDATE satellites SET DECAY_DATE = %s, DATE_MODIFIED = %s
                WHERE SAT_NAME = %s AND SAT_NUMBER = %s;
                """

            cursor.execute(query, (decay_date, current_date_time, sat_name, sat_number))
            logging.info(f"Query: {cursor.query}")
            # if cursor.rowcount == 0:
            #    logging.warning(
            #        f"Unable to update decay date for {sat_name} ({sat_number})"
            #    )  # noqa: E501
        except Exception as err:
            log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            logging.error(log_time + "\t" + "database ERROR:", err)
            raise


def get_starlink_satellites(cursor: psycopg2.extensions.cursor) -> list[tuple]:
    """
    Get all Starlink satellites from the database.

    Args:
        cursor: Database cursor

    Returns:
        List of satellite tuples
    """
    cursor.execute("SELECT * FROM satellites WHERE sat_name LIKE '%STARLINK%'")
    return cursor.fetchall()


def extract_launch_number(launch_id: Optional[str]) -> str:
    """
    Extract and clean the launch number.

    Args:
        launch_id: Raw launch ID string

    Returns:
        Cleaned launch number
    """
    if not launch_id:
        return ""

    # Remove any letter characters (leave numbers and punctuation)
    return re.sub(r"[a-zA-Z]", "", launch_id)


def fetch_wikipedia_page(url: str) -> BeautifulSoup:
    """
    Fetch and parse a Wikipedia page.

    Args:
        url: The URL of the Wikipedia page

    Returns:
        BeautifulSoup object with the parsed HTML

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    logging.info(f"Fetching data from {url}")

    # Add headers to mimic a real browser request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                logging.error(f"Failed to fetch {url} after 3 attempts: {e}")
                raise
            else:
                logging.warning(
                    f"Attempt {attempt + 1} failed for {url}, retrying: {e}"
                )
                time.sleep(1)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame column names, handling multi-level headers.

    Args:
        df: The DataFrame with columns to clean

    Returns:
        DataFrame with cleaned column names
    """
    cleaned_columns = []
    for col in df.columns:
        if isinstance(col, tuple):
            # Join multi-level column names
            col_str = "_".join([str(c).strip() for c in col if c])
        else:
            col_str = str(col)
        # Clean the resulting string
        cleaned_columns.append(col_str.strip().lower().replace(" ", "_"))

    df.columns = cleaned_columns
    return df


def clean_generation_name(generation: str) -> str:
    """
    Clean generation name by removing footnote references.

    Args:
        generation: Raw generation name

    Returns:
        Cleaned generation name
    """
    return re.sub(r"\[\d+\]", "", generation).strip()


def scrape_starlink_data(
    sat_number_and_launch: list[tuple[int, int, str, str]],
) -> dict:
    """
    Scrape Starlink generation data from Wikipedia and match with satellite information.

    Args:
        sat_number_and_launch: List of tuples containing satellite information:
            - sat_id: Satellite database ID
            - sat_number: NORAD catalog number
            - sat_name: Satellite name
            - launch_number: Launch identifier

    Returns:
        Dictionary with satellite data matched to Starlink generations
    """
    url = "https://en.wikipedia.org/wiki/List_of_Starlink_and_Starshield_launches"

    try:
        soup = fetch_wikipedia_page(url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch Wikipedia data: {e}")
        logging.info(
            "Skipping Starlink generation data due to Wikipedia access failure"
        )
        return {"error": "Wikipedia access failed"}

    # Find the table - usually "wikitable" class for Wikipedia tables
    table = soup.find("table", {"class": "wikitable"})
    if not table:
        logging.error("Failed to find wikitable on the page")
        return {"error": "Table not found"}

    # Use pandas to parse the table
    dfs = pd.read_html(str(table))
    df = dfs[0]  # Get the first table, other two are starship and starshield

    # Clean column names
    df = clean_column_names(df)

    # Extract generation info from table
    generation_sets = []
    for _, row in df.iterrows():
        try:
            generation = row.get("sat._ver._sat._ver.", "")

            # Clean up the generation string
            generation = clean_generation_name(generation)

            generation_info = {
                "launch_number": row.get("cospar_id_cospar_id", ""),
                "generation": generation,
            }
            generation_sets.append(generation_info)
        except (ValueError, AttributeError) as e:
            logging.warning(f"Error processing row {row}: {e}")

    # Keep a list of all generation names
    generation_names = list(
        {entry["generation"] for entry in generation_sets if entry["generation"]}
    )
    logging.info(f"Found {len(generation_names)} different Starlink generations")

    # Match satellites with their generations
    satellites = []
    total_matched = 0
    for entry in generation_sets:
        satellites_from_this_launch = []
        for sat in sat_number_and_launch:
            try:
                if sat[3] == entry["launch_number"]:
                    satellites_from_this_launch.append(sat)
            except (IndexError, TypeError) as e:
                logging.warning(f"Error matching satellite {sat}: {e}")

        # Create entry for each satellite
        generation = entry["generation"]
        for satellite in satellites_from_this_launch:
            satellite_entry = {
                "launch_number": entry["launch_number"],
                "generation": generation,
                "sat_id": satellite[0],
                "sat_number": satellite[1],
                "sat_name": satellite[2],
            }
            satellites.append(satellite_entry)

        total_matched += len(satellites_from_this_launch)

    logging.info(f"Matched {total_matched} satellites to their generations")

    # Create final structure
    data = {
        "metadata": {
            "last_updated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
            "source": url,
        },
        "satellites": satellites,
        "satellite_count": len(satellites),
        "generations": generation_names,
    }

    return data


def get_starlink_generations(cursor, connection):
    """
    Update Starlink satellite generations in the database by scraping Wikipedia data.

    Args:
        cursor: Database cursor
        connection: Database connection
    """
    current_starlink_satellites = get_starlink_satellites(cursor)

    # Prepare satellite data for matching
    sat_id_number_and_launch = []
    for satellite in current_starlink_satellites:
        launch_number = extract_launch_number(satellite[10])
        sat_id_number_and_launch.append(
            (satellite[0], satellite[1], satellite[2], launch_number)
        )

    # Use existing function to scrape and process data
    data = scrape_starlink_data(sat_id_number_and_launch)
    if "error" in data:
        logging.error(f"Failed to scrape Starlink data: {data['error']}")
        return

    # Update database with generation information
    total_matched = 0
    for satellite in data["satellites"]:
        cursor.execute(
            "UPDATE satellites SET generation = %s WHERE id = %s",
            (satellite["generation"], satellite["sat_id"]),
        )
        total_matched += 1

    connection.commit()
    logging.info(
        f"Updated generation information for {total_matched} Starlink satellites"
    )


def insert_ephemeris_data(
    parsed_data, cursor, connection
) -> Optional[tuple[InterpolableEphemeris, int]]:
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

        # Create Satellite object from database result
        satellite = Satellite(
            sat_number=satellite_result[1],
            sat_name=satellite_result[2],
            constellation=satellite_result[3],
            generation=satellite_result[4],
            rcs_size=satellite_result[5],
            launch_date=satellite_result[6],
            decay_date=satellite_result[7],
            object_id=satellite_result[8],
            object_type=satellite_result[9],
            has_current_sat_number=satellite_result[10],
        )
        # Create and return the InterpolableEphemeris object
        ephemeris = InterpolableEphemeris(
            satellite=satellite,
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
        # Split by spaces to handle multiple key-value pairs on one line
        parts = line.split()
        for part in parts:
            if ":" in part:
                key, value = part.split(":", 1)
                headers[key] = value.strip()

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
        cursor: Database cursor for executing queries
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
                        ephemeris, ephemeris_id = insert_ephemeris_data(
                            parsed_data, cursor, connection
                        )
                        # calculate splines and store in database
                        # ephemeris_data = parse_ephemeris_file(ephemeris_file)
                        sigma_points_dict = generate_and_propagate_sigma_points(
                            ephemeris
                        )
                        interpolated_splines = interpolate_sigma_pointsKI(  # noqa: F841
                            sigma_points_dict
                        )

                        insert_interpolated_splines(
                            ephemeris_id,
                            ephemeris.generated_at,
                            ephemeris.data_source,
                            ephemeris.frame,
                            ephemeris.ephemeris_start,
                            ephemeris.ephemeris_stop,
                            interpolated_splines,
                            cursor,
                            connection,
                        )
                        num_points = len(parsed_data["timestamps"]) if ephemeris else 0

                    except Exception as e:
                        logging.error(
                            "Error parsing/inserting ephemeris data for file %s: %s",
                            file_name,
                            e,
                        )
                        continue

                except Exception as e:
                    logging.error(f"Error processing file {file_name}: {e}")
                    continue

                total_data_points += num_points
                files_processed += 1

            logging.info(f"Total data points: {total_data_points}")
            logging.info(f"Files processed: {files_processed}")
    except Exception as err:
        logging.error(f"Error getting ephemeris data for Starlink satellites: {err}")
        raise
