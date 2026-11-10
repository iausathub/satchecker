# ruff: noqa: S101
"""Tests for examples/validate_fov_predictions.py.

The script lives in examples/, which isn't on the test pythonpath (it's a
standalone contributor tool, not part of the installed package), so it's
loaded directly from its file path.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SCRIPT_PATH = Path(__file__).parents[2] / "examples" / "validate_fov_predictions.py"
_SPEC = importlib.util.spec_from_file_location("validate_fov_predictions", _SCRIPT_PATH)
assert _SPEC and _SPEC.loader
validate_fov_predictions = importlib.util.module_from_spec(_SPEC)
# register in sys.modules before exec: the module uses @dataclass, which on
# newer Pythons looks itself up there while the class body is executing
sys.modules[_SPEC.name] = validate_fov_predictions
_SPEC.loader.exec_module(validate_fov_predictions)


def test_separation_deg_is_zero_for_identical_points():
    assert validate_fov_predictions.separation_deg(
        10.0, -20.0, 10.0, -20.0
    ) == pytest.approx(0.0, abs=1e-9)


def test_separation_deg_matches_known_right_angle():
    # a point on the celestial equator and a point at the pole are 90 degrees apart
    sep = validate_fov_predictions.separation_deg(0.0, 0.0, 0.0, 90.0)
    assert sep == pytest.approx(90.0, abs=1e-9)


def test_load_observations_parses_points_and_defaults_label(tmp_path):
    path = tmp_path / "observations.json"
    path.write_text(
        json.dumps(
            [
                {
                    "satellite_name": "ISS (ZARYA)",
                    "norad_id": 25544,
                    "latitude_deg": 32,
                    "longitude_deg": -110,
                    "elevation_m": 0,
                    "points": [
                        {"julian_date": 2461000.5, "ra_deg": 208.4, "dec_deg": -17.1}
                    ],
                }
            ]
        )
    )

    observations = validate_fov_predictions.load_observations(path)

    assert len(observations) == 1
    obs = observations[0]
    assert (
        obs.label == "ISS (ZARYA)"
    )  # falls back to satellite_name when no label is given
    assert obs.norad_id == 25544
    assert len(obs.points) == 1
    assert obs.points[0].ra_deg == pytest.approx(208.4)


def test_fetch_satchecker_predictions_parses_field_order(mocker):
    # SatChecker returns rows as positional arrays alongside a "fields" list
    # naming each column -- this must look the column up by name, not by a
    # hardcoded index, so it still works if the API reorders them.
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "fields": ["julian_date", "declination_deg", "right_ascension_deg"],
        "data": [[2461000.5, -17.1, 208.4]],
    }
    mocker.patch("validate_fov_predictions.requests.get", return_value=fake_response)

    obs = validate_fov_predictions.Observation(
        label="test",
        satellite_name="ISS (ZARYA)",
        norad_id=25544,
        latitude_deg=32,
        longitude_deg=-110,
        elevation_m=0,
        points=[
            validate_fov_predictions.ObservedPoint(
                julian_date=2461000.5, ra_deg=208.4, dec_deg=-17.1
            )
        ],
    )

    predicted = validate_fov_predictions.fetch_satchecker_predictions(obs)

    assert predicted == {2461000.5: (208.4, -17.1)}


def test_validate_observation_reports_zero_separation_for_a_perfect_prediction(mocker):
    mocker.patch(
        "validate_fov_predictions.fetch_satchecker_predictions",
        return_value={2461000.5: (208.4, -17.1)},
    )

    obs = validate_fov_predictions.Observation(
        label="test",
        satellite_name="ISS (ZARYA)",
        norad_id=25544,
        latitude_deg=32,
        longitude_deg=-110,
        elevation_m=0,
        points=[
            validate_fov_predictions.ObservedPoint(
                julian_date=2461000.5, ra_deg=208.4, dec_deg=-17.1
            )
        ],
    )

    results = validate_fov_predictions.validate_observation(obs)

    assert len(results) == 1
    assert results[0]["satchecker_sep_deg"] == pytest.approx(0.0, abs=1e-6)
    assert "spacetrack_sep_deg" not in results[0]
