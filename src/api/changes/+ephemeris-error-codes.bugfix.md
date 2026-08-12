Return correct HTTP status codes from the ephemeris endpoints for TLE issues: 404 when no TLE is found and 422 when the requested date is outside the range of available TLE data, instead of 500.
