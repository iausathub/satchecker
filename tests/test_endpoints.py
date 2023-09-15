import pytest
import datetime
import api.core
import api.core.database.models

def test_get_ephemeris_by_name(client, mocker):
    mocker.patch.object(api.core.routes,"get_recent_TLE", return_value=get_mock_TLE())
    response = client.get("/ephemeris/name/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167")
   
    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert data[0]['ALTITUDE-DEG'] == -8.16137402215
    assert data[0]['AZIMUTH-DEG'] == 306.59130150861
    assert data[0]['DDEC-DEG_PER_SEC'] == 0.00471072904
    assert data[0]['DECLINATION-DEG'] == 25.04591441092
    assert data[0]['DRA_COSDEC-DEG_PER_SEC'] == 0.05809617341
    assert data[0]['ILLUMINATED'] == True
    assert data[0]['JULIAN_DATE'] == 2460193.104167
    assert data[0]['NAME'] == 'ISS (ZARYA)'
    assert data[0]['PHASE_ANGLE-DEG'] == 33.59995261255
    assert data[0]['RANGE-KM'] == 3426.649224172898
    assert data[0]['RANGE_RATE-KM_PER_SEC'] == -6.597948905187
    assert data[0]['RIGHT_ASCENSION-DEG'] == 333.08094588626
    assert data[0]['TLE-DATE'] == '2023-09-05 16:21:29'

def test_get_ephemeris_by_name_jdstep(client, mocker):
    mocker.patch.object(api.core.routes,"get_recent_TLE", return_value=get_mock_TLE())
    response = client.get("/ephemeris/namejdstep/?name=ISS%20(ZARYA)&elevation=150&latitude=32&longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1")
   
    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert data[0]['ALTITUDE-DEG'] == -22.16343307904
    assert data[0]['AZIMUTH-DEG'] == 313.30708204802
    assert data[0]['DDEC-DEG_PER_SEC'] == 0.02061734218
    assert data[0]['DECLINATION-DEG'] == 19.71059982444
    assert data[0]['DRA_COSDEC-DEG_PER_SEC'] == 0.03480327715
    assert data[0]['ILLUMINATED'] == True
    assert data[0]['JULIAN_DATE'] == 2460193.1
    assert data[0]['NAME'] == 'ISS (ZARYA)'
    assert data[0]['PHASE_ANGLE-DEG'] == 38.23308559305
    assert data[0]['RANGE-KM'] == 5773.187963839149
    assert data[0]['RANGE_RATE-KM_PER_SEC'] == -6.337586503698
    assert data[0]['RIGHT_ASCENSION-DEG'] == 315.91572204924
    assert data[0]['TLE-DATE'] == '2023-09-05 16:21:29'

    assert data[1]['ALTITUDE-DEG'] == -59.87503033798
    assert data[1]['AZIMUTH-DEG'] == 129.21859963133
    assert data[1]['DDEC-DEG_PER_SEC'] == 0.02919672877
    assert data[1]['DECLINATION-DEG'] == -46.67552227562
    assert data[1]['DRA_COSDEC-DEG_PER_SEC'] == 0.02033564678
    assert data[1]['ILLUMINATED'] == True
    assert data[1]['JULIAN_DATE'] == 2460193.2
    assert data[1]['NAME'] == 'ISS (ZARYA)'
    assert data[1]['PHASE_ANGLE-DEG'] == 72.93173570671
    assert data[1]['RANGE-KM'] == 11500.17459762438
    assert data[1]['RANGE_RATE-KM_PER_SEC'] == 2.699116660657
    assert data[1]['RIGHT_ASCENSION-DEG'] == 271.57445320308
    assert data[1]['TLE-DATE'] == '2023-09-05 16:21:29'

def test_get_ephemeris_by_catalog_number(client, mocker):
    mocker.patch.object(api.core.routes,"get_recent_TLE", return_value=get_mock_TLE())
    response = client.get("/ephemeris/catalog-number/?catalog=25544&elevation=150&latitude=32&longitude=-110&julian_date=2460193.104167")
   
    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert data[0]['ALTITUDE-DEG'] == -8.16137402215
    assert data[0]['AZIMUTH-DEG'] == 306.59130150861
    assert data[0]['DDEC-DEG_PER_SEC'] == 0.00471072904
    assert data[0]['DECLINATION-DEG'] == 25.04591441092
    assert data[0]['DRA_COSDEC-DEG_PER_SEC'] == 0.05809617341
    assert data[0]['ILLUMINATED'] == True
    assert data[0]['JULIAN_DATE'] == 2460193.104167
    assert data[0]['NAME'] == 'ISS (ZARYA)'
    assert data[0]['PHASE_ANGLE-DEG'] == 33.59995261255
    assert data[0]['RANGE-KM'] == 3426.649224172898
    assert data[0]['RANGE_RATE-KM_PER_SEC'] == -6.597948905187
    assert data[0]['RIGHT_ASCENSION-DEG'] == 333.08094588626
    assert data[0]['TLE-DATE'] == '2023-09-05 16:21:29'

def test_get_ephemeris_by_catalog_number_jdstep(client, mocker):
    mocker.patch.object(api.core.routes,"get_recent_TLE", return_value=get_mock_TLE())
    response = client.get("/ephemeris/catalog-number-jdstep/?catalog=25544&elevation=150&latitude=32&longitude=-110&startjd=2460193.1&stopjd=2460193.2&stepjd=0.1")
   
    # Check that the response was returned without error
    assert response.status_code == 200

    # Check that the response was correct
    data = response.json
    assert data[0]['ALTITUDE-DEG'] == -22.16343307904
    assert data[0]['AZIMUTH-DEG'] == 313.30708204802
    assert data[0]['DDEC-DEG_PER_SEC'] == 0.02061734218
    assert data[0]['DECLINATION-DEG'] == 19.71059982444
    assert data[0]['DRA_COSDEC-DEG_PER_SEC'] == 0.03480327715
    assert data[0]['ILLUMINATED'] == True
    assert data[0]['JULIAN_DATE'] == 2460193.1
    assert data[0]['NAME'] == 'ISS (ZARYA)'
    assert data[0]['PHASE_ANGLE-DEG'] == 38.23308559305
    assert data[0]['RANGE-KM'] == 5773.187963839149
    assert data[0]['RANGE_RATE-KM_PER_SEC'] == -6.337586503698
    assert data[0]['RIGHT_ASCENSION-DEG'] == 315.91572204924
    assert data[0]['TLE-DATE'] == '2023-09-05 16:21:29'

    assert data[1]['ALTITUDE-DEG'] == -59.87503033798
    assert data[1]['AZIMUTH-DEG'] == 129.21859963133
    assert data[1]['DDEC-DEG_PER_SEC'] == 0.02919672877
    assert data[1]['DECLINATION-DEG'] == -46.67552227562
    assert data[1]['DRA_COSDEC-DEG_PER_SEC'] == 0.02033564678
    assert data[1]['ILLUMINATED'] == True
    assert data[1]['JULIAN_DATE'] == 2460193.2
    assert data[1]['NAME'] == 'ISS (ZARYA)'
    assert data[1]['PHASE_ANGLE-DEG'] == 72.93173570671
    assert data[1]['RANGE-KM'] == 11500.17459762438
    assert data[1]['RANGE_RATE-KM_PER_SEC'] == 2.699116660657
    assert data[1]['RIGHT_ASCENSION-DEG'] == 271.57445320308
    assert data[1]['TLE-DATE'] == '2023-09-05 16:21:29'

def get_mock_TLE():
    tleLine1 = "1 25544U 98067A   23248.54842295  .00012769  00000+0  22936-3 0  9997"
    tleLine2 = "2 25544  51.6416 290.4299 0005730  30.7454 132.9751 15.50238117414255"
    date_collected = datetime.datetime(2023,9,5,16,21,29)
    sat_name = "ISS (ZARYA)"

    return (tleLine1, tleLine2, date_collected, sat_name)