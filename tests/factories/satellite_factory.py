import datetime
import random

import factory
from faker import Faker
from src.api.domain.models.satellite import Satellite

faker = Faker()

# List of valid satellite constellations from validation_service.py
CONSTELLATIONS = ["starlink", "oneweb", "kuiper", "planet", "ast"]


def generate_object_id():
    year = faker.random_int(min=1957, max=datetime.datetime.now().year)
    launch_num = str(faker.random_int(min=1, max=999)).zfill(3)
    piece = faker.random_element(elements=tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return f"{year}-{launch_num}{piece}"


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
    )
    decay_date = faker.date_time_between(
        start_date="-10y", end_date=datetime.datetime.now()
    )

    object_id = factory.LazyFunction(generate_object_id)
    object_type = faker.word()
    has_current_sat_number = factory.LazyAttribute(lambda o: True)
