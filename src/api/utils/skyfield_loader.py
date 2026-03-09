"""
Centralized Skyfield data loader.

Uses a fixed directory (from SKYFIELD_DATA_DIR env, default /app/skyfield-data)
so the DE430t.bsp file added to the Docker image at build time
"""

import os

from skyfield.api import Loader

_SKYFIELD_DATA_DIR = os.environ.get("SKYFIELD_DATA_DIR", "/app/skyfield-data")
load = Loader(_SKYFIELD_DATA_DIR, verbose=False)
