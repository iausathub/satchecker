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
    info = requests.get(
        f"https://cps.iau.org/tools/satchecker/api/ephemeris/name-jdstep/?name={satellite}&elevation={observer_elevation}&latitude={observer_latitude}&longitude={observer_longitude}&startjd={start_jd}&stopjd={stop_jd}&stepjd={step_jd}&min_altitude=-90",
        timeout=10,
    )
    visible = False
    for point in info.json():
        if point["ALTITUDE-DEG"] > 0:
            visible_satellites.append(point)
            visible = True

        if not visible:
            not_visible_satellites.append(satellite)
            visible = False
print("\n")
print("Visible Satellites: ")
for satellite in visible_satellites:
    print(satellite["NAME"])
    print("Altitude (degrees): ", satellite["ALTITUDE-DEG"])
    print("Azimuth (degrees): ", satellite["AZIMUTH-DEG"])
    print("Time: ", satellite["JULIAN_DATE"])
    print("--------------------------------------")

print("\n\n")

print("Not Currently Visible: ")
for satellite in not_visible_satellites:
    print("Name: ", satellite)
    print("-------------------------")
