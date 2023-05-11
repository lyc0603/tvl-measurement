"""
Function to fetch the price of a token from the coingecko API
"""

import time
import requests
from pycoingecko import CoinGeckoAPI
from multicall import Call, Multicall
from environ.data_fetching import (
    web3_call,
    curve_v1_data_fetching,
    balancer_data_fetching,
)

# Initialise the API
cg = CoinGeckoAPI()

# Common price oracle


def get_token_price(token_address: str) -> float:
    """
    Function to fetch the price of a token from the coingecko API
    """
    time.sleep(6)
    token_info = cg.get_coin_market_chart_from_contract_address_by_id(
        id="ethereum", contract_address=token_address, vs_currency="usd", days=1
    )

    # Get the price of the token
    return token_info["prices"][-1][1]


def get_token_price_defillama(token_address: str) -> float:
    """
    Function to fetch the price of a token from the defillama API
    """
    url_defillama = f"https://coins.llama.fi/prices/current/ethereum:{token_address}"
    token_info_defillama = requests.get(url_defillama, timeout=30).json()

    # Get the price of the token
    return token_info_defillama["coins"][f"ethereum:{token_address}"]["price"]


def get_eth_price() -> float:
    """
    Function to fetch the price of ETH from the coingecko API
    """
    time.sleep(6)
    eth_info = cg.get_coin_market_chart_by_id(id="ethereum", vs_currency="usd", days=1)

    # Get the price of the token
    return eth_info["prices"][-1][1]


# Special price oracle for balancer


def get_balancer_lp_price(token_address: str) -> float:
    """
    Function to fetch the price of a balancer lp token
    """

    # Get the total supply and composition of the balancer pool
    (
        _,
        receipt_token_to_composition,
    ) = balancer_data_fetching.get_receipt_tokens_and_composition()

    # get the total supply of the lp token
    total_supply = balancer_data_fetching.get_token_actual_supply(token_address)

    # Get the pool token value
    token_composition = receipt_token_to_composition[token_address]
    pool_value = 0

    # Iterate through the underlying tokens and calculate the price
    for token, token_amount in token_composition.items():
        # Special case for the ETH token
        if token == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
            pool_value += token_amount * get_eth_price()
        else:
            pool_value += token_amount * get_token_price(token)

    # Calculate the price of the lp token
    return pool_value / total_supply


# Special price oracle for curve


def get_curve_lp_price(token_address: str) -> float:
    """
    Function to unwrap the curve lp token and calculate the price of the lp token
    """

    # Get the composition of the curve
    (
        receipt_token_to_total_supply,
        receipt_token_to_underlying_tokens,
    ) = curve_v1_data_fetching.get_receipt_tokens_and_composition()

    # Total supply of the lp token
    total_supply = receipt_token_to_total_supply[token_address]

    # Caculate the pool value
    pool_value = 0

    # Iterate through the underlying tokens and calculate the price
    for token, token_amount in receipt_token_to_underlying_tokens[
        token_address
    ].items():
        # Special case for the ETH token
        if token == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
            token_price = get_eth_price()
        else:
            token_price = get_token_price(token)
        pool_value += token_amount * token_price

    return pool_value / total_supply


# Special price oracle for gelato


def get_gelato_lp_price(token_address: str) -> float:
    """
    Function to unwrap the gelato lp token and calculate the price of the lp token
    """

    # Get the token circulating supply
    total_supply = web3_call.get_token_total_supply(token_address)

    # unwrap the lp token
    call_list = []
    call_list.append(
        Call(
            token_address,
            [
                "token0()(address)",
            ],
            [["token0" + token_address, None]],
        )
    )
    call_list.append(
        Call(
            token_address,
            [
                "token1()(address)",
            ],
            [["token1" + token_address, None]],
        )
    )
    call_list.append(
        Call(
            token_address,
            [
                "gelatoBalance0()(uint256)",
            ],
            [
                ["reserve0" + token_address, None],
            ],
        )
    )
    call_list.append(
        Call(
            token_address,
            [
                "gelatoBalance1()(uint256)",
            ],
            [
                ["reserve1" + token_address, None],
            ],
        )
    )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()
    token0 = multicall["token0" + token_address]
    token1 = multicall["token1" + token_address]
    token0_decimal = web3_call.get_token_decimals(token0)
    token1_decimal = web3_call.get_token_decimals(token1)
    reserve0 = multicall["reserve0" + token_address] / 100 ** (token0_decimal / 2)
    reserve1 = multicall["reserve1" + token_address] / 100 ** (token1_decimal / 2)

    # Get the price of the token
    token0_price = get_token_price(token0)
    token1_price = get_token_price(token1)

    # Get the price of the lp token
    lp_price = (token0_price * reserve0 + token1_price * reserve1) / total_supply

    return lp_price


# Special price oracle for lp tokens


def get_lp_price(token_address: str) -> float:
    """
    Function to unwrap the lp token and calculate the price of the lp token
    """

    # Get the token circulating supply
    total_supply = web3_call.get_token_total_supply(token_address)

    # unwrap the lp token
    call_list = []
    call_list.append(
        Call(
            token_address,
            [
                "token0()(address)",
            ],
            [["token0" + token_address, None]],
        )
    )
    call_list.append(
        Call(
            token_address,
            [
                "token1()(address)",
            ],
            [["token1" + token_address, None]],
        )
    )
    call_list.append(
        Call(
            token_address,
            [
                "getReserves()(uint112,uint112,uint32)",
            ],
            [
                ["reserve0" + token_address, None],
                ["reserve1" + token_address, None],
            ],
        )
    )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()
    token0 = multicall["token0" + token_address]
    token1 = multicall["token1" + token_address]
    token0_decimal = web3_call.get_token_decimals(token0)
    token1_decimal = web3_call.get_token_decimals(token1)
    reserve0 = multicall["reserve0" + token_address] / 100 ** (token0_decimal / 2)
    reserve1 = multicall["reserve1" + token_address] / 100 ** (token1_decimal / 2)

    # Get the price of the token
    token0_price = get_token_price(token0)
    token1_price = get_token_price(token1)

    # Get the price of the lp token
    lp_price = (token0_price * reserve0 + token1_price * reserve1) / total_supply

    return lp_price


if __name__ == "__main__":
    # Test the function
    # print(get_lp_price("0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"))
    # print(get_curve_lp_price("0x06325440d014e39736583c165c2963ba99faf14e"))
    # print(get_eth_price())
    # print(get_token_price_defillama("0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"))
    print(get_token_price("0xba100000625a3754423978a60c9317c58a424e3d"))
    # print(get_balancer_lp_price("0x2bbf681cc4eb09218bee85ea2a5d3d13fa40fc0c".lower()))
