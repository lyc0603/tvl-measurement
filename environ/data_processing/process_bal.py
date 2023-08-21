"""
Functions to process the balance sheet
"""

import pandas as pd


def remove_no_info(
    df_bal: pd.DataFrame, dict_compo: dict, token_contract: str
) -> pd.DataFrame:
    """
    Function to remove the rows with no token price info
    """

    for ptc_name, ptc_lst in dict_compo.items():
        for receipt_token, underlying_token_dict in ptc_lst[1].items():
            underlying_token_lst = [token for token, _ in underlying_token_dict.items()]

            if (token_contract == receipt_token) | (
                token_contract in underlying_token_lst
            ):
                df_bal = df_bal.loc[
                    ~(
                        (
                            (df_bal["protocol_name"] == ptc_name)
                            & (df_bal["entry"] == "Liabilities")
                            & (df_bal["token_contract"] == receipt_token)
                            & (
                                df_bal["related_token"].apply(lambda x: set(x))
                                == set(underlying_token_lst)
                            )
                        )
                        | (
                            (df_bal["protocol_name"] == ptc_name)
                            & (df_bal["entry"] == "Assets")
                            & (df_bal["token_contract"].isin(underlying_token_lst))
                            & (
                                df_bal["related_token"].apply(lambda x: set(x))
                                == set([receipt_token])
                            )
                        )
                    )
                ]

    return df_bal


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
        "related_token": [],
    }

    # iterate over the deri_dict
    for deri_token, deri_quantity in deri_dict.items():
        protocol_name_lst = []
        entry_lst = []
        token_contract_lst = []
        token_quantity_lst = []
        related_token_lst = []

        quantity_sum = 0

        if deri_quantity != 0:
            for receipt_token, receipt_quantity in receipt_dict[deri_token].items():
                quantity_sum += receipt_quantity
                # append the receipt token
                if receipt_quantity != 0:
                    protocol_name_lst.append(ptc_dict_name)
                    entry_lst.append("Assets")
                    token_contract_lst.append(receipt_token)
                    token_quantity_lst.append(receipt_quantity)
                    related_token_lst.append([deri_token])

            # append the derivative token
            protocol_name_lst.append(ptc_dict_name)
            entry_lst.append("Liabilities")
            token_contract_lst.append(deri_token)
            token_quantity_lst.append(deri_quantity)
            related_token_lst.append(
                [token for token, _ in receipt_dict[deri_token].items()]
            )

            if quantity_sum != 0:
                dict_bal["protocol_name"].extend(protocol_name_lst)
                dict_bal["entry"].extend(entry_lst)
                dict_bal["token_contract"].extend(token_contract_lst)
                dict_bal["token_quantity"].extend(token_quantity_lst)
                dict_bal["related_token"].extend(related_token_lst)

    return pd.DataFrame(dict_bal)
