Release History
================

See the full changelog `here <https://github.com/iausathub/satchecker/releases>`_.

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
