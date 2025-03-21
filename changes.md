# SatChecker Changelog

This document tracks all notable changes to SatChecker across versions. Entries are organized by release date and version number, with changes categorized as Features, Bugfixes, Changes, Deprecations, Documentation improvements, or Miscellaneous updates. SatChecker follows semantic versioning (MAJOR.MINOR.PATCH).

<!-- towncrier release notes start -->

# 1.2.1 (2025-03-21)

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
