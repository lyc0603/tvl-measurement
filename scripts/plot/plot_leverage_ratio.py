"""
Script to plot the laverage ratio
"""


import matplotlib.pyplot as plt

from config.constants import (
    CHAIN_LIST,
    FIGURES_PATH,
)
from environ.data_processing.preprocess_tvl import (
    preprocess_ptc_tvl,
)

for chain in CHAIN_LIST:
    # set the figure size
    plt.figure(figsize=(6, 4))

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

    # calculate the leverage ratio

    plt.plot(
        df_agg["date"],
        df_agg["totalLiquidityUSD"] / df_agg["tvr"],
        label="Leverage Ratio",
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
    plt.savefig(f"{FIGURES_PATH}/leverage_ratio_{chain}.pdf", dpi=300)

    # show the plot
    plt.show()

    # close the plot
    plt.close()
