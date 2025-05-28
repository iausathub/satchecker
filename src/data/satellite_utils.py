import datetime
import logging
import re
from typing import Optional

import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
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
            # if cursor.rowcount == 0:
            #    logging.warning(
            #        f"Unable to update decay date for {sat_name} ({sat_number})"
            #    )  # noqa: E501
        except Exception as err:
            log_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
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
    sat_number_and_launch: list[tuple[int, int, str, str]]
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
