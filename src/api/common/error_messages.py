"""
This module defines error messages for invalid inputs in the application.

Constants:
    INVALID_LOCATION: Error message for invalid location parameters.

    INVALID_PARAMETER: Error message for invalid parameter format.

    INVALID_JD: Error message for invalid Julian Date.

    INVALID_SOURCE: Error message for invalid data source.

    NO_TLE_FOUND: Error message when no TLE is found.
"""

INVALID_LOCATION = "Error: Invalid location parameters"
INVALID_PARAMETER = "Error: Invalid parameter format"
INVALID_JD = "Error: Invalid Julian Date"
INVALID_SOURCE = "Error: Invalid data source"
INVALID_TLE = "Error: Invalid TLE format"
INVALID_FORMAT = "Error: Invalid result format"
NO_TLE_FOUND = "Error: No TLE found"
TOO_MANY_RESULTS = (
    "Error: Too many results to return (maximum of 1000 in a single request)"
)
PAGINATION_LIMIT_EXCEEDED = "Error: Pagination limit exceeded"
