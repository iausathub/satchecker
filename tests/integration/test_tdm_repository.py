# ruff: noqa: S101

from datetime import datetime, timedelta, timezone

from src.api.adapters.database_orm import TdmPredictionDb, TdmPredictionPointDb
from src.api.adapters.repositories.satellite_repository import (
    SqlAlchemySatelliteRepository,
)
from src.api.adapters.repositories.tdm_repository import (
    SqlAlchemyTdmPredictionRepository,
)
from tests.factories import SatelliteFactory
from tests.factories.tdm_prediction_factory import TdmPredictionFactory


def test_add_tdm_prediction(session, services_available):
    satellite = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    tdm_prediction = TdmPredictionFactory(satellite=satellite)
    tdm_prediction_repository = SqlAlchemyTdmPredictionRepository(session)

    tdm_prediction_repository.add(tdm_prediction)
    session.commit()

    orm_tdm = session.query(TdmPredictionDb).one()
    repo_tdm_prediction = SqlAlchemyTdmPredictionRepository._to_domain(orm_tdm, session)
    assert repo_tdm_prediction.satellite.sat_number == satellite.sat_number
    assert repo_tdm_prediction.satellite.sat_name == satellite.sat_name
    assert repo_tdm_prediction.date_added == tdm_prediction.date_added
    assert repo_tdm_prediction.track_id == tdm_prediction.track_id
    assert repo_tdm_prediction.folder_name == tdm_prediction.folder_name
    assert repo_tdm_prediction.reference_frame == tdm_prediction.reference_frame
    assert repo_tdm_prediction.site_name == tdm_prediction.site_name
    assert repo_tdm_prediction.creation_date == tdm_prediction.creation_date
    assert repo_tdm_prediction.time_range_start == tdm_prediction.time_range_start
    assert repo_tdm_prediction.time_range_end == tdm_prediction.time_range_end


def test_get_all_tdm_predictions_at_epoch(session, services_available):
    tdm_prediction_repository = SqlAlchemyTdmPredictionRepository(session)

    site_name = "LSST"

    satellite = SatelliteFactory(decay_date=None)
    satellite_2 = SatelliteFactory(decay_date=None)
    satellite_3 = SatelliteFactory(decay_date=None)
    sat_repository = SqlAlchemySatelliteRepository(session)
    sat_repository.add(satellite)
    sat_repository.add(satellite_2)
    sat_repository.add(satellite_3)

    now = datetime.now(timezone.utc)
    tdm_prediction_1 = TdmPredictionFactory(
        creation_date=now,
        satellite=satellite,
        site_name=site_name,
    )
    tdm_prediction_2 = TdmPredictionFactory(
        creation_date=now - timedelta(days=30),
        satellite=satellite_2,
        site_name=site_name,
    )
    tdm_prediction_repository.add(tdm_prediction_1)
    tdm_prediction_repository.add(tdm_prediction_2)
    session.commit()

    results = tdm_prediction_repository.get_all_tdm_predictions_at_epoch(
        now + timedelta(hours=9), 30, 1, 10, "zip", site_name
    )
    assert len(results[0]) == 1

    tdm_prediction_3 = TdmPredictionFactory(
        creation_date=now - timedelta(days=29),
        time_range_start=now - timedelta(days=29.6),
        time_range_end=now - timedelta(days=29.4),
        satellite=satellite_3,
        site_name=site_name,
    )
    tdm_prediction_repository.add(tdm_prediction_3)
    session.commit()

    results = tdm_prediction_repository.get_all_tdm_predictions_at_epoch(
        now - timedelta(days=29.5), 30, 1, 10, "zip", site_name
    )
    assert len(results[0]) == 2


def test_get_all_tdm_predictions_most_recent_by_satellite(session, services_available):
    tdm_prediction_repository = SqlAlchemyTdmPredictionRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(decay_date=None)
    sat_repository.add(satellite)

    now = datetime.now(timezone.utc)
    query_epoch = now + timedelta(hours=9)
    time_range_start = now + timedelta(hours=8)
    time_range_end = now + timedelta(hours=34)

    older_prediction = TdmPredictionFactory(
        satellite=satellite,
        creation_date=now - timedelta(hours=2),
        time_range_start=time_range_start,
        time_range_end=time_range_end,
    )
    newer_prediction = TdmPredictionFactory(
        satellite=satellite,
        creation_date=now,
        time_range_start=time_range_start,
        time_range_end=time_range_end,
    )
    tdm_prediction_repository.add(older_prediction)
    tdm_prediction_repository.add(newer_prediction)
    session.commit()

    site_name = older_prediction.site_name
    results, total_count, _ = (
        tdm_prediction_repository.get_all_tdm_predictions_at_epoch(
            query_epoch, 30, 1, 10, "zip", site_name
        )
    )

    assert total_count == 1
    assert results[0].track_id == newer_prediction.track_id


def test_get_tdm_prediction_points(session, services_available):
    tdm_prediction_repository = SqlAlchemyTdmPredictionRepository(session)
    sat_repository = SqlAlchemySatelliteRepository(session)

    satellite = SatelliteFactory(decay_date=None)
    sat_repository.add(satellite)

    now = datetime.now(timezone.utc)
    prediction = TdmPredictionFactory(satellite=satellite, creation_date=now)
    prediction2 = TdmPredictionFactory(
        satellite=satellite, creation_date=now + timedelta(minutes=1)
    )
    tdm_prediction_repository.add(prediction)
    tdm_prediction_repository.add(prediction2)
    session.flush()

    orm_prediction = (
        session.query(TdmPredictionDb)
        .filter(TdmPredictionDb.track_id == prediction.track_id)
        .one()
    )
    orm_prediction2 = (
        session.query(TdmPredictionDb)
        .filter(TdmPredictionDb.track_id == prediction2.track_id)
        .one()
    )
    point1 = TdmPredictionPointDb(
        tdm_prediction_id=orm_prediction.id,
        timestamp=now + timedelta(minutes=1),
        right_ascension=10.5,
        declination=-20.3,
        apparent_magnitude=5.1,
    )
    point2 = TdmPredictionPointDb(
        tdm_prediction_id=orm_prediction.id,
        timestamp=now + timedelta(minutes=2),
        right_ascension=11.0,
        declination=-21.0,
        apparent_magnitude=5.2,
    )
    point3 = TdmPredictionPointDb(
        tdm_prediction_id=orm_prediction2.id,
        timestamp=now + timedelta(minutes=2),
        right_ascension=11.0,
        declination=-21.0,
        apparent_magnitude=5.2,
    )
    session.add_all([point1, point2, point3])
    session.commit()

    points = tdm_prediction_repository.get_tdm_prediction_points([orm_prediction.id])

    assert len(points) == 2
    assert points[0].right_ascension == 10.5
    assert points[0].declination == -20.3
    assert points[0].apparent_magnitude == 5.1
    assert points[0].satellite_number == satellite.sat_number
    assert points[0].satellite_name == satellite.sat_name
    assert points[0].tdm_prediction_id == orm_prediction.id


def test_get_tdm_prediction_points_empty_input(session, services_available):
    tdm_prediction_repository = SqlAlchemyTdmPredictionRepository(session)

    points = tdm_prediction_repository.get_tdm_prediction_points([])

    assert points == []
