"""
Function to fetch the price of a token from the coingecko API
"""

import time

import requests
from multicall import Call, Multicall
from pycoingecko import CoinGeckoAPI

from config import constants
from environ.data_fetching import (
    balancer_data_fetching,
    curve_v1_data_fetching,
    subgraph_query,
    web3_call,
)
from environ.data_fetching.balancer_data_fetching import balancer_subgraph_token_price

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


# Regular price oracle from Uniswap V2
def uniswap_v2_subgraph_token_price(token_address: str):
    """
    Function to get the price via the price oracle from Uniswap V2
    """

    # call the graph
    data_json = subgraph_query.run_query_var(
        http=constants.UNISWAP_V2_URL,
        query_scripts=constants.UNISWAP_V2_TOKEN_PRICE_QUERY,
        var={"id": token_address},
    )

    return float(data_json["data"]["tokenDayDatas"][0]["priceUSD"])


# Special price oracle for balancer
def get_balancer_lp_price(
    token_address: str, receipt_token_to_composition: dict
) -> float:
    """
    Function to fetch the price of a balancer lp token
    """

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


def get_balancer_derivative_price(
    derivative_token_address: str,
    receipt_token_to_total_supply: dict,
    receipt_token_to_composition: dict,
) -> float:
    """
    Function to calculate the balancer derivative price
    """

    def _get_plain_vanilla_token_price(token: str) -> float:
        """
        Internal function to calculate the price of a default token
        """

        try:
            return get_token_price(token)
        except:  # pylint: disable=W0702
            pass

        try:
            return balancer_subgraph_token_price(token)
        except:  # pylint: disable=W0702
            pass

        print(
            f"Cannot find price for {token},"
            + f"the underlying of {derivative_token_address}, use default price 1"
        )
        return 1

    def _get_derivative_simple_price(
        derivative_token_address: str,
        receipt_token_to_total_supply: dict,
        receipt_token_to_composition: dict,
    ) -> float:
        """
        Internal function to calculate the simple derivative price
        e.g. Balancer Aave v3 Boosted Pool (DAI) (bb-a-DAI)
        """

        # initial value
        underlying_value = 0

        # iterate through the underlying tokens and calculate the price
        for token, token_amount in receipt_token_to_composition[
            derivative_token_address
        ].items():
            if token_amount != 0:
                underlying_value += _get_plain_vanilla_token_price(token) * token_amount

        # get the total supply of the derivative token
        return (
            underlying_value / receipt_token_to_total_supply[derivative_token_address]
        )

    def _get_derivative_square_price(
        derivative_token_address: str,
        receipt_token_to_total_supply: dict,
        receipt_token_to_composition: dict,
    ) -> float:
        """
        Internal function to calculate the complex derivative price
        e.g. Balancer Aave v3 Boosted StablePool (bb-a-USD)
        """

        # initial value
        underlying_value = 0

        # iterate through the simple derivateive underlying the complex derivative
        for simple_derivative, simple_derivative_amount in receipt_token_to_composition[
            derivative_token_address
        ].items():
            # if the token is a simple derivative with non-zero amount
            if (simple_derivative_amount != 0) & (
                simple_derivative in list(receipt_token_to_total_supply.keys())
            ):
                # calculate the amount of the simple derivative
                underlying_value += (
                    simple_derivative_amount
                    * _get_derivative_simple_price(
                        simple_derivative,
                        receipt_token_to_total_supply,
                        receipt_token_to_composition,
                    )
                )
            # if the token is not a derivative
            elif (simple_derivative_amount != 0) & (
                simple_derivative in list(receipt_token_to_total_supply.keys())
            ):
                underlying_value += (
                    simple_derivative_amount
                    * _get_plain_vanilla_token_price(simple_derivative)
                )

            # if the token is a derivative with zero amount
            else:
                pass

        # get the total supply of the derivative token
        return (
            underlying_value / receipt_token_to_total_supply[derivative_token_address]
        )

    # check whether the token is a complex derivative
    # iterate through the underlying tokens and check whether
    # the underlying tokens are simple derivatives
    for token, _ in receipt_token_to_composition[derivative_token_address].items():
        if token in list(receipt_token_to_total_supply.keys()):
            return _get_derivative_square_price(
                derivative_token_address,
                receipt_token_to_total_supply,
                receipt_token_to_composition,
            )

    return _get_derivative_simple_price(
        derivative_token_address,
        receipt_token_to_total_supply,
        receipt_token_to_composition,
    )


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
    # print(get_token_price_defillama("0xf8fd466f12e236f4c96f7cce6c79eadb819abf58"))
    # print(get_token_price("0x470ebf5f030ed85fc1ed4c2d36b9dd02e77cf1b7"))
    # print(get_balancer_lp_price("0x2bbf681cc4eb09218bee85ea2a5d3d13fa40fc0c".lower()))
    # (
    #     receipt_token_to_total_supply,
    #     receipt_token_to_composition,
    # ) = get_receipt_tokens_and_composition()
    # print(
    #     get_balancer_derivative_price(
    #         receipt_token_to_total_supply=receipt_token_to_total_supply,
    #         receipt_token_to_composition=receipt_token_to_composition,
    #         derivative_token_address="0x60d604890feaa0b5460b28a424407c24fe89374a",
    #     )
    # )
    print(uniswap_v2_subgraph_token_price("0x1985365e9f78359a9b6ad760e32412f4a445e862"))
    pass
