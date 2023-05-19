"""
Functions for token origination
"""

import os
from enum import Enum
from typing import Optional

from config import constants
from environ.data_fetching import (
    aave_v2_data_fetching,
    balancer_data_fetching,
    compound_v2_data_fetching,
    curve_v1_data_fetching,
    makerdao_data_fetching,
    uniswap_v2_data_fetching,
    uniswap_v3_data_fetching,
    yearn_data_fetching,
)


class Origin(Enum):
    """
    Class `Origin` to record the origin of a token
    """

    UNKNOWN = 0
    MAKER = 1
    AAVE_V2 = 2
    BALANCER = 3
    COMPOUND_V2 = 4
    CURVE = 5
    UNISWAP_V2 = 6
    UNISWAP_V3 = 7
    YEARN = 8
    ETHEREUM = 9
    LIDO = 10
    GELATO = 11
    CIRCLE = 12
    TETHER = 13
    GEMINI = 14
    BITGO = 15
    PAXOS = 16
    TRUSTTOKEN = 17
    BINANCE = 18
    SYNTHETIX = 19


def get_origin_to_name() -> dict[Origin, str]:
    """
    Function to get the mapping from `Origin` to name
    """

    return {
        Origin.UNKNOWN: "Unknown",
        Origin.MAKER: "MakerDAO",
        Origin.AAVE_V2: "AaveV2",
        Origin.BALANCER: "Balancer",
        Origin.COMPOUND_V2: "CompoundV2",
        Origin.CURVE: "Curve",
        Origin.UNISWAP_V2: "UniswapV2",
        Origin.UNISWAP_V3: "UniswapV3",
        Origin.YEARN: "yearn",
        Origin.ETHEREUM: "Ether",
        Origin.LIDO: "LIDO",
        Origin.GELATO: "Gelato/Arakis",
        Origin.CIRCLE: "Circle/Coinbase",
        Origin.TETHER: "Tether/Bitfinex",
        Origin.GEMINI: "Gemini",
        Origin.BITGO: "BitGo",
        Origin.PAXOS: "Paxos",
        Origin.TRUSTTOKEN: "TrustToken",
        Origin.BINANCE: "Binance",
        Origin.SYNTHETIX: "Synthetix",
    }


def get_all_receipt_token_origin(reset_the_cache: bool) -> dict[str, Origin]:
    """
    Function to get the origin of all receipt tokens
    Check if the cache exists, if not, create it
    """

    if reset_the_cache or not os.path.exists(
        f"{constants.CACHE_PATH}/token_origins_cache.csv"
    ):
        address_to_protocol = {}
        for receipt_token in makerdao_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.MAKER
        for receipt_token in aave_v2_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.AAVE_V2
        for receipt_token in balancer_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.BALANCER
        for receipt_token in compound_v2_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.COMPOUND_V2
        for receipt_token in curve_v1_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.CURVE
        for receipt_token in uniswap_v2_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.UNISWAP_V2
        for receipt_token in uniswap_v3_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.UNISWAP_V3
        for receipt_token in yearn_data_fetching.get_all_receipt_tokens():
            address_to_protocol[receipt_token.lower()] = Origin.YEARN

        # output a csv for the origins
        with open(
            f"{constants.CACHE_PATH}/token_origins_cache.csv", "w", encoding="utf-8"
        ) as cache_file:
            cache_file.write("receipt_token,origin\n")
            for receipt_token in address_to_protocol:
                cache_file.write(
                    f"{receipt_token},{address_to_protocol[receipt_token].value}\n"
                )
    else:
        address_to_protocol = {}
        with open(
            f"{constants.CACHE_PATH}/token_origins_cache.csv", "r", encoding="utf-8"
        ) as cache_file:
            for line in cache_file:
                if line == "receipt_token,origin\n":
                    continue
                receipt_token, origin = line.removesuffix("\n").split(",")
                address_to_protocol[receipt_token] = Origin(int(origin))
    return address_to_protocol


def get_data_from_origin(
    origin: Origin,
) -> (dict[str, float], dict[str, dict[str, str]]):
    """
    Function to get the data from the origin
    """

    match origin:
        case Origin.MAKER:
            return makerdao_data_fetching.get_receipt_tokens_and_composition()
        case Origin.AAVE_V2:
            return aave_v2_data_fetching.get_receipt_tokens_and_composition()
        case Origin.BALANCER:
            return balancer_data_fetching.get_receipt_tokens_and_composition()
        case Origin.COMPOUND_V2:
            return compound_v2_data_fetching.get_receipt_tokens_and_composition()
        case Origin.CURVE:
            return curve_v1_data_fetching.get_receipt_tokens_and_composition()
        case Origin.UNISWAP_V2:
            return uniswap_v2_data_fetching.get_receipt_tokens_and_composition()
        case Origin.UNISWAP_V3:
            return uniswap_v3_data_fetching.get_receipt_tokens_and_composition()
        case Origin.YEARN:
            return yearn_data_fetching.get_receipt_tokens_and_composition()
        case _:
            return (None, None)


if __name__ == "__main__":
    # test the function
    print(get_all_receipt_token_origin(reset_the_cache=True))
