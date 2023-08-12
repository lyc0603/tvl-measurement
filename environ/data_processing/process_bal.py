"""
Functions to process the balance sheet
"""

import pandas as pd


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
        "protocol_name": [],
        "entry": [],
        "token_contract": [],
        "token_quantity": [],
    }

    # iterate over the receipt_dict
    for deri_token, receipt_token_dict in receipt_dict.items():
        # apped the derivative token
        dict_bal["protocol_name"].append(ptc_dict_name)
        dict_bal["entry"].append("Liabilities")
        dict_bal["token_contract"].append(deri_token)
        dict_bal["token_quantity"].append(deri_dict[deri_token])

        # iterate over the receipt token dict
        for receipt_token, quantity in receipt_token_dict.items():
            # append the receipt token
            dict_bal["protocol_name"].append(ptc_dict_name)
            dict_bal["entry"].append("Assets")
            dict_bal["token_contract"].append(receipt_token)
            dict_bal["token_quantity"].append(quantity)
    return pd.DataFrame(dict_bal)
