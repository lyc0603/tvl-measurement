"""
Script to fetch the price of the flows
"""

import json

import numpy as np
import pandas as pd
from tqdm import tqdm

from config.constants import BALANCER_AAVE_V3_BOOSTED_POOL, PROCESSED_DATA_PATH
from environ.data_fetching.balancer_data_fetching import (
    get_receipt_tokens_and_composition,
)
from environ.data_fetching.token_price import (
    get_derivative_simple_price,
    get_derivative_square_price,
    get_token_price_defillama,
)

# load the flow data
with open(
    f"{PROCESSED_DATA_PATH}/token_flow/defi_flow.json", "r", encoding="utf-8"
) as f_json:
    flow_dict = json.load(f_json)

# convert the json to dataframe
flow_df = pd.DataFrame(flow_dict)

# get the unique list of tokens
token_lst = flow_df["contract"].unique().tolist()

# get balancer data
(
    receipt_token_to_total_supply,
    receipt_token_to_composition,
) = get_receipt_tokens_and_composition()

# iterate through the token list
for token in tqdm(token_lst):
    print(token)
    try:
        # get the price of the token
        price = get_token_price_defillama(token)
    except:  # pylint: disable=W0702
        # if the token is not in defillama, then it is a derivative in balancer
        if token in BALANCER_AAVE_V3_BOOSTED_POOL["derivative_square"].keys():
            price = get_derivative_square_price(
                token, receipt_token_to_total_supply, receipt_token_to_composition
            )

        elif token in BALANCER_AAVE_V3_BOOSTED_POOL["derivative_simple"]:
            price = get_derivative_simple_price(
                token, receipt_token_to_total_supply, receipt_token_to_composition
            )

        else:
            price = np.nan
    else:
        pass

    # set the price of the token
    flow_df.loc[flow_df["contract"] == token, "price"] = price

    # calculate the flow in USD
    flow_df.loc[flow_df["contract"] == token, "flow_usd"] = (
        flow_df.loc[flow_df["contract"] == token, "amount"] * price
    )

# save the flow data
flow_df.to_csv(f"{PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv", index=False)
