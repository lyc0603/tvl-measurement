"""
Functions to fetch data from the Compound V2
"""

from multicall import Call, Multicall
from tqdm import tqdm
from environ.data_fetching import web3_call
from config import constants


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get all the receipt tokens
    """
    # Call the Comptroller contract to get all the cTokens
    ctokens = Call(
        constants.COMPTROLLER_ADDRESS,
        ["getAllMarkets()(address[])"],
        [["ctokens", None]],
        _w3=web3_call.eth_w3,
    )()["ctokens"]
    return ctokens


def get_receipt_tokens_and_composition() -> (
    dict[str, int],
    dict[str, dict[str, int]],
):
    """
    Functions to get the total supply of receipt tokens and the composition of receipt tokens
    """
    # Get the list of all the receipt tokens
    receipt_tokens = get_all_receipt_tokens()
    receipt_token_to_total_supply = web3_call.get_tokens_total_supply(receipt_tokens)
    receipt_token_to_composition = {}
    call_list = []

    # Get the underlying token of each receipt token
    for receipt_token in tqdm(receipt_tokens):
        call_list.append(
            Call(
                receipt_token,
                ["underlying()(address)"],
                [[receipt_token, None]],
            )
        )
    receipt_token_to_underlying = Multicall(call_list, _w3=web3_call.eth_w3)()
    call_list = []
    for receipt_token, underlying_token in tqdm(receipt_token_to_underlying.items()):
        # Get the exchange rate and divisor of each receipt token
        call_list.append(
            Call(
                receipt_token,
                ["getCash()(uint256)"],
                [["getCash" + receipt_token, None]],
            )
        )
        if underlying_token is not None:
            # cETH is a special case without decimals and underlying_tokens
            call_list.append(
                Call(
                    underlying_token,
                    ["decimals()(uint8)"],
                    [["decimals" + underlying_token, None]],
                )
            )
        else:
            receipt_token_to_underlying[receipt_token] = "ETH"
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # Calculate the reserve of each underlying token
    for receipt_token, underlying_token in receipt_token_to_underlying.items():
        if underlying_token == "ETH":
            get_cash = multicall["getCash" + receipt_token]
            receipt_token_to_composition[receipt_token] = {
                underlying_token: get_cash / 10**18
            }
            continue
        get_cash = multicall["getCash" + receipt_token]
        decimals = multicall["decimals" + underlying_token]
        receipt_token_to_composition[receipt_token] = {
            underlying_token: get_cash / 10**decimals
        }
    return receipt_token_to_total_supply, receipt_token_to_composition


if __name__ == "__main__":
    # Test the functions
    print(get_receipt_tokens_and_composition())
