"""Validate SatChecker's generated satellite positions against real
observed positions, and optionally against an independent Space-Track
propagation (addresses
https://github.com/iausathub/satchecker/issues/230).

Takes a small file of real observations -- each one a satellite actually
seen in the sky at one or more (time, RA, Dec) points -- and reports, for
every point:

  * how far SatChecker's own /ephemeris/name-jdstep/ prediction for that
    satellite was from the measured position at the same time, and
  * (with --use-spacetrack) how far an independent SGP4 propagation of
    that satellite's current Space-Track TLE was from the measured
    position.

A large divergence against SatChecker but not Space-Track points at a bug
in SatChecker's own generated ephemeris; a large divergence against both
instead suggests the TLE itself (or the input observation) is the problem.

Usage:
    python examples/validate_fov_predictions.py examples/sample_fov_observations.json
    python examples/validate_fov_predictions.py my_observations.json --use-spacetrack

`--use-spacetrack` needs SPACETRACK_USERNAME and SPACETRACK_PASSWORD in the
environment; see https://www.space-track.org/documentation#/api for how to
register (free). It fetches the *current* TLE for each satellite (Space-
Track's `gp` class only keeps the latest one per object), so the Space-
Track comparison is only meaningful when the observation is from close to
now -- for an older observation, SGP4 propagation error from an outdated
TLE will dominate and swamp any real signal.

Input file format -- a JSON list of observations:
    [
      {
        "label": "my streak #1",
        "satellite_name": "ISS (ZARYA)",
        "norad_id": 25544,
        "latitude_deg": 32, "longitude_deg": -110, "elevation_m": 0,
        "points": [
          {"julian_date": 2461000.50, "ra_deg": 208.418, "dec_deg": -17.104},
          {"julian_date": 2461000.51, "ra_deg": 115.182, "dec_deg": 59.356}
        ]
      }
    ]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import astropy.units as u
import requests
from astropy.coordinates import SkyCoord

DEFAULT_BASE_URL = "https://satchecker.cps.iau.org"
SPACETRACK_LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
SPACETRACK_TLE_URL = (
    "https://www.space-track.org/basicspacedata/query/class/gp/"
    "NORAD_CAT_ID/{norad_id}/orderby/EPOCH%20desc/limit/1/format/json"
)


@dataclass
class ObservedPoint:
    julian_date: float
    ra_deg: float
    dec_deg: float


@dataclass
class Observation:
    label: str
    satellite_name: str
    norad_id: int
    latitude_deg: float
    longitude_deg: float
    elevation_m: float
    points: list[ObservedPoint]


def load_observations(path: Path) -> list[Observation]:
    """Parse the JSON observation file described in the module docstring."""
    raw = json.loads(path.read_text())
    observations = []
    for entry in raw:
        points = [ObservedPoint(**point) for point in entry["points"]]
        observations.append(
            Observation(
                label=entry.get("label", entry["satellite_name"]),
                satellite_name=entry["satellite_name"],
                norad_id=entry["norad_id"],
                latitude_deg=entry["latitude_deg"],
                longitude_deg=entry["longitude_deg"],
                elevation_m=entry["elevation_m"],
                points=points,
            )
        )
    return observations


def separation_deg(
    ra1_deg: float, dec1_deg: float, ra2_deg: float, dec2_deg: float
) -> float:
    """Great-circle angular separation between two RA/Dec points, in degrees."""
    a = SkyCoord(ra1_deg, dec1_deg, unit="deg")
    b = SkyCoord(ra2_deg, dec2_deg, unit="deg")
    return float(a.separation(b).to(u.deg).value)


def fetch_satchecker_predictions(
    obs: Observation, base_url: str = DEFAULT_BASE_URL, timeout_s: float = 60.0
) -> dict[float, tuple[float, float]]:
    """SatChecker's own predicted (ra_deg, dec_deg) for `obs.satellite_name`
    at each of `obs.points`' Julian dates, via /ephemeris/name-jdstep/.

    Queries each requested Julian date individually (startjd == stopjd) --
    requesting one jdstep window spanning all of them would need a step
    size matching the *smallest* gap between points to land exactly on
    every one, which silently returns wrong, aliased samples for unevenly
    spaced points otherwise.

    Returns a dict keyed by julian_date (as SatChecker reports it back)
    rather than a plain list, so results line up with `obs.points` even if
    SatChecker doesn't echo back the exact float that was requested.
    """
    predicted = {}
    for point in obs.points:
        response = requests.get(
            f"{base_url}/ephemeris/name-jdstep/",
            params={
                "name": obs.satellite_name,
                "latitude": obs.latitude_deg,
                "longitude": obs.longitude_deg,
                "elevation": obs.elevation_m,
                "startjd": point.julian_date,
                "stopjd": point.julian_date,
                "stepjd": 1e-6,
                "min_altitude": -90,
            },
            timeout=timeout_s,
        )
        response.raise_for_status()
        body = response.json()
        fields = body["fields"]
        ra_idx = fields.index("right_ascension_deg")
        dec_idx = fields.index("declination_deg")
        jd_idx = fields.index("julian_date")
        row = body["data"][0]
        predicted[row[jd_idx]] = (row[ra_idx], row[dec_idx])
    return predicted


def fetch_spacetrack_tle(
    norad_id: int, username: str, password: str, timeout_s: float = 30.0
) -> tuple[str, str]:
    """The most recent TLE line pair for `norad_id` from Space-Track.org.

    Needs a free Space-Track account; see
    https://www.space-track.org/documentation#/api for registration.
    """
    session = requests.Session()
    login_response = session.post(
        SPACETRACK_LOGIN_URL,
        data={"identity": username, "password": password},
        timeout=timeout_s,
    )
    login_response.raise_for_status()
    if login_response.text.strip().startswith('{"Login":"Failed"}'):
        raise RuntimeError(
            "Space-Track login failed -- check SPACETRACK_USERNAME/SPACETRACK_PASSWORD"
        )

    query_response = session.get(
        SPACETRACK_TLE_URL.format(norad_id=norad_id), timeout=timeout_s
    )
    query_response.raise_for_status()
    records = query_response.json()
    if not records:
        raise ValueError(f"no Space-Track GP record found for NORAD {norad_id}")
    return records[0]["TLE_LINE1"], records[0]["TLE_LINE2"]


def propagate_spacetrack(
    tle_line1: str,
    tle_line2: str,
    latitude_deg: float,
    longitude_deg: float,
    elevation_m: float,
    julian_date: float,
) -> tuple[float, float]:
    """(ra_deg, dec_deg) for the satellite described by this TLE as seen
    from the given observer at `julian_date` (UTC) -- an SGP4 propagation
    done independently of SatChecker's own pipeline, as a cross-check."""
    from astropy.time import Time
    from skyfield.api import EarthSatellite, load, wgs84

    ts = load.timescale()
    satellite = EarthSatellite(tle_line1, tle_line2, "", ts)
    observer = wgs84.latlon(latitude_deg, longitude_deg, elevation_m)
    t = ts.from_astropy(Time(julian_date, format="jd", scale="utc"))
    ra, dec, _ = (satellite - observer).at(t).radec()
    return ra._degrees, dec.degrees


def validate_observation(
    obs: Observation,
    base_url: str = DEFAULT_BASE_URL,
    spacetrack_tle: tuple[str, str] | None = None,
) -> list[dict[str, float | str]]:
    """Per-point validation results for one observation: separation (deg)
    between the measured position and SatChecker's prediction, and -- if
    `spacetrack_tle` is given -- against an independent SGP4 propagation
    of that TLE too."""
    predicted = fetch_satchecker_predictions(obs, base_url=base_url)
    predicted_jds = sorted(predicted)

    results = []
    for point in obs.points:
        # SatChecker's step sampling may not land exactly on the requested
        # date -- use its closest returned sample instead of an exact match.
        closest_jd = min(predicted_jds, key=lambda jd: abs(jd - point.julian_date))
        pred_ra, pred_dec = predicted[closest_jd]
        row: dict[str, float | str] = {
            "label": obs.label,
            "julian_date": point.julian_date,
            "satchecker_sep_deg": separation_deg(
                point.ra_deg, point.dec_deg, pred_ra, pred_dec
            ),
        }
        if spacetrack_tle is not None:
            st_ra, st_dec = propagate_spacetrack(
                *spacetrack_tle,
                obs.latitude_deg,
                obs.longitude_deg,
                obs.elevation_m,
                point.julian_date,
            )
            row["spacetrack_sep_deg"] = separation_deg(
                point.ra_deg, point.dec_deg, st_ra, st_dec
            )
        results.append(row)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "observations", type=Path, help="path to a JSON observation file"
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--use-spacetrack",
        action="store_true",
        help="also cross-check against an independent Space-Track TLE propagation",
    )
    args = parser.parse_args()

    username = os.environ.get("SPACETRACK_USERNAME")
    password = os.environ.get("SPACETRACK_PASSWORD")
    if args.use_spacetrack and not (username and password):
        sys.exit("--use-spacetrack needs SPACETRACK_USERNAME/SPACETRACK_PASSWORD set")

    for obs in load_observations(args.observations):
        spacetrack_tle = (
            fetch_spacetrack_tle(obs.norad_id, username, password)
            if args.use_spacetrack
            else None
        )
        for row in validate_observation(
            obs, base_url=args.base_url, spacetrack_tle=spacetrack_tle
        ):
            print(row)


if __name__ == "__main__":
    main()
