"""
Functions to process the data of TVL decomposition sankey plot
"""

import pandas as pd

NAMING_DICT = {
    "curve-dex": "Curve",
    "makerdao": "MakerDAO",
    "convex-finance": "Convex",
    "aave-v2": "Aave V2",
    "lido": "Lido",
    "wbtc": "WBTC",
    "Others": "Others",
}


def tvl_decompose_sankey_data(
    tvl_total_df: pd.DataFrame, tvr_total_df: pd.DataFrame, date: str
) -> dict[str, list]:
    """
    Function to process the data of TVL decomposition sankey plot
    """

    # isolate the tvl data
    tvl_plot_df = tvl_total_df.loc[tvl_total_df["date"] == date]
    tvl_top_tive = (
        tvl_plot_df.sort_values(["totalLiquidityUSD"], ascending=False)
        .iloc[:4, :]
        .copy()
    )

    tvl_other_ptc = (
        tvl_plot_df.sort_values(["totalLiquidityUSD"], ascending=False)
        .iloc[4:, :]
        .copy()
    )
    tvl_other_ptc = (
        tvl_other_ptc.groupby(["date"])["totalLiquidityUSD"].sum().reset_index()
    )
    tvl_other_ptc["protocol"] = "Others"
    tvl_plot_df = pd.concat([tvl_top_tive, tvl_other_ptc], ignore_index=True)

    total_tvl = tvl_plot_df["totalLiquidityUSD"].sum()

    # isolate the tvr data
    tvr_plot_df = tvr_total_df.loc[tvr_total_df["date"] == date]
    tvr_plot_df = (
        tvr_plot_df.groupby(["date"])[["tvr", "gov", "native", "stable"]]
        .sum()
        .reset_index()
    )
    total_tvr = tvr_plot_df["tvr"].sum()

    flows_list = [
        tvl_plot_df["totalLiquidityUSD"].to_list()
        + [
            -total_tvr,
            -(total_tvl - total_tvr),
        ],
        [total_tvr] + list(-tvr_plot_df.values[0][2:]),
    ]

    return {
        "flows": [[_ * 100 / total_tvl for _ in flows] for flows in flows_list],
        "labels": [
            [NAMING_DICT[slug] for slug in tvl_plot_df["protocol"].to_list()]
            + ["TVR", "Double Counting"],
            ["TVR"] + tvr_plot_df.keys()[2:].to_list(),
        ],
        "orientations": [[1, 1, -1, -1, 0, 0, -1], [0, 1, 1, -1]],
    }
