import datetime
import random
from datetime import timezone

import factory
from faker import Faker
from src.api.domain.models.satellite import Satellite

from api.domain.models.satellite_designation import SatelliteDesignation

faker = Faker()

# List of valid satellite constellations from validation_service.py
CONSTELLATIONS = ["starlink", "oneweb", "kuiper", "planet", "ast"]

_object_id_counter = 0


class SatelliteDesignationFactory(factory.Factory):
    class Meta:
        model = SatelliteDesignation

    sat_number = factory.Sequence(lambda n: n)
    sat_name = factory.LazyFunction(faker.word)
    valid_from = datetime.datetime(1957, 1, 1, tzinfo=timezone.utc)
    valid_to = None


class SatelliteFactory(factory.Factory):
    class Meta:
        model = Satellite

    constellation = factory.LazyFunction(
        lambda: random.choice(CONSTELLATIONS)  # noqa: S311
    )
    rcs_size = faker.word()
    launch_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    )
    decay_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    )

    @factory.lazy_attribute
    def object_id(self):
        global _object_id_counter
        _object_id_counter += 1
        return f"test_object_{_object_id_counter}"

    object_type = faker.word()
    generation = factory.LazyFunction(
        lambda: random.choice(["v1", "v2", "v3"])  # noqa: S311
    )
    designations = factory.LazyFunction(lambda: [SatelliteDesignationFactory()])
