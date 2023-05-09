"""
Function to fetch curve v1 data
"""

from multicall import Call, Multicall
from environ.data_fetching import web3_call
from config import constants


def get_curve_registry() -> str:
    """
    Function to get the curve registry address
    """

    return str(
        Call(
            constants.CURVE_ADDRESS_PROVIDER_ADDRESS,
            ["get_registry()(address)"],
            [["registry", None]],
            _w3=web3_call.eth_w3,
        )()["registry"]
    )


def get_curve_pools_list() -> list[str]:
    """
    Function to get the list of curve pools
    """

    # get the curve registry address
    curve_registry_address = get_curve_registry()

    # get the pool count
    pool_count = Call(
        curve_registry_address,
        ["pool_count()(uint256)"],
        [["pool_count", None]],
        _w3=web3_call.eth_w3,
    )()["pool_count"]

    # iterate through the pool count and get the pool address
    call_list = []
    for pool_idx in range(0, pool_count):
        call_list.append(
            Call(
                curve_registry_address,
                ["pool_list(uint256)(address)", pool_idx],
                [["pool_" + str(pool_idx), None]],
            )
        )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # get the pool list
    pool_list = []
    for pool_idx in range(0, pool_count):
        pool_list.append(multicall["pool_" + str(pool_idx)])

    return pool_list


def get_vecrv_address() -> str:
    """
    Function to get the Vote-Escrowed CRV address
    """

    # Get the address of the fee distributor
    # https://curve.readthedocs.io/registry-address-provider.html
    # 4: The fee distributor. Used to distribute collected fees to veCRV holders.
    fee_distributor_address = Call(
        constants.CURVE_ADDRESS_PROVIDER_ADDRESS,
        ["get_id_info(uint256)(address)", 4],
        [["fee_distributor", None]],
        _w3=web3_call.eth_w3,
    )()["fee_distributor"]

    return Call(
        fee_distributor_address,
        ["voting_escrow()(address)"],
        [["veCRV", None]],
        _w3=web3_call.eth_w3,
    )()["veCRV"]


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get the list of all receipt tokens
    """

    # get the curve registry address and pool list
    curve_pools_list = get_curve_pools_list()
    curve_registry_address = get_curve_registry()

    # iterate through the pool list and get the receipt tokens
    call_list = []
    for curve_pool_address in curve_pools_list:
        call_list.append(
            Call(
                curve_registry_address,
                ["get_lp_token(address)(address)", curve_pool_address],
                [["lp_token" + curve_pool_address, None]],
            )
        )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # create the list of receipt tokens
    receipt_tokens = []
    for curve_pool_address in curve_pools_list:
        receipt_tokens.append(multicall["lp_token" + curve_pool_address])
    receipt_tokens.append(get_vecrv_address())
    return receipt_tokens


def get_receipt_tokens_and_composition() -> (dict[str, int], dict[str, dict[str, int]]):
    """
    Function to get the receipt tokens and their composition
    """

    curve_pools_list = get_curve_pools_list()
    curve_lp_tokens = get_all_receipt_tokens()
    curve_registry_address = get_curve_registry()

    # get the total supply of all the receipt tokens
    receipt_token_to_total_supply = web3_call.get_tokens_total_supply(curve_lp_tokens)

    # get the composition of all the receipt tokens
    # pool and lp token are separately
    call_list = []
    for curve_pool_address in curve_pools_list:
        # Get the LP token address for a given Curve pool.
        call_list.append(
            Call(
                curve_registry_address,
                ["get_lp_token(address)(address)", curve_pool_address],
                [["lp_token" + curve_pool_address, None]],
            )
        )

        # Get the number of coins and underlying coins within a pool.
        call_list.append(
            Call(
                curve_registry_address,
                ["get_n_coins(address)(uint256[2])", curve_pool_address],
                [["n_coins" + curve_pool_address, None]],
            )
        )

        # Get a list of the swappable coins within a pool.
        call_list.append(
            Call(
                curve_registry_address,
                ["get_coins(address)(address[8])", curve_pool_address],
                [["coins" + curve_pool_address, None]],
            )
        )

        # Get available balances for each coin within a pool.
        call_list.append(
            Call(
                curve_registry_address,
                ["get_balances(address)(uint256[8])", curve_pool_address],
                [["balances" + curve_pool_address, None]],
            )
        )
    multicall = Multicall(call_list, _w3=web3_call.eth_w3)()

    # get the decimals of underlying tokens
    underlying_tokens = []
    for curve_pool_address in curve_pools_list:
        n_coins = multicall["n_coins" + curve_pool_address][0]
        coins = multicall["coins" + curve_pool_address]
        for coin_idx in range(0, n_coins):
            underlying_tokens.append(coins[coin_idx])
    decimals = web3_call.get_tokens_to_decimals(underlying_tokens)

    # add ETH to the decimals dict
    decimals["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"] = 18

    # get the amount of underlying tokens in each receipt token
    receipt_token_to_underlying_tokens = {}
    for curve_pool_address in curve_pools_list:
        lp_token = multicall["lp_token" + curve_pool_address]
        receipt_token_to_underlying_tokens[lp_token] = {}
        for coin_idx in range(0, multicall["n_coins" + curve_pool_address][0]):
            coin_i = multicall["coins" + curve_pool_address][coin_idx]
            balance_i = multicall["balances" + curve_pool_address][coin_idx]
            receipt_token_to_underlying_tokens[lp_token][coin_i] = (
                balance_i / 10 ** decimals[coin_i]
            )

    # special case: add veCRV to the receipt token to underlying tokens dict
    ve_crv_address = get_vecrv_address()
    balance_of_crv = web3_call.get_token_balance_of(
        ve_crv_address, constants.CRV_ADDRESS
    )
    receipt_token_to_underlying_tokens[ve_crv_address] = {
        constants.CRV_ADDRESS: balance_of_crv
    }
    return receipt_token_to_total_supply, receipt_token_to_underlying_tokens


if __name__ == "__main__":
    # test code
    # print(get_curve_registry())
    print(get_curve_pools_list())
    # print(get_all_receipt_tokens())
    # print(get_vecrv_adress())
    # print(get_receipt_tokens_and_composition())
    pass
