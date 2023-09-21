"""
Function to plot the decomposition of the tvl time series
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from config.constants import (
    CHAIN_LIST,
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
)
from environ.data_processing.preprocess_tvl import preprocess_total_tvl

for chain in CHAIN_LIST:
    print(chain)

    # set the figure size
    plt.figure(figsize=(5, 2))

    # load the total tvr data
    df_tvr_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv"
    )

    # plot the staked tvl
    plt.stackplot(
        df_tvr_all["date"],
        df_tvr_all["stable"],
        df_tvr_all["wrap"],
        df_tvr_all["gov"],
        df_tvr_all["native"],
        labels=[
            "Non-crypto-backed Stablecoins",
            "Wrapped Tokens",
            "Governance Tokens",
            "Native Tokens",
        ],
    )

    # show the legend on the upper left corner
    plt.legend(loc="upper left")

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # set the unit of the x axis
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m"),
    )
    plt.gca().xaxis.set_major_locator(
        mdates.MonthLocator(interval=2),
    )

    # label the y axis
    plt.ylabel("Dollar Amount", fontsize=6)

    # set the unit of the y axis
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.0f}B".format(x / 1e9))
    )
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=50e9))

    # if the chain is total, make the ticks and legend smaller
    if chain == "Total":
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        plt.legend(prop={"size": 6})
    else:
        # if the chain is not total, make the ticks and legend bigger
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        plt.legend(prop={"size": 6})

    # rotate the xticks
    plt.xticks(rotation=90)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(f"{FIGURES_PATH}/tvr_stack_{chain}.pdf", dpi=300)

    # show the plot
    plt.show()

    # close the plot
    plt.close()
