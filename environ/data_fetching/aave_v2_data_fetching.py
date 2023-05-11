"""
Fetch all aave V2 pools
"""

from multicall import Call, Multicall

from config import constants
from environ.data_fetching import web3_call
from environ.utils import info_logger


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get the list of all the receipt tokens
    """

    # Call the contract
    atokens_list = Call(
        constants.AAVE2_PROTOCOL_DATA_PROVIDER_ADDRESS,
        ["getAllATokens()((string,address)[])"],
        [["list", None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()["list"]

    # Get the contract addresses of underlying tokens
    underlying_tokens = [token_address[1] for token_address in atokens_list]

    # Info log
    info_logger.print_info_log("AAVE list of aToken sucessfully fecthed", "success")

    return underlying_tokens


def get_receipt_tokens_and_composition() -> (
    tuple[dict[str, int], dict[str, dict[str, int]]]
):
    """
    Function to get the total supply of all compositions
    """

    # Get the list of all the receipt tokens
    atokens = get_all_receipt_tokens()

    # Get the total supply of all the receipt tokens
    receipt_token_to_total_supply = web3_call.get_tokens_total_supply(atokens)

    # Call list for multicall
    call_list = []

    # Get the underlying token address for each receipt token
    for atoken in atokens:
        call_list.append(
            Call(
                atoken,
                ["UNDERLYING_ASSET_ADDRESS()(address)"],
                [[atoken, None]],  # type: ignore
            )
        )

    # Get the underlying token address for each receipt token
    receipt_tokens_to_underlying_token = Multicall(call_list, _w3=web3_call.eth_w3)()

    # Get the composition of each receipt token
    receipt_token_to_composition = {}

    # Get the composition of each receipt token
    for atoken, underlying in receipt_tokens_to_underlying_token.items():
        receipt_token_to_composition[atoken] = {
            underlying: receipt_token_to_total_supply[atoken]
        }
    return receipt_token_to_total_supply, receipt_token_to_composition


if __name__ == "__main__":
    # Test
    print(get_all_receipt_tokens())
    # print(get_receipt_tokens_and_composition())
