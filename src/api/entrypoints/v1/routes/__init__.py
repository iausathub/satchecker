# ruff: noqa: I001
from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__)
api_main = Blueprint("api_main", __name__)

api_source = "IAU CPS SatChecker"
api_version = "1.3.1"

# Import all route modules to register the routes with the blueprints
# This ensures all routes are registered when the blueprints are imported elsewhere
from . import routes  # noqa: E402, F401
from . import ephemeris_routes  # noqa: E402, F401
from . import fov_routes  # noqa: E402, F401
from . import tools_routes  # noqa: E402, F401
