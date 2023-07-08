"""
Script to plot the total TVL, total TVL without double counting, and TVR of the protocol
"""


import matplotlib.pyplot as plt
import pandas as pd

from config.constants import (
    CHAIN_LIST,
    END_OF_SAMPLE_PERIOD,
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
)
from environ.data_fetching.fetch_llama_tvl import fetch_llama_total_tvl
from environ.data_processing.preprocess_total_tvl import preprocess_total_tvl

for chain in CHAIN_LIST:
    # set the figure size
    plt.figure(figsize=(6, 4))

    # load the total tvl data
    total_tvl_eth_without_double_counting = fetch_llama_total_tvl(
        chain=chain,
    )

    # convert json to dataframe
    total_tvl_eth_without_double_counting_df = pd.DataFrame(
        total_tvl_eth_without_double_counting
    )

    # convert the timestamp to datetime
    total_tvl_eth_without_double_counting_df["date"] = pd.to_datetime(
        total_tvl_eth_without_double_counting_df["date"],
        unit="s",
    )

    # only keep the data before 20223-07-01
    total_tvl_eth_without_double_counting_df = total_tvl_eth_without_double_counting_df[
        total_tvl_eth_without_double_counting_df["date"] < END_OF_SAMPLE_PERIOD
    ]

    # plot the total tvl
    plt.plot(
        total_tvl_eth_without_double_counting_df["date"],
        total_tvl_eth_without_double_counting_df["tvl"],
        label="$TVL$",
    )

    # load the total tvl data
    df_tvl_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all_{chain}.csv"
    )

    # load the total tvr data
    df_tvr_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv"
    )

    # plot the total tvl without double counting and tvr
    plt.plot(
        df_tvl_all["date"],
        df_tvl_all["totalLiquidityUSD"],
        label="$TVL_{DC}$",
    )

    # plot the tvr
    plt.plot(
        df_tvr_all["date"],
        df_tvr_all["tvr"],
        label="$TVR$",
    )

    # show the legend
    plt.legend()

    # if the chain is total, make the ticks and legend smaller
    if chain == "Total":
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend(loc="upper left", prop={"size": 8})
    else:
        # if the chain is not total, make the ticks and legend bigger
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.legend(loc="upper left", prop={"size": 11})

    # rotate the xticks
    plt.xticks(rotation=45)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(f"{FIGURES_PATH}/tvl_{chain}.pdf", dpi=300)

    # show the plot
    plt.show()

    # close the plot
    plt.close()
