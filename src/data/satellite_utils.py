import io
import logging
import re
import time
import zipfile
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
from connections import get_spacetrack_login
from psycopg2.extras import execute_values


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
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


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
    soup = fetch_wikipedia_page(url)

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


def insert_ephemeris_data(parsed_data, cursor, connection):
    """
    Insert ephemeris data into the database efficiently using batch inserts.

    Args:
        parsed_data (dict): Dictionary containing parsed ephemeris data
        cursor: Database cursor
        connection: Database connection
    """
    try:
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
                (SELECT id FROM satellites
                 WHERE sat_name = %s
                 AND has_current_sat_number = true),
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
                parsed_data["satellite_name"],
                datetime.now(timezone.utc),  # date_collected
                parsed_data["generated_at"],
                "spacetrack",
                parsed_data["filename"],
                parsed_data["ephemeris_start"],
                parsed_data["ephemeris_stop"],
                parsed_data["frame"],
            ),
        )
        ephemeris_id = cursor.fetchone()[0]

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

    # log parsed data
    logging.info(f"Parsed {len(timestamps)} timestamps")
    logging.info(f"Parsed {len(positions)} positions")
    logging.info(f"Parsed {len(velocities)} velocities")
    logging.info(f"Parsed {len(covariances)} covariances")
    logging.info(f"Ephemeris start: {ephemeris_start}")
    logging.info(f"Ephemeris stop: {ephemeris_stop}")
    logging.info(f"Generated at: {generated_at}")
    logging.info(f"Satellite name: {satellite_name}")
    logging.info(f"Filename: {filename}")

    return {
        "timestamps": np.array(timestamps),
        "positions": np.array(positions, dtype=np.float64),
        "velocities": np.array(velocities, dtype=np.float64),
        "covariances": np.array(covariances, dtype=np.float64),
        "frame": "UVW",
        "ephemeris_start": ephemeris_start,
        "ephemeris_stop": ephemeris_stop,
        "generated_at": generated_at,
        "satellite_name": satellite_name,
        "filename": filename,
    }


def get_ephemeris_data_from_spacetrack(cursor, connection):
    """
    Fetch and process ephemeris data from Space-Track for SpaceX satellites.

    This function:
    1. Authenticates with Space-Track API
    2. Retrieves metadata for public files
    3. Filters for SpaceX files from today
    4. Downloads and processes each file
    5. Parses ephemeris data and inserts it into the database

    The function processes files in the following format:
    - Each file is a zip archive containing multiple ephemeris files
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
        - Only processes files from the current UTC day
        - Includes rate limiting (2 second delay between files)
        - Logs processing statistics for each file
        - Uses ON CONFLICT DO NOTHING for database inserts to handle duplicates
    """
    try:
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

            # First get metadata about public files
            public_files_metadata = session.get(
                "https://www.space-track.org/publicfiles/query/class/loadpublicdata",
                timeout=60,
            )

            # Get files and filter for SpaceX
            files_metadata = public_files_metadata.json()
            spacex_files = [
                f for f in files_metadata if f["source"].lower() == "spacex"
            ]

            # Get today's date in UTC
            today = datetime.now(timezone.utc).date()

            logging.info(f"Today's date: {today}")

            # Filter files for today's date only
            today_files = [
                f
                for f in spacex_files
                if datetime.strptime(f["date"], "%Y-%m-%d %H:%M:%S").date() == today
            ]

            if not today_files:
                logging.info(f"No SpaceX files found for today ({today})")
                return

            # Sort files by date in descending order (newest first)
            today_files.sort(
                key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"),
                reverse=True,
            )

            logging.info(f"Found {len(today_files)} SpaceX files for today ({today})")

            # Process each file individually
            for file in today_files:
                try:
                    # Check if file has already been processed
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM interpolable_ephemeris
                        WHERE file_reference = %s
                        """,
                        (file["name"],),
                    )
                    if cursor.fetchone()[0] > 0:
                        logging.info(f"Skipping already processed file: {file['name']}")
                        continue

                    # Download the file
                    file_url = (
                        f"{base_uri}/publicfiles/query/class/download"
                        f"?name={file['link']}"
                    )
                    response = session.get(file_url, timeout=120)
                    response.raise_for_status()

                    logging.info(f"Processing file: {file['name']}")

                    # Process the zip file in memory
                    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                        file_list = zip_ref.namelist()
                        logging.info(f"Found {len(file_list)} files in the zip")

                        start_time = datetime.now(timezone.utc)
                        total_data_points = 0
                        files_processed = 0
                        for file_name in file_list:
                            try:
                                with zip_ref.open(file_name) as f:
                                    file_content = f.read().decode("utf-8")
                                parsed_data = parse_ephemeris_file(
                                    file_content, file_name
                                )
                                insert_ephemeris_data(parsed_data, cursor, connection)
                                num_points = len(parsed_data["timestamps"])
                                total_data_points += num_points
                                files_processed += 1
                            except Exception as e:
                                logging.error(f"Error processing file {file_name}: {e}")
                                continue

                        end_time = datetime.now(timezone.utc)
                        total_duration = (end_time - start_time).total_seconds()
                        logging.info(f"\nProcessing Summary for {file['name']}:")
                        logging.info(f"Total files processed: {files_processed}")
                        logging.info(f"Total data points: {total_data_points}")
                        logging.info(
                            f"Total processing time: " f"{total_duration:.2f} seconds"
                        )
                        logging.info(
                            f"Average time per file: "
                            f"{total_duration/len(file_list):.2f} seconds"
                        )

                        # Add a small delay between files to avoid rate limiting
                        time.sleep(2)

                except Exception as e:
                    logging.error(f"Error processing zip file {file['name']}: {e}")
                    continue
    except Exception as err:
        logging.error(f"Error getting ephemeris data from Space-Track: {err}")
        raise
