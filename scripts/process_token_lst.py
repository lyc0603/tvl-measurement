"""
Script to process token category list
"""

import json

import numpy as np
import pandas as pd

from config.constants import DATA_PATH, NON_CRYPTO_BACKING_STABLECOINS

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
    }
}

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
        gov_tokens = json.load(gov_file)
    target_df = pd.DataFrame(gov_tokens["data"]["cryptoCurrencyList"])
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

# iterate through NON_CRYPTO_BACKING_STABLECOINS
for token in NON_CRYPTO_BACKING_STABLECOINS:
    # append to df_agg
    df_agg["name"].append(token["Name"])
    df_agg["symbol"].append(token["Symbol"])
    df_agg["token_address"].append(token["Contract"])
    df_agg["category"].append("Stablecoins")
    df_agg["stable_type"].append(token["Category"])

# create df
df_token_cate = pd.DataFrame(df_agg)
