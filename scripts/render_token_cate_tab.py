"""
Script to render token category tab
"""
import pandas as pd
from scripts.process_token_lst import df_token_cate
from config.constants import TABLES_PATH

# iterate through unique category in df_token_cate
for cate in df_token_cate["category"].unique():
    # filter df_token_cate by cate
    df_cate = df_token_cate[df_token_cate["category"] == cate]

    # drop category column
    df_cate = df_cate.drop(columns=["category"])

    # sort df_cate by name
    df_cate.columns = ["Name", "Symbol", "Token Address"]

    # render df_cate
    with pd.option_context("max_colwidth", 1000):
        df_cate.to_latex(
            f"{TABLES_PATH}/{cate}_list.tex",
            escape=False,
            index=False,
        )
