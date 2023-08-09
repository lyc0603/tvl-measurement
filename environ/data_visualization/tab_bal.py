"""
Functions to generate the balance sheet for each protocol
"""

import json

import pandas as pd

from config.constants import DATA_PATH
from environ.data_fetching.web3_call import get_token_symbol


def preprocess_tvl_compo(
    dict_compo: dict,
    ptc_dict_name: str = "MakerDAO",
) -> pd.DataFrame:
    """
    Function to tabulate the balance sheet
    """

    # extract the given protocol
    deri_dict, receipt_dict = dict_compo[ptc_dict_name]

    dict_bal = {
        "entry": [],
        "token_contract": [],
        "token_quantity": [],
    }

    # iterate over the receipt_dict
    for deri_token, receipt_token_dict in receipt_dict.items():
        # apped the derivative token
        dict_bal["entry"].append("Liabilities")
        dict_bal["token_contract"].append(deri_token)
        dict_bal["token_quantity"].append(deri_dict[deri_token])

        # iterate over the receipt token dict
        for receipt_token, quantity in receipt_token_dict.items():
            # append the receipt token
            dict_bal["entry"].append("Assets")
            dict_bal["token_contract"].append(receipt_token)
            dict_bal["token_quantity"].append(quantity)
    return pd.DataFrame(dict_bal)


def preprocess_token_symbol(
    df_bal: pd.DataFrame, df_compo: pd.DataFrame
) -> pd.DataFrame:
    """
    Function to preprocess the token symbol in the balance sheet
    """

    # iterate over the df_bal
    for token_contract in df_bal["token_contract"].unique():
        try:
            df_bal.loc[
                df_bal["token_contract"] == token_contract, "token_symbol"
            ] = df_compo.loc[
                df_compo["token_contract"] == token_contract, "token_symbol"
            ].values[
                0
            ]
        except:  # pylint: disable=bare-except
            df_bal.loc[
                df_bal["token_contract"] == token_contract, "token_symbol"
            ] = get_token_symbol(token_address=token_contract)

    print(df_bal)

    return df_bal


if __name__ == "__main__":
    # load the json file
    with open(
        f"{DATA_PATH}/composition/defi_compo.json", encoding="utf-8"
    ) as compo_json:
        dict_compo = json.load(compo_json)

    # load the composition dataframe
    df_compo = pd.read_csv(f"{DATA_PATH}/tvl/tvl_composition_Origin.MAKER.csv")

    # preprocess the composition dataframe
    df_bal = preprocess_tvl_compo(dict_compo=dict_compo, ptc_dict_name="MakerDAO")

    # preprocess the token symbol
    df_bal = preprocess_token_symbol(df_bal=df_bal, df_compo=df_compo)
