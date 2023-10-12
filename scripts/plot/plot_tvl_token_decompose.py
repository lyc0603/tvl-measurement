"""
Script to plot the stacked bar chart of TVL
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from config.constants import FIGURES_PATH, PROCESSED_DATA_PATH

plt.figure(figsize=(5, 2))

for ptc_slug in ["uniswap-v3", "aave-v3", "makerdao"]:
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
    top_token_lst = df_token_top["token"].head(9).tolist()

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

    # convert the date to string
    df_token.index = pd.to_datetime(df_token.index.strftime("%Y-%m-%d"))

    # plot the stacked line graph
    df_token.plot(kind="area", stacked=True)

    # remove "token" from the legend
    plt.legend(loc="upper left", ncol=2, title="")

    # x axis in the format of %Y-%m-%d
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # control the frequency of the x axisnj
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(len(df_token.index) // 30))

    # set the unit of the y axis
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.0f}B".format(x / 1e9))
    )
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=1e9))

    # add grid
    plt.grid()

    # limit setting
    plt.xlim(df_token.index.min(), df_token.index.max())

    # add x , y label
    plt.xlabel("")
    plt.ylabel("Dollar Amount")

    # rotate the xticks
    plt.xticks(rotation=90)

    # save the figure to the figure path
    plt.savefig(f"{FIGURES_PATH}/defillama_tvl_token_decompose_{ptc_slug}.pdf", dpi=400)
