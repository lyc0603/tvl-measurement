"""
Fetch the balancer-related data from the graph
"""

from multicall import Call, Multicall
from tqdm import tqdm

from config import constants
from environ.data_fetching import subgraph_query, web3_call
from environ.data_fetching.web3_call import get_token_total_supply


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get all the receipt tokens from the balancer subgraph
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
    for liquidity_pool in tqdm(liquidity_pools_info, desc="Fetching Balancer data"):
        receipt_token_to_total_supply[liquidity_pool["id"]] = (
            # int(liquidity_pool["outputTokenSupply"])
            # / 10 ** liquidity_pool["outputToken"]["decimals"]
            get_token_actual_supply(liquidity_pool["id"])
        )
        underlying_token_to_amount = {}

        # TODO: check whether there are negative value in amount
        for i, underlying_token in enumerate(liquidity_pool["inputTokens"]):
            underlying_token_to_amount[underlying_token["id"]] = abs(
                int(liquidity_pool["inputTokenBalances"][i])
                / 10 ** liquidity_pool["inputTokens"][i]["decimals"]
            )
        receipt_token_to_composition[liquidity_pool["id"]] = underlying_token_to_amount
    return receipt_token_to_total_supply, receipt_token_to_composition


def get_token_actual_supply(token_address: str) -> float:
    """
    Function to get the actual supply of the token
    in boosted pools such as bb-a-usd
    """

    # One possble way to get the actual supply of the token
    try:
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

    except:  # pylint: disable=bare-except
        pass
    else:
        return multicall["actualSupply"] / 10 ** multicall["decimals"]

    # Another possible way to get the actual supply of the token
    # For example 0xA13a9247ea42D743238089903570127DdA72fE44
    try:
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
    except:  # pylint: disable=bare-except
        pass
    else:
        return multicall["virtualSupply"] / 10 ** multicall["decimals"]

    # final general method
    return get_token_total_supply(token_address)


def balancer_subgraph_token_price(
    token_address: str,
) -> float:
    """
    Function to get the price of the token from balancer subgraph
    e.g. such as TempleDAO, BagerDAO
    """

    # call the graph
    data_json = subgraph_query.run_query_var(
        http=constants.BALANCER_URL,
        query_scripts=constants.BALANCER_TOKEN_PRICE_QUERY,
        var={"id": token_address},
    )

    return float(data_json["data"]["token"]["latestUSDPrice"])


if __name__ == "__main__":
    # test
    # save the data to a json file
    # with open(
    #     f"{constants.DATA_PATH}/composition/balancer.json", "w", encoding="utf-8"
    # ) as f:
    #     json.dump(get_receipt_tokens_and_composition(), f, indent=4)

    # print(get_receipt_tokens_and_composition())
    # print(get_token_actual_supply("0x5c6ee304399dbdb9c8ef030ab642b10820db8f56".lower()))
    print(balancer_subgraph_token_price("0x50cf90b954958480b8df7958a9e965752f627124"))
