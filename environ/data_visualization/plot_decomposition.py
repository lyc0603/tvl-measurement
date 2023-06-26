"""
Function to plot the decomposition of the TVL
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.sankey import Sankey
from environ.data_fetching.uniswap_v2_data_fetching import query_tvl

from config.constants import DATA_PATH, TVL_LIST, PROCESSED_DATA_PATH, FIGURES_PATH

ORIENTATION_LIST = [1, 1, -1, -1, 0, -1, 1, 0, -1]
TEXT_POS_DICT = {
    0: [-0.3, 0.95],  # Aave V2
    1: [-1.0, 0.95],  # Balancer
    2: [-1.8, -0.6],  # Yearn
    3: [-1.0, -0.95],  # Curve
    4: [-1.8, -0.1],  # Maker
    5: [-0.1, -0.95],  # Compound
    6: [-1.8, 0.4],  # Uniswap V2
    # 7: [0.85, 0.95],  # TVR
    8: [1, -0.95],  # Double Counting
}

TEXT_POS_DICT_2 = {
    1: [2.0, 0.9],  # Governance Tokens
    3: [2.5, -0.3],  # Non-crypto-backed Stablecoins
    4: [1.6, -0.3],  # Wrapped Tokens
}


def load_tvl_data() -> dict:
    """
    Function to load the TVL data
    """

    # initialize the dictionary
    tvl_dict = {}

    # loop through the TVL list
    for tvl in TVL_LIST:
        # load the data
        tvl_dict[tvl] = pd.read_csv(
            f"{DATA_PATH}/tvl/tvl_composition_Origin.{tvl}.csv"
        )["total_value"].sum()

    # tvl_dict["Uniswap_V2"] = query_tvl()
    tvl_dict["Uniswap_V2"] = 1.19e9

    # return the dictionary
    return tvl_dict


def load_double_counting_data() -> float:
    """
    Function to load the double counting data
    """

    # load the data
    return pd.read_csv(f"{PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv")[
        "flow_usd"
    ].sum()


def plot_sankey_tvl_decompose(
    tvr_data_path: str = f"{PROCESSED_DATA_PATH}/non_derivative/non_derivative_usd.csv",
) -> None:
    """
    Function to plot the decomposition of the TVL
    """

    # get the TVL data
    tvl_dict = load_tvl_data()

    # plot the sankey diagram
    fig = plt.figure(figsize=(10, 5))
    ax_df = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])
    sankey = Sankey(
        ax=ax_df, scale=0.01, offset=0.2, head_angle=180, format="%.1f", unit="%"
    )

    # get the TVL list
    tvl_list = list(tvl_dict.values())
    nomial_tvl = sum(tvl_list)

    # load the TVR data
    tvr_df = pd.read_csv(tvr_data_path)
    tvr = tvr_df.loc[
        tvr_df["category"].isin(
            ["Wrapped Tokens", "ETH", "Stablecoins", "Governance Tokens"]
        )
    ]["flow_usd"].sum()

    # conver the TVL to percentage
    tvl_list = [i / nomial_tvl for i in tvl_list]

    # calculate the double counting stats
    double_counting_usd = nomial_tvl - tvr
    tvl_list = tvl_list + [-tvr / nomial_tvl, -double_counting_usd / nomial_tvl]
    flows_list = [i * 100 for i in tvl_list]

    labels_list = list(tvl_dict.keys()) + ["TVR", "Double Counting"]

    # remove "_" in the labels
    labels_list = [i.replace("_", " ") for i in labels_list]

    sankey.add(
        flows=flows_list,
        labels=labels_list,
        orientations=ORIENTATION_LIST,
        patchlabel="TVL",
        label="TVL",
        # pathlengths=[0.01] * len(flows_list),
    )

    # decomposite the TVR
    tvr_gov = tvr_df.loc[tvr_df["category"] == "Governance Tokens"]["flow_usd"].sum()
    tvr_eth = tvr_df.loc[tvr_df["category"] == "ETH"]["flow_usd"].sum()
    tvr_stable = tvr_df.loc[tvr_df["category"] == "Stablecoins"]["flow_usd"].sum()
    tvr_wrapped = tvr_df.loc[tvr_df["category"] == "Wrapped Tokens"]["flow_usd"].sum()

    tvr_list = [tvr, -tvr_gov, -tvr_eth, -tvr_stable, -tvr_wrapped]
    tvr_list = [i / nomial_tvl * 100 for i in tvr_list]
    labels_list = [
        "",
        "Governance Tokens",
        "ETH",
        "Non-crypto-backed\nStablecoins",
        "Wrapped Tokens",
    ]
    sankey.add(
        flows=tvr_list,
        labels=labels_list,
        orientations=[0, 1, 0, -1, -1],
        # patchlabel="TVR",
        label="TVR",
        prior=0,
        connect=(7, 0),
    )

    diagrams = sankey.finish()

    # iterate through the text to change the font size
    for text in diagrams[0].texts:
        text.set_fontsize(10)
        text.set_fontweight("bold")

    for text in diagrams[1].texts:
        text.set_fontsize(10)
        text.set_fontweight("bold")

    # text position
    for key, value in TEXT_POS_DICT.items():
        diagrams[0].texts[key].set_position(xy=value)

    for key, value in TEXT_POS_DICT_2.items():
        diagrams[1].texts[key].set_position(xy=value)

    # tight layout
    plt.tight_layout()

    # remove the frame
    plt.box(False)

    # add the legend to the right bottom
    plt.legend(
        loc="lower right",
        bbox_to_anchor=(0.9, 0.1),
    )

    plt.show()

    # save the figure to FIGURES_PATH
    fig.savefig(f"{FIGURES_PATH}/tvl_decomposition.pdf")


if __name__ == "__main__":
    # load the TVL data
    plot_sankey_tvl_decompose(
        tvr_data_path=f"{PROCESSED_DATA_PATH}/non_derivative/non_derivative_usd.csv",
    )
