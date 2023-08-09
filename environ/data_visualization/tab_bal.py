"""
Functions to generate the balance sheet for each protocol
"""

import pandas as pd
import json
from config.constants import DATA_PATH


def preprocess_tvl_compo(
    dict_compo: dict,
    df_compo: pd.DataFrame,
    ptc_dict_name: str = "MakerDAO",
    compo_name: str = "MAKER",
) -> None:
    """
    Function to tabulate the balance sheet
    """

    # extract the given protocol
    deri_dict, receipt_dict = dict_compo[ptc_dict_name]

    dict_bal = {
        "entry": [],
        "token_symbol": [],
        "token_quantity": [],
    }

    # iterate over the receipt_dict
    for deri_token, receipt_token_dict in receipt_dict.items():
        # apped the derivative token
        dict_bal["entry"].append("Liabilities")
        dict_bal["token_symbol"].append(deri_token)
        dict_bal["token_quantity"].append(deri_dict[deri_token])


if __name__ == "__main__":
    # load the json file
    with open(
        f"{DATA_PATH}/composition/defi_compo.json", encoding="utf-8"
    ) as compo_json:
        dict_compo = json.load(compo_json)

    print(dict_compo)
