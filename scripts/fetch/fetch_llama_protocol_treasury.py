"""
Script to fetch treasury from DeFiLlama
"""

import json
import os
import time

from tqdm import tqdm

from config.constants import DATA_PATH, LLAMA_SLUG_LIST
from environ.data_fetching.fetch_llama_tvl import (
    fetch_llama_protocol_lst,
    fetch_llama_tvl,
)

# check whether the protocol list exists
if not os.path.exists(f"{DATA_PATH}/defillama/protocol_lst.json"):
    # load the protocol list
    fetch_llama_protocol_lst(save_path=f"{DATA_PATH}defillama/protocol_lst.json")

# process the protocol list
with open(
    f"{DATA_PATH}/defillama/protocol_lst.json", "r", encoding="utf-8"
) as target_file:
    protocol_lst = json.load(target_file)

# extract the protocol slugs
LLAMA_SLUG_LIST = [protocol["slug"] for protocol in protocol_lst]

# get the file in the tvl folder
tvl_file_list = os.listdir(f"{DATA_PATH}/defillama/tvl")

# extract the protocol slugs
tvl_slug_list = [file_name.split(".")[0] for file_name in tvl_file_list]

# remove the protocol slugs that have been fetched
LLAMA_SLUG_LIST = list(set(LLAMA_SLUG_LIST) - set(tvl_slug_list))

# iterate over the protocol list
for ptc_slug in tqdm(LLAMA_SLUG_LIST):
    try:
        # fetch the tvl data
        fetch_llama_treasury(ptc_slug=ptc_slug)
    except:  # pylint: disable=bare-except
        time.sleep(10)
        print(f"Failed to fetch {ptc_slug}.")
