import logging
import traceback
from datetime import datetime, timezone

from flask import jsonify, request

# Use the application's centralized logging configuration
logger = logging.getLogger(__name__)


def handle_error(error):
    """
    Global error handler for consistent error logging and responses
    """

    # Get timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Determine status code and message
    if hasattr(error, "code"):
        code = error.code
        message = getattr(error, "description", str(error))
    elif hasattr(error, "status_code"):
        code = error.status_code
        message = str(error)
    else:
        code = 500
        message = "Internal server error"

    # Create error details
    error_details = {
        "timestamp": timestamp,
        "path": request.path,
        "method": request.method,
        "error_type": error.__class__.__name__,
        "message": message,
        "status_code": code,
    }

    # Always log error details for debugging
    logger.error(
        f"\nError occurred:\n"
        f"Status Code: {code}\n"
        f"Type: {error_details['error_type']}\n"
        f"Path: {error_details['path']}\n"
        f"Method: {error_details['method']}\n"
        f"Message: {message}\n"
        f"Stack Trace:\n{traceback.format_exc()}"
    )

    return jsonify(error_details), code


def init_error_handler(app):
    """Register error handlers with Flask app"""
    logger.info("Registering error handler")

    # Register for all exceptions
    app.register_error_handler(Exception, handle_error)
