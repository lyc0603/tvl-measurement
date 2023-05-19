"""
Functions to calculate the total value locked (TVL) of a given token.
"""

import warnings

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from config import constants
from environ.data_fetching import token_price, web3_call
from environ.data_fetching.balancer_data_fetching import balancer_subgraph_token_price
from environ.data_fetching.makerdao_data_fetching import (
    get_makerdao_tokens_to_spot_price,
)
from environ.data_processing import protocol_token_origination
from environ.data_processing.protocol_token_origination import Origin

# ignore warnings
warnings.filterwarnings("ignore")

ETH_INFO = {
    "address": ["ETH", "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"],
    "name": "ETH",
    "symbol": "ETH",
}


def _get_token_name_symbol(token: str) -> tuple["str", "str"]:
    """
    Function to get the token name and symbol
    """

    # call the web3 api to get the token name
    try:
        name = web3_call.get_token_name(token)
    except:  # pylint: disable=W0702
        name = "Unknown"
    else:
        pass

    # call the web3 api to get the token symbol
    try:
        symbol = web3_call.get_token_symbol(token)
    except:  # pylint: disable=W0702
        symbol = "Unknown"
    else:
        pass

    return name, symbol


def _get_general_token_prc_from_cg(
    origin: Origin,
    token: str,
    amount: float,
    receipt_token_to_total_supply: dict,
    receipt_token_to_composition: dict,
) -> tuple[float, float]:
    """
    Function to get the token price
    """

    value_defillama, value = 0, 0

    # simply ignore the token if the amount is 0
    if amount != 0:
        # general method to get the token price from the coingecko api
        try:
            if token in ETH_INFO["address"]:
                value_defillama = token_price.get_token_price_defillama(
                    ETH_INFO["address"][1]
                )
                value = token_price.get_eth_price()
            else:
                value_defillama = token_price.get_token_price_defillama(token)
                value = token_price.get_token_price(token)
        except:  # pylint: disable=W0702
            # special method for different DeFi protocols
            try:
                if (origin == Origin.MAKER) | (origin == Origin.AAVE_V2):
                    # Special case for MakerDAO and Aave
                    value = _get_makerdao_aave_tvl(token)

                if origin == Origin.BALANCER:
                    # Special case for Balancer
                    value = _get_balancer_tvl(
                        token,
                        receipt_token_to_total_supply,
                        receipt_token_to_composition,
                    )
            except:  # pylint: disable=W0702
                value = 0
                print(f"Could not get the price of {token}")
                # raise LookupError(f"Could not get the price of {token}")

    return value_defillama, value


def _get_makerdao_aave_tvl(token: str) -> float:
    """
    Function to calculate the special case of the TVL of Maker Dao and AAVE
    """

    # if the token is a general lp token
    try:
        value = token_price.get_lp_price(token)
    except:  # pylint: disable=W0702
        pass
    else:
        return value

    # if the token price can be fetched from the makerdao price oracle
    try:
        value = get_makerdao_tokens_to_spot_price()[token]
    except:  # pylint: disable=W0702
        pass
    else:
        return value

    # if the token is a curve lp token
    try:
        value = token_price.get_curve_lp_price(token)
    except:  # pylint: disable=W0702
        pass
    else:
        return value

    # if the token is delisted
    if token in constants.DELISTED_TOKENS:
        return 0

    raise LookupError(f"Could not get the price of {token}")


def _get_balancer_tvl(
    token: str, receipt_token_to_total_supply: dict, receipt_token_to_composition: dict
) -> float:
    """
    Function to calculate the special case of the TVL of balancer
    """

    try:
        value = token_price.get_balancer_lp_price(token, receipt_token_to_composition)
    except:  # pylint: disable=W0702
        pass
    else:
        return value

    # The token could be atoken. Now has been no pool
    # and could not be retrieved in DefiLlama

    match token:
        case defi_token if defi_token in list(receipt_token_to_total_supply.keys()):
            value = token_price.get_balancer_derivative_price(
                token,
                receipt_token_to_total_supply,
                receipt_token_to_composition,
            )
        case defi_token if defi_token in constants.NO_RECORD_TOKEN:
            value = 0
        case _:
            value = balancer_subgraph_token_price(
                token,
            )
    return 0


def _get_compound_tvl(
    token: str,
) -> float:
    """
    Function to calculate the special case of the TVL of compound
    """

    try:
        value = token_price.uniswap_v2_subgraph_token_price(token)
    except:  # pylint: disable=W0702
        pass
    else:
        return value

    return 0


def _visualize_tvl(composition_df: pd.DataFrame, tvl: float, origin: Origin):
    """
    Function to visualize the composition of the TVL of a given token
    """

    # Sort the dataframe by the total value
    composition_df = composition_df.sort_values(by="total_value", ascending=False)

    # Plot the composition
    composition_df.plot(
        kind="bar",
        x="token_symbol",
        y="total_value",
        title=f"Composition of the TVL of {origin.name}",
    )

    # small font size for the x-axis labels
    plt.xticks(fontsize=8)

    # tight_layout() is used to avoid overlapping of the title and the x-axis labels
    plt.tight_layout()

    # set the title of the plot
    plt.title(f"Composition of the TVL {tvl} of {origin.name}")

    # Save the plot
    plt.savefig(f"{constants.FIGURES_PATH}/tvl_composition_{origin}.pdf")

    # Save the composition dataframe
    composition_df.to_csv(
        f"{constants.DATA_PATH}/tvl/tvl_composition_{origin}.csv", index=False
    )


def get_tvl(
    origin: Origin,
) -> float:
    """
    Function to calculate the TVL of a given token
    """

    # get the data from the origin
    (
        receipt_token_to_total_supply,
        receipt_to_composition,
    ) = protocol_token_origination.get_data_from_origin(origin)

    # container for the tvl
    tvl = 0
    tvl_defillama = 0

    # Create a dictionary to store the outcome
    composition_dict = {
        "token_contract": [],
        "token_name": [],
        "token_symbol": [],
        "amount": [],
        "value": [],
        "defillama_value": [],
        "total_value": [],
        "total_value_defillama": [],
    }

    # A dataframe to store the token price
    token_prc_df = pd.DataFrame(columns=["token", "value", "value_defillama"])

    # Iterate through the receipts and calculate the TVL
    for _, composition in tqdm(receipt_to_composition.items()):
        # Iterate through the composition of the receipt
        for token, amount in composition.items():
            # check whether the token is in the token price dataframe
            if token_prc_df.loc[token_prc_df["token"] == token.lower].shape[0] == 0:
                # get the token name and symbol
                if token in ETH_INFO["address"]:
                    # if the token is ETH
                    name = ETH_INFO["name"]
                    symbol = ETH_INFO["symbol"]
                else:
                    # if the token is not ETH
                    name, symbol = _get_token_name_symbol(token=token)

                # remove the real-world-asset token
                if token in constants.RWA_ASSETS:
                    continue

                # general method to get the token price from the coingecko api
                value_defillama, value = _get_general_token_prc_from_cg(
                    origin=origin,
                    token=token,
                    amount=amount,
                    receipt_token_to_total_supply=receipt_token_to_total_supply,
                    receipt_token_to_composition=receipt_to_composition,
                )

                # record the outcome
                append_dict = {
                    "token_contract": token,
                    "token_name": name,
                    "token_symbol": symbol,
                    "amount": amount,
                    "value": value,
                    "defillama_value": value_defillama,
                    "total_value": value * amount,
                    "total_value_defillama": value_defillama * amount,
                }

                for dict_key, dict_value in append_dict.items():
                    composition_dict[dict_key].append(dict_value)

            else:
                # get the token price from the dataframe
                value_defillama, value = token_prc_df.loc[
                    token_prc_df["token"] == token.lower()
                ][["value", "value_defillama"]].values[0]

            tvl += value * amount
            tvl_defillama += value_defillama * amount

    # convert the dictionary to a dataframe
    composition_df = pd.DataFrame(composition_dict)

    # visualize the composition
    _visualize_tvl(composition_df, tvl, origin)

    return tvl


if __name__ == "__main__":
    # Test the function
    print(f"The TVL is {get_tvl(Origin.YEARN)}")
