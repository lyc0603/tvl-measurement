"""
Functions to fetch the data from the Yearn
"""

from multicall import Multicall, Call
from environ.data_fetching import web3_call, subgraph_query
from config import constants


def get_vaults_list() -> list[str]:
    """
    Function to get the list of vaults in the yearn
    """
    # Query the graph
    json_response = subgraph_query.run_query(
        constants.YEARN_URL,
        constants.YEARN_POOLS_QUERY,
    )

    # Get the list of vaults
    return [id["id"] for id in json_response["data"]["vaults"]]


def get_receipt_tokens_and_composition() -> None:
    """
    Function to get the receipt tokens and their composistions
    """

    # get the list of vaults
    receipt_tokens = get_vaults_list()

    receipt_token_to_total_supply = {}
    receipt_token_to_composition = {}

    # get the total assets, decimals, and underlying token of each receipt token
    call_list = []
    for receipt_token in receipt_tokens:
        call_list.append(
            Call(
                receipt_token,
                ["totalSupply()(uint256)"],
                [["totalSupply " + receipt_token, None]],
            )
        )
        call_list.append(
            Call(
                receipt_token,
                ["decimals()(uint256)"],
                [["decimals " + receipt_token, None]],
            )
        )
        call_list.append(
            Call(
                receipt_token, ["token()(address)"], [["token " + receipt_token, None]]
            )
        )

    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # calculate the total supply of each receipt token
    for receipt_token in receipt_tokens:
        receipt_token_to_total_supply[receipt_token] = multicall[
            "totalSupply " + receipt_token
        ] / (10 ** multicall["decimals " + receipt_token])

    # get the composition and composition tokens' decimals
    underlying_tokens = []
    for receipt_token in receipt_tokens:
        token_address = multicall["token " + receipt_token]
        underlying_tokens.append(token_address)
    tokens_to_decimals = web3_call.get_tokens_to_decimals(
        underlying_tokens + list(receipt_tokens)
    )

    # get the composition of each receipt token
    call_list = []
    for receipt_token in receipt_tokens:
        if receipt_token_to_total_supply[receipt_token] == 0:
            continue
        call_list.append(
            Call(
                receipt_token,
                ["totalAssets()(uint256)"],
                [[receipt_token, None]],
            )
        )
    multicall2 = Multicall(call_list, _w3=web3_call.eth_w3)()

    # calculate the composition of each receipt token
    for receipt_token in receipt_tokens:
        if receipt_token_to_total_supply[receipt_token] == 0:
            continue
        receipt_token_to_composition[receipt_token] = {}
        receipt_token_to_composition[receipt_token][
            multicall["token " + receipt_token]
        ] = multicall2[receipt_token] / (
            10 ** tokens_to_decimals[multicall["token " + receipt_token]]
        )

    return receipt_token_to_total_supply, receipt_token_to_composition


if __name__ == "__main__":
    # print(get_vaults_list())
    print(get_receipt_tokens_and_composition())
