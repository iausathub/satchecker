"""Compare observed satellite positions to live SatChecker predictions.

Reads a CSV of observations, queries production SatChecker for each row's
predicted RA/Dec (and sky rates), then reports total / on-track / cross-track
residuals. Large separations are flagged as likely misidentifications; for
those, FOV neighbors and an optional time-offset sweep help diagnose wrong
NORAD vs observer clock error.

Always re-queries the live API rather than using any precomputed prediction
columns (e.g. ``satchecker_ra_deg`` / ``satchecker_dec_deg`` in
``STARLINK_2yr_public_with_satchecker_data.csv``), so results reflect current
catalog/serving behavior and require network access.

Required CSV columns:
  - observation_time_utc
  - norad_cat_id
  - satellite_right_ascension_deg
  - satellite_declination_deg
  - observer_latitude_deg
  - observer_longitude_deg
  - observer_altitude_m

These column names are the same as ones from the SCORE data format.

Example usage::

  python compare_observations_to_predictions.py \\
      STARLINK_2yr_public.csv \\
      --output-file STARLINK_2yr_public_comparison.csv \\
      --fov-candidate-radius-deg 3.0
"""

import argparse
import math
import sys
from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
import requests
from astropy.coordinates import SkyCoord
from astropy.time import Time

SATCHECKER_CATALOG_URL = "https://satchecker.cps.iau.org/ephemeris/catalog-number/"
SATCHECKER_FOV_URL = "https://satchecker.cps.iau.org/fov/satellite-passes/"

REQUIRED_COLUMNS = (
    "observation_time_utc",
    "norad_cat_id",
    "satellite_right_ascension_deg",
    "satellite_declination_deg",
    "observer_latitude_deg",
    "observer_longitude_deg",
    "observer_altitude_m",
)

# Below this, the closest FOV candidate is treated as a confident spatial
# match and the time-offset sweep (observer clock check) is skipped.
FOV_CONFIDENT_MATCH_ARCSEC = 600.0  # 10 arcmin

# Sky-rate magnitude below which on/cross-track is undefined (deg/s).
_MIN_SKY_RATE_DEG_PER_SEC = 1e-12


def _julian_date_from_timestamp(timestamp: str) -> float:
    """Julian date for a UTC timestamp string, tolerant of the formats seen
    across input files: ISO8601 with ``T`` or a space as date/time separator,
    and an optional trailing ``Z`` or ``UTC`` marker."""
    normalized = timestamp.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1]
    elif normalized.upper().endswith("UTC"):
        normalized = normalized[: -len("UTC")].strip()

    return float(Time(normalized, scale="utc").jd)


def predict_position_at_jd(
    julian_date: float, norad_cat_id: int, lat: float, lon: float, alt: float
) -> dict | None:
    """Query SatChecker for the predicted position/rate at ``julian_date``.

    Returns the row's fields as a dict (keyed by the API's own ``fields``
    list, e.g. ``right_ascension_deg``, ``dra_cosdec_deg_per_sec``), or
    ``None`` if the request fails or no position is found.
    """
    try:
        result = requests.get(
            SATCHECKER_CATALOG_URL,
            params={
                "catalog": norad_cat_id,
                "elevation": alt,
                "latitude": lat,
                "longitude": lon,
                "julian_date": julian_date,
                "min_altitude": -90,
                "max_altitude": 90,
            },
            timeout=120,
        )
        result.raise_for_status()
        result_json = result.json()

        rows = result_json.get("data") or []
        if not rows:
            print(
                f"No SatChecker position for NORAD {norad_cat_id} "
                f"at JD {julian_date}"
            )
            return None

        return dict(zip(result_json["fields"], rows[0], strict=True))

    except Exception as e:
        print(
            f"Error calling SatChecker for NORAD {norad_cat_id} "
            f"at JD {julian_date}: {e}"
        )
        return None


def predict_position(
    timestamp: str, norad_cat_id: int, lat: float, lon: float, alt: float
) -> dict | None:
    """Query SatChecker for the predicted position/rate at ``timestamp``."""
    julian_date = _julian_date_from_timestamp(timestamp)
    return predict_position_at_jd(julian_date, norad_cat_id, lat, lon, alt)


def find_time_offset_candidates(
    norad_cat_id: int,
    timestamp: str,
    lat: float,
    lon: float,
    alt: float,
    observed_ra_deg: float,
    observed_dec_deg: float,
    window_seconds: float = 180.0,
    step_seconds: float = 10.0,
) -> list[dict]:
    """Sweep time around ``timestamp`` for the *reported* satellite.

    Complements ``find_fov_candidates`` (which searches nearby objects at a
    fixed, possibly-wrong time): this instead asks whether the *reported*
    NORAD ID actually explains the observation at some nearby time, e.g. from
    an observer clock offset. Returns rows sorted by separation from the
    observed position (closest first); empty on failure.

    Cost: one catalog API call per offset sample
    (``2 * window_seconds / step_seconds + 1`` requests).
    """
    julian_date = _julian_date_from_timestamp(timestamp)
    observed = SkyCoord(ra=observed_ra_deg * u.deg, dec=observed_dec_deg * u.deg)

    offsets_seconds = np.arange(-window_seconds, window_seconds + 1e-9, step_seconds)
    candidates = []
    for offset_seconds in offsets_seconds:
        jd = julian_date + float(offset_seconds) / 86400.0
        prediction = predict_position_at_jd(jd, norad_cat_id, lat, lon, alt)
        if prediction is None:
            continue
        predicted = SkyCoord(
            ra=prediction["right_ascension_deg"] * u.deg,
            dec=prediction["declination_deg"] * u.deg,
        )
        candidates.append(
            {
                "offset_seconds": float(offset_seconds),
                "time_sep_arcsec": observed.separation(predicted).arcsec,
                "predicted_ra_deg": prediction["right_ascension_deg"],
                "predicted_dec_deg": prediction["declination_deg"],
                "data_source": prediction["data_source"],
                "tle_epoch": prediction["tle_epoch"],
            }
        )

    candidates.sort(key=lambda c: c["time_sep_arcsec"])
    return candidates


def find_fov_candidates(
    timestamp: str,
    lat: float,
    lon: float,
    alt: float,
    observed_ra_deg: float,
    observed_dec_deg: float,
    fov_radius_deg: float = 5.0,
) -> list[dict]:
    """Look up what else was in the sky near an observation.

    For a likely-misidentified observation (predicted position for the
    reported NORAD ID is way off), query the FOV endpoint centered on the
    *observed* RA/Dec at that time/site to list nearby catalog objects --
    candidates for what was actually seen. Returns rows sorted by angular
    separation from the observed position (closest first); empty list on
    failure or no candidates.
    """
    julian_date = _julian_date_from_timestamp(timestamp)

    try:
        result = requests.get(
            SATCHECKER_FOV_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "elevation": alt,
                "duration": 1,
                "ra": observed_ra_deg,
                "dec": observed_dec_deg,
                "fov_radius": fov_radius_deg,
                "mid_obs_time_jd": julian_date,
                "group_by": "satellite",
                "async": "false",
            },
            timeout=120,
        )
        result.raise_for_status()
        satellites = result.json().get("data", {}).get("satellites", {})
    except Exception as e:
        print(f"Error calling SatChecker FOV at {timestamp}: {e}")
        return []

    observed = SkyCoord(ra=observed_ra_deg * u.deg, dec=observed_dec_deg * u.deg)
    candidates = []
    for sat in satellites.values():
        if not sat["positions"]:
            continue
        pos = sat["positions"][0]
        candidate = SkyCoord(ra=pos["ra"] * u.deg, dec=pos["dec"] * u.deg)
        candidates.append(
            {
                "candidate_name": sat["name"],
                "candidate_norad_id": sat["norad_id"],
                "candidate_sep_arcsec": observed.separation(candidate).arcsec,
                "candidate_range_km": pos["range_km"],
                "candidate_orbital_data_source": pos["orbital_data_source"],
                "candidate_orbital_data_epoch": pos["orbital_data_epoch"],
            }
        )

    candidates.sort(key=lambda c: c["candidate_sep_arcsec"])
    return candidates


def separation_on_track_cross_track_arcsec(
    predicted_ra_deg: float,
    predicted_dec_deg: float,
    observed_ra_deg: float,
    observed_dec_deg: float,
    dra_cosdec_deg_per_sec: float,
    ddec_deg_per_sec: float,
) -> tuple[float, float, float]:
    """Decompose the predicted->observed residual into along-track/cross-track.

    The track direction is the predicted velocity direction on the sky
    (``dra_cosdec``, ``ddec``, both already returned by SatChecker -- no
    second API call needed to sample a nearby time). On-track error is the
    residual component parallel to that direction (positive = observation is
    ahead of the prediction along its direction of motion); cross-track is
    the component perpendicular to it (positive = observation is rotated
    counterclockwise from the track direction, i.e. towards increasing
    position angle).

    When the predicted sky rate is essentially zero, on-track and cross-track
    are undefined and returned as NaN (total separation is still computed).

    Returns:
        (separation_arcsec, on_track_arcsec, cross_track_arcsec)
    """
    predicted = SkyCoord(ra=predicted_ra_deg * u.deg, dec=predicted_dec_deg * u.deg)
    observed = SkyCoord(ra=observed_ra_deg * u.deg, dec=observed_dec_deg * u.deg)

    separation_arcsec = float(predicted.separation(observed).arcsec)

    rate_mag = math.hypot(dra_cosdec_deg_per_sec, ddec_deg_per_sec)
    if rate_mag < _MIN_SKY_RATE_DEG_PER_SEC:
        return separation_arcsec, float("nan"), float("nan")

    residual_position_angle = predicted.position_angle(observed)

    # Position angle of the track direction: 0 deg = North, increasing
    # through East -- same convention as SkyCoord.position_angle.
    track_position_angle = np.arctan2(dra_cosdec_deg_per_sec, ddec_deg_per_sec) * u.rad

    angle_from_track = (residual_position_angle - track_position_angle).wrap_at(
        180 * u.deg
    )
    on_track_arcsec = separation_arcsec * np.cos(angle_from_track)
    cross_track_arcsec = separation_arcsec * np.sin(angle_from_track)

    return separation_arcsec, float(on_track_arcsec), float(cross_track_arcsec)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Compare observations to current SatChecker predictions")
    )
    parser.add_argument("input_file", type=str, help="The input file to compare")
    parser.add_argument(
        "--output-file",
        type=str,
        help="The output file to write the results to",
    )
    parser.add_argument(
        "--misidentification-threshold-deg",
        type=float,
        default=1.0,
        help=(
            "Separations above this are flagged as likely misidentified "
            "satellites rather than genuine tracking error, and excluded "
            "from the clean summary stats (default: 1.0 deg)"
        ),
    )
    parser.add_argument(
        "--fov-candidate-radius-deg",
        type=float,
        default=5.0,
        help="FOV radius used to look up candidate satellites for flagged/"
        "likely-misidentified observations (default: 5.0 deg)",
    )
    parser.add_argument(
        "--time-sweep-window-seconds",
        type=float,
        default=180.0,
        help=(
            "For flagged observations with no confident FOV candidate "
            f'(closest candidate still beyond {FOV_CONFIDENT_MATCH_ARCSEC:g}"), '
            "sweep the *reported* satellite's own predicted position over "
            "+/- this many seconds around the reported timestamp, to check "
            "for an observer clock offset. Each such observation costs about "
            "2*window/step+1 catalog API calls (default: 180s)"
        ),
    )
    parser.add_argument(
        "--time-sweep-step-seconds",
        type=float,
        default=10.0,
        help="Step size for the time-offset sweep (default: 10s)",
    )
    args = parser.parse_args(argv)
    misidentification_threshold_arcsec = args.misidentification_threshold_deg * 3600.0

    print(f"Reading input file: {args.input_file}")
    input_data = pd.read_csv(args.input_file)
    print(f"Read {len(input_data)} rows")

    missing = [c for c in REQUIRED_COLUMNS if c not in input_data.columns]
    if missing:
        print(f"Input CSV missing required columns: {missing}")
        print(f"Required columns: {list(REQUIRED_COLUMNS)}")
        return 1

    observed_data = input_data[list(REQUIRED_COLUMNS)]

    results = []
    n_failed_predictions = 0
    total_rows = len(observed_data)
    progress_interval = max(1, total_rows // 20)  # ~20 status lines regardless of size

    # call SatChecker for each row in the observed_data dataframe
    for i, (_, row) in enumerate(observed_data.iterrows(), start=1):
        if i % progress_interval == 0 or i == total_rows:
            print(f"[{i}/{total_rows}] {100 * i / total_rows:.0f}%")

        timestamp = row["observation_time_utc"]
        norad_cat_id = row["norad_cat_id"]
        observed_ra = row["satellite_right_ascension_deg"]
        observed_dec = row["satellite_declination_deg"]
        lat = row["observer_latitude_deg"]
        lon = row["observer_longitude_deg"]
        alt = row["observer_altitude_m"]

        prediction = predict_position(
            timestamp=timestamp,
            norad_cat_id=norad_cat_id,
            lat=lat,
            lon=lon,
            alt=alt,
        )
        if prediction is None:
            n_failed_predictions += 1
            continue

        predicted_ra = prediction["right_ascension_deg"]
        predicted_dec = prediction["declination_deg"]

        separation_arcsec, on_track_arcsec, cross_track_arcsec = (
            separation_on_track_cross_track_arcsec(
                predicted_ra_deg=predicted_ra,
                predicted_dec_deg=predicted_dec,
                observed_ra_deg=observed_ra,
                observed_dec_deg=observed_dec,
                dra_cosdec_deg_per_sec=prediction["dra_cosdec_deg_per_sec"],
                ddec_deg_per_sec=prediction["ddec_deg_per_sec"],
            )
        )

        results.append(
            {
                "observation_time_utc": timestamp,
                "norad_cat_id": norad_cat_id,
                "data_source": prediction["data_source"],
                "tle_epoch": prediction["tle_epoch"],
                "observer_latitude_deg": lat,
                "observer_longitude_deg": lon,
                "observer_altitude_m": alt,
                "observed_ra_deg": observed_ra,
                "observed_dec_deg": observed_dec,
                "predicted_ra_deg": predicted_ra,
                "predicted_dec_deg": predicted_dec,
                "separation_arcsec": separation_arcsec,
                "on_track_arcsec": on_track_arcsec,
                "cross_track_arcsec": cross_track_arcsec,
            }
        )

    if not results:
        print(
            f"No predictions were returned for any observation "
            f"({n_failed_predictions}/{total_rows} failed)."
        )
        return 1

    results_df = pd.DataFrame(results)

    # Separations this large essentially never come from genuine SGP4/TLE-fit
    # error against an epoch-matched TLE/OMM; they are usually the result of
    # the observation being attributed to the wrong satellite.
    # Flag and keep them out of the "real" accuracy stats rather than letting
    # them affect the averages.
    results_df["likely_misidentified"] = (
        results_df["separation_arcsec"] > misidentification_threshold_arcsec
    )

    if args.output_file:
        results_df.to_csv(args.output_file, index=False)
        print(f"Wrote {len(results_df)} rows -> {args.output_file}")

    n_flagged = int(results_df["likely_misidentified"].sum())
    clean_df = results_df.loc[~results_df["likely_misidentified"]]

    print(
        f"\nCompared {len(results_df)}/{total_rows} observations "
        f"({n_failed_predictions} without prediction)"
    )
    print(
        f"{n_flagged} flagged as likely misidentified "
        f"(separation > {args.misidentification_threshold_deg:g} deg)"
    )

    print(f"\nClean summary ({len(clean_df)} observations, misidentified excluded):")
    print(
        clean_df[["separation_arcsec", "on_track_arcsec", "cross_track_arcsec"]]
        .describe(percentiles=[0.5, 0.9])
        .to_string()
    )

    # A few catastrophic outliers (wrong satellite match, stale TLE/OMM epoch,
    # etc.) can drag the mean/std far from what the median suggests -- surface
    # the worst *clean* rows so genuine tracking-error outliers are visible
    # too, separately from the misidentified ones handled below.
    n_worst = min(10, len(clean_df))
    if n_worst:
        worst = clean_df.sort_values("separation_arcsec", ascending=False).head(n_worst)
        print(f"\nWorst {n_worst} clean observations by separation_arcsec:")
        print(
            worst[
                [
                    "observation_time_utc",
                    "norad_cat_id",
                    "data_source",
                    "tle_epoch",
                    "separation_arcsec",
                    "on_track_arcsec",
                    "cross_track_arcsec",
                ]
            ].to_string(index=False)
        )

    if n_flagged:
        print(f"\nLooking up FOV candidates for {n_flagged} flagged observation(s)...")
        candidate_rows = []
        time_sweep_rows = []
        flagged_df = results_df.loc[results_df["likely_misidentified"]]
        for _, row in flagged_df.iterrows():
            candidates = find_fov_candidates(
                timestamp=row["observation_time_utc"],
                lat=row["observer_latitude_deg"],
                lon=row["observer_longitude_deg"],
                alt=row["observer_altitude_m"],
                observed_ra_deg=row["observed_ra_deg"],
                observed_dec_deg=row["observed_dec_deg"],
                fov_radius_deg=args.fov_candidate_radius_deg,
            )

            print(
                f"\n  NORAD {row['norad_cat_id']} at {row['observation_time_utc']} "
                f"(reported separation {row['separation_arcsec']:.0f}\") "
                f"-- {len(candidates)} candidate(s) within "
                f"{args.fov_candidate_radius_deg:g} deg of observed position:"
            )
            for candidate in candidates[:5]:
                print(
                    f"    {candidate['candidate_sep_arcsec']:9.1f}\"  "
                    f"{candidate['candidate_name']:24s} "
                    f"{candidate['candidate_norad_id']!s:>8s}  "
                    f"range={candidate['candidate_range_km']:.1f}km  "
                    f"{candidate['candidate_orbital_data_source']}"
                )

            for candidate in candidates:
                candidate_rows.append(
                    {
                        "observation_time_utc": row["observation_time_utc"],
                        "reported_norad_cat_id": row["norad_cat_id"],
                        "reported_separation_arcsec": row["separation_arcsec"],
                        **candidate,
                    }
                )

            # No confident spatial match at the reported time -- check whether
            # the *reported* satellite fits better at a nearby time instead
            # (observer clock offset) before giving up on it.
            best_candidate_sep = (
                candidates[0]["candidate_sep_arcsec"] if candidates else None
            )
            if (
                best_candidate_sep is None
                or best_candidate_sep > FOV_CONFIDENT_MATCH_ARCSEC
            ):
                offsets = find_time_offset_candidates(
                    norad_cat_id=row["norad_cat_id"],
                    timestamp=row["observation_time_utc"],
                    lat=row["observer_latitude_deg"],
                    lon=row["observer_longitude_deg"],
                    alt=row["observer_altitude_m"],
                    observed_ra_deg=row["observed_ra_deg"],
                    observed_dec_deg=row["observed_dec_deg"],
                    window_seconds=args.time_sweep_window_seconds,
                    step_seconds=args.time_sweep_step_seconds,
                )
                if offsets:
                    best = offsets[0]
                    print(
                        f"    No confident FOV match -- best time offset for "
                        f"NORAD {row['norad_cat_id']} itself: "
                        f"{best['offset_seconds']:+.1f}s -> "
                        f"{best['time_sep_arcsec']:.1f}\" "
                        f"(vs {row['separation_arcsec']:.0f}\" at reported time)"
                    )
                for offset in offsets:
                    time_sweep_rows.append(
                        {
                            "observation_time_utc": row["observation_time_utc"],
                            "reported_norad_cat_id": row["norad_cat_id"],
                            "reported_separation_arcsec": row["separation_arcsec"],
                            **offset,
                        }
                    )

        if candidate_rows and args.output_file:
            candidates_path = Path(args.output_file).with_name(
                Path(args.output_file).stem + "_misidentification_candidates.csv"
            )
            pd.DataFrame(candidate_rows).to_csv(candidates_path, index=False)
            print(f"\nWrote misidentification candidates -> {candidates_path}")

        if time_sweep_rows and args.output_file:
            time_sweep_path = Path(args.output_file).with_name(
                Path(args.output_file).stem + "_misidentification_time_sweep.csv"
            )
            pd.DataFrame(time_sweep_rows).to_csv(time_sweep_path, index=False)
            print(f"Wrote time-offset sweep -> {time_sweep_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
