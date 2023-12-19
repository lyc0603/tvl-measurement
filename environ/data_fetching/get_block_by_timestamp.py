"""
Functions to get the block by timestamp
"""

from datetime import datetime
from typing import Iterable, Optional

import pandas as pd
import requests


def get_block_by_timestamp(target_block: int) -> Optional[int]:
    """
    Function to get the block by timestamp
    """

    length = 0
    result = {"timestamp": None, "height": None}

    while length == 0:
        result = requests.get(
            f"https://coins.llama.fi/block/ethereum/{target_block}", timeout=60
        ).json()
        length = len(result)

    return result["height"]


def get_blocks_by_timestamps(start_date: str, end_date: str) -> Iterable:
    """
    Function to get the blocks by timestamps
    """

    timestamp_list = get_date_range(start_date, end_date)

    for timestamp in timestamp_list:
        yield (unix_to_timestamp(timestamp), get_block_by_timestamp(timestamp))


def timestamp_to_unix(timestamp: str) -> int:
    """
    Function to convert timestamp to unix
    """

    return int(datetime.strptime(timestamp, "%Y-%m-%d").timestamp())


def unix_to_timestamp(unix: int) -> str:
    """
    Function to convert unix to timestamp
    """

    return datetime.fromtimestamp(unix).strftime("%Y-%m-%d")


def get_date_range(start_date: str, end_date: str):
    """
    Function to get the date range
    """

    return [
        timestamp_to_unix(_)
        for _ in pd.date_range(start=start_date, end=end_date, freq="D").strftime(
            "%Y-%m-%d"
        )
    ]
