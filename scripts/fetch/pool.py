"""
Script to fetch Aave Pool data
"""

import os

from eth_tools.event_fetcher import EventFetcher, FetchTask

from config.constants import (
    ADAI_V2,
    ABI_PATH,
    DATA_PATH,
    END_OF_SAMPLE_PERIOD_BLOCK,
)
from environ.data_fetching.web3_call import eth_w3

# check whether the aave data folder exists
if not os.path.exists(f"{DATA_PATH}/aave"):
    os.makedirs(f"{DATA_PATH}/aave")

fetcher = EventFetcher(eth_w3)
task = FetchTask.from_dict(
    {
        "address": ADAI_V2,
        "abi": f"{ABI_PATH}/{ADAI_V2}.json",
        "start_block": 11367200,
        "end_block": END_OF_SAMPLE_PERIOD_BLOCK,
    }
)
fetcher.fetch_and_persist_events(task, f"{DATA_PATH}/aave/aDAI.jsonl.gz")
