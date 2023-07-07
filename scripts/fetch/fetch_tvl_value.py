"""
Script to fetch the price of the flows
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import PROCESSED_DATA_PATH
from environ.data_processing.process_compo import _get_token_price
from environ.data_fetching.token_price import (
    backup_price_fetching_method,
    get_balancer_derivative_price,
)
from environ.data_fetching.balancer_data_fetching import (
    get_receipt_tokens_and_composition,
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

# get the price of the token
dict_price = _get_token_price()

# get the composition of balancer
(
    receipt_token_to_total_supply,
    receipt_token_to_composition,
) = get_receipt_tokens_and_composition()


def _update_token_data(
    flow_df: pd.DataFrame,
    token: str,
    price: float,
):
    """
    Function to update price data
    """

    # if the token is not in the dict, use the backup method
    flow_df.loc[flow_df["contract"] == token, "price"] = price

    # calculate the flow in USD
    flow_df.loc[flow_df["contract"] == token, "flow_usd"] = (
        flow_df.loc[flow_df["contract"] == token, "amount"] * price
    )


# iterate through the token list
for token in tqdm(token_lst):
    try:
        # set the price of the token
        token_prc = dict_price[token]
    except:  # pylint disable=bare-except
        pass
    else:
        _update_token_data(
            flow_df,
            token,
            token_prc,
        )
        continue

    try:
        # set the price of the token using backup method
        token_prc = backup_price_fetching_method(token)
    except:  # pylint disable=bare-except
        pass
    else:
        _update_token_data(
            flow_df,
            token,
            token_prc,
        )
        continue

    if token in list(receipt_token_to_total_supply.keys()):
        value = get_balancer_derivative_price(
            token,
            receipt_token_to_total_supply,
            receipt_token_to_composition,
        )
    else:
        _update_token_data(
            flow_df,
            token,
            0,
        )
        print(f"Token {token} not found")


# save the flow data
flow_df.to_csv(f"{PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv", index=False)
