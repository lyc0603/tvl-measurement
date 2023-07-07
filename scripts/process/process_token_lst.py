"""
Script to process token category list
"""

import json

import numpy as np
import pandas as pd

from config.constants import DATA_PATH

CATE_DATA_INFO = {
    "cmc": {
        "gov_tokens": {
            "path": f"{DATA_PATH}/token_category/gov_tokens.json",
            "category": "Governance Tokens",
        },
        "wrapped_tokens": {
            "path": f"{DATA_PATH}/token_category/wrapped_tokens.json",
            "category": "Wrapped Tokens",
        },
        "layer_one_tokens": {
            "path": f"{DATA_PATH}/token_category/layer_one_tokens.json",
            "category": "Layer One Tokens",
        },
        "layer_two_tokens": {
            "path": f"{DATA_PATH}/token_category/layer_two_tokens.json",
            "category": "Layer Two Tokens",
        },
    },
    "defi_llama": {
        "stable_coins": {
            "path": f"{DATA_PATH}/token_category/stable_coins.json",
            "category": "Stablecoins",
        },
    },
}

NON_CRYPTO_BACKING_STABLECOINS_TYPE = [
    "fiat-backed",
    "algorithmic",
]

df_agg = {
    "name": [],
    "symbol": [],
    "token_address": [],
    "category": [],
    "stable_type": [],
}

for cate, cate_info in CATE_DATA_INFO["cmc"].items():
    # Load governance and wrapped tokens
    with open(cate_info["path"], "r", encoding="utf-8") as gov_file:
        target_tokens = json.load(gov_file)
    target_df = pd.DataFrame(target_tokens["data"]["cryptoCurrencyList"])
    target_df = target_df[["name", "symbol", "platform"]]

    # create category column
    target_df["category"] = cate_info["category"]

    # drop platform row with None
    target_df = target_df.dropna(subset=["platform"])

    # iterate through df
    for index, row in target_df.iterrows():
        if row["platform"]["name"] == "Ethereum":
            # append to df_agg
            df_agg["name"].append(row["name"])
            df_agg["symbol"].append(row["symbol"])
            df_agg["token_address"].append(row["platform"]["token_address"])
            df_agg["category"].append(row["category"])
            df_agg["stable_type"].append(np.nan)

with open(
    CATE_DATA_INFO["defi_llama"]["stable_coins"]["path"], "r", encoding="utf-8"
) as stable_file:
    stable_coins = json.load(stable_file)

stable_df = pd.DataFrame(stable_coins["peggedAssets"])

# isolate 'fiat-backed'and 'algorithmic' stablecoins
stable_df = stable_df[
    stable_df["pegMechanism"].isin(NON_CRYPTO_BACKING_STABLECOINS_TYPE)
].reset_index(drop=True)

# iterate through df
for index, row in stable_df.iterrows():
    # append to df_agg
    df_agg["name"].append(row["name"])
    df_agg["symbol"].append(row["symbol"])
    df_agg["token_address"].append(np.nan)
    df_agg["category"].append(CATE_DATA_INFO["defi_llama"]["stable_coins"]["category"])
    df_agg["stable_type"].append(row["pegMechanism"])

# create df
df_token_cate = pd.DataFrame(df_agg)
