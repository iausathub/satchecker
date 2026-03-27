"""
Centralized Skyfield data loader.

Uses SKYFIELD_DATA_DIR env when set (e.g. /app/skyfield-data in Docker).
Otherwise uses current directory for CI/local dev
"""

import os

from skyfield.api import Loader

_SKYFIELD_DATA_DIR = os.environ.get("SKYFIELD_DATA_DIR", ".")
load = Loader(_SKYFIELD_DATA_DIR, verbose=False)
