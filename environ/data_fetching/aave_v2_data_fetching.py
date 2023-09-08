"""
Fetch all aave V2 pools
"""

from multicall import Call, Multicall

from config import constants
from environ.data_fetching import web3_call


def aave_v3_oracle(token) -> float:
    """
    Function to get the token market price from the oracle
    """

    # Call the contract
    token_price = Call(
        constants.AAVE_V3_ORACLE,
        ["getAssetPrice(address)(uint256)", token],
        [[token, None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()[token]

    return token_price / 10**8


def get_all_atokens_aave_v3() -> list[str]:
    """
    Function to get all the atokens of aave v3
    """

    # Call the contract
    atokens_list = Call(
        constants.AAVE_V3_POOL_DATA_PROVIDER,
        ["getAllATokens()((string,address)[])"],
        [["list", None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()["list"]

    return atokens_list


def get_all_reserve_tokens_aave_v3() -> list[str]:
    """
    Function to get all reserve data of aave v3
    """

    # Call the contract
    reserve_tokens_list = Call(
        constants.AAVE_V3_POOL_DATA_PROVIDER,
        ["getAllReservesTokens()((string,address)[])"],
        [["list", None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()["list"]

    return reserve_tokens_list


def get_underlying_asset_address_aave_v3(atoken_address: str) -> str:
    """
    Function to get the underlying asset address
    """

    # Call the contract
    underlying_asset_address = Call(
        atoken_address,
        ["UNDERLYING_ASSET_ADDRESS()(address)"],
        [[atoken_address, None]],  # type: ignore
        _w3=web3_call.eth_w3,
    )()[atoken_address]

    return underlying_asset_address


def get_reserve_token_address_aave_v3(reserve_token) -> dict[str, str]:
    """
    Function to get the reserve configuration data (aToken / stableDebtToken / variableDebtToken)
    """

    # Call the contract
    reserve_token_address_data = Call(
        constants.AAVE_V3_POOL_DATA_PROVIDER,
        ["getReserveTokensAddresses(address)(address,address,address)", reserve_token],
        [
            ["aTokenAddress", None],
            ["stableDebtTokenAddress", None],
            ["variableDebtTokenAddress", None],
        ],  # type: ignore
        _w3=web3_call.eth_w3,
    )()

    return reserve_token_address_data


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
    # print(get_all_receipt_tokens())
    # print(get_underlying_asset_address("0x018008bfb33d285247A21d44E50697654f754e63"))
    # print(get_receipt_tokens_and_composition())
    # print(get_all_atokens())
    # print(get_all_reserve_tokens_aave_v3())
    print(aave_v3_oracle("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"))
    # print(get_reserve_token_address("0x6B175474E89094C44Da98b954EedeAC495271d0F"))
