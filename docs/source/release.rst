Release History
================

See the full changelog `here <https://github.com/iausathub/satchecker/releases>`_.

v1.2.0
------------
* Initial field of view service to check satellite passes through a given field of view, and which satellites are currently above the horizon.
* Added endpoint to get all active satellites
* Add txt as a result format option for getting all TLEs from a given epoch
* Support astropy site names as alternatives to lat/lon/elevation in ephemeris and FOV endpoints

v1.1.0
------------
* Add TLE epoch date to ephemeris data response

v1.0.4
------------
* Add endpoint to get all TLEs for active objects at the current (or specified ) epoch.

v1.0.3
------------
* Add endpoint to get satellite data by name or NORAD ID

v1.0.2
------------
* Add international designator/COSPAR ID to ephemeris data responses

v1.0.0-beta
------------
* Add versioning to API URL (v1 currently); version is optional and not including it will return the most recent version
* Add is_current_version to name/id check endpoints to show which is the current version of the satellite information
* Change to using Celery for satellite propagation; add flask-migrate
* Change JSON response format
* Refactor to consolidate shared functionality and support versioning
* Change to use closest TLE from any source if source is not specified

v0.4.0-beta
------------
* Add new endpoints for satellite name/id lookup: get-names-from-norad-id and get-norad-ids-from-name
* Add new endpoint to get all available TLE data for a given satellite over a given date range

v0.3.1-beta
------------
* Change response when no position data is found to return a relevant message
* Extend timeout to retrieve Space-Track TLEs
* Update documentation and example links
* Add observer and satellite GCRS positions to the response

v0.3.0-beta
------------
* Pass in datetime instead of astropy.Time
* Add spacetrack as a new data source, chose TLE closest to given date

v0.2.1-beta
------------
* Temporarily remove service stability check

v0.2.0-beta
------------
* Add minimum and maximum altitudes as optional parameters
* Minor updates - default jd time step, add database fields, update documentation
* Add min/max altitude parameters, add database fields, update documentation and health check

beta
------------

.. note:: This is a pre-release version

* Initial deploy to AWS ECS and documentation
* Add error handling and rate limiting
* Add illuminated flag
* Update script to populate primary database
* Add endpoint to retrieve ephemeris by satellite catalog number
* Fix for attribute not found when retrieving TLE
* Add tests to GitHub workflows, fix test assert precision
* Add catalog number endpoints and integration tests
* Use astropy Time and EarthLocation
* Add endpoint to get ephemeris from a TLE
* TLE endpoint, switch to astropy objects, deployment related clean up
* Clean up and documentation
* Merge readme updates and minor code formatting fixes
