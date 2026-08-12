# SatChecker Changelog

This document tracks all notable changes to SatChecker across versions. Entries are organized by release date and version number, with changes categorized as Features, Bugfixes, Changes, Deprecations, Documentation improvements, or Miscellaneous updates. SatChecker follows semantic versioning (MAJOR.MINOR.PATCH).

<!-- towncrier release notes start -->

# 1.7.0 (2026-08-12)

### Bugfixes

- Fix for FOV endpoing not returning results in chronological order for default group_by=time. ([#173](https://github.com/iausathub/satchecker/pull/173))
- Fix the angular distance from the FOV center reported for ephemeris-refined satellite positions. It was computed with a flat-sky `sqrt((ra1 - ra2)**2 + (dec1 - dec2)**2)`, which ignores cos(dec) foreshortening in right ascension and breaks across the RA 0/360 degree boundary. It now uses a haversine great-circle separation, so positions at high declination and near RA = 0 are placed in or out of the field of view correctly. ([#239](https://github.com/iausathub/satchecker/pull/239))
- Fix the `illuminated_only` filter in FOV searches. The illumination status was computed and used to decide whether a satellite had any visible point, but the returned points were then selected by field-of-view membership alone, so non-illuminated (eclipsed) positions were still included whenever the satellite had at least one illuminated point in the window. Illuminated and dark points are now selected consistently, so `illuminated_only=true` returns only illuminated positions. ([#241](https://github.com/iausathub/satchecker/pull/241))
- Return HTTP 400 instead of 500 when an invalid observatory `site` name is supplied, and resolve site names from a bundled sites.json so lookups work without runtime network access. ([#245](https://github.com/iausathub/satchecker/pull/245))
- Return HTTP 400 instead of a 500 database error when a non-integer NORAD ID is supplied to the tools or ephemeris endpoints (`id` with `id_type=catalog`, the names-from-norad-id endpoint, and the `norad_id` parameter). ([#245](https://github.com/iausathub/satchecker/pull/245))
- Fix data caching on container startup so the recent-data cache populates reliably, prevent the scheduler from starting multiple times, and pass the Flask app (not the `current_app` proxy) to the initial cache refresh.
- Return correct HTTP status codes from the ephemeris endpoints for TLE issues: 404 when no TLE is found and 422 when the requested date is outside the range of available TLE data, instead of 500.

### Features

- Use operator-provided ephemeris data to interpolate satellite positions when available. This is only available for Starlink satellites. Covariance info for uncertainties will be included in the response in the future. ([#173](https://github.com/iausathub/satchecker/pull/173))
- Use orbital elements in OMM format from both Celestrak and Space-Track since Celestrak won't be using the alpha-5 notation for NORAD IDs to support the orginal TLE format.

  TLEs for dates before 2026-07-12 will continue to be used as is with no changes to any of the related endpoints, but OMM will be used for everything going forward.

  References to `tle_data` in API responses will be replaced with `orbital_data`. The ability to see which orbital data was used will be added in the future for the OMM format. ([#225](https://github.com/iausathub/satchecker/pull/225))
- Add OMM (Orbital Mean-Element Message) data access. New tools endpoints (get-omm-data, get-nearest-omm, get-adjacent-omms, get-omms-around-epoch, and omms-at-epoch) mirror the existing TLE endpoints, and OMM data is now included in FOV results at parity with TLE (TLE is used for epochs before the orbital-elements cutoff, OMM after). The `object_id` field is included in the satellite data returned for both TLE and OMM results. ([#245](https://github.com/iausathub/satchecker/pull/245))

### Changes

- Add a 20% margin to the FOV radius when selecting satellites, so objects just outside the requested field of view are still returned to account for satellite position uncertainties. ([#173](https://github.com/iausathub/satchecker/pull/173))


# 1.6.0 (2026-01-29)

## Features

- Update FOV endpoint to calculate results asynchronously. The original FOV endpoint will return a task ID and status of the task. The task will be completed in the background and the results will be available via the new task status endpoint.

  Backwards compatibility will be maintained by returning the results immediately if the async parameter is set to false (also usable for FOV requests with shorter durations and smaller FOV radii since those are faster to calculate). ([#175](https://github.com/iausathub/satchecker/pull/175))
- Add endpoint to search satellites by metadata (NORAD ID, name, international designator, launch date, decay date, object type, rcs size, etc.). ([#178](https://github.com/iausathub/satchecker/pull/178))

## Changes

- Added API version to remaining tools endpoints and standardized output format. ([#178](https://github.com/iausathub/satchecker/pull/178))


# 1.5.0 (2025-08-28)

### Features

- Added `illuminated_only` parameter to FOV endpoints to filter satellites based on expected solar illumination status. ([#163](https://github.com/iausathub/satchecker/pull/163))
- Add `sat_altitude_km`, `solar_elevation_deg`, and `solar_azimuth_deg` to ephemeris API responses. ([#164](https://github.com/iausathub/satchecker/pull/164))

### Changes

- Updated validation errors to use the main error handler and improve error message text for ra, dec, duration, and fov_radius. ([#156](https://github.com/iausathub/satchecker/pull/156))


# 1.4.0 (2025-07-01)

### Miscellaneous

- Added type checking to linting part of GitHub actions (and associated changes to address type checking errors). ([#136](https://github.com/iausathub/satchecker/pull/136))
- Start collecting ephemeris files from the public files on Space-Track (Starlink only). ([#143](https://github.com/iausathub/satchecker/pull/143))

### Bugfixes

- Fix for range_km being null in satellite-passes FOV endpoint. ([#151](https://github.com/iausathub/satchecker/pull/151))

### Features

- Add `include_tles` parameter to the satellite-passes FOV endpoint to show the TLE data used to generate the position data. ([#135](https://github.com/iausathub/satchecker/pull/135))
- Add satellite generation (Starlink only at the moment) to the available satellite metadata. ([#137](https://github.com/iausathub/satchecker/pull/137))
- Add `constellation` parameter to the satellite-passes FOV endpoint satellites-above-horizon to filter the results to a specific constellation. Valid options are currently `starlink`, `oneweb`, `kuiper`, `ast` and `planet`. ([#149](https://github.com/iausathub/satchecker/pull/149))
- Added optional `data_source` parameter to `fov` endpoint. Can be Celestrak or Spacetrack - default is "any". ([#152](https://github.com/iausathub/satchecker/pull/152))

### Changes

- Cache most recent TLE set for use with FOV queries from the current time either into the future or up to 3 hours into the past. If cache is inaccessible for any reason, it defaults to a regular database query. ([#136](https://github.com/iausathub/satchecker/pull/136))
- Update API error message text to add more context to the error. ([#151](https://github.com/iausathub/satchecker/pull/151))


# 1.3.0 (2025-03-21)

### Miscellaneous

- Add support for Towncrier change logs ([#129](https://github.com/iausathub/satchecker/pull/129))

### Improved Documentation

- Separate documentation for TLE and satellite related endpoints for the Tools API ([#127](https://github.com/iausathub/satchecker/pull/127))

### Features

- Add endpoints to the tools API to get the TLE nearest to a given date, get TLEs immediately before and after a given date, and get any specified number of TLEs before or after a given date ([#127](https://github.com/iausathub/satchecker/pull/127))
- Add caching for FOV queries with a 1 hour expiration. Caching is based on all FOV query parameters so only identical queries are cached. ([#129](https://github.com/iausathub/satchecker/pull/129))


# 1.2.0 (2025-03-06)

### Features

- Added endpoint to get all active satellites
- Support astropy site names as alternatives to lat/lon/elevation in ephemeris and FOV endpoints
- Initial field of view service to check satellite passes through a given field of view, and which satellites are currently above the horizon.
- Add txt as a result format option for getting all TLEs from a given epoch


# 1.1.0 (2024-10-31)

### Bugfixes

- Fix for rogue satellites with no apparent current sat number

### Features

- Add endpoint to get all TLEs for a given date
- Add endpoint to get satellite metadata; update tests and documentation
- Add tools endpoint to get satellite metadata
- Add TLE epoch date to ephemeris data response
- Add option to zip TLE results

### Changes

- Change 'and' condition to filter satellite search for metadata properly
- Get satellite info by name: use date_added instead of has_current_sat_number
- Change intl_designator to international_designator


# v1.0.4 (2024-10-01)

### Features

- Add endpoint to get all TLEs for active objects at the current (or specified) epoch.


# v1.0.3 (2024-09-15)

### Features

- Add endpoint to get satellite data by name or NORAD ID


# v1.0.2 (2024-09-06)

### Features

- Add international designator/COSPAR ID to ephemeris data responses


# v1.0.1 (2025-08-27)

### Bugfixes

- Fix path to conf.py
- Fix 403 error causing health check to fail


# v1.0.0 (2024-07-01)

### Features

- Add versioning to API URL (v1 currently); version is optional and not including it will return the most recent version (api-versioning)
- Add is_current_version to name/id check endpoints to show which is the current version of the satellite information (current-version-flag)

### Changes

- Change to using Celery for satellite propagation; add flask-migrate (celery-migration)
- Change to use closest TLE from any source if source is not specified (closest-tle)
- Change JSON response format (json-response-format)
- Refactor to consolidate shared functionality and support versioning (refactor-versioning)


# v0.4.0-beta (2024-05-08)

### Features

- Add new endpoint to get all available TLE data for a given satellite over a given date range (historical-tle)
- Add new endpoints for satellite name/id lookup: get-names-from-norad-id and get-norad-ids-from-name (name-id-lookup)


# v0.3.1-beta (2024-05-01)

### Miscellaneous

- Extend timeout to retrieve Space-Track TLEs

### Improved Documentation

- Update documentation and example links

### Features

- Add observer and satellite GCRS positions to the response

### Changes

- Change response when no position data is found to return a relevant message


# v0.3.0-beta (2024-04-01)

### Features

- Add spacetrack as a new data source, chose TLE closest to given date

### Miscellaneous

- Pass in datetime instead of astropy.Time


# v0.2.1-beta (2025-03-20)

### Deprecations and Removals

- Temporarily remove service stability check


# v0.2.0-beta (2024-01-13)

### Features

- Add minimum and maximum altitudes as optional parameters
- Add min/max altitude parameters, add database fields, update documentation and health check

### Miscellaneous

- Minor updates - default jd time step, add database fields, update documentation


# beta (2023-11-08)

### Features

- Use astropy Time and EarthLocation
- Add endpoint to retrieve ephemeris by satellite catalog number
- Add catalog number endpoints and integration tests
- Add endpoint to get ephemeris from a TLE
- Add error handling and rate limiting
- Add illuminated flag
- TLE endpoint, switch to astropy objects, deployment related clean up

### Bugfixes

- Fix for attribute not found when retrieving TLE

### Improved Documentation

- Clean up and documentation
- Merge readme updates and minor code formatting fixes
