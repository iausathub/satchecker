# ruff: noqa: S101
from datetime import datetime

from api.services.tasks.ephemeris_tasks import process_results


def test_process_results_within_altitude_range():
    results = [
        (
            # ra, dec, dracosdec, ddec, alt, az, r, dr, phaseangle, illuminated
            1.0,
            2.0,
            3.0,
            4.0,
            50.0,
            100.0,
            7000.0,
            0.1,
            45.0,
            True,
            # satellite_gcrs, observer_gcrs, julian_date
            [1, 2, 3],
            [4, 5, 6],
            2451545.0,
        ),
        (
            # ra, dec, dracosdec, ddec, alt, az, r, dr, phaseangle, illuminated
            5.0,
            6.0,
            7.0,
            8.0,
            60.0,
            110.0,
            7100.0,
            0.2,
            50.0,
            False,
            # satellite_gcrs, observer_gcrs, julian_date
            [7, 8, 9],
            [10, 11, 12],
            2451546.0,
        ),
    ]
    min_altitude = 40
    max_altitude = 70
    date_collected = datetime(2023, 1, 1)
    name = "Satellite"
    intl_designator = "2024-test"
    catalog_id = "12345"
    data_source = "Source"
    api_source = "API"
    api_version = "1.0"

    expected_result = {
        "count": 2,
        "fields": [
            "name",
            "catalog_id",
            "julian_date",
            "satellite_gcrs_km",
            "right_ascension_deg",  # noqa: E501
            "declination_deg",
            "tle_date",
            "dra_cosdec_deg_per_sec",
            "ddec_deg_per_sec",  # noqa: E501
            "altitude_deg",
            "azimuth_deg",
            "range_km",
            "range_rate_km_per_sec",
            "phase_angle_deg",
            "illuminated",
            "data_source",
            "observer_gcrs_km",
            "intl_designator",
        ],
        "data": [
            [
                "Satellite",
                12345,
                2451545.0,
                [1, 2, 3],
                1.0,
                2.0,
                "2023-01-01 00:00:00 ",  # noqa: E501
                3.0,
                4.0,
                50.0,
                100.0,
                7000.0,
                0.1,
                45.0,
                True,
                "Source",
                [4, 5, 6],
                "2024-test",
            ],  # noqa: E501
            [
                "Satellite",
                12345,
                2451546.0,
                [7, 8, 9],
                5.0,
                6.0,
                "2023-01-01 00:00:00 ",  # noqa: E501
                7.0,
                8.0,
                60.0,
                110.0,
                7100.0,
                0.2,
                50.0,
                False,
                "Source",
                [10, 11, 12],
                "2024-test",
            ],
        ],  # noqa: E501
        "source": "API",
        "version": "1.0",
    }

    result = process_results(
        results,
        min_altitude,
        max_altitude,
        date_collected,
        name,
        intl_designator,
        catalog_id,
        data_source,
        api_source,
        api_version,
    )
    assert result == expected_result


def test_process_results_outside_altitude_range():
    results = [
        (
            # ra, dec, dracosdec, ddec, alt, az, r, dr, phaseangle, illuminated
            1.0,
            2.0,
            3.0,
            4.0,
            50.0,
            100.0,
            7000.0,
            0.1,
            45.0,
            True,
            # satellite_gcrs, observer_gcrs, julian_date
            [1, 2, 3],
            [4, 5, 6],
            2451545.0,
        ),
        (
            # ra, dec, dracosdec, ddec, alt, az, r, dr, phaseangle, illuminated
            5.0,
            6.0,
            7.0,
            8.0,
            60.0,
            110.0,
            7100.0,
            0.2,
            50.0,
            False,
            # satellite_gcrs, observer_gcrs, julian_date
            [7, 8, 9],
            [10, 11, 12],
            2451546.0,
        ),
    ]
    min_altitude = 80
    max_altitude = 90
    date_collected = datetime(2023, 1, 1)
    name = "Satellite"
    intl_designator = "2024-test"
    catalog_id = "12345"
    data_source = "Source"
    api_source = "API"
    api_version = "1.0"

    expected_result = {
        "info": "No position information found with this criteria",
        "api_source": api_source,
        "version": api_version,
    }

    result = process_results(
        results,
        min_altitude,
        max_altitude,
        date_collected,
        name,
        intl_designator,
        catalog_id,
        data_source,
        api_source,
        api_version,
    )
    assert result == expected_result


def test_process_results_empty_tles():
    results = []
    min_altitude = 40
    max_altitude = 70
    date_collected = "2023-01-01"
    name = "Satellite"
    intl_designator = "2024-test"
    catalog_id = "12345"
    data_source = "Source"
    api_source = "API"
    api_version = "1.0"

    expected_result = {
        "info": "No position information found with this criteria",
        "api_source": api_source,
        "version": api_version,
    }

    result = process_results(
        results,
        min_altitude,
        max_altitude,
        date_collected,
        name,
        intl_designator,
        catalog_id,
        data_source,
        api_source,
        api_version,
    )
    assert result == expected_result
