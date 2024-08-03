import datetime

import factory
from faker import Faker

from src.api.domain.models.satellite import Satellite

faker = Faker()


class SatelliteFactory(factory.Factory):
    class Meta:
        model = Satellite

    sat_number = factory.Sequence(lambda n: n)
    sat_name = faker.word()
    constellation = faker.word()
    rcs_size = faker.word()
    launch_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    )
    decay_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    )
    object_id = faker.word()
    object_type = faker.word()
    has_current_sat_number = factory.LazyAttribute(lambda o: True)
