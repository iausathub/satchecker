import requests
from flask import abort, redirect

from api.entrypoints.extensions import limiter

from . import api_main, api_v1


@api_main.app_errorhandler(404)
@api_v1.app_errorhandler(404)
def page_not_found(error):
    """Handle page not found errors.
    ---
    tags:
      - Errors
    summary: Page not found error
    description: Returns when a requested page or endpoint doesn't exist
    responses:
      404:
        description: The requested page or endpoint was not found
    """
    return (
        "Error 404: Page not found<br /> \
        Check your spelling to ensure you are accessing the correct endpoint.",
        404,
    )


@api_main.app_errorhandler(400)
@api_v1.app_errorhandler(400)
def missing_parameter(e):
    """Handle bad request errors.
    ---
    tags:
      - Errors
    summary: Bad request error
    description: Returns when request parameters are incorrect or missing
    responses:
      400:
        description: The request contains invalid parameters or too many results
    """
    return (
        f"Error 400: Incorrect parameters or too many results to return \
        (maximum of 1000 in a single request)<br /> \
        Check your request and try again.<br /><br />{str(e)}",
        400,
    )


@api_main.app_errorhandler(429)
@api_v1.app_errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors.
    ---
    tags:
      - Errors
    summary: Rate limit error
    description: Returns when API request rate limits are exceeded
    responses:
      429:
        description: The client has exceeded the allowed request rate
    """
    return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429


@api_main.app_errorhandler(500)
def internal_server_error(e):
    """Handle internal server errors.
    ---
    tags:
      - Errors
    summary: Internal server error
    description: Returns when an unexpected server error occurs
    responses:
      500:
        description: An unexpected error occurred on the server
    """
    return "Error 500: Internal server error:<br />" + e.description, 500


@api_v1.route("/")
@api_v1.route("/index")
@api_main.route("/")
@api_main.route("/index")
@limiter.limit("100 per second, 2000 per minute")
def root():
    """Redirect to API documentation.
    ---
    tags:
      - System
    summary: API root endpoint
    description: Redirects to the API documentation page
    responses:
      302:
        description: Redirects to the API documentation URL
    """
    return redirect("https://satchecker.readthedocs.io/en/latest/")


@api_v1.route("/health")
@api_main.route("/health")
@limiter.exempt
def health():
    """Check the health of the application.
    ---
    tags:
      - System
    summary: Check the health of the API
    description: Checks if the application can connect to the IAU CPS URL and is healthy
    responses:
      200:
        description: API is healthy and can connect to required services
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Healthy
      503:
        description: API is not healthy due to connection issues
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Error unable to connect to IAU CPS URL
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        url = "https://satchecker.cps.iau.org/tools/get-satellite-data/"
        url += "?id=25544&id_type=catalog"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        abort(503, f"Error: Unable to connect to test URL - {e}")
    else:
        return {"message": "Healthy"}
