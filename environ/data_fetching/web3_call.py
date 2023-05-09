"""
Functions related to fetching data from the blockchain using web3.py
"""

from web3 import Web3
from multicall import Multicall, Call
from environ.utils import info_logger

# Constants
from config.constants import ALCHEMY_ETH_SOCKET, BURN_ADDRESS, NONSTANDARD_CONTRACTS
from config import constants


def init_web3() -> Web3:
    """
    Connect to Ethereum blockchain using web3.py
    """

    # Connect to the Ethereum blockchain
    info_logger.print_info_log("Connect to Ethereum", "progress")
    eth_w3 = Web3(Web3.HTTPProvider(ALCHEMY_ETH_SOCKET))

    # Check if connection is successful
    if eth_w3.isConnected():
        info_logger.print_info_log("Connection successful", "success")
    else:
        info_logger.print_info_log("Connection failed", "error")

    return eth_w3


eth_w3 = init_web3()

# Functions for the unit conversion


def from_wad(value: int) -> float:
    """
    Convert the value from wad to ETH
    """
    return value / 10**18


def from_ray(value: int) -> float:
    """
    Convert the value from ray to ETH
    """
    return value / 10**27


def from_rad(value: int) -> float:
    """
    Convert the value from rad to ETH
    """
    return value / 10**45


# Utility functions


def get_eth_balance(account_address: str) -> float:
    """
    Function to get the ETH balance of an account
    """
    return from_wad(eth_w3.eth.get_balance(Web3.toChecksumAddress(account_address)))


def get_token_balance_of(account_address: str, token_address: str) -> int:
    """
    Function to get the current token balance of an account
    """

    # Check if the token address is a burn address
    # If it is, return the ETH balance of the account
    if token_address in BURN_ADDRESS:
        return get_eth_balance(account_address)

    # If it is not, return the token balance of the account
    # according to standard ERC20 contract methods
    multicall = Multicall(
        [
            Call(
                token_address,
                ["balanceOf(address)(uint256)", account_address],
                [["balance", None]],
            ),
            Call(token_address, ["decimals()(uint256)"], [["decimals", None]]),
        ],
        _w3=eth_w3,
    )()

    return multicall["balance"] / 10 ** multicall["decimals"]


def get_tokens_balances_of(token_to_account: dict[str, str]) -> dict[str, str]:
    """
    Function to get the balances of multiple tokens of multiple accounts
    """
    exception_balances = {}
    call_list = []
    for token_address, account_address in token_to_account.items():
        if token_address in BURN_ADDRESS:
            # generally the address used for native ETH
            exception_balances[token_address] = get_eth_balance(account_address)
        else:
            # call the balanceOf and decimals methods of the token contract
            call_list.append(
                Call(
                    token_address,
                    ["balanceOf(address)(uint256)", account_address],
                    [[token_address + account_address, None]],
                ),
            )
            call_list.append(
                Call(
                    token_address,
                    ["decimals()(uint256)"],
                    [["decimals" + token_address, None]],
                )
            )
    multicall = Multicall(call_list, _w3=eth_w3)()
    tokens_to_balances = {}
    for token_address, account_address in token_to_account.items():
        if token_address in exception_balances:
            tokens_to_balances[token_address] = (
                tokens_to_balances.get(token_address, 0)
                + exception_balances[token_address]
            )
        else:
            tokens_to_balances[token_address] = (
                tokens_to_balances.get(token_address, 0)
                + multicall[token_address + account_address]
                / 10 ** multicall["decimals" + token_address]
            )
    return tokens_to_balances


def get_token_balance_of_multiple_account(
    account_to_token: dict[str, str]
) -> dict[str, str]:
    """
    Function to get the balances of multiple tokens of a single account
    """
    exception_balances = {}
    call_list = []
    for account_address, token_address in account_to_token.items():
        if token_address in BURN_ADDRESS:
            # generally the address used for native ETH
            exception_balances[token_address] = get_eth_balance(account_address)
        else:
            # call the balanceOf and decimals methods of the token contract
            call_list.append(
                Call(
                    token_address,
                    ["balanceOf(address)(uint256)", account_address],
                    [[token_address + account_address, None]],
                ),
            )
            call_list.append(
                Call(
                    token_address,
                    ["decimals()(uint256)"],
                    [["decimals" + token_address, None]],
                )
            )
    multicall = Multicall(call_list, _w3=eth_w3)()
    tokens_to_balances = {}
    for account_address, token_address in account_to_token.items():
        if token_address in exception_balances:
            tokens_to_balances[token_address] = (
                tokens_to_balances.get(token_address, 0)
                + exception_balances[token_address]
            )
        else:
            tokens_to_balances[token_address] = (
                tokens_to_balances.get(token_address, 0)
                + multicall[token_address + account_address]
                / 10 ** multicall["decimals" + token_address]
            )
    return tokens_to_balances


def get_token_decimals(token_address) -> int:
    """
    Function to get the token divisor
    """

    # Call ERC20 contract method to get the divisor
    multicall = Multicall(
        [Call(token_address, ["decimals()(uint8)"], [["decimals", None]])], _w3=eth_w3
    )()

    return multicall["decimals"]


def get_tokens_to_decimals(token_addresses: list[str]) -> dict[int]:
    """
    Function to get the token divisor for a list of tokens
    """
    call_list = []
    default_decimals = {}
    for token_address in token_addresses:
        if token_address in NONSTANDARD_CONTRACTS:
            default_decimals[token_address] = 18
        else:
            call_list.append(
                Call(token_address, ["decimals()(uint8)"], [[token_address, None]])
            )
    tokens_to_decimals = Multicall(call_list, _w3=eth_w3)()
    for token, decimal in default_decimals.items():
        tokens_to_decimals[token] = decimal
    return tokens_to_decimals


def get_token_total_supply(token_address) -> int:
    """
    Function to get the current total supply of a token
    """

    # Call ERC20 contract methods to get the total supply and divisor
    multicall = Multicall(
        [
            Call(token_address, ["totalSupply()(uint256)"], [["totalSupply", None]]),
            Call(token_address, ["decimals()(uint256)"], [["decimals", None]]),
        ],
        _w3=eth_w3,
    )()
    return multicall["totalSupply"] / 10 ** multicall["decimals"]


def get_tokens_total_supply(token_addresses: list[str]) -> dict[int]:
    """
    Function to get the current token supplies of multiple tokens
    """

    # create a list of multicall objects
    call_list = []

    # Loop through the token addresses
    for token_address in token_addresses:
        # Call ERC20 contract methods to get the total supply and divisor
        call_list.append(
            Call(token_address, ["totalSupply()(uint256)"], [[token_address, None]]),
        )
        call_list.append(
            Call(
                token_address,
                ["decimals()(uint256)"],
                [["decimals" + token_address, None]],
            )
        )
    multicall = Multicall(call_list, _w3=eth_w3)()

    # Create a dictionary to store the total supply of each token
    token_address_to_total_supply = {}
    for token_address in token_addresses:
        # Calculate the total supply of the token
        token_address_to_total_supply[token_address] = (
            multicall[token_address] / 10 ** multicall["decimals" + token_address]
        )
    return token_address_to_total_supply


def get_manual_addresses_to_name() -> dict[str, str]:
    """
    Manual addresses to name mapping
    """
    return {
        "eth": "Ether",
        "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "Ether",
        "0x0000000000000000000000000000000000000000": "Ether",
        constants.MKR_ADDRESS.lower(): "Maker",
        constants.SAI_ADDRESS.lower(): "Sai",
    }


def get_token_symbol(token_address: str) -> str:
    """
    Function to get the name of a token
    """
    multicall = Multicall(
        [
            Call(token_address, ["symbol()(string)"], [["symbol", None]]),
        ],
        _w3=eth_w3,
    )()
    return multicall["symbol"]


def get_token_name(token_address: str) -> str:
    """
    Function to get the name of a token
    """
    manual_addresses = get_manual_addresses_to_name()
    if token_address in manual_addresses.keys():
        return manual_addresses[token_address]
    multicall = Multicall(
        [
            Call(token_address, ["name()(string)"], [["name", None]]),
        ],
        _w3=eth_w3,
    )()
    return multicall["name"]


if __name__ == "__main__":
    # Connect to the Ethereum blockchain
    eth_w3 = init_web3()
    # print(get_eth_balance("0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"))
    # print(
    #     get_token_balance_of(
    #         "0xe025e3ca2be02316033184551d4d3aa22024d9dc".lower(),
    #         "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    #     )
    # )
    # print(
    #     get_tokens_total_supply(
    #         [
    #             "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc",
    #             "0x3139ffc91b99aa94da8a2dc13f1fc36f9bdc98ee",
    #         ]
    #     )
    # )
    # print(get_token_decimals("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"))
    # print(
    #     get_tokens_to_decimals(
    #         [
    #             "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc",
    #             "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    #         ]
    #     )
    # )
