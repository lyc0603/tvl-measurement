"""
Functions for token origination
"""

import os
from enum import Enum

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

    Unknown = 0
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
        Origin.Unknown: "Unknown",
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

        # manually add the 0x0 and 0xe addresses
        address_to_protocol[
            "0x0000000000000000000000000000000000000000"
        ] = Origin.ETHEREUM
        address_to_protocol[
            "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        ] = Origin.ETHEREUM
        address_to_protocol["eth"] = Origin.ETHEREUM
        # manually add the wETH token address
        address_to_protocol[
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        ] = Origin.ETHEREUM
        # manualy add the stETH and wstETH token addresses
        address_to_protocol["0xae7ab96520de3a18e5e111b5eaab095312d7fe84"] = Origin.LIDO
        address_to_protocol["0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"] = Origin.LIDO
        # manually add the Gelato UniswapV3 tokens addresses
        address_to_protocol[
            "0x50379f632ca68D36E50cfBC8F78fe16bd1499d1e".lower()
        ] = Origin.GELATO
        # manually add the Uniswap Governance token address
        address_to_protocol[
            "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984".lower()
        ] = Origin.UNISWAP_V2
        # manually add the USDC token address
        address_to_protocol[
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower()
        ] = Origin.CIRCLE
        # manually add the USDT token address
        address_to_protocol[
            "0xdAC17F958D2ee523a2206206994597C13D831ec7".lower()
        ] = Origin.TETHER
        # manually add the GUSD token address
        address_to_protocol[
            "0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd".lower()
        ] = Origin.GEMINI
        # manually add the USDP token address
        address_to_protocol[
            "0x8E870D67F660D95d5be530380D0eC0bd388289E1".lower()
        ] = Origin.PAXOS
        # manually add the WBTC token address
        address_to_protocol[
            "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599".lower()
        ] = Origin.BITGO
        # manually add the CRV token address
        address_to_protocol[constants.CRV_ADDRESS] = Origin.CURVE
        # manually add the YFI token address
        address_to_protocol[
            "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e".lower()
        ] = Origin.YEARN
        # manually add the BAL token address
        address_to_protocol[constants.BAL_ADDRESS] = Origin.BALANCER
        # manually add the TUSD token address
        address_to_protocol[
            "0x0000000000085d4780B73119b644AE5ecd22b376".lower()
        ] = Origin.TRUSTTOKEN
        # manually add the BUSD token address
        address_to_protocol[
            "0x4Fabb145d64652a948d72533023f6E7A623C7C53".lower()
        ] = Origin.BINANCE
        # manually add the BBTC token address
        address_to_protocol[
            "0x9BE89D2a4cd102D8Fecc6BF9dA793be995C22541".lower()
        ] = Origin.BINANCE
        # manually add the MKR token address
        address_to_protocol[constants.MKR_ADDRESS] = Origin.MAKER
        # manually add the SAI token address
        address_to_protocol[constants.SAI_ADDRESS] = Origin.MAKER
        # manually add the AAVE token address
        address_to_protocol[constants.AAVE_ADDRESS] = Origin.AAVE_V2
        # manually add the COMP token address
        address_to_protocol[constants.COMP_ADDRESS] = Origin.COMPOUND_V2
        # manually add the CRV token address
        address_to_protocol[constants.CRV_ADDRESS] = Origin.CURVE
        # manually add the sUSD token address
        address_to_protocol[
            "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51".lower()
        ] = Origin.SYNTHETIX
        # manually add the sBTC token address
        address_to_protocol[
            "0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6".lower()
        ] = Origin.SYNTHETIX
        # manually add the sEUR token address
        address_to_protocol[
            "0xD71eCFF9342A5Ced620049e616c5035F1dB98620".lower()
        ] = Origin.SYNTHETIX
        # manually add the sLINK token address
        address_to_protocol[
            "0xbBC455cb4F1B9e4bFC4B73970d360c8f032EfEE6".lower()
        ] = Origin.SYNTHETIX
        # manually add the sETH token address
        address_to_protocol[
            "0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb".lower()
        ] = Origin.SYNTHETIX
        # manually add the yearn tokens address
        address_to_protocol[
            "0x73a052500105205d34Daf004eAb301916DA8190f".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x1bE5d71F2dA660BFdee8012dDc58D024448A0A59".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x9777d7E2b60bB01759D0E2f8be2095df444cb07E".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x48759F220ED983dB51fA7A8C0D2AAb8f3ce4166a".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x76Eb2FE28b36B3ee97F3Adae0C69606eeDB2A37c".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x83f798e925BcD4017Eb265844FDDAbb448f1707D".lower()
        ] = Origin.YEARN
        address_to_protocol[
            "0x99d1Fa417f94dcD62BfE781a1213c092a47041Bc".lower()
        ] = Origin.YEARN

        # output a csv for the origins
        with open(f"{constants.CACHE_PATH}/token_origins_cache.csv", "w") as cache_file:
            cache_file.write("receipt_token,origin\n")
            for receipt_token in address_to_protocol:
                cache_file.write(
                    f"{receipt_token},{address_to_protocol[receipt_token].value}\n"
                )
    else:
        address_to_protocol = {}
        with open(f"{constants.CACHE_PATH}/token_origins_cache.csv", "r") as cache_file:
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

    if origin == Origin.MAKER:
        return makerdao_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.AAVE_V2:
        return aave_v2_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.BALANCER:
        return balancer_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.COMPOUND_V2:
        return compound_v2_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.CURVE:
        return curve_v1_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.UNISWAP_V2:
        return uniswap_v2_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.UNISWAP_V3:
        return uniswap_v3_data_fetching.get_receipt_tokens_and_composition()
    if origin == Origin.YEARN:
        return yearn_data_fetching.get_receipt_tokens_and_composition()


if __name__ == "__main__":
    # test the function
    print(get_all_receipt_token_origin(reset_the_cache=True))
