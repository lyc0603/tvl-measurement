"""
Script to preprocess the protocol token decomposition data
"""

import pandas as pd

from config.constants import PROCESSED_DATA_PATH

PTC_TOKEN_DECOMPO_STAKE_PLOT = {
    "makerdao": pd.DataFrame(),
    "uniswap-v3": pd.DataFrame(),
    "aave-v3": pd.DataFrame(),
}

for ptc_slug, ptc_df in PTC_TOKEN_DECOMPO_STAKE_PLOT.items():
    df_token = pd.read_csv(
        f"{PROCESSED_DATA_PATH}/defillama/defillama_token_decomp_{ptc_slug}.csv"
    )
    df_token["date"] = pd.to_datetime(
        pd.to_datetime(df_token["date"]).dt.strftime("%Y-%m-%d")
    )
    df_token = df_token.sort_values(by=["date"])

    # get the top tokens with the highest TVL in average
    df_token_top = (
        df_token.groupby(["token"])["token_tvl_usd"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    # get the top 10 tokens
    top_token_lst = df_token_top["token"].head(5).tolist()

    # filter the data
    df_token_top = df_token.loc[df_token["token"].isin(top_token_lst)]
    df_token_others = df_token.loc[~df_token["token"].isin(top_token_lst)]

    # sum up others
    df_token_others = (
        df_token_others.groupby(["date"])["token_tvl_usd"].sum().reset_index()
    )

    df_token_others["token"] = "Others"
    df_token_others = df_token_others[["date", "token", "token_tvl_usd"]]

    # append others to the top tokens
    df_token = pd.concat([df_token_top, df_token_others])

    # pivot the data
    df_token = df_token.pivot(index="date", columns="token", values="token_tvl_usd")

    # rename the columns WETH as ETH/WETH
    df_token = df_token.rename(columns={"WETH": "ETH/WETH"})

    PTC_TOKEN_DECOMPO_STAKE_PLOT[ptc_slug] = df_token
