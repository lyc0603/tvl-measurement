"""
Function to plot the decomposition of the tvl time series
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


from config.constants import (
    CHAIN_LIST,
    FIGURES_PATH,
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
)
from environ.data_processing.preprocess_tvl import preprocess_total_tvl

EVENT_INFO_DICT = {
    "max_tvl": {"label": "Max TVL", "ls": "dashdot"},
    "luna_collapse": {"label": "Luna Collapse", "ls": "dashed"},
    "ftx_collapse": {"label": "FTX Collapse", "ls": "dotted"},
}

PLOT_INFO_DICT = {
    "stable": {"label": "Non-crypto-backed Stablecoins", "color": "red"},
    "gov": {"label": "Governance Tokens", "color": "orange"},
    "native": {"label": "Native Tokens", "color": "green"},
}

for chain in CHAIN_LIST:
    if chain == "Total":
        # set the figure size
        fig, axes = plt.subplots(
            figsize=(5, 2),
        )
    else:
        # set the figure size
        fig, axes = plt.subplots(
            figsize=(5, 2),
        )

    # load the total tvr data
    df_tvr_all = preprocess_total_tvl(
        df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_{chain}.csv"
    )

    # convert the data to percentage

    # for col in ["stable", "wrap", "gov", "native"]:
    for col in ["stable", "gov", "native"]:
        df_tvr_all[col] = df_tvr_all[col] / df_tvr_all["tvr"]

    # plot the staked tvl
    axes.stackplot(
        df_tvr_all["date"],
        df_tvr_all["stable"],
        # df_tvr_all["wrap"],
        df_tvr_all["gov"],
        df_tvr_all["native"],
        # labels=[
        #     "Non-crypto-backed Stablecoins",
        #     # "Wrapped Tokens",
        #     "Governance Tokens",
        #     "Native Tokens",
        # ],
        colors=[
            "red",
            # "grey",
            "orange",
            "green",
        ],
        alpha=0.5,
    )

    for event, date in SAMPLE_DATA_DICT.items():
        axes.axvline(
            pd.to_datetime(date),
            color="black",
            linewidth=1,
            # label=EVENT_INFO_DICT[event]["label"],
            ls=EVENT_INFO_DICT[event]["ls"],
        )

    # # show the legend on the upper left corner
    # plt.legend(loc="upper left")

    # # change the font size of the legend
    # plt.legend(prop={"size": 15})

    lines = axes.get_lines()
    legend1 = plt.legend(
        [
            lines[i]
            for i in [
                0,
                1,
                2,
            ]
        ],
        [info["label"] for _, info in PLOT_INFO_DICT.items()],
        frameon=False,
        loc="upper right",
        prop={"size": 6},
        title="Metrics",
        title_fontsize="7",
    )
    legend2 = plt.legend(
        [lines[i] for i in [3, 4, 5]],
        [info["label"] for _, info in EVENT_INFO_DICT.items()],
        frameon=False,
        loc="lower left",
        prop={"size": 6},
        title="Events",
        title_fontsize="7",
    )
    axes.add_artist(legend1)
    axes.add_artist(legend2)

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # set the unit of the x axis
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m"),
    )
    plt.gca().xaxis.set_major_locator(
        mdates.MonthLocator(interval=2),
    )

    # limit the x axis
    plt.xlim([df_tvr_all["date"].min(), df_tvr_all["date"].max()])

    # limit the y axis
    plt.ylim([0, 1])

    # label the y axis
    plt.ylabel("Percentage of TVR", fontsize=6)

    # set the unit of the y axis as 0.2
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.2))

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
