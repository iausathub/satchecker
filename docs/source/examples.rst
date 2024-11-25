API Examples
=============

Here are a few examples of how to use the API:


**Get all visible passes of STARLINK-1600 at a given location for the specified time range:**
https://satchecker.cps.iau.org/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460010.1&stepjd=0.5

**Get any passes (visible or not) of STARLINK-1600 at a given location for the specified time range:**
https://satchecker.cps.iau.org/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1&min_altitude=-90

**Attempt to get visible passes STARLINK-1600 at a given location for the specified time range, with no results:**
https://satchecker.cps.iau.org/ephemeris/name-jdstep/?name=STARLINK-1600&latitude=40.1106&longitude=-88.2073&elevation=222&startjd=2460000.1&stopjd=2460000.3&stepjd=0.1

--------------------------

**Get all TLEs for active objects at the current epoch:**

.. code-block:: python

    from datetime import datetime, timezone
    import pandas as pd
    import requests

    def get_tles_at_epoch(base_url, epoch_date=None, page=1, per_page=100):
        url = f"{base_url}/tools/tles-at-epoch/"
        params = {
            "epoch": epoch_date,
            "page": page,
            "per_page": per_page
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_all_tles(base_url, epoch_date=None, data_source="spacetrack"):
        all_tles = []
        page = 1
        per_page = 100

        while True:
            results = get_tles_at_epoch(base_url, epoch_date, page, per_page)
            tles = results[0]["data"]
            all_tles.extend(tles)
            if len(tles) < per_page:
                break
            page += 1

        return all_tles

    if __name__ == "__main__":
        base_url = "https://satchecker.cps.iau.org"

        # This will give the current TLE set, use a specific epoch (in Julian date format) if needed
        # epoch_date = 2460606
        all_tles = fetch_all_tles(base_url""", epoch_date=epoch_date """)

        # Create a DataFrame from the TLE data
        df = pd.DataFrame(all_tles)
        print(df.columns)
        print(df.head())
        print(df.shape[0])
