"""
Fetch Uniswap V2 data via the graph
"""

import pandas as pd

from config.constants import (
    MAXIMUM_LP_COUNT_UNISWAP_V3,
    UNISWAP_POOLS_QUERY,
    UNISWAP_V3_SUBGRAPH_ID,
    UNISWAP_V3_TOKENS_QUERY_DICT,
    UNISWAP_V3_URL,
)
from environ.data_fetching import subgraph_query
from multicall import Call, Multicall
from environ.data_fetching import web3_call


def _query_tokens_first_batch() -> pd.DataFrame:
    """
    Function to query the first batch of token data
    """

    # get the response json
    json_response = subgraph_query.run_query(
        http=UNISWAP_V3_URL,
        query_scripts=UNISWAP_V3_TOKENS_QUERY_DICT["first_batch"],
    )

    # convert the json to a dataframe
    return pd.json_normalize(json_response["data"]["pools"])


def _query_tokens_following_batch(id_gt: str) -> pd.DataFrame:
    """
    Function to query the following batches of token data
    """

    # get the response json
    json_response = subgraph_query.run_query_var(
        http=UNISWAP_V3_URL,
        query_scripts=UNISWAP_V3_TOKENS_QUERY_DICT["following_batch"],
        var={"id_gt": id_gt},
    )

    # convert the json to a dataframe
    return pd.json_normalize(json_response["data"]["pools"])


def get_all_uni_v3_tokens_subgraph() -> list[str]:
    """
    Function to get the data of all Uniswap V3 tokens
    """
    # a list to store the dataframes
    df_list = []

    # length of the list and the batch number
    length = 0
    batch_num = 0

    # query the first batch
    df_first_batch = _query_tokens_first_batch()

    # append the first batch to the list
    df_list.append(df_first_batch)

    # update the length
    length = len(df_first_batch)

    # get the last id of the first batch
    last_id = df_first_batch.tail(1)["id"].values[0]

    while length == 1000:
        try:
            # query the next batch
            df_next_batch = _query_tokens_following_batch(id_gt=last_id)

            # append the next batch to the list
            df_list.append(df_next_batch)

            # get the last id of the next batch
            last_id = df_next_batch.tail(1)["id"].values[0]

            # update the length
            length = len(df_next_batch)
            # increment the batch number
            batch_num += 1
            print(f"Batch number {batch_num} of token data fetched. ")
        except:  # pylint: disable=bare-except
            print("Query failed, retrying...")

    df_tokens = pd.concat(df_list)

    return df_tokens["id"].to_list()


def get_receipt_tokens_and_composition() -> None:
    """
    Function to get the receipt tokens and their composition
    """

    # Get the list of all Uniswap V2 tokens
    uniswap_v2_tokens = get_all_uni_v3_tokens_subgraph()

    # a list to store result
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
    # Constuct the dictionary of the composition of the pool
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    print(multicall)


# def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, dict[str, int]]):
#     """
#     Function to decompose the receipt tokens into their underlying tokens
#     for the Uniswap V3 protocol
#     """

#     # Query the graph
#     json_response = subgraph_query.query_the_graph(
#         UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID
#     )

#     # Parse the response
#     liquidity_pools_info = json_response["data"]["liquidityPools"]

#     # Dict of receipt token address to total supply
#     # Dict of underlying token address to amount of underlying token
#     receipt_token_to_total_supply = {}
#     receipt_token_to_composition = {}

#     # Count of the number of LPs
#     count = 0

#     # Iterate over the liquidity pools
#     for liquidity_pool in liquidity_pools_info:
#         # If we have not reached the maximum number of LPs
#         if count < MAXIMUM_LP_COUNT_UNISWAP_V3:
#             count += 1

#             # Add the receipt token to the dict
#             receipt_token_to_total_supply[liquidity_pool["id"]] = 1
#             underlying_token_to_amount = {}
#             for i, underlying_token in enumerate(liquidity_pool["inputTokens"]):
#                 underlying_token_to_amount[underlying_token["id"]] = (
#                     int(liquidity_pool["inputTokenBalances"][i])
#                     / 10 ** liquidity_pool["inputTokens"][i]["decimals"]
#                 )
#             receipt_token_to_composition[
#                 liquidity_pool["id"]
#             ] = underlying_token_to_amount

#     return receipt_token_to_total_supply, receipt_token_to_composition


# def get_all_receipt_tokens() -> list[str]:
#     """
#     Function to get all receipt tokens for the Uniswap V3 protocol
#     """

#     # Query the graph
#     json_response = subgraph_query.query_the_graph(
#         UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID
#     )

#     # Parse the response
#     liquidity_pools_info = json_response["data"]["liquidityPools"]

#     # List of receipt tokens
#     receipt_tokens = []

#     # Iterate over the liquidity pools
#     for liquidity_pool in liquidity_pools_info:
#         receipt_tokens.append(liquidity_pool["id"])

#     return receipt_tokens


if __name__ == "__main__":
    # example usage
    # print(get_all_receipt_tokens())
    # print(get_receipt_tokens_and_composition())
    # print(_query_tokens_first_batch())
    # print(_query_tokens_following_batch("0x0000000000004946c0e9f43f4dee607b0ef1fa1c"))
    print(get_receipt_tokens_and_composition())
