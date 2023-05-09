"""
Fetch the balancer-related data from the graph
"""

from multicall import Call, Multicall

from config import constants
from environ.data_fetching import subgraph_query, web3_call


def get_all_receipt_tokens() -> list[str]:
    """
    Functio to get all the receipt tokens from the balancer subgraph
    """

    # call the graph
    json_response = subgraph_query.query_the_graph(
        constants.BALANCER_POOLS_QUERY, constants.BALANCER_SUBGRAPH_ID
    )
    liquidity_pools_info = json_response["data"]["liquidityPools"]
    receipt_tokens = []
    for liquidity_pool in liquidity_pools_info:
        receipt_tokens.append(liquidity_pool["id"])
    return receipt_tokens


def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, dict[str, int]]):
    """
    Function to get the receipt tokens and their composition from the balancer subgraph
    """

    # call the graph
    json_response = subgraph_query.query_the_graph(
        constants.BALANCER_POOLS_QUERY, constants.BALANCER_SUBGRAPH_ID
    )
    liquidity_pools_info = json_response["data"]["liquidityPools"]
    receipt_token_to_total_supply = {}
    receipt_token_to_composition = {}
    for liquidity_pool in liquidity_pools_info:
        receipt_token_to_total_supply[liquidity_pool["id"]] = (
            int(liquidity_pool["outputTokenSupply"])
            / 10 ** liquidity_pool["outputToken"]["decimals"]
        )
        underlying_token_to_amount = {}
        for i, underlying_token in enumerate(liquidity_pool["inputTokens"]):
            underlying_token_to_amount[underlying_token["id"]] = (
                int(liquidity_pool["inputTokenBalances"][i])
                / 10 ** liquidity_pool["inputTokens"][i]["decimals"]
            )
        receipt_token_to_composition[liquidity_pool["id"]] = underlying_token_to_amount
    return receipt_token_to_total_supply, receipt_token_to_composition


def get_token_actual_supply(token_address: str) -> int:
    """
    Function to get the actual supply of the token
    in boosted pools such as bb-a-usd
    """

    try:
        # One possble way to get the actual supply of the token
        multicall = Multicall(
            [
                Call(
                    token_address,
                    ["getActualSupply()(uint256)"],
                    [["actualSupply", None]],
                ),
                Call(
                    token_address,
                    ["decimals()(uint8)"],
                    [["decimals", None]],
                ),
            ],
            _w3=web3_call.eth_w3,
        )()

        return multicall["actualSupply"] / 10 ** multicall["decimals"]
    except:
        # Another possible way to get the actual supply of the token
        # For example 0xA13a9247ea42D743238089903570127DdA72fE44
        multicall = Multicall(
            [
                Call(
                    token_address,
                    ["getVirtualSupply()(uint256)"],
                    [["virtualSupply", None]],
                ),
                Call(
                    token_address,
                    ["decimals()(uint8)"],
                    [["decimals", None]],
                ),
            ],
            _w3=web3_call.eth_w3,
        )()

        return multicall["virtualSupply"] / 10 ** multicall["decimals"]


if __name__ == "__main__":
    # test
    print(get_receipt_tokens_and_composition())
    # print(get_token_actual_supply("0xA13a9247ea42D743238089903570127DdA72fE44".lower()))
