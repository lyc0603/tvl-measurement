"""
Functions to fetch LIDO data
"""

from multicall import Call

from config.constants import LDO_ADDRESS, STETH_ADDRESS, WSTETH_ADDRESS
from environ.data_fetching import web3_call
from environ.data_fetching.web3_call import get_token_decimals, get_token_total_supply


def get_total_pooled_ether_lido() -> float:
    """
    Function to get the total pooled ether
    """

    # Call the contract to get the total pooled ether
    total_pooled_ether = Call(
        LDO_ADDRESS,
        ["getTotalPooledEther()(uint256)"],
        [["totalPooledEther", None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()["totalPooledEther"]

    return total_pooled_ether / 10 ** get_token_decimals(LDO_ADDRESS)


def get_steth_per_token_lido() -> float:
    """
    Function to get the steth per token
    """

    # Call the contract to get the steth per token
    steth_per_token = Call(
        WSTETH_ADDRESS,
        ["stEthPerToken()(uint256)"],
        [["stETHPerToken", None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()["stETHPerToken"]

    return steth_per_token / 10 ** get_token_decimals(WSTETH_ADDRESS)


def get_steth_total_supply_lido() -> float:
    """
    Function to get the total supply of steth
    """

    # Call the contract to get the total supply of steth
    return get_token_total_supply(STETH_ADDRESS)


def get_wsteth_total_supply_lido() -> float:
    """
    Function to get the total supply of wsteth
    """

    # Call the contract to get the total supply of wsteth
    return get_token_total_supply(WSTETH_ADDRESS)


if __name__ == "__main__":
    print(get_total_pooled_ether_lido())
    print(get_steth_per_token_lido())
    print(get_steth_total_supply_lido())
    print(get_wsteth_total_supply_lido())
