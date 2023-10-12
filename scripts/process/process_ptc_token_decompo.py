"""
Script to aggregate the token decomposition data for TVL
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import DATA_PATH, PROCESSED_DATA_PATH

# iterate over the protocol list
# for ptc_slug in ["uniswap-v3", "aave-v2", "makerdao"]:
for ptc_slug in ["aave-v2"]:
    df_token = pd.DataFrame()
    # load the json file
    with open(
        f"{DATA_PATH}/defillama/tvl/{ptc_slug}.json", "r", encoding="utf-8"
    ) as target_file:
        llama_tvl_json = json.load(target_file)

    llama_tvl_df = pd.DataFrame(pd.DataFrame(llama_tvl_json["tokensInUsd"]))
    llama_tvl_df["date"] = pd.to_datetime(llama_tvl_df["date"], unit="s").dt.strftime(
        "%Y-%m-%d"
    )
    llama_tvl_df = llama_tvl_df.drop_duplicates(subset=["date"], keep="first")

    if "tvl" not in llama_tvl_json.keys() or len(llama_tvl_df) == 0:
        continue

    for _, row in tqdm(llama_tvl_df.iterrows(), total=len(llama_tvl_df)):
        for token, token_tvl_usd in row["tokens"].items():
            df_token = pd.concat(
                [
                    df_token,
                    pd.DataFrame(
                        {
                            "date": row["date"],
                            "token": token,
                            "token_tvl_usd": token_tvl_usd,
                        },
                        index=[0],
                    ),
                ]
            )
    # save the data
    df_token.to_csv(
        f"{PROCESSED_DATA_PATH}/defillama/defillama_token_decomp_{ptc_slug}.csv",
        index=False,
    )
