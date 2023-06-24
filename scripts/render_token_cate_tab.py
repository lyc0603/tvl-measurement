"""
Script to render token category tab
"""
import pandas as pd
from scripts.process_token_lst import df_token_cate
from config.constants import TABLES_PATH

# iterate through unique category in df_token_cate
for cate in df_token_cate["category"].unique():
    cate_name = cate.lower().replace(" ", "_")

    # filter df_token_cate by cate
    df_cate = df_token_cate[df_token_cate["category"] == cate]

    # drop category column
    df_cate = df_cate.drop(columns=["category"])

    # if cate is not Stablecoins, drop stable_type column
    if cate != "Stablecoins":
        df_cate = df_cate.drop(columns=["stable_type"])

    # sort df_cate by name
    df_cate.columns = (
        ["Name", "Symbol", "Token Address"]
        if cate != "Stablecoins"
        else ["Name", "Symbol", "Token Address", "Type"]
    )

    # change smart contract column to be a link to etherscan
    df_cate["Token Address"] = df_cate["Token Address"].apply(
        lambda x: f"\\href{{https://etherscan.io/address/{x}}}{{\\tt {x}}}"
    )

    # render df_cate
    with pd.option_context("max_colwidth", 1000):
        df_cate.to_latex(
            f"{TABLES_PATH}/{cate_name}_list.tex",
            escape=False,
            index=False,
        )
