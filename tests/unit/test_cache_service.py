# ruff: noqa: S101
import astropy.units as u
from astropy.coordinates import EarthLocation

from api.services.cache_service import (
    check_redis_memory,
    create_fov_cache_key,
    get_cached_data,
    refresh_tle_cache,
    set_cached_data,
)


def test_get_cached_data_redis_connection_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_redis.get.side_effect = ConnectionError("Redis connection failed")

    result = get_cached_data("test_key", "default_value")

    assert result == "default_value"
    mock_redis.get.assert_called_once_with("test_key")


def test_get_cached_data_json_decode_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_redis.get.return_value = b"invalid json {"

    result = get_cached_data("test_key", "default_value")

    assert result == "default_value"
    mock_redis.get.assert_called_once_with("test_key")


def test_get_cached_data_timeout_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_redis.get.side_effect = TimeoutError("Redis timeout")

    result = get_cached_data("test_key", {"fallback": True})

    assert result == {"fallback": True}


def test_get_cached_data_general_exception(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_redis.get.side_effect = Exception("Unexpected error")

    result = get_cached_data("test_key")

    assert result is None


def test_set_cached_data_json_serialization_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mocker.patch("api.services.cache_service.check_redis_memory")

    unserializable_data = {"func": lambda x: x}

    result = set_cached_data("test_key", unserializable_data)

    assert result is False
    mock_redis.setex.assert_not_called()


def test_set_cached_data_redis_setex_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mocker.patch("api.services.cache_service.check_redis_memory")

    mock_redis.setex.side_effect = ConnectionError("Redis connection failed")
    mock_redis.get.return_value = None  # Verification will fail

    result = set_cached_data("test_key", {"data": "test"})

    assert result is False


def test_set_cached_data_verification_failure(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mocker.patch("api.services.cache_service.check_redis_memory")

    mock_redis.setex.return_value = True
    mock_redis.get.return_value = None  # Verification fails

    result = set_cached_data("test_key", {"data": "test"})

    assert result is False


def test_set_cached_data_verification_json_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mocker.patch("api.services.cache_service.check_redis_memory")

    mock_redis.setex.return_value = True
    mock_redis.get.return_value = b"invalid json {"

    result = set_cached_data("test_key", {"data": "test"})

    assert result is False


def test_set_cached_data_data_too_large(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")

    # Create data that exceeds the 500MB limit
    large_data = {"data": "x" * (500 * 1024 * 1024 + 1)}

    result = set_cached_data("test_key", large_data)

    assert result is False
    mock_redis.setex.assert_not_called()


def test_refresh_tle_cache_no_flask_context(mocker):
    mock_logger = mocker.patch("api.services.cache_service.logger")
    mocker.patch("flask.current_app", None)

    result = refresh_tle_cache()

    assert result is False
    mock_logger.error.assert_called_once()


def test_refresh_tle_cache_database_error(mocker):
    mock_repo_class = mocker.patch(
        "api.adapters.repositories.tle_repository.SqlAlchemyTLERepository"
    )
    mock_db = mocker.patch("api.services.cache_service.db")
    mock_current_app = mocker.MagicMock()
    mocker.patch("flask.current_app", mock_current_app)

    mock_session = mocker.Mock()
    mock_db.session = mock_session

    mock_repo = mocker.Mock()
    mock_repo._get_all_tles_at_epoch.side_effect = Exception("Database error")
    mock_repo_class.return_value = mock_repo

    result = refresh_tle_cache()

    assert result is False
    mock_session.rollback.assert_called_once()


def test_refresh_tle_cache_serialization_error(mocker):
    mock_repo_class = mocker.patch(
        "api.adapters.repositories.tle_repository.SqlAlchemyTLERepository"
    )
    mock_batch_serialize = mocker.patch(
        "api.adapters.repositories.tle_repository.SqlAlchemyTLERepository.batch_serialize_tles"
    )
    mock_db = mocker.patch("api.services.cache_service.db")
    mock_current_app = mocker.MagicMock()
    mocker.patch("flask.current_app", mock_current_app)

    mock_session = mocker.Mock()
    mock_db.session = mock_session

    mock_repo = mocker.Mock()
    mock_repo._get_all_tles_at_epoch.return_value = ([], 0, "database")
    mock_repo_class.return_value = mock_repo

    mock_batch_serialize.side_effect = Exception("Serialization error")

    result = refresh_tle_cache()

    assert result is False


def test_refresh_tle_cache_cache_set_failure(mocker):
    mock_repo_class = mocker.patch(
        "api.adapters.repositories.tle_repository.SqlAlchemyTLERepository"
    )
    mock_set_cached = mocker.patch("api.services.cache_service.set_cached_data")
    mock_batch_serialize = mocker.patch(
        "api.adapters.repositories.tle_repository.SqlAlchemyTLERepository.batch_serialize_tles"
    )
    mock_db = mocker.patch("api.services.cache_service.db")
    mock_current_app = mocker.MagicMock()
    mocker.patch("flask.current_app", mock_current_app)

    mock_session = mocker.Mock()
    mock_db.session = mock_session

    mock_repo = mocker.Mock()
    mock_repo._get_all_tles_at_epoch.return_value = ([], 0, "database")
    mock_repo_class.return_value = mock_repo

    mock_batch_serialize.return_value = []
    mock_set_cached.return_value = False

    result = refresh_tle_cache()

    assert result is True


def test_check_redis_memory_connection_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_logger = mocker.patch("api.services.cache_service.logger")

    mock_redis.info.side_effect = ConnectionError("Redis connection failed")

    check_redis_memory()

    mock_logger.error.assert_called_once()


def test_check_redis_memory_timeout_error(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_logger = mocker.patch("api.services.cache_service.logger")

    mock_redis.info.side_effect = TimeoutError("Redis timeout")

    check_redis_memory()

    mock_logger.error.assert_called_once()


def test_check_redis_memory_missing_memory_info(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_logger = mocker.patch("api.services.cache_service.logger")

    mock_redis.info.side_effect = [{}, {"evicted_keys": 0, "expired_keys": 0}]

    check_redis_memory()

    # Should not raise exception
    assert mock_logger.info.call_count >= 1


def test_check_redis_memory_missing_stats_info(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")
    mock_logger = mocker.patch("api.services.cache_service.logger")

    mock_redis.info.side_effect = [
        {"used_memory": 1000000, "used_memory_peak": 2000000, "maxmemory": 0},
        {},  # Empty stats
    ]

    check_redis_memory()

    # Should not raise exception
    assert mock_logger.info.call_count >= 1


def test_create_fov_cache_key_none_time_values():
    location = EarthLocation(lat=45.0 * u.deg, lon=-122.0 * u.deg, height=100.0 * u.m)

    result = create_fov_cache_key(
        location=location,
        mid_obs_time_jd=None,
        start_time_jd=None,
        duration=3600.0,
        ra=180.0,
        dec=45.0,
        fov_radius=10.0,
    )

    assert isinstance(result, str)
    assert "mid_time_None" in result
    assert "start_time_None" in result


def test_cache_roundtrip_with_redis_failure(mocker):
    mock_redis = mocker.patch("api.services.cache_service.redis_client")

    # Set up Redis to fail on get but succeed on set
    mock_redis.get.side_effect = ConnectionError("Redis connection failed")
    mock_redis.setex.return_value = True

    result = get_cached_data("test_key", "default")
    assert result == "default"

    result = set_cached_data("test_key", {"data": "test"})
    assert result is False
