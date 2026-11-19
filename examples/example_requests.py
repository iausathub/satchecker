# This is an example of how to use the API with the python requests library

import requests

# .25 is 6 hours
start_jd = 2460208.5
stop_jd = 2460209.75

# .05 is 1.2 hours
step_jd = 0.05

observer_latitude = 32
observer_longitude = -110
observer_elevation = 0


satellite_list = [
    "STARLINK-30109",
    "STARLINK-30407",
    "STARLINK-30408",
    "STARLINK-30377",
    "STARLINK-30422",
    "STARLINK-30402",
    "STARLINK-30411",
    "STARLINK-30418",
]

visible_satellites = []
not_visible_satellites = []

for satellite in satellite_list:
    response = requests.get(
        f"https://satchecker.cps.iau.org/ephemeris/name-jdstep/?name={satellite}&elevation={observer_elevation}&latitude={observer_latitude}&longitude={observer_longitude}&startjd={start_jd}&stopjd={stop_jd}&stepjd={step_jd}&min_altitude=-90",
        timeout=10,
    )
    body = response.json()
    # the API reports each row as a plain list alongside a "fields" list
    # naming each column, rather than one dict per point -- zip them back
    # together so the lookups below can use the field names directly.
    points = [dict(zip(body["fields"], row, strict=True)) for row in body["data"]]

    visible = False
    for point in points:
        if point["altitude_deg"] > 0:
            visible_satellites.append(point)
            visible = True

        if not visible:
            not_visible_satellites.append(satellite)
            visible = False
print("\n")
print("Visible Satellites: ")
for satellite in visible_satellites:
    print(satellite["name"])
    print("Altitude (degrees): ", satellite["altitude_deg"])
    print("Azimuth (degrees): ", satellite["azimuth_deg"])
    print("Time: ", satellite["julian_date"])
    print("--------------------------------------")

print("\n\n")

print("Not Currently Visible: ")
for satellite in not_visible_satellites:
    print("Name: ", satellite)
    print("-------------------------")
