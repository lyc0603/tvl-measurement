"""
Script to plot the total TVL, total TVL without double counting, and TVR of the protocol
"""


import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from config.constants import CHAIN_LIST, FIGURES_PATH
from environ.data_processing.preprocess_tvl import preprocess_ptc_tvl

PLOT_INFO_DICT = {
    "tvl": {"label": "$TVL$", "color": "blue"},
    "totalLiquidityUSD": {"label": "$TVL_{adj}$", "color": "red"},
    "tvr": {"label": "$TVR$", "color": "black"},
}

for chain in CHAIN_LIST:
    if chain == "Total":
        # set the figure size
        plt.figure(figsize=(5, 2))
    else:
        # set the figure size
        plt.figure(figsize=(2.5, 2))

    # load the total tvl data
    df_agg = preprocess_ptc_tvl(
        chain=chain,
    )

    # sort the dataframe by date
    df_agg = df_agg.sort_values(by="date", ascending=True)

    # if the chain is Mixin, ffill the totalLiquidityUSD in 2022-11-06 to 2022-11-08
    if chain == "Mixin":
        df_agg.loc[
            (df_agg["date"] >= "2022-11-06") & (df_agg["date"] <= "2022-11-08"),
            "totalLiquidityUSD",
        ] = df_agg.loc[
            (df_agg["date"] == "2022-11-05"),
            "totalLiquidityUSD",
        ].values[
            0
        ]

    # plot the tvl with DC, tvl, and tvr
    for col, info in PLOT_INFO_DICT.items():
        plt.plot(
            df_agg["date"],
            df_agg[col],
            label=info["label"],
            color=info["color"],
            linewidth=1,
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
    plt.savefig(f"{FIGURES_PATH}/tvl_{chain}.pdf", dpi=300)
