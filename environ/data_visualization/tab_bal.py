"""
Functions to generate the balance sheet for each protocol
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import DATA_PATH, TABLES_PATH
from environ.data_fetching.token_price import get_token_price_defillama
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


def tabulate_bal(
    ptc_name: str, df_bal: pd.DataFrame, block_num: int = 1691593279
) -> None:
    """
    Function to generate LaTeX table
    """

    # header of LaTeX of balance sheet
    bal_latex = (
        r"""
\begin{table}
\centering
\caption{Balance Sheet of MakerDAO}
\label{tab:bal}

\begin{longtable}{@{}p{0.25\linewidth}p{0.25\linewidth}p{0.25\linewidth}p{0.25\linewidth}@{}}

\toprule

"""
        + f"""
& Block {block_num} & & Block {block_num} \\\\
"""
        + r"""
\midrule
\textit{Assets} & & \textit{Liabilities and Net Position} \\
"""
    )

    print(df_bal)
    df_bal = df_bal.loc[df_bal["dollar_amount"] != 0]

    df_ast = df_bal.loc[df_bal["entry"] == "Assets"].copy().reset_index(drop=True)
    df_liab = df_bal.loc[df_bal["entry"] == "Liabilities"].copy().reset_index(drop=True)

    # compare the length of the two dataframe
    if len(df_ast) > len(df_liab):
        # iterate over the assets dataframe
        for idx, row in df_ast.iterrows():
            # append assets to the left two columns
            bal_latex += f"{row['token_symbol']} & {row['dollar_amount']:.2f}"

            # try to append liabilities
            try:
                bal_latex += f""" & {df_liab.loc[idx, 'token_symbol']} &\
{df_liab.loc[idx, 'dollar_amount']:.2f} \\\\
"""
            except:  # pylint: disable=bare-except
                bal_latex += r""" & & \\
"""
    else:
        # iterate over the liabilities dataframe
        for idx, row in df_liab.iterrows():
            # append liabilities to the right two columns
            bal_latex += f"{df_ast.loc[idx, 'token_symbol']} &\
{df_ast.loc[idx, 'dollar_amount']:.2f}"

            # try to append assets
            try:
                bal_latex += f"""& {row['token_symbol']} & {row['dollar_amount']:.2f} \\\\
"""
            except:  # pylint: disable=bare-except
                bal_latex += r""" & & \\
"""

    # append the total assets and liabilities
    bal_latex += (
        r"""
\midrule
"""
        + f"""
\\textbf{"{Total Assets}"} & \${df_ast["dollar_amount"].sum():.2f} & \\textbf{"{Total Liabilities and Net Position}"} & \${df_liab["dollar_amount"].sum():.2f} \\\\
"""
    )

    # footer of LaTeX of balance sheet
    bal_latex += r"""
\bottomrule

\end{longtable}

\end{table}
"""

    # save the LaTeX table
    with open(f"{TABLES_PATH}/bal_{ptc_name}.tex", "w", encoding="utf-8") as f:
        f.write(bal_latex)


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
    for token_contract in tqdm(df_bal["token_contract"].unique()):
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

        # preprocess the dollar amount
        try:
            df_bal.loc[
                df_bal["token_contract"] == token_contract, "dollar_amount"
            ] = df_bal.loc[
                df_bal["token_contract"] == token_contract, "token_quantity"
            ] * get_token_price_defillama(
                token_address=token_contract
            )
        except Exception as e:  # pylint: disable=bare-except
            print(e)
            df_bal.loc[df_bal["token_contract"] == token_contract, "dollar_amount"] = (
                df_bal.loc[df_bal["token_contract"] == token_contract, "token_quantity"]
                * 0
            )

    df_bal.sort_values(by="dollar_amount", ascending=False, inplace=True)
    df_bal.drop(columns=["token_quantity"], inplace=True)

    # calculate the net position
    df_bal = pd.concat(
        [
            df_bal,
            pd.DataFrame(
                {
                    "protocol_name": ["MakerDAO"],
                    "entry": ["Liabilities"],
                    "token_symbol": ["Net Position"],
                    "dollar_amount": [
                        df_bal.loc[df_bal["entry"] == "Assets", "dollar_amount"].sum()
                        - df_bal.loc[
                            df_bal["entry"] == "Liabilities", "dollar_amount"
                        ].sum()
                    ],
                }
            ),
        ],
    )

    tabulate_bal(ptc_name="MakerDAO", df_bal=df_bal)

    print(df_bal)
    print(
        "Liabilities: ",
        df_bal.loc[df_bal["entry"] == "Liabilities", "dollar_amount"].sum(),
    )
    print("Assets: ", df_bal.loc[df_bal["entry"] == "Assets", "dollar_amount"].sum())
