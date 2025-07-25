# ruff: noqa: S101
from datetime import datetime, timezone

import pytest
from flask import request

from api.common.exceptions import ValidationError
from api.services.validation_service import (
    extract_parameters,
    jd_arange,
    parse_tle,
    validate_parameters,
)


def test_extract_parameters_success(app):
    with app.test_request_context("/?latitude=1&longitude=2&elevation=3"):
        parameter_list = ["latitude", "longitude", "elevation"]
        parameters = extract_parameters(request, parameter_list)

        assert parameters["latitude"] == "1"
        assert parameters["longitude"] == "2"
        assert parameters["elevation"] == "3"


def test_extract_parameters_not_a_list(app):
    with pytest.raises(ValidationError):
        with app.test_request_context("/"):
            request.args = ""
            parameter_list = "latitude"

            parameters = extract_parameters(request, parameter_list)  # noqa: F841


def test_extract_parameters_no_parameters(app):
    with app.test_request_context("/?latitude="):
        parameter_list = "latitude"
    with pytest.raises(ValidationError):
        parameters = extract_parameters(request, parameter_list)  # noqa: F841


def test_validate_parameters_single_jd(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&min_altitude=30&data_source=spacetrack&julian_date=2459000"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
            "min_altitude",
            "max_altitude",
            "data_source",
            "julian_date",
        ]
        required_parameters = ["latitude", "longitude", "elevation", "julian_date"]

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["location"].lat.value == pytest.approx(1, rel=1e-9)
        assert parameters["location"].lon.value == pytest.approx(2, rel=1e-9)
        assert parameters["location"].height.value == pytest.approx(3, rel=1e-9)
        assert parameters["min_altitude"] == 30
        assert parameters["data_source"] == "spacetrack"
        assert parameters["julian_dates"][0].jd == 2459000


def test_validate_parameters_multiple_jd(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&min_altitude=30&data_source=spacetrack&startjd=2459000&stopjd=2459001&stepjd=0.5"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
            "min_altitude",
            "data_source",
            "startjd",
            "stopjd",
            "stepjd",
        ]
        required_parameters = [
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
        ]

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["location"].lat.value == pytest.approx(1, rel=1e-9)
        assert parameters["location"].lon.value == pytest.approx(2, rel=1e-9)
        assert parameters["location"].height.value == pytest.approx(3, rel=1e-9)
        assert parameters["min_altitude"] == 30
        assert parameters["data_source"] == "spacetrack"
        assert len(parameters["julian_dates"]) == 3
        assert parameters["julian_dates"][1].jd == 2459000.5


def test_validate_parameters_invalid_location(app):
    with app.test_request_context(
        "/?latitude=-500&longitude=2&elevation=3&min_altitude=30&data_source=spacetrack&julian_date=2459000"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
        ]
        required_parameters = ["latitude", "longitude", "elevation"]

        with pytest.raises(ValidationError, match="Invalid location"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_missing_parameter(app):
    with app.test_request_context("/?latitude=1&longitude=2"):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
        ]
        required_parameters = ["latitude", "longitude", "elevation"]

        with pytest.raises(ValidationError, match="Missing parameter: elevation"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_invalid_format(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&min_altitude=test"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
            "min_altitude",
        ]
        required_parameters = []

        with pytest.raises(ValidationError) as exc_info:
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )

        assert "could not convert string to float" in str(
            exc_info.value.original_exception
        )


def test_validate_parameters_invalid_jd(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&julian_date=2024-07-01"
    ):
        parameter_list = ["latitude", "longitude", "elevation", "julian_date"]
        required_parameters = ["latitude", "longitude", "elevation", "julian_date"]

        with pytest.raises(ValidationError, match="Invalid Julian Date"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_invalid_id_type(app):
    with app.test_request_context(
        "/?id=1&id_type=invalid&start_date_jd=2459000&end_date_jd=2459001"
    ):
        parameter_list = ["id", "id_type", "start_date_jd", "end_date_jd"]
        required_parameters = ["id", "id_type"]

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_invalid_group_by(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&group_by=invalid"
    ):
        parameter_list = ["latitude", "longitude", "elevation", "group_by"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_fov_obs_time(app):
    with app.test_request_context(
        "?start_time_jd=2459000&mid_obs_time_jd=2459001&duration=30"
    ):
        parameter_list = ["start_time_jd", "mid_obs_time_jd", "duration"]
        required_parameters = ["duration"]

        with pytest.raises(
            ValidationError,
            match="Cannot specify both mid_obs_time_jd and start_time_jd",
        ):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )

    with app.test_request_context("?duration=30"):
        parameter_list = ["start_time_jd", "mid_obs_time_jd", "duration"]
        required_parameters = ["duration"]

        with pytest.raises(
            ValidationError,
            match="Must specify either mid_obs_time_jd or start_time_jd",
        ):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )

    with app.test_request_context("?start_time_jd=test&duration=30"):
        parameter_list = ["start_time_jd", "mid_obs_time_jd", "duration"]
        required_parameters = ["duration"]

        with pytest.raises(ValidationError, match="Invalid Julian Date"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_too_many_times(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&startjd=2459000&stopjd=2459001&stepjd=0.000001"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
            "stepjd",
        ]
        required_parameters = [
            "latitude",
            "longitude",
            "elevation",
            "startjd",
            "stopjd",
        ]

        with pytest.raises(ValidationError, match="Too many results to return"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_invalid_data_source(app):
    with app.test_request_context(
        "/?latitude=1&longitude=2&elevation=3&data_source=invalid"
    ):
        parameter_list = [
            "latitude",
            "longitude",
            "elevation",
            "data_source",
        ]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid data source"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_invalid_object_type(app):
    with app.test_request_context("/?object_type=invalid"):
        parameter_list = ["object_type"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_constellation(app):
    with app.test_request_context("/?constellation=invalid"):
        parameter_list = ["constellation"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )

    with app.test_request_context("/?constellation=starlink"):
        parameter_list = ["constellation"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["constellation"] == "starlink"


def test_validate_parameters_tle(app):
    # valid TLE
    with app.test_request_context(
        "/?elevation=150&longitude=-110&julian_date=2459000.5&tle=ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    ):
        parameter_list = [
            "elevation",
            "longitude",
            "julian_date",
            "tle",
        ]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["tle"] is not None


def test_validate_parameters_name(app):
    with app.test_request_context("/?name=test"):
        parameter_list = ["name"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["name"] == "TEST"


def test_start_end_date_jd(app):
    with app.test_request_context("/?start_date_jd=2459000&end_date_jd=2459001"):
        parameter_list = ["start_date_jd", "end_date_jd"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["start_date_jd"] == datetime(
            2020, 5, 30, 12, 0, tzinfo=timezone.utc
        )
        assert parameters["end_date_jd"] == datetime(
            2020, 5, 31, 12, 0, tzinfo=timezone.utc
        )


def test_start_end_date_jd_invalid(app):
    with app.test_request_context("/?start_date_jd=invalid&end_date_jd=2459001"):
        parameter_list = ["start_date_jd", "end_date_jd"]
        required_parameters = []

        with pytest.raises(ValidationError):
            parameters = validate_parameters(
                request, parameter_list, required_parameters
            )

    with app.test_request_context("/?start_date_jd=2459000&end_date_jd=invalid"):
        parameter_list = ["start_date_jd", "end_date_jd"]
        required_parameters = []

        with pytest.raises(ValidationError):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_jd_arange():
    a = 2459000.0
    b = 2459001.0
    dr = 0.5
    expected = [2459000.0, 2459000.5, 2459001.0]
    result = jd_arange(a, b, dr)
    assert result.jd.tolist() == expected

    a = 2459000.0
    b = 2459000.1
    dr = 0.05
    expected = [2459000.0, 2459000.05, 2459000.1]
    result = jd_arange(a, b, dr)
    assert result.jd.tolist() == expected

    a = 2459000.0
    b = 2459001.0
    dr = 2.0
    expected = [2459000.0]
    result = jd_arange(a, b, dr)
    assert result.jd.tolist() == expected


def test_jd_arange_invalid_jd():
    a = "invalid"
    b = 2459001.0
    dr = 0.5
    with pytest.raises(ValidationError):
        jd_arange(a, b, dr)


def test_jd_arange_rounding():
    a = 2459000.0
    b = 2459000.1
    dr = 0.033333333333
    expected = [2459000.0, 2459000.03333333333, 2459000.06666666667, 2459000.1]
    result = jd_arange(a, b, dr, decimals=11)
    assert result.jd.tolist() == expected


def test_jd_arange_no_results():
    a = 2459000.0
    b = 2459000.0
    dr = 0.5
    expected = [2459000.0]
    result = jd_arange(a, b, dr)
    assert result.jd.tolist() == expected


def test_parse_tle():
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    result = parse_tle(tle)
    assert result.satellite.sat_name == "ISS (ZARYA)"
    assert result.satellite.sat_number == 25544
    assert (
        result.tle_line1
        == "1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997"
    )  # noqa: E501
    assert (
        result.tle_line2
        == "2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    )  # noqa: E501
    assert result.data_source == "user"


def test_parse_tle_invalid_format():
    tle = "ISS (ZARYA) \\n \
            1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997\\n\
            2 25544  51.6416 290.4299 0005730  30.7454 132.9751"
    with pytest.raises(ValidationError, match="Invalid TLE format"):
        parse_tle(tle)

    tle = None
    with pytest.raises(ValidationError, match="Invalid TLE format"):
        parse_tle(tle)


def test_parse_tle_missing_data():
    tle = "ISS (ZARYA) 1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997 2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"  # noqa: E501
    with pytest.raises(ValidationError, match="Invalid TLE format"):
        parse_tle(tle)


def test_validate_parameters_site(app):
    with app.test_request_context("/?site=greenwich"):
        parameter_list = ["site"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["location"].lat.deg == pytest.approx(51.477811, rel=1e-9)
        assert parameters["location"].lon.deg == pytest.approx(-0.001475, rel=1e-9)
        assert parameters["location"].height.value == pytest.approx(46, rel=1e-9)


def test_validate_parameters_site_invalid(app):
    with app.test_request_context("/?site=invalid"):
        parameter_list = ["site"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid site"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_site_and_location(app):
    with app.test_request_context(
        "/?site=greenwich&latitude=1&longitude=2&elevation=3"
    ):
        parameter_list = ["site", "latitude", "longitude", "elevation"]
        required_parameters = []

        with pytest.raises(
            ValidationError, match="Cannot specify both site and location parameters"
        ):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_ra_dec(app):
    with app.test_request_context("/?ra=1"):
        parameter_list = ["ra"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["ra"] == pytest.approx(1, rel=1e-9)

    with app.test_request_context("/?ra=a"):
        parameter_list = ["ra"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )

    with app.test_request_context("/?dec=1"):
        parameter_list = ["dec"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)
        assert parameters["dec"] == pytest.approx(1, rel=1e-9)

    with app.test_request_context("/?dec=a"):
        parameter_list = ["dec"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_duration(app):
    with app.test_request_context("/?duration=1"):
        parameter_list = ["duration"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["duration"] == pytest.approx(1, rel=1e-9)

    with app.test_request_context("/?duration=a"):
        parameter_list = ["duration"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )


def test_validate_parameters_fov_radius(app):
    with app.test_request_context("/?fov_radius=1"):
        parameter_list = ["fov_radius"]
        required_parameters = []

        parameters = validate_parameters(request, parameter_list, required_parameters)

        assert parameters["fov_radius"] == pytest.approx(1, rel=1e-9)

    with app.test_request_context("/?fov_radius=a"):
        parameter_list = ["fov_radius"]
        required_parameters = []

        with pytest.raises(ValidationError, match="Invalid parameter format"):
            parameters = validate_parameters(  # noqa: F841
                request, parameter_list, required_parameters
            )
