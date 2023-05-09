"""
Fetch Uniswap V2 data via the graph
"""

from environ.data_fetching import subgraph_query
from config.constants import (
    UNISWAP_V3_SUBGRAPH_ID,
    UNISWAP_POOLS_QUERY,
    MAXIMUM_LP_COUNT_UNISWAP_V3,
)


def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, dict[str, int]]):
    """
    Function to decompose the receipt tokens into their underlying tokens
    for the Uniswap V3 protocol
    """

    # Query the graph
    json_response = subgraph_query.query_the_graph(
        UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID
    )

    # Parse the response
    liquidity_pools_info = json_response["data"]["liquidityPools"]

    # Dict of receipt token address to total supply
    # Dict of underlying token address to amount of underlying token
    receipt_token_to_total_supply = {}
    receipt_token_to_composition = {}

    # Count of the number of LPs
    count = 0

    # Iterate over the liquidity pools
    for liquidity_pool in liquidity_pools_info:
        # If we have not reached the maximum number of LPs
        if count < MAXIMUM_LP_COUNT_UNISWAP_V3:
            count += 1

            # Add the receipt token to the dict
            receipt_token_to_total_supply[liquidity_pool["id"]] = 1
            underlying_token_to_amount = {}
            for i, underlying_token in enumerate(liquidity_pool["inputTokens"]):
                underlying_token_to_amount[underlying_token["id"]] = (
                    int(liquidity_pool["inputTokenBalances"][i])
                    / 10 ** liquidity_pool["inputTokens"][i]["decimals"]
                )
            receipt_token_to_composition[
                liquidity_pool["id"]
            ] = underlying_token_to_amount

    return receipt_token_to_total_supply, receipt_token_to_composition


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get all receipt tokens for the Uniswap V3 protocol
    """

    # Query the graph
    json_response = subgraph_query.query_the_graph(
        UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID
    )

    # Parse the response
    liquidity_pools_info = json_response["data"]["liquidityPools"]

    # List of receipt tokens
    receipt_tokens = []

    # Iterate over the liquidity pools
    for liquidity_pool in liquidity_pools_info:
        receipt_tokens.append(liquidity_pool["id"])

    return receipt_tokens


if __name__ == "__main__":
    # example usage
    # print(get_all_receipt_tokens())
    print(get_receipt_tokens_and_composition())
