"""
Fetch Uniswap V2 data directly from the blockchain
"""

from multicall import Call, Multicall
from tqdm import tqdm
import pandas as pd

from environ.data_fetching.web3_call import (
    eth_w3,
    get_tokens_total_supply,
    get_tokens_to_decimals,
)
from environ.data_fetching.subgraph_query import run_query, run_query_var
from environ.utils import info_logger
from config.constants import (
    UNISWAP_V2_FACTORY_ADDRESS,
    MAXIMUM_LP_COUNT_UNISWAP_V2,
    UNISWAP_V2_URL,
    UNISWAP_V2_POOLS_QUERY_DICT,
    DATA_PATH,
    UNISWAP_V2_POOL_TVL_QUERY,
)


def query_tvl() -> float:
    """
    Function to query the TVL of Uniswap V2
    """

    # get the response json
    json_response = run_query(
        http=UNISWAP_V2_URL, query_scripts=UNISWAP_V2_POOL_TVL_QUERY
    )

    # get the TVL
    return float(json_response["data"]["uniswapDayDatas"][0]["totalLiquidityUSD"])


def _query_pairs_first_batch() -> pd.DataFrame:
    """
    Internal function to query the first batch of pair data
    """

    # get the response json
    json_response = run_query(
        http=UNISWAP_V2_URL,
        query_scripts=UNISWAP_V2_POOLS_QUERY_DICT["first_batch"],
    )

    # convert the json to a dataframe
    return pd.json_normalize(json_response["data"]["pairs"])


def _query_pairs_following_batch(id_gt: str) -> pd.DataFrame:
    """
    Internal function to query the following batches of pair data
    """

    # get the response json
    json_response = run_query_var(
        http=UNISWAP_V2_URL,
        query_scripts=UNISWAP_V2_POOLS_QUERY_DICT["following_batch"],
        var={"id_gt": id_gt},
    )

    # convert the json to a dataframe
    return pd.json_normalize(json_response["data"]["pairs"])


def get_all_uni_v2_pools_subgraph(
    save_path: str = f"{DATA_PATH}/composition/uniswap_v2.csv",
) -> None:
    """
    Function to get the data of all Uniswap V2 pools
    """

    # a list to store the dataframes
    df_list = []

    # length of the list and the batch number
    length = 0
    batch_number = 0

    # query the first batch
    df_first_batch = _query_pairs_first_batch()

    # append the first batch to the list
    df_list.append(df_first_batch)

    # get the id of the last pair in the first batch
    id_gt = df_first_batch.tail(1)["id"].values[0]

    # get the length of the first batch
    length = len(df_first_batch)

    # query the following batches
    while length == 1000:
        try:
            df_following_batch = _query_pairs_following_batch(id_gt)
            df_list.append(df_following_batch)
            id_gt = df_following_batch.tail(1)["id"].values[0]
            length = len(df_following_batch)
            batch_number += 1
            print(f"Batch {batch_number} finished")
        except:  # pylint: disable=bare-except
            print("Query failed, retrying...")

    # concat the dataframes
    df_pair = pd.concat(df_list)

    # save the dataframe to data path
    df_pair.to_csv(save_path, index=False)


def get_receipt_tokens_and_composition(
    load_path: str = f"{DATA_PATH}/composition/uniswap_v2.csv",
) -> (dict[str, int], dict[str, [str, int]]):
    """
    This function returns two dictionaries: one with the total supply and
    the other with the composition of all Uniswap V2 pools
    """

    # load the dataframe
    df_pair = pd.read_csv(load_path)

    # two dictionaries to store the data
    receipt_token_to_total_supply = {}
    receipt_token_to_underlying_token_to_amount = {}

    # filter out the abnormal value
    df_pair = df_pair.loc[df_pair["reserveUSD"] != "Wrapped Ether"]
    df_pair = df_pair.loc[df_pair["reserve1"] != "LAEEB"]

    # filter out the pools with non-zero reserve
    df_pair = df_pair.loc[(df_pair["reserve0"] != 0) & (df_pair["reserve1"] != 0)]

    # fill in the missing values with 0 for all the columns
    df_pair = df_pair.fillna(0)

    # iterate through the dataframe
    for _, row in tqdm(df_pair.iterrows(), total=len(df_pair)):
        # get the receipt token and the underlying tokens
        receipt_token_to_total_supply[row["id"]] = float(row["totalSupply"])
        receipt_token_to_underlying_token_to_amount[row["id"]] = {
            row["token0.id"]: float(row["reserve0"]),
            row["token1.id"]: float(row["reserve1"]),
        }

    return receipt_token_to_total_supply, receipt_token_to_underlying_token_to_amount


# def get_total_number_of_uni_v2_pools() -> int:
#     """
#     Get the total number of Uniswap V2 pools
#     """

#     # Info log
#     info_logger.print_info_log("Fetch the total number of Uniswap V2 pools", "success")

#     # The document of the multicall function is here:
#     # https://github.com/banteg/multicall.py
#     total_number_of_uni_v2_pools = Call(
#         UNISWAP_V2_FACTORY_ADDRESS,
#         ["allPairsLength()(uint256)"],
#         [["allPairsLength", None]],
#         _w3=eth_w3,
#     )()["allPairsLength"]

#     return total_number_of_uni_v2_pools


# def get_all_uni_v2_pools() -> list[str]:
#     """
#     Fetch the list of all uniswap V2 pools
#     """

#     # Info log
#     info_logger.print_info_log("Fetch list of all uniswap V2 pools", "success")

#     pool_num = get_total_number_of_uni_v2_pools()
#     call_list = []

#     # Fetch the list of a maximum of MAXIMUM_LP_COUNT_UNISWAP_V2 pools Returns the
#     # address of the nth pair (0-indexed) created through the factory, or address(0)
#     # (0x0000000000000000000000000000000000000000) if not enough pairs have been created yet.
#     for pool_idx in tqdm(range(0, min(pool_num, MAXIMUM_LP_COUNT_UNISWAP_V2))):
#         # The list of all pairs is stored in a mapping
#         call_list.append(
#             Call(
#                 UNISWAP_V2_FACTORY_ADDRESS,
#                 ["allPairs(uint256)(address)", pool_idx],
#                 [["pair" + str(pool_idx), None]],
#             )
#         )

#         # Call the multicall contract
#         multicall = Multicall(call_list, _w3=eth_w3)()

#     return multicall.values()


# def get_all_receipt_tokens() -> list[str]:
#     """
#     Function to get the list of all receipt tokens
#     """

#     return get_all_uni_v2_pools()


# def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, [str, int]]):
#     """
#     This function returns two dictionaries: one with the total supply and
#     the other with the composition of all Uniswap V2 pools
#     """

#     # Get the list of all Uniswap V2 pools
#     uniswap_v2_tokens = get_all_uni_v2_pools()

#     # Info log
#     info_logger.print_info_log("Fetch all uniswap V2 pools", "success")

#     # Get the total supply of all Uniswap V2 pools
#     receipt_token_to_total_supply = get_tokens_total_supply(uniswap_v2_tokens)

#     # Get the composition of all Uniswap V2 pools
#     receipt_token_to_underlying_token_to_amount = {}
#     call_list = []

#     for receipt_token in uniswap_v2_tokens:
#         # Call the method of the Uniswap V2 pool contract
#         # to get the composition of the pool
#         call_list.append(
#             Call(
#                 receipt_token,
#                 [
#                     "token0()(address)",
#                 ],
#                 [["token0" + receipt_token, None]],
#             )
#         )
#         call_list.append(
#             Call(
#                 receipt_token,
#                 [
#                     "token1()(address)",
#                 ],
#                 [["token1" + receipt_token, None]],
#             )
#         )
#         # Returns the reserves of token0 and token1 used to price trades and distribute liquidity. See Pricing.
#         # Also returns the block.timestamp (mod 2**32) of the last block during which an interaction occured for the pair.
#         call_list.append(
#             Call(
#                 receipt_token,
#                 [
#                     "getReserves()(uint112,uint112,uint32)",
#                 ],
#                 [
#                     ["reserve0" + receipt_token, None],
#                     ["reserve1" + receipt_token, None],
#                 ],
#             )
#         )
#     # Constuct the dictionary of the composition of the pool
#     multicall = Multicall(call_list, _w3=eth_w3)()
#     token_list = []

#     for receipt_token in tqdm(uniswap_v2_tokens):
#         token0 = multicall["token0" + receipt_token]
#         token1 = multicall["token1" + receipt_token]
#         token_list.append(token0)
#         token_list.append(token1)
#     token_to_decimals = get_tokens_to_decimals(token_list)
#     for receipt_token in uniswap_v2_tokens:
#         token0 = multicall["token0" + receipt_token]
#         token1 = multicall["token1" + receipt_token]

#         # 100 ** (n / 2) == 10 ** n
#         reserve0 = multicall["reserve0" + receipt_token] / 100 ** (
#             token_to_decimals[token0] / 2
#         )
#         reserve1 = multicall["reserve1" + receipt_token] / 100 ** (
#             token_to_decimals[token1] / 2
#         )
#         receipt_token_to_underlying_token_to_amount[receipt_token] = {
#             token0: reserve0,
#             token1: reserve1,
#         }

#     return receipt_token_to_total_supply, receipt_token_to_underlying_token_to_amount


if __name__ == "__main__":
    # Example of how to use the functions
    # print(get_total_number_of_uni_v2_pools())
    # print(get_all_uni_v2_pools())
    # print(get_receipt_tokens_and_composition())
    # print(_query_pairs_first_batch())
    # print(_query_pairs_following_batch("0x0000871c95bb027c90089f4926fd1ba82cdd9a8b"))
    # print(get_all_uni_v2_pools_subgraph())
    print(query_tvl())
