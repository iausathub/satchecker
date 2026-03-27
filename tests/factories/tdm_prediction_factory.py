import datetime
from datetime import timedelta, timezone

import factory
from faker import Faker
from src.api.domain.models.tdm_prediction import TdmPrediction

from api.domain.models.tdm_prediction_point import TdmPredictionPoint
from tests.factories.satellite_factory import SatelliteFactory

faker = Faker()


class TdmPredictionFactory(factory.Factory):
    class Meta:
        model = TdmPrediction

    satellite = factory.SubFactory(SatelliteFactory)
    creation_date = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    time_range_start = factory.LazyAttribute(
        lambda o: o.creation_date + timedelta(hours=8)
    )
    time_range_end = factory.LazyAttribute(
        lambda o: o.time_range_start + timedelta(hours=26)
    )
    site_name = "LSST"
    reference_frame = "TEME"
    date_added = factory.LazyAttribute(lambda o: o.creation_date + timedelta(hours=2))
    track_id = factory.LazyFunction(lambda: faker.uuid4())
    folder_name = factory.LazyAttribute(
        lambda o: f"Aero_LOST_TLE_TDMs_{o.time_range_start.strftime('%Y-%m-%dT%H-%M')}"
    )


class TdmPredictionPointFactory(factory.Factory):
    class Meta:
        model = TdmPredictionPoint
        exclude = ["tdm_prediction"]

    tdm_prediction = factory.SubFactory(TdmPredictionFactory)
    tdm_prediction_id = factory.LazyAttribute(
        lambda o: getattr(o.tdm_prediction, "id", faker.random_int(min=1, max=99999))
    )
    timestamp = factory.LazyAttribute(
        lambda o: faker.date_time_between(
            start_date=o.tdm_prediction.time_range_start,
            end_date=o.tdm_prediction.time_range_end,
        ).replace(tzinfo=timezone.utc)
    )
    right_ascension = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=0, max_value=360
        )
    )
    declination = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=-90, max_value=90
        )
    )
    apparent_magnitude = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=-1, max_value=10
        )
    )
    satellite_number = factory.LazyFunction(
        lambda: faker.random_int(min=1, max=99999, step=1)
    )
    satellite_name = factory.LazyFunction(lambda: faker.word())
