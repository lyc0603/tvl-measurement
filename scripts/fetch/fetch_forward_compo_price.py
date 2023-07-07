"""
Script to fetch token price via forward method
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import PROCESSED_DATA_PATH
from environ.data_fetching.token_price import backup_price_fetching_method
from environ.data_processing.process_compo import _get_token_price

# load the flow data
with open(
    f"{PROCESSED_DATA_PATH}/non_derivative/non_derivative.json",
    "r",
    encoding="utf-8",
) as f_json:
    non_derivative = json.load(f_json)

# convert the json to dataframe
non_derivative_df = pd.DataFrame(non_derivative)

# get the price of the token
dict_price = _get_token_price()


def _update_token_data(
    non_derivative_df: pd.DataFrame,
    token: str,
    price: float,
):
    """
    Function to update price data
    """

    # if the token is not in the dict, use the backup method
    non_derivative_df.loc[non_derivative_df["contract"] == token, "price"] = price

    # calculate the flow in USD
    non_derivative_df.loc[non_derivative_df["contract"] == token, "flow_usd"] = (
        non_derivative_df.loc[non_derivative_df["contract"] == token, "amount"] * price
    )


# iterate through the token list
for token in tqdm(set(non_derivative_df["contract"])):
    # iterate through the token list
    try:
        # set the price of the token
        token_prc = dict_price[token]
    except:  # pylint disable=bare-except
        pass
    else:
        _update_token_data(
            non_derivative_df,
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
            non_derivative_df,
            token,
            token_prc,
        )
        continue


# save the flow data
non_derivative_df.to_csv(
    f"{PROCESSED_DATA_PATH}/non_derivative/non_derivative_usd.csv", index=False
)
