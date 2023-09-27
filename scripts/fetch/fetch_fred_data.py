"""
Script to fetch the money supply data from FRED
"""

import json
import os

from config.constants import DATA_PATH, FRED_DICT
from environ.data_fetching.fetch_fred import fetch_fred_data

# check if the fred folder exists
if not os.path.exists(f"{DATA_PATH}/fred"):
    os.mkdir(f"{DATA_PATH}/fred")

for series_type, series_name in FRED_DICT.items():
    # fetch the data
    data = fetch_fred_data(series_type=series_type)

    # save the data
    with open(f"{DATA_PATH}/fred/{series_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
