"""
Function to fetch governance tokens from CoinMarketCap
"""

import os
import time
from tqdm import tqdm

from config.constants import (
    CMC_GOV,
    CMC_LAYER_ONE,
    CMC_LAYER_TWO,
    CMC_WRAPPED,
    DATA_PATH,
    LLAMA_STABLE,
)
from environ.data_fetching.fetch_token_category import fetch_cate_data, save_json

# check if the data folder exists
if not os.path.exists(f"{DATA_PATH}/token_category"):
    os.makedirs(f"{DATA_PATH}/token_category")


ITER_DICT = {
    CMC_GOV: f"{DATA_PATH}/token_category/gov_tokens.json",
    CMC_WRAPPED: f"{DATA_PATH}/token_category/wrapped_tokens.json",
    LLAMA_STABLE: f"{DATA_PATH}/token_category/stable_coins.json",
    CMC_LAYER_ONE: f"{DATA_PATH}/token_category/layer_one_tokens.json",
    CMC_LAYER_TWO: f"{DATA_PATH}/token_category/layer_two_tokens.json",
}

for url, path in tqdm(ITER_DICT.items()):
    time.sleep(3)
    data_json = fetch_cate_data(url=url)
    save_json(data_json=data_json, save_path=path)
