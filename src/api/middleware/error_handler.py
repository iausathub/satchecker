import logging

from flask import jsonify, request

logger = logging.getLogger(__name__)


def handle_error(error):
    """
    Global error handler for consistent error logging and responses
    """

    # Determine status code and message. Only treat code/status_code as an HTTP
    # status when it is actually an int -- some exceptions (e.g. SQLAlchemy errors)
    # carry a non-integer "code" attribute (a docs slug like "9h9h"), which would
    # otherwise break the comparison below and mask the real error as a bare 500.
    if hasattr(error, "code") and isinstance(error.code, int):
        code = error.code
        message = getattr(error, "description", str(error))
    elif hasattr(error, "status_code") and isinstance(error.status_code, int):
        code = error.status_code
        message = getattr(error, "message", str(error))
    else:
        code = 500
        message = "Internal server error"

    log_extra = {
        "error_type": error.__class__.__name__,
        "status_code": code,
        "method": request.method,
        "path": request.path,
    }

    if code >= 500:
        logger.error(
            "unhandled exception",
            exc_info=error,
            extra=log_extra,
        )
    else:
        logger.info(
            "client error",
            extra=log_extra,
        )

    return (
        jsonify(
            {
                "path": request.path,
                "method": request.method,
                "error_type": error.__class__.__name__,
                "message": message,
                "status_code": code,
            }
        ),
        code,
    )


def init_error_handler(app):
    """Register error handlers with Flask app"""
    logger.info("Registering error handler")

    # Register for all exceptions
    app.register_error_handler(Exception, handle_error)
