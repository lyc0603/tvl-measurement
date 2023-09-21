"""
Function to fetch data from FRED
"""

import requests

from config.constants import FRED_API_KEY


def fetch_fred_data(series_type: str = "BOGMBASE") -> dict:
    """
    Function to fetch data from FRED
    """
    return requests.get(
        f"https://api.stlouisfed.org/fred/series/observations?\
series_id={series_type}&api_key={FRED_API_KEY}&file_type=json",
        timeout=60,
    ).json()


if __name__ == "__main__":
    print(fetch_fred_data())
