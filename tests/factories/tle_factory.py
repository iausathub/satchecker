import datetime
from datetime import timezone

import factory
from faker import Faker
from src.api.domain.models.tle import TLE

from tests.factories.satellite_factory import SatelliteFactory

faker = Faker()


def generate_tle_line1():
    # TLE line format: "1 <NoradNumber><Classification> <IntlDesig> <EpochYear><EpochDay> <FirstDerivativeMeanMotion> <SecondDerivativeMeanMotion> <BStarDragTerm> <EphemerisType> <ElementSetNumber><Checksum>"  # noqa: E501
    norad_number = faker.random_int(min=1, max=99999, step=1)
    classification = faker.random_element(elements=("U", "C", "S"))
    intl_desig = (
        f"{faker.random_int(00, 24):02d}"
        f"{faker.random_int(1, 100):02d}"
        f"{faker.random_element(elements=('A', 'B', 'C'))}"
    )
    epoch_year = faker.random_int(min=1998, max=2024, step=1)
    epoch_day = faker.random_int(min=1, max=365, step=1)
    first_derivative_mean_motion = (
        f"{faker.random.choice(['0', '1'])}"
        f"{faker.random_int(min=0, max=9999, step=1):08d}"
    )
    second_derivative_mean_motion = 00000 - 0
    b_star_drag_term = -11606 - 4
    ephemeris_type = faker.random_element(elements=("0", "1", "2"))
    element_set_number = faker.random_int(min=1, max=999, step=1)
    checksum = faker.random_int(min=0, max=9, step=1)

    tle_line1 = f"1 {norad_number:05d}{classification} {intl_desig} {epoch_year:04d}{epoch_day:03d} {first_derivative_mean_motion} {second_derivative_mean_motion:08d} {b_star_drag_term:08d} {ephemeris_type} {element_set_number:03d}{checksum:01d}"  # noqa: E501
    return tle_line1


def generate_tle_line2():
    # TLE line format: "2 <Checksum> <Epoch> <MeanMotion> <MeanMotionDot> <BStarDragTerm> <EphemerisType> <ElementSetNumber>"  # noqa: E501
    norad_number = faker.random_int(min=1, max=99999, step=1)
    inclination = faker.pyfloat(
        left_digits=None, right_digits=4, min_value=0, max_value=90
    )
    right_ascension = faker.pyfloat(
        left_digits=None, right_digits=4, min_value=0, max_value=360
    )
    eccentricity = faker.pyfloat(
        left_digits=None, right_digits=7, min_value=0, max_value=1
    )
    argument_of_perigee = faker.pyfloat(
        left_digits=None, right_digits=4, min_value=0, max_value=360
    )
    mean_anomaly = faker.pyfloat(
        left_digits=None, right_digits=4, min_value=0, max_value=360
    )
    mean_motion = faker.pyfloat(
        left_digits=None, right_digits=8, min_value=0, max_value=17
    )
    revolution_number = faker.random_int(min=0, max=99999)
    checksum = faker.random_int(min=0, max=9, step=1)

    tle_line2 = f"2 {norad_number:05d} {inclination} {right_ascension} {eccentricity} {argument_of_perigee} {mean_anomaly} {mean_motion}{revolution_number:05d} {checksum:01d}"  # noqa: E501
    return tle_line2


class TLEFactory(factory.Factory):
    class Meta:
        model = TLE

    satellite = factory.SubFactory(SatelliteFactory)
    date_collected = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    tle_line1 = factory.LazyFunction(generate_tle_line1)
    tle_line2 = factory.LazyFunction(generate_tle_line2)
    epoch = factory.LazyFunction(
        lambda: faker.date_time_between(
            start_date="-10y", end_date=datetime.datetime.now(timezone.utc)
        ).replace(tzinfo=timezone.utc)
    )
    is_supplemental = factory.LazyAttribute(lambda o: faker.boolean())
    data_source = factory.LazyFunction(
        lambda: faker.random_element(elements=("celestrak", "spacetrack"))
    )
