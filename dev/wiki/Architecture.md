# Overview
SatChecker is designed to facilitate precise satellite position and brightness estimates for observation planning and estimating the effects of satellite constellations on astronomy. This system provides a suite of APIs to support detailed satellite position and brightness estimates, crucial for applications ranging from astronomical research to satellite monitoring. The Ephemeris API, a core component of SatChecker, allows users to obtain satellite positions and brightness estimates for specific locations and time ranges, with filtering options such as altitude and brightness thresholds. It supports satellite searches by name or NORAD ID and offers position propagation using custom Two-Line Element (TLE) sets. Complementing the Ephemeris API, the Tools API provides essential resources for satellite information management, including endpoints for querying satellite names and NORAD IDs, and accessing raw TLE data. Additionally, the Field of View (FOV) API will eventually predict satellite crossings within a specified field of view at given coordinates and times.

## Ephemeris
Ephemeris
The Ephemeris API provides satellite position and brightness estimates for a specified location over a given time range. Data returned can be further filtered by minimum and maximum altitude of the satellite, estimated brightness range, and data source.

## Tools
The Tools API has some supporting resources for satellite information and data access. It has endpoints to query satellite names associated with a given NORAD id and vice versa. This is because many satellites are issued temporary designations (usually a temporary name, less often a temporary id), and since TLEs are associated with a specific version of a satellite, it’s necessary to have a history of related data to connect the full TLE record for an object.

The Satellite Constellation Observation Repository (SCORE) also uses the name/id check endpoints for a tool to query the most recent name associated with a given NORAD id for data submission consistency.

The raw TLE data for a satellite and metadata for each satellite is also available via other endpoints, which gives the option to either get all available data for a satellite or limit it to a certain date range.

## Field of View (FOV) - TBD
The FOV API will provide the ability to see which satellites are predicted to cross the specified field of view at a given date/time/geographic location. The field of view is given by an RA/Dec coordinate for the center, and either a radius or rectangular area in degrees.

Satellites can be searched by name or by NORAD id, and at either at a single date/time or over a date range. All dates used as endpoint parameters are Julian dates. The Ephemeris API also has an endpoint that will propagate a satellite’s position using a user-specified TLE.


# Implementation
SatChecker is primarily a Flask API, with the front end for web access to be determined; all TLE and satellite data is stored in a Postgres database. ORM (object-relational mapping) is handled with SQLAlchemy.

SatChecker uses Celery for task management, primarily to distribute the individual satellite propagation iterations needed for FOV mode.


## API Response Details

Field | Description | Type
-- | -- | --
altitude_deg | Satellite position altitude in degrees at the given time and location | float
azimuth_deg | Satellite position azimuth in degrees at the given time and location | float
catalog_id | NORAD ID of the satellite | integer
data_source | Source for the TLE data used to generate this satellite position (either Celestrak or Space-Track | text
ddec_deg_per_sec | Change in declination position in degrees per second | float
declination_deg | Declination of the satellite at this specific date/time/location in decimal degrees | float
dra_cosdec_deg_per_sec | Change in declination in degrees per second | float
illuminated | Whether the satellite is illuminated at the given time and location | bool
julian_date | The date/time corresponding to the given position prediction | float
name | Name of the satellite (either specified by the user, or the one associated with the given NORAD ID and TLE data) | text
observer_gcrs_km | Position vector for the observer (Geocentric Celestial Reference System (GCRS)) | array[ float ]
phase_angle_deg | The angle between the satellite, the observer, and the sun in degrees | float
range_km | Distance to the satellite in kilometers | float
range_rate_km_per_sec | Velocity of the satellite in kilometers per second | float
right_ascension_deg | Right Ascension of the satellite at this specific date/time/location in decimal degrees | float
satellite_gcrs_km | Position vector for the satellite (Geocentric Celestial Reference System (GCRS)) | array[ float ]
tle_date | Date that the TLE used to generate this position information was collected (UTC) | text (datetime)
international_designator | International designator/COSPAR ID for the satellite | text
tle_epoch | Date that the TLE used to calculate the satellite position was created/valid for (UTC timezone) | text (datetime)
