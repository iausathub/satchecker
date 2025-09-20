import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from typing import Optional

import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup


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


def scrape_starlink_data(sat_number_and_launch: list[tuple[int, int, str, str]]):
    """
    Scrape Starlink generation data from Wikipedia and match with satellite information.

    Args:
        sat_number_and_launch: List of tuples with
        (sat_id, sat_number, sat_name, launch_number)

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

    # Save to JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "starlink_generations.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    logging.info(f"Saved Starlink generation data to {file_path}")


def get_database_connection() -> (
    tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]
):
    """
    Get a connection to the database.

    Returns:
        Tuple of (connection, cursor)

    Raises:
        SystemExit: If connection fails
    """
    try:
        # In production, use environment variables for these credentials
        connection = psycopg2.connect(
            host="host",
            port="port",
            database="database",
            user="username",
            password="password",  # noqa: S106
        )
        cursor = connection.cursor()
        return connection, cursor
    except psycopg2.OperationalError as err:
        log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{log_time}\tDatabase ERROR: {err}")
        sys.exit(1)


def get_starlink_satellites(cursor: psycopg2.extensions.cursor) -> list[tuple]:
    """
    Get all Starlink satellites from the database.

    Args:
        cursor: Database cursor

    Returns:
        List of satellite tuples
    """
    cursor.execute(
        """
        SELECT s.*, d.sat_name
        FROM satellites s
        JOIN (
            SELECT DISTINCT ON (sat_id) sat_id, sat_name
            FROM satellite_designation
            WHERE sat_name ILIKE '%STARLINK%'
            ORDER BY sat_id, sat_name
        ) d ON s.id = d.sat_id
    """
    )
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


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Get database connection
    connection, cursor = get_database_connection()

    try:
        # Get all Starlink satellites
        satellites = get_starlink_satellites(cursor)
        logging.info(f"Found {len(satellites)} Starlink satellites in database")

        # Prepare satellite data for matching
        sat_id_number_and_launch = []
        for satellite in satellites:
            launch_number = extract_launch_number(satellite[10])
            sat_id_number_and_launch.append(
                (satellite[0], satellite[1], satellite[2], launch_number)
            )

        # Scrape and match generation data
        scrape_starlink_data(sat_id_number_and_launch)

        # Parse the generation data from the json file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "starlink_generations.json")

        with open(file_path) as f:
            data = json.load(f)
            for satellite in data["satellites"]:
                # update the generation field for the satellite
                cursor.execute(
                    "UPDATE satellites SET generation = %s WHERE id = %s",
                    (satellite["generation"], satellite["sat_id"]),
                )

        logging.info("Starlink generation data processing completed successfully")
    except Exception as e:
        logging.error(f"Error in main process: {e}")
        raise
    finally:
        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Database connection closed")


if __name__ == "__main__":
    main()
