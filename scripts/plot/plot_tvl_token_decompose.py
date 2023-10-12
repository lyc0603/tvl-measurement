"""
Script to plot the stacked bar chart of TVL
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker

from config.constants import FIGURES_PATH
from scripts.process.preprocess_ptc_token_decompose import PTC_TOKEN_DECOMPO_STAKE_PLOT

for ptc_slug, df_token in PTC_TOKEN_DECOMPO_STAKE_PLOT.items():
    # convert the date to string
    df_token.index = pd.to_datetime(df_token.index.strftime("%Y-%m-%d"))

    # plot the stacked line graph
    df_token.plot(kind="area", stacked=True, figsize=(5, 2), alpha=0.8)

    # remove "token" from the legend
    plt.legend(loc="upper left", ncol=2, title="")

    # x axis in the format of %Y-%m-%d
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # control the frequency of the x axisnj
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(len(df_token.index) // 20))

    # set the unit of the y axis
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.0f}B".format(x / 1e9))
    )
    # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=1e9))

    # add grid
    plt.grid()

    # limit setting
    plt.xlim(df_token.index.min(), df_token.index.max())

    # add x , y label
    plt.xlabel("")
    plt.ylabel("Dollar Amount")

    # rotate the xticks
    plt.xticks(rotation=90)

    # tight layout
    plt.tight_layout()

    # save the figure to the figure path
    plt.savefig(f"{FIGURES_PATH}/defillama_tvl_token_decompose_{ptc_slug}.pdf", dpi=400)
