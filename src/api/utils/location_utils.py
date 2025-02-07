from astropy.coordinates import EarthLocation


def get_location_from_astropy_site(site_name: str) -> EarthLocation:
    """
    Get the location of a site from the astropy site name.

    See https://www.astropy.org/astropy-data/coordinates/sites.json
    for a list of valid sites.

    Args:
        site_name (str): The name of the site to get the location of.

    Returns:
        EarthLocation: The location of the site.
    """
    try:
        return EarthLocation.of_site(site_name)
    except Exception as e:
        raise ValueError(f"Error getting location for site {site_name}: {e}") from e
