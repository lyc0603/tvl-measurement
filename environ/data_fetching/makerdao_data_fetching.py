"""
Function to fetch MakerDAO data directly from the blockchain
"""

import json

from multicall import Call, Multicall

from config import collateral, constants
from environ.data_fetching import web3_call


def get_all_receipt_tokens() -> list[str]:
    """
    Function to get the address of DAI
    """
    return [constants.DAI_ADDRESS]


def get_collaterals_list() -> list:
    """
    Function to get the collateral list
    """

    # Get the number of collateral assets
    collateral_assets_count = Call(
        constants.ILK_REGISTRY_ADDRESS,
        ["count()(uint256)"],
        [["count", None]],
        _w3=web3_call.eth_w3,
    )()["count"]

    # Iterate through the collateral assets to get hex
    # Hex can be converted to string
    collateral_type_list = Call(
        constants.ILK_REGISTRY_ADDRESS,
        ["list()(bytes32[])"],
        [["list", None]],
        _w3=web3_call.eth_w3,
    )(0, collateral_assets_count - 1)["list"]

    return collateral_type_list


def get_collaterals_info(
    collateral_type_list: list[bytes],
) -> dict[bytes, collateral.CollateralInfo]:
    """
    Function to get the token price from oracles (spot * mat)
    """
    info_list_call = []
    for collateral_type in collateral_type_list:
        # call the ILK Registry contract to get the collateral info
        # info(bytes32 ilk): return information about an ilk
        # name: token name (string)
        # symbol: token symbol (string)
        # dec: token decimals (uint256)
        # gem: token address
        # pip: price feed
        # join: token join adapter
        # flip: ilk flipper

        info_list_call.append(
            Call(
                constants.ILK_REGISTRY_ADDRESS,
                [
                    "info(bytes32)(string,string,uint256,uint256,address,address,address,address)",
                    collateral_type,
                ],
                [
                    ["name" + str(collateral_type), None],
                    ["symbol" + str(collateral_type), None],
                    ["class" + str(collateral_type), None],
                    ["dec" + str(collateral_type), None],
                    ["gem" + str(collateral_type), None],
                    ["pip" + str(collateral_type), None],
                    ["join" + str(collateral_type), None],
                ],
            )
        )

    # store the info into the class
    ilks_info_multicall_data = Multicall(info_list_call, _w3=web3_call.eth_w3)()
    collateral_type_to_info = dict()
    for collateral_type in collateral_type_list:
        collateral_type_to_info[collateral_type] = collateral.CollateralInfo(
            ilks_info_multicall_data["name" + str(collateral_type)],
            ilks_info_multicall_data["symbol" + str(collateral_type)],
            ilks_info_multicall_data["class" + str(collateral_type)],
            ilks_info_multicall_data["dec" + str(collateral_type)],
            ilks_info_multicall_data["gem" + str(collateral_type)],
            ilks_info_multicall_data["pip" + str(collateral_type)],
            ilks_info_multicall_data["join" + str(collateral_type)],
        )
    return collateral_type_to_info


def get_collaterals_data(
    collateral_type_list: list[bytes],
) -> dict[bytes, collateral.CollateralData]:
    """
    Function to get the collateral data
    """
    data_list_call = []
    for collateral_type in collateral_type_list:
        # call the Vat contract (core accounting contract) to get the collateral data
        data_list_call.append(
            Call(
                constants.VAT_ADDRESS,
                [
                    "ilks(bytes32)(uint256,uint256,uint256,uint256,uint256)",
                    collateral_type,
                ],
                [
                    ["Art" + str(collateral_type), None],
                    ["rate" + str(collateral_type), None],
                    ["spot" + str(collateral_type), None],
                    ["line" + str(collateral_type), None],
                    ["dust" + str(collateral_type), None],
                ],
            )
        )
    ilks_data_multicall_data = Multicall(data_list_call, _w3=web3_call.eth_w3)()
    collateral_type_to_data = dict()
    for collateral_type in collateral_type_list:
        collateral_type_to_data[collateral_type] = collateral.CollateralData(
            web3_call.from_wad(ilks_data_multicall_data["Art" + str(collateral_type)]),
            web3_call.from_ray(ilks_data_multicall_data["rate" + str(collateral_type)]),
            web3_call.from_ray(ilks_data_multicall_data["spot" + str(collateral_type)]),
            web3_call.from_ray(ilks_data_multicall_data["line" + str(collateral_type)]),
            web3_call.from_wad(ilks_data_multicall_data["dust" + str(collateral_type)]),
        )
    return collateral_type_to_data


def get_collateral_to_info_and_data() -> (dict, dict, dict):
    """
    Function to get the collateral info and data
    """
    collateral_type_list = get_collaterals_list()
    collateral_type_to_info = get_collaterals_info(collateral_type_list)
    collateral_type_to_data = get_collaterals_data(collateral_type_list)

    return collateral_type_list, collateral_type_to_info, collateral_type_to_data


def get_receipt_tokens_and_composition() -> (
    dict[str, int],
    dict[str, dict[str, int]],
):
    """
    Function to get the receipt tokens and compositions
    Because the receipt tokens are DAI, we need to get the pool composition
    """

    # get the total supply of the receipt tokens
    receipt_token_to_total_supply = dict()

    # get the total supply of DAI
    receipt_token_to_total_supply[
        constants.DAI_ADDRESS
    ] = web3_call.get_token_total_supply(constants.DAI_ADDRESS)

    # get the information of the collateral types
    receipt_token_to_composition = dict()
    receipt_token_to_composition[constants.DAI_ADDRESS] = dict()
    (
        collateral_type_list,
        collateral_type_to_info,
        collateral_type_to_data,
    ) = get_collateral_to_info_and_data()

    # create a list to store the token join (join adapter) and token gem (address)
    join_to_token = dict()
    for collateral_type in collateral_type_list:
        # join = collateral_type_to_info[collateral_type].join
        # token_to_join[collateral_type_to_info[collateral_type].gem] = join
        join = collateral_type_to_info[collateral_type].join
        join_to_token[join] = collateral_type_to_info[collateral_type].gem

    tokens_to_balances = web3_call.get_token_balance_of_multiple_account(join_to_token)
    for token, balance in tokens_to_balances.items():
        # if the balance is 0, we need to get the staked balance
        if balance == 0:
            # iterate through the join adapters to get the staked balance
            staked_balance = 0
            for join in join_to_token.keys():
                if token == join_to_token[join]:
                    try:
                        staked_balance += Call(
                            token_to_join[token],
                            ["total()(uint256)"],
                            [["total", None]],
                            _w3=web3_call.eth_w3,
                        )()["total"] / 10 ** web3_call.get_token_decimals(token)
                    except:
                        staked_balance += 0
            tokens_to_balances[token] = staked_balance

        # if the balance is still 0, we need to get the pooled balance
        if tokens_to_balances.get(token, 0) == 0:
            pooled_balance = 0
            for join in join_to_token.keys():
                if token == join_to_token[join]:
                    try:
                        direct_pool_address = Call(
                            token_to_join[token],
                            ["pool(bytes32)(address)", collateral_type],
                            [["pool", None]],
                            _w3=web3_call.eth_w3,
                        )()["pool"]
                        pooled_balance += web3_call.get_token_balance_of(
                            direct_pool_address, token
                        )
                    except:
                        pooled_balance += 0
            tokens_to_balances[token] = pooled_balance

    # for collateral_type in collateral_type_list:
    #     if collateral_type_to_data[collateral_type].Art > 10:
    #         collateral_address = collateral_type_to_info[collateral_type].gem
    #         collateral_amount = tokens_to_balances[collateral_address]
    #         receipt_token_to_composition[constants.DAI_ADDRESS][collateral_address] = (
    #             receipt_token_to_composition[constants.DAI_ADDRESS].get(
    #                 collateral_address, 0
    #             )
    #             + collateral_amount
    #         )

    # create a list to check duplicated collateral types
    collateral_type_to_check = []

    for collateral_type in collateral_type_list:
        if collateral_type_to_data[collateral_type].Art > 10:
            collateral_address = collateral_type_to_info[collateral_type].gem

            # check if the collateral type is duplicated
            if collateral_address in collateral_type_to_check:
                continue
            else:
                collateral_type_to_check.append(collateral_address)
            collateral_amount = tokens_to_balances[collateral_address]
            receipt_token_to_composition[constants.DAI_ADDRESS][collateral_address] = (
                receipt_token_to_composition[constants.DAI_ADDRESS].get(
                    collateral_address, 0
                )
                + collateral_amount
            )
    return receipt_token_to_total_supply, receipt_token_to_composition


def get_tokens_to_collateralization_ratio(
    collateral_list: list[bytes],
) -> dict[str, float]:
    """
    Function to get the tokens to collateralization ratio
    """
    tokens_to_collateralization_ratio = dict()
    call_list = []
    for collateral_type in collateral_list:
        call_list.append(
            Call(
                constants.MCD_SPOT_ADDRESS,
                ["ilks(bytes32)(address,uint256)", collateral_type],
                [
                    ["pip" + str(collateral_type), None],
                    ["mat" + str(collateral_type), None],
                ],
            )
        )
    multicall_data = Multicall(call_list, _w3=web3_call.eth_w3)()
    for collateral_type in collateral_list:
        tokens_to_collateralization_ratio[collateral_type] = web3_call.from_ray(
            multicall_data["mat" + str(collateral_type)]
        )
    return tokens_to_collateralization_ratio


def get_makerdao_tokens_to_spot_price() -> dict:
    """
    Function to get the makerdao tokens to spot price
    """
    (
        collateral_type_list,
        collateral_type_to_info,
        collateral_type_to_data,
    ) = get_collateral_to_info_and_data()
    tokens_to_collateralization_ratio = get_tokens_to_collateralization_ratio(
        collateral_type_list
    )
    tokens_to_spot_price = dict()
    for collateral_type in collateral_type_list:
        tokens_to_spot_price[collateral_type_to_info[collateral_type].gem] = (
            collateral_type_to_data[collateral_type].spot
            * tokens_to_collateralization_ratio[collateral_type]
        )
    return tokens_to_spot_price


if __name__ == "__main__":
    # print(get_collaterals_list())
    # print(get_collaterals_info(get_collaterals_list()))
    # print(get_collateral_to_info_and_data())
    print(get_receipt_tokens_and_composition())
    with open(
        f"{constants.DATA_PATH}/composition/MakerDAO.json",
        "w",
        encoding="utf-8",
    ) as f_json:
        json.dump(get_receipt_tokens_and_composition(), f_json, indent=4)
