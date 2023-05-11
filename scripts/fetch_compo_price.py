"""
Script to fetch the price of the flows
"""

import json
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

from config.constants import PROCESSED_DATA_PATH
from environ.data_fetching.token_price import get_token_price_defillama

# load the flow data
with open(
    f"{PROCESSED_DATA_PATH}/token_flow/defi_flow.json", "r", encoding="utf-8"
) as f_json:
    flow_dict = json.load(f_json)

# convert the json to dataframe
flow_df = pd.DataFrame(flow_dict)

# get the unique list of tokens
token_lst = flow_df["contract"].unique().tolist()

# iterate through the token list
for token in tqdm(token_lst):
    # sleep for 1 second
    time.sleep(1)

    try:
        # get the price of the token
        price = get_token_price_defillama(token)
    except:  # pylint: disable=W0702
        # if the token is not found, set the price to 0
        price = np.nan

    # set the price of the token
    flow_df.loc[flow_df["contract"] == token, "price"] = price

    # calculate the flow in USD
    flow_df.loc[flow_df["contract"] == token, "flow_usd"] = (
        flow_df.loc[flow_df["contract"] == token, "amount"] * price
    )

# save the flow data
flow_df.to_csv(f"{PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv", index=False)
