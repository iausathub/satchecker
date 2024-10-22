from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__)
api_main = Blueprint("api_main", __name__)

api_source = "IAU CPS SatChecker"
api_version = "1.0.4"
