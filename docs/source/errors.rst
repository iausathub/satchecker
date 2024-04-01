Error Codes
===============

This section provides a list of error codes that can be returned by the API.

200 - OK
------------
The request was successful.

400 - Incorrect parameters or too many results to return
---------------------------------------------------------
This error occurs if a mandaroty parameter is missing, an incorrect parameter is used, or
the request would return more than 1000 results. Use a larger time step or a shorter time range.

404 - Page not found
--------------------
Check your spelling to ensure you are accessing the correct endpoint. This may occur if
there is a typo in the URL or you are trying to access a resource that does not exist.

429 - Too many requests
------------------------
You have exceeded the rate limit for the API. Please wait a few minutes before trying again.

500 - Internal Server Error
---------------------------
This one is used for any other error that may occur. Below are the current reasons it may occur:

* **Invalid parameter format:** Format of the location or min/max altitude parameters is not correct.
* **Invalid date format:** Anything other than Julian date will fail.
* **Invalid data source:** Anything other than 'celestrak' or 'spacetrack' will fail.
* **Incorrect TLE format:** Check to make sure the TLE string used is in the correct format, and doesn't include any extra characters)
* **No TLE found:** No data found for that satellite - if this occurs, try a different data sourceor check the spelling of the satellite name. If the satellite is new, it may not be in the database yet. If none of these work, please contact us with the details of the issue.
