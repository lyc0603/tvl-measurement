"""
Fetch Uniswap V2 data directly from the blockchain
"""

from multicall import Call, Multicall
from tqdm import tqdm

from environ.data_fetching.web3_call import (
    eth_w3,
    get_tokens_total_supply,
    get_tokens_to_decimals,
)
from environ.utils import info_logger
from config.constants import UNISWAP_V2_FACTORY_ADDRESS, MAXIMUM_LP_COUNT_UNISWAP_V2


def get_total_number_of_uni_v2_pools() -> int:
    """
    Get the total number of Uniswap V2 pools
    """

    # Info log
    info_logger.print_info_log("Fetch the total number of Uniswap V2 pools", "success")

    # The document of the multicall function is here:
    # https://github.com/banteg/multicall.py
    total_number_of_uni_v2_pools = Call(
        UNISWAP_V2_FACTORY_ADDRESS,
        ["allPairsLength()(uint256)"],
        [["allPairsLength", None]],
        _w3=eth_w3,
    )()["allPairsLength"]

    return total_number_of_uni_v2_pools


def get_all_uni_v2_pools() -> list[str]:
    """
    Fetch the list of all uniswap V2 pools
    """

    # Info log
    info_logger.print_info_log("Fetch list of all uniswap V2 pools", "success")

    pool_num = get_total_number_of_uni_v2_pools()
    call_list = []

    # Fetch the list of a maximum of MAXIMUM_LP_COUNT_UNISWAP_V2 pools Returns the
    # address of the nth pair (0-indexed) created through the factory, or address(0)
    # (0x0000000000000000000000000000000000000000) if not enough pairs have been created yet.
    for pool_idx in tqdm(range(0, min(pool_num, MAXIMUM_LP_COUNT_UNISWAP_V2))):
        # The list of all pairs is stored in a mapping
        call_list.append(
            Call(
                UNISWAP_V2_FACTORY_ADDRESS,
                ["allPairs(uint256)(address)", pool_idx],
                [["pair" + str(pool_idx), None]],
            )
        )

        # Call the multicall contract
        multicall = Multicall(call_list, _w3=eth_w3)()

    return multicall.values()


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get the list of all receipt tokens
    """

    return get_all_uni_v2_pools()


def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, [str, int]]):
    """
    This function returns two dictionaries: one with the total supply and
    the other with the composition of all Uniswap V2 pools
    """

    # Get the list of all Uniswap V2 pools
    uniswap_v2_tokens = get_all_uni_v2_pools()

    # Info log
    info_logger.print_info_log("Fetch all uniswap V2 pools", "success")

    # Get the total supply of all Uniswap V2 pools
    receipt_token_to_total_supply = get_tokens_total_supply(uniswap_v2_tokens)

    # Get the composition of all Uniswap V2 pools
    receipt_token_to_underlying_token_to_amount = {}
    call_list = []

    for receipt_token in uniswap_v2_tokens:
        # Call the method of the Uniswap V2 pool contract
        # to get the composition of the pool
        call_list.append(
            Call(
                receipt_token,
                [
                    "token0()(address)",
                ],
                [["token0" + receipt_token, None]],
            )
        )
        call_list.append(
            Call(
                receipt_token,
                [
                    "token1()(address)",
                ],
                [["token1" + receipt_token, None]],
            )
        )
        # Returns the reserves of token0 and token1 used to price trades and distribute liquidity. See Pricing.
        # Also returns the block.timestamp (mod 2**32) of the last block during which an interaction occured for the pair.
        call_list.append(
            Call(
                receipt_token,
                [
                    "getReserves()(uint112,uint112,uint32)",
                ],
                [
                    ["reserve0" + receipt_token, None],
                    ["reserve1" + receipt_token, None],
                ],
            )
        )
    # Constuct the dictionary of the composition of the pool
    multicall = Multicall(call_list, _w3=eth_w3)()
    token_list = []

    for receipt_token in tqdm(uniswap_v2_tokens):
        token0 = multicall["token0" + receipt_token]
        token1 = multicall["token1" + receipt_token]
        token_list.append(token0)
        token_list.append(token1)
    token_to_decimals = get_tokens_to_decimals(token_list)
    for receipt_token in uniswap_v2_tokens:
        token0 = multicall["token0" + receipt_token]
        token1 = multicall["token1" + receipt_token]

        # 100 ** (n / 2) == 10 ** n
        reserve0 = multicall["reserve0" + receipt_token] / 100 ** (
            token_to_decimals[token0] / 2
        )
        reserve1 = multicall["reserve1" + receipt_token] / 100 ** (
            token_to_decimals[token1] / 2
        )
        receipt_token_to_underlying_token_to_amount[receipt_token] = {
            receipt_token: reserve0,
            token1: reserve1,
        }

    return receipt_token_to_total_supply, receipt_token_to_underlying_token_to_amount


if __name__ == "__main__":
    # Example of how to use the functions
    print(get_all_uni_v2_pools())
    print(get_receipt_tokens_and_composition())
