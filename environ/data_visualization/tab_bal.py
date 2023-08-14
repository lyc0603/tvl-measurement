"""
Functions to generate the balance sheet for each protocol
"""


import pandas as pd

from config.constants import TABLES_PATH


def tabulate_bal(
    ptc_name: str, df_bal: pd.DataFrame, block_num: int = 17899400
) -> None:
    """
    Function to generate LaTeX table
    """

    # header of LaTeX of balance sheet
    bal_latex = (
        r"""
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

    df_ptc = df_bal.loc[
        (df_bal["dollar_amount"] != 0) & (df_bal["protocol_name"] == ptc_name)
    ].copy()

    df_ptc.reset_index(drop=True, inplace=True)

    df_ast = df_ptc.loc[(df_ptc["entry"] == "Assets")].copy().reset_index(drop=True)
    df_liab = (
        df_ptc.loc[(df_ptc["entry"] == "Liabilities")].copy().reset_index(drop=True)
    )

    # compare the length of the two dataframe
    if len(df_ast) > len(df_liab):
        # iterate over the assets dataframe
        for idx, row in df_ast.iterrows():
            # append assets to the left two columns
            bal_latex += f"{row['token_symbol']} & {row['dollar_amount']:,.2f}"

            # try to append liabilities
            try:
                bal_latex += f""" & {df_liab.loc[idx, 'token_symbol']} &\
{df_liab.loc[idx, 'dollar_amount']:,.2f} \\\\
"""
            except:  # pylint: disable=bare-except
                bal_latex += r""" & & \\
"""
    else:
        # iterate over the liabilities dataframe
        for idx, row in df_liab.iterrows():
            # try to append assets
            try:
                bal_latex += f"{df_ast.loc[idx, 'token_symbol']} & \
{df_ast.loc[idx, 'dollar_amount']:,.2f}"
            except:  # pylint: disable=bare-except
                bal_latex += " & "

            # append liabilities to the right two columns
            bal_latex += f""" & {row['token_symbol']} & {row['dollar_amount']:,.2f} \\\\
"""

    # append the total assets and liabilities
    bal_latex += (
        r"""
\midrule
"""
        + f"""
\\textbf{"{Total Assets}"} & \${df_ast["dollar_amount"].sum():,.2f} & \\textbf{"{Total Liabilities and Net Position}"} & \${df_liab["dollar_amount"].sum():,.2f} \\\\
"""
    )

    # footer of LaTeX of balance sheet
    bal_latex += r"""
\bottomrule

\end{longtable}
"""

    # remove " " in the protocol name
    ptc_name = ptc_name.replace(" ", "")

    # save the LaTeX table
    with open(f"{TABLES_PATH}/bal_{ptc_name}.tex", "w", encoding="utf-8") as f_tab:
        f_tab.write(bal_latex)
