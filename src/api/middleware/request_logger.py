import logging
import time

from flask import g, request


def init_request_logging(app):  # pragma: no cover
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        # Skip noise
        if request.endpoint in (
            "health",
            "static",
            "flasgger.static",
            "flasgger.apispec",
            None,
        ):
            return response

        duration_ms = round(
            (time.time() - getattr(g, "start_time", time.time())) * 1000, 2
        )

        xff = request.headers.get("X-Forwarded-For", "")
        ip = xff.split(",")[0].strip() if xff else request.remote_addr

        # DEBUG: Log all request headers
        all_headers = {k: v for k, v in request.headers}
        app.logger.info(
            f"DEBUG ALL HEADERS: remote_addr='{request.remote_addr}', "
            f"headers={all_headers}"
        )

        level = logging.ERROR if response.status_code >= 500 else logging.INFO

        app.logger.log(
            level,
            "api_request",
            extra={
                "endpoint": request.endpoint,
                "method": request.method,
                "path": request.path,
                "query": request.query_string.decode("utf-8")[:500],
                "status": response.status_code,
                "duration_ms": duration_ms,
                "ip": ip,
                "user_agent": (
                    request.user_agent.string[:500] if request.user_agent else None
                ),
            },
        )
        return response
