"""
Script to process the Llama TVL dataset to get aggregate tvl data for plotting.
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import CHAIN_LIST, DATA_PATH, PROCESSED_DATA_PATH
from environ.data_processing.process_llama_tvl import process_llama_tvls

for chain in CHAIN_LIST:
    # process the protocol list
    with open(
        f"{DATA_PATH}/defillama/protocol_lst.json", "r", encoding="utf-8"
    ) as target_file:
        protocol_lst = json.load(target_file)

    # extract the protocol slugs
    LLAMA_SLUG_LIST = [protocol["slug"] for protocol in protocol_lst]

    # a dataframe to store the tvl data
    df_all_tvl = pd.DataFrame()
    df_all_tvr = pd.DataFrame()

    # iterate over the protocol list
    for ptc_slug in tqdm(LLAMA_SLUG_LIST, desc=f"Processing protocols in {chain}"):
        try:
            # load the json file
            with open(
                f"{DATA_PATH}/defillama/tvl/{ptc_slug}.json", "r", encoding="utf-8"
            ) as target_file:
                data_json = json.load(target_file)

            tvr_dict, df_tvl = process_llama_tvls(
                llama_tvl_json=data_json,
                slug=ptc_slug,
                chain=chain,
            )

            # process the data
            df_tvr = pd.DataFrame(tvr_dict)

            # append the data to df_all_tvl
            df_all_tvr = pd.concat([df_all_tvr, df_tvr])
            df_all_tvl = pd.concat([df_all_tvl, df_tvl])
        except:  # pylint: disable=bare-except
            print(f"Failed to process {ptc_slug}.")

    # save the data
    df_all_tvl.to_csv(
        f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all_{chain}.csv", index=False
    )
    df_all_tvr.to_csv(
        f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv", index=False
    )
