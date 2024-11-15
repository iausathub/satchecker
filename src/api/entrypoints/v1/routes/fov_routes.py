from flask import abort, jsonify, request
from flask import current_app as app

from api.adapters.repositories.tle_repository import SqlAlchemyTLERepository
from api.common.exceptions import ValidationError
from api.entrypoints.extensions import db, get_forwarded_address, limiter
from api.services.fov_service import get_satellite_passes_in_fov
from api.services.validation_service import validate_parameters

from . import api_main, api_source, api_v1, api_version


@api_v1.route("/fov/satellite-passes/")
@api_main.route("/fov/satellite-passes/")
@limiter.limit(
    "100 per second, 2000 per minute", key_func=lambda: get_forwarded_address(request)
)
def get_satellite_passes():
    required_parameters = [
        "latitude",
        "longitude",
        "elevation",
        "duration",
        "ra",
        "dec",
        "fov_radius",
    ]

    optional_parameters = ["start_time_jd", "mid_obs_time_jd", "group_by"]

    try:
        parameters = validate_parameters(
            request, required_parameters + optional_parameters, required_parameters
        )
    except ValidationError as e:
        abort(e.status_code, e.message)

    session = db.session
    tle_repo = SqlAlchemyTLERepository(session)

    try:
        satellite_passes = get_satellite_passes_in_fov(
            tle_repo,
            parameters["location"],
            parameters["mid_obs_time_jd"],
            parameters["start_time_jd"],
            parameters["duration"],
            parameters["ra"],
            parameters["dec"],
            parameters["fov_radius"],
            parameters["group_by"],
            api_source,
            api_version,
        )
        if not satellite_passes:
            return {
                "info": "No position information found with this criteria",
                "api_source": api_source,
                "version": api_version,
            }

        return jsonify(satellite_passes)
    except ValueError as e:
        app.logger.error(e)
        return jsonify({"error": "Incorrect parameters"}), 400
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500
