import datetime
import random
from datetime import timezone

import factory
from faker import Faker

from api.domain.models.satellite import Satellite

faker = Faker()

# List of valid satellite constellations from validation_service.py
CONSTELLATIONS = ["starlink", "oneweb", "kuiper", "planet", "ast"]


class SatelliteFactory(factory.Factory):
    class Meta:
        model = Satellite

    sat_number = factory.Sequence(lambda n: n)
    sat_name = factory.LazyFunction(faker.word)
    constellation = factory.LazyFunction(
        lambda: random.choice(CONSTELLATIONS)  # noqa: S311
    )
    rcs_size = faker.word()
    launch_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    ).replace(tzinfo=timezone.utc)
    decay_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    ).replace(tzinfo=timezone.utc)
    object_id = faker.word()
    object_type = faker.word()
    has_current_sat_number = factory.LazyAttribute(lambda o: True)
