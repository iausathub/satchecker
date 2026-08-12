# ruff: noqa: S101
import json

import pytest
from astropy.coordinates import EarthLocation

from api.utils import location_utils


@pytest.fixture
def bundled_sites(tmp_path, mocker):
    sites = {
        "fakesite": {
            "name": "Fake Observatory",
            "longitude": -70.0,
            "latitude": -24.0,
            "elevation": 1000.0,
            "longitude_unit": "degree",
            "latitude_unit": "degree",
            "elevation_unit": "meter",
            "source": "test",
            "aliases": [],
        }
    }
    path = tmp_path / "sites.json"
    path.write_text(json.dumps(sites))
    mocker.patch.dict("os.environ", {"ASTROPY_SITES_JSON": str(path)})
    mocker.patch.object(location_utils, "_loaded_bundled_sites", False)
    EarthLocation._site_registry = None
    yield path
    location_utils._loaded_bundled_sites = False
    EarthLocation._site_registry = None


def test_get_location_from_bundled_sites_json(bundled_sites):
    loc = location_utils.get_location_from_astropy_site("fakesite")
    assert loc.lat.deg == pytest.approx(-24.0)
    assert loc.lon.deg == pytest.approx(-70.0)
    assert loc.height.value == pytest.approx(1000.0)


def test_get_location_unknown_site_raises(bundled_sites):
    with pytest.raises(ValueError, match="Error getting location for site"):
        location_utils.get_location_from_astropy_site("not-a-real-site")
