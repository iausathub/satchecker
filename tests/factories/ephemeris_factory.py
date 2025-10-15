import datetime
from datetime import timezone

import factory
import numpy as np
from faker import Faker

from api.domain.models.interpolable_ephemeris import (
    EphemerisPoint,
    InterpolableEphemeris,
)

faker = Faker()


def generate_covariance_matrix():
    matrix = np.random.rand(6, 6)
    matrix = matrix @ matrix.T
    return matrix


def generate_ephemeris_point(timestamp):
    # Generate random position and velocity vectors
    position = np.array(
        [
            faker.pyfloat(min_value=-10000, max_value=10000),
            faker.pyfloat(min_value=-10000, max_value=10000),
            faker.pyfloat(min_value=-10000, max_value=10000),
        ]
    )

    velocity = np.array(
        [
            faker.pyfloat(min_value=-10, max_value=10),
            faker.pyfloat(min_value=-10, max_value=10),
            faker.pyfloat(min_value=-10, max_value=10),
        ]
    )

    covariance = generate_covariance_matrix()

    return EphemerisPoint(
        timestamp=timestamp, position=position, velocity=velocity, covariance=covariance
    )


class InterpolableEphemerisFactory(factory.Factory):
    class Meta:
        model = InterpolableEphemeris

    id = factory.LazyFunction(lambda: faker.random_int(min=1, max=10000))
    satellite = factory.LazyFunction(lambda: faker.random_int(min=1, max=10000))
    generated_at = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    data_source = factory.LazyFunction(
        lambda: faker.random_element(
            elements=(
                "other",
                "spacetrack",
            )
        )
    )
    frame = factory.LazyFunction(
        lambda: faker.random_element(elements=("UVW", "ECI", "ECEF"))
    )
    file_reference = factory.LazyFunction(lambda: faker.uuid4())
    date_collected = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    ephemeris_start = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    ephemeris_stop = factory.LazyAttribute(
        lambda o: o.ephemeris_start + datetime.timedelta(days=3)
    )
    points = factory.List([])

    @factory.post_generation
    def _generate_points(self, create, extracted, **kwargs):
        if not create:
            return

        # Generate a random number of points between 10 and 100
        num_points = faker.random_int(min=10, max=100)

        # Generate points at regular intervals
        time_step = (self.ephemeris_stop - self.ephemeris_start) / num_points
        self.points = [
            generate_ephemeris_point(self.ephemeris_start + i * time_step)
            for i in range(num_points)
        ]
