import json
import logging
import os
import re
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    # Regex to strip ANSI color codes
    ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")

    def __init__(self):
        super().__init__()
        self._service = os.environ.get("SERVICE_NAME", "satchecker")

    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc)

        # Strip ANSI color codes from message
        message = self.ANSI_ESCAPE.sub("", record.getMessage())

        log_data = {
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "service": self._service,
            "message": message,
        }
        # Add extra fields if present (from request and error logging)
        for key in [
            "endpoint",
            "method",
            "path",
            "status",
            "duration_ms",
            "ip",
            "query",
            "user_agent",
            "error_type",
            "status_code",
        ]:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        # Include exception traceback if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)
