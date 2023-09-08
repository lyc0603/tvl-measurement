"""
Function to preprocess balance sheet data of a protocol
"""

import pandas as pd

from config.constants import DAI_ADDRESS, RWA_ASSETS_PRICES
from environ.data_fetching.aave_v2_data_fetching import (
    aave_v3_oracle,
    get_all_reserve_tokens_aave_v3,
    get_reserve_token_address_aave_v3,
)
from environ.data_fetching.makerdao_data_fetching import (
    get_collaterals_list,
    get_ilks_makerdao,
    get_info_makerdao,
)
from environ.data_fetching.web3_call import (
    get_token_balance_of,
    get_token_symbol,
    get_token_total_supply,
)

from environ.data_fetching.token_price import get_token_price_defillama


def preprocess_makerdao_bal() -> pd.DataFrame:
    """
    Function to preprocess the raw makerdao data into working balance sheet entries
    """

    bal_dict = {
        "side": [],
        "entries": [],
        "idx": [],
        "token_symbols": [],
        "token_addresses": [],
        "dollar_amount": [],
    }

    dai_prc = get_token_price_defillama(DAI_ADDRESS)

    # get all collaterals
    collaterals_list = get_collaterals_list()

    idx = 0

    for collateral_bytes in collaterals_list:
        idx += 1

        # get the collateral info
        collateral_info = get_info_makerdao(collateral_bytes)
        collateral_ilk = get_ilks_makerdao(collateral_bytes)

        symbol = collateral_info["symbol"]
        reserve = collateral_info["gem"]
        join = collateral_info["join"]

        if symbol in RWA_ASSETS_PRICES.keys():
            token_prc = RWA_ASSETS_PRICES[symbol]
        else:
            try:
                token_prc = get_token_price_defillama(reserve)
            except:  # pylint: disable=bare-except
                token_prc = 0.0

        bal_dict["side"].append("Assets")
        bal_dict["entries"].append("Reserve Token")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(symbol)
        bal_dict["token_addresses"].append(reserve)
        bal_dict["dollar_amount"].append(
            get_token_balance_of(join.lower(), reserve.lower()) * token_prc
        )

        bal_dict["side"].append("Liabilities")
        bal_dict["entries"].append("Dai")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(f"Dai from {symbol}")
        bal_dict["token_addresses"].append(DAI_ADDRESS)
        bal_dict["dollar_amount"].append(
            (collateral_ilk["Art"] * 10 ** (-18) * collateral_ilk["rate"] * 10 ** (-27))
            * dai_prc
        )

    return pd.DataFrame(bal_dict)


def preprocess_aave_v3_bal() -> pd.DataFrame:
    """
    Function to preprocess the raw aave v3 data into working balance sheet entries
    """

    bal_dict = {
        "side": [],
        "entries": [],
        "idx": [],
        "token_symbols": [],
        "token_addresses": [],
        "dollar_amount": [],
    }

    # get all reserve tokens
    reserve_tokens_list = get_all_reserve_tokens_aave_v3()

    idx = 0

    for reserve_token_symbol, reserve_token in reserve_tokens_list:
        idx += 1

        # get the oracle price
        oracle_price = aave_v3_oracle(reserve_token)

        # get the reserve configuration data (aToken / stableDebtToken / variableDebtToken)
        config_data = get_reserve_token_address_aave_v3(reserve_token)

        atoken, stable_debt_token, variable_debt_token = (
            config_data["aTokenAddress"],
            config_data["stableDebtTokenAddress"],
            config_data["variableDebtTokenAddress"],
        )

        dollar_amount = (
            get_token_balance_of(atoken.lower(), reserve_token.lower()) * oracle_price
        )
        bal_dict["side"].append("Assets")
        bal_dict["entries"].append("Reserve Token")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(reserve_token_symbol)
        bal_dict["token_addresses"].append(reserve_token)
        bal_dict["dollar_amount"].append(dollar_amount)

        dollar_amount = get_token_total_supply(atoken.lower()) * oracle_price
        bal_dict["side"].append("Liabilities")
        bal_dict["entries"].append("aToken")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(get_token_symbol(atoken.lower()))
        bal_dict["token_addresses"].append(atoken)
        bal_dict["dollar_amount"].append(dollar_amount)

        dollar_amount = get_token_total_supply(stable_debt_token.lower()) * oracle_price
        bal_dict["side"].append("Assets")
        bal_dict["entries"].append("Stable Debt Token")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(get_token_symbol(stable_debt_token.lower()))
        bal_dict["token_addresses"].append(stable_debt_token)
        bal_dict["dollar_amount"].append(dollar_amount)

        dollar_amount = (
            get_token_total_supply(variable_debt_token.lower()) * oracle_price
        )
        bal_dict["side"].append("Assets")
        bal_dict["entries"].append("Variable Debt Token")
        bal_dict["idx"].append(idx)
        bal_dict["token_symbols"].append(get_token_symbol(variable_debt_token.lower()))
        bal_dict["token_addresses"].append(variable_debt_token)
        bal_dict["dollar_amount"].append(dollar_amount)

    return pd.DataFrame(bal_dict)


if __name__ == "__main__":
    preprocess_aave_v3_bal()
    # preprocess_makerdao_bal()
