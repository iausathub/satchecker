import requests
from flask import abort, redirect, request

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


@api_v1.route("/debug/whoami")
@api_main.route("/debug/whoami")
@limiter.exempt
def whoami():
    """Report the client-identifying values the app actually receives.
    ---
    tags:
      - System
    summary: Diagnostic for client IP / forwarding headers
    description: >
      Returns the socket peer address and the forwarding headers the
      application sees, so we can determine which value (if any) carries the
      real client IP behind the load balancer. Exempt from rate limiting so it
      stays reachable while the shared limit is saturated. Temporary diagnostic.
    responses:
      200:
        description: The client-identifying values seen by the application
        content:
          application/json:
            schema:
              type: object
    """
    return {
        "remote_addr": request.remote_addr,
        "x_forwarded_for": request.headers.get("X-Forwarded-For"),
        "x_real_ip": request.headers.get("X-Real-IP"),
        "cloudfront_viewer_address": request.headers.get("CloudFront-Viewer-Address"),
        "true_client_ip": request.headers.get("True-Client-IP"),
        "forwarded": request.headers.get("Forwarded"),
    }


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
