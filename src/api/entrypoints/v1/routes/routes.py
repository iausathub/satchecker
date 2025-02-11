import requests
from flask import abort, redirect

from api.entrypoints.extensions import limiter

from . import api_main, api_v1


@api_main.app_errorhandler(404)
@api_v1.app_errorhandler(404)
def page_not_found(error):
    """
    Handles page not found errors by returning the error message and a 404 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message.
        int: The HTTP status code for a page not found error (404).
    """
    return (
        "Error 404: Page not found<br /> \
        Check your spelling to ensure you are accessing the correct endpoint.",
        404,
    )


@api_main.app_errorhandler(400)
@api_v1.app_errorhandler(400)
def missing_parameter(e):
    """
    Handles bad request errors by returning the error message and a 400 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for a bad request error (400).
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
    """
    Handles rate limit errors by returning the error message and a 429 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for a rate limit error (429).
    """
    return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429


@api_main.app_errorhandler(500)
def internal_server_error(e):
    """
    Handles internal server errors by returning the error message and a 500 status code.

    Args:
        e (HTTPException): The exception instance with details about the error.

    Returns:
        str: A string containing a custom error message and the error's description.
        int: The HTTP status code for an internal server error (500).
    """
    return "Error 500: Internal server error:<br />" + e.description, 500


@api_v1.route("/")
@api_v1.route("/index")
@api_main.route("/")
@api_main.route("/index")
@limiter.limit("100 per second, 2000 per minute")
def root():
    """
    Redirect to API documentation
    """
    return redirect("https://satchecker.readthedocs.io/en/latest/")


@api_v1.route("/health")
@api_main.route("/health")
@limiter.exempt
def health():
    """
    Checks the health of the application by making a GET request to the IAU CPS URL.

    This function sends a GET request to the IAU CPS URL and checks the status of the
    response. If the request is successful, it returns a JSON response with a
    message indicating that the application is healthy. If the request fails for any
    reason, it aborts the request and returns a 503 status code with an error message.

    Returns:
        dict: A dictionary containing a message indicating the health of the
            application.
    Raises:
        HTTPException: An exception with a 503 status code and an error message if the
            GET request fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(
            "https://cps.iau.org/tools/satchecker/api/", headers=headers, timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        abort(503, f"Error: Unable to connect to IAU CPS URL - {e}")
    else:
        return {"message": "Healthy"}
