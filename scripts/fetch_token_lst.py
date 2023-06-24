"""
Function to fetch governance tokens from CoinMarketCap
"""

import os
from config.constants import CMC_GOV, CMC_WRAPPED, LLAMA_STABLE, DATA_PATH
from environ.data_fetching.fetch_token_category import fetch_cate_data, save_json

# check if the data folder exists
if not os.path.exists(f"{DATA_PATH}/token_category"):
    os.makedirs(f"{DATA_PATH}/token_category")

# Fetch governance tokens from CoinMarketCap
gov_data_json = fetch_cate_data(url=CMC_GOV)
save_json(
    data_json=gov_data_json, save_path=f"{DATA_PATH}/token_category/gov_tokens.json"
)

# Fetch wrapped tokens from CoinMarketCap
wrapped_data_json = fetch_cate_data(url=CMC_WRAPPED)
save_json(
    data_json=wrapped_data_json,
    save_path=f"{DATA_PATH}/token_category/wrapped_tokens.json",
)

# Fetch stable coins from Llama
stable_data_json = fetch_cate_data(url=LLAMA_STABLE)
save_json(
    data_json=stable_data_json,
    save_path=f"{DATA_PATH}/token_category/stable_coins.json",
)
