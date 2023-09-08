"""
Script to fetch data from defiexplore.com
"""

import os
import time
import json

from config.constants import DATA_PATH
from environ.data_fetching.fetch_defiexplore import (
    fetch_defiexplore_data,
    get_defiexplore_page_number,
)

# check whether the data folder exists
if not os.path.exists(f"{DATA_PATH}/defiexplore"):
    os.makedirs(f"{DATA_PATH}/defiexplore")


idx = 1427
data_len = 1

while data_len > 0:
    time.sleep(1)

    print(f"Fetching defiexplore data: {idx}")

    response_json = fetch_defiexplore_data(page_num=idx)
    data_len = len(response_json["data"])
    idx = get_defiexplore_page_number(response=response_json)

    with open(f"{DATA_PATH}/defiexplore/{idx}.json", "w", encoding="utf-8") as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)

    idx = get_defiexplore_page_number(response=response_json) + 1
