"""
Script to process the Llama TVL dataset for each protocol.
"""

import json

from tqdm import tqdm

from config.constants import (
    DATA_PATH,
    LLAMA_SLUG_LIST,
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
)
from environ.data_processing.process_llama_tvl import process_llama_tvl

# iterate over the protocol list
for ptc_slug in tqdm(LLAMA_SLUG_LIST):
    # load the json file
    with open(
        f"{DATA_PATH}/defillama/tvl/{ptc_slug}.json", "r", encoding="utf-8"
    ) as target_file:
        data_json = json.load(target_file)

    # process the data
    process_llama_tvl(
        llama_tvl_json=data_json,
        save_path=f"{PROCESSED_DATA_PATH}/defillama/tvr/{ptc_slug}.csv",
        fig_path=f"{FIGURES_PATH}/tvr_{ptc_slug}.pdf",
    )
