"""
Script to render token category tab
"""
import pandas as pd
from scripts.process_token_lst import df_token_cate
from config.constants import TABLES_PATH

import warnings

warnings.filterwarnings("ignore")

# iterate through unique category in df_token_cate
for cate in df_token_cate["category"].unique():
    cate_name = cate.lower().replace(" ", "_")

    # filter df_token_cate by cate
    df_cate = df_token_cate[df_token_cate["category"] == cate]

    # if cate is not Stablecoins, drop stable_type column
    if cate != "Stablecoins":
        df_cate = df_cate.drop(columns=["stable_type"])

    # change smart contract column to be a link to etherscan
    for index, row in df_cate.iterrows():
        token_address = row["token_address"]
        symbol = row["symbol"]

        df_cate.loc[
            index, "symbol"
        ] = f"\\href{{https://etherscan.io/address/{token_address}}}{{\\tt {symbol}}}"

    # drop category column
    df_cate = df_cate.drop(columns=["category", "token_address"])

    # sort df_cate by name
    df_cate.columns = (
        ["Name", "Symbol"] if cate != "Stablecoins" else ["Name", "Symbol", "Type"]
    )

    # render df_cate
    with pd.option_context("max_colwidth", 1000):
        df_cate.to_latex(
            f"{TABLES_PATH}/{cate_name}_list.tex",
            escape=False,
            index=False,
        )
