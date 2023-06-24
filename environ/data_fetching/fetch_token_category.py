"""
Functions to fetch data from CoinMarketCap by category
"""


import json

import requests


def fetch_cate_data(url: str) -> dict:
    """
    Function to fetch governance tokens from CoinMarketCap
    """

    # Fetch data from CoinMarketCap
    data_json = requests.get(url=url, timeout=120).json()

    return data_json


def save_json(data_json: dict, save_path: str) -> None:
    """
    Function to save json data
    """

    with open(save_path, "w", encoding="utf-8") as target_file:
        json.dump(data_json, target_file, indent=4)
