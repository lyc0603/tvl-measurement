"""
Functions to fetch the data from the Yearn
"""

from multicall import Multicall, Call
from environ.data_fetching import web3_call
from config import constants


def get_vaults_list() -> list[str]:
    """
    Function to get the list of vaults
    """
    return list(
        Call(
            constants.YREGISTRY_ADDRESS,
            ["getVaults()(address[])"],
            [["vaults", None]],
            _w3=web3_call.eth_w3,
        )()["vaults"]
    )


def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, dict[str, int]]):
    """
    Function to get the receipt tokens and their composition
    """

    # get the list of vaults
    receipt_tokens = get_vaults_list()

    receipt_token_to_total_supply = {}
    receipt_token_to_composition = {}

    # get the total supply of each receipt token
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
                receipt_token, ["token()(address)"], [["token " + receipt_token, None]]
            )
        )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # get the tokens' decimals
    underlying_tokens = []
    for receipt_token in receipt_tokens:
        token_address = multicall["token " + receipt_token]
        underlying_tokens.append(token_address)
    tokens_to_decimals = web3_call.get_tokens_to_decimals(
        underlying_tokens + list(receipt_tokens)
    )

    # Returns the price of the Vault’s wrapped token,
    # denominated in the unwrapped native token.
    price_per_share = {}
    call_list = []
    for receipt_token in receipt_tokens:
        # if no supply, set price to 0
        if multicall["totalSupply " + receipt_token] == 0:
            price_per_share[receipt_token] = 0
            continue
        call_list.append(
            Call(
                receipt_token,
                ["getPricePerFullShare()(uint256)"],
                [[receipt_token, None]],
            )
        )
    multicall2 = Multicall(call_list, _w3=web3_call.eth_w3)()
    for receipt_token, p_p_p in multicall2.items():
        price_per_share[receipt_token] = p_p_p / 10 ** tokens_to_decimals[receipt_token]

    # Totay supply times price per share gives the quantity of the underlying token
    for receipt_token in receipt_tokens:
        total_supply = multicall["totalSupply " + receipt_token]
        receipt_token_to_total_supply[receipt_token] = (
            total_supply / 10 ** tokens_to_decimals[receipt_token]
        )
        underlying_to_amount = {}
        underlying_token = multicall["token " + receipt_token]
        amount = (
            price_per_share[receipt_token]
            * total_supply
            / 10 ** tokens_to_decimals[underlying_token]
        )
        underlying_to_amount[underlying_token] = amount
        receipt_token_to_composition[receipt_token] = underlying_to_amount
    return receipt_token_to_total_supply, receipt_token_to_composition


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get the list of all receipt tokens
    """
    return get_vaults_list()


if __name__ == "__main__":
    print(get_vaults_list())
