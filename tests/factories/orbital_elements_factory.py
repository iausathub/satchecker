import datetime
from datetime import timezone

import factory
from faker import Faker

from api.domain.models.orbital_elements import OrbitalElements
from tests.factories.satellite_factory import SatelliteFactory

faker = Faker()


class OrbitalElementsFactory(factory.Factory):
    class Meta:
        model = OrbitalElements

    satellite = factory.SubFactory(SatelliteFactory)
    date_collected = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    # U for unclassified, C for celestrak supplemental data
    classification_type = factory.LazyFunction(
        lambda: faker.random_element(elements=("U", "C"))
    )

    epoch = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    data_source = factory.LazyFunction(
        lambda: faker.random_element(elements=("celestrak", "spacetrack"))
    )
    inclination = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=0, max_value=90
        )
    )
    ra_of_ascending_node = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=0, max_value=360
        )
    )
    eccentricity = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=7, min_value=0, max_value=1
        )
    )
    arg_of_pericenter = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=0, max_value=360
        )
    )
    mean_anomaly = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=4, min_value=0, max_value=360
        )
    )
    mean_motion = factory.LazyFunction(
        lambda: faker.pyfloat(
            left_digits=None, right_digits=8, min_value=0, max_value=17
        )
    )
    rev_at_epoch = factory.LazyFunction(lambda: faker.random_int(min=0, max=99999))
    ephemeris_type = factory.LazyFunction(
        lambda: int(faker.random_element(elements=("0", "1", "2")))
    )
    element_set_no = factory.LazyFunction(
        lambda: faker.random_int(min=1, max=999, step=1)
    )
    mean_motion_dot = factory.LazyFunction(
        lambda: float(f"0.{faker.random_int(min=0, max=9999, step=1):08d}")
    )
    mean_motion_ddot = factory.LazyFunction(lambda: 00000 - 0)
    bstar = factory.LazyFunction(lambda: -11606 - 4)
