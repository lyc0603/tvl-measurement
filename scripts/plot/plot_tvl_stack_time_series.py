"""
Function to plot the decomposition of the tvl time series
"""

import matplotlib.pyplot as plt
import pandas as pd

from config.constants import (
    CHAIN_LIST,
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
)
from environ.data_processing.preprocess_total_tvl import preprocess_total_tvl

for chain in CHAIN_LIST:
    # set the figure size
    plt.figure(figsize=(6, 4))

    # load the total tvr data
    df_tvr_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv"
    )

    # plot the staked tvl
    plt.stackplot(
        df_tvr_all["date"],
        df_tvr_all["gov"],
        df_tvr_all["wrap"],
        df_tvr_all["native"],
        df_tvr_all["stable"],
        labels=[
            "Governance Tokens",
            "Wrapped Tokens",
            "Native Tokens",
            "Non-crypto-backed Stablecoins",
        ],
    )

    # show the legend
    plt.legend()

    # if the chain is total, make the ticks and legend smaller
    if chain == "Total":
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend(prop={"size": 8})
    else:
        # if the chain is not total, make the ticks and legend bigger
        plt.xticks(fontsize=19)
        plt.yticks(fontsize=19)
        plt.legend(prop={"size": 14})

    # rotate the xticks
    plt.xticks(rotation=45)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(f"{FIGURES_PATH}/tvr_stack_{chain}.pdf", dpi=300)

    # show the plot
    plt.show()

    # close the plot
    plt.close()
