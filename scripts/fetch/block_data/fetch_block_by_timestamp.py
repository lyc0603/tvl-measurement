"""
Script to fetch block data by timestamp
"""

import csv
import os

from eth_tools.utils import smart_open
from tqdm import tqdm

from config.constants import DATA_PATH
from environ.data_fetching.get_block_by_timestamp import get_blocks_by_timestamps

OUTPUT_PATH = f"{DATA_PATH}/block/"

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

with smart_open(f"{OUTPUT_PATH}/block.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp", "block"])
    writer.writeheader()
    for timestamp, block in tqdm(get_blocks_by_timestamps("2018-07-01", "2023-11-29")):
        writer.writerow({"timestamp": timestamp, "block": block})
