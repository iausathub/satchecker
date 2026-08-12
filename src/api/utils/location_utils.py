import os
from pathlib import Path

from astropy.coordinates import EarthLocation

# Bundled in the API/Celery images; optional for local development.
_DEFAULT_SITES_JSON = "/app/astropy-data/sites.json"
_loaded_bundled_sites = False


def _ensure_site_registry() -> None:
    """Load observatory sites from a local file when available.

    Astropy falls back to a Greenwich-only builtin list if the remote
    sites.json download fails. Prefer the image-bundled copy so lookups
    work without runtime network access in case of network issues.
    """
    global _loaded_bundled_sites
    if _loaded_bundled_sites:
        return

    sites_path = Path(os.environ.get("ASTROPY_SITES_JSON", _DEFAULT_SITES_JSON))
    if sites_path.is_file():
        EarthLocation._get_site_registry(force_download=str(sites_path))
        _loaded_bundled_sites = True


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
        _ensure_site_registry()
        return EarthLocation.of_site(site_name)
    except Exception as e:
        raise ValueError(f"Error getting location for site {site_name}: {e}") from e
