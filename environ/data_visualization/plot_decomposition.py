"""
Function to plot the decomposition of the TVL
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.sankey import Sankey
from environ.data_fetching.uniswap_v2_data_fetching import query_tvl

from config.constants import DATA_PATH, TVL_LIST, PROCESSED_DATA_PATH, FIGURES_PATH

ORIENTATION_LIST = [1, 1, -1, -1, 0, -1, 1, 1, -1]


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

    tvl_dict["Uniswap_V2"] = query_tvl()

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


def plot_sankey_tvl_decompose() -> None:
    """
    Function to plot the decomposition of the TVL
    """

    # get the TVL data
    tvl_dict = load_tvl_data()

    # plot the sankey diagram
    fig = plt.figure(figsize=(6, 3))
    ax_df = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])
    sankey = Sankey(
        ax=ax_df, scale=0.01, offset=0.2, head_angle=180, format="%.1f", unit="%"
    )

    # get the TVL list
    tvl_list = list(tvl_dict.values())
    nomial_tvl = sum(tvl_list)

    # conver the TVL to percentage
    tvl_list = [i / nomial_tvl for i in tvl_list]

    # calculate the double counting stats
    tvr = nomial_tvl - 5e9
    tvl_list = tvl_list + [-tvr / nomial_tvl, -5e9 / nomial_tvl]
    flows_list = [i * 100 for i in tvl_list]

    labels_list = list(tvl_dict.keys()) + ["TVR", "Double Counting"]

    # remove "_" in the labels
    labels_list = [i.replace("_", " ") for i in labels_list]

    sankey.add(
        flows=flows_list,
        labels=labels_list,
        orientations=ORIENTATION_LIST,
        patchlabel="TVL"
        # pathlengths=[0.01] * len(flows_list),
    )

    diagrams = sankey.finish()

    # iterate through the text to change the font size
    for text in diagrams[0].texts:
        text.set_fontsize(5)
        text.set_fontweight("bold")

    # # tight layout
    # plt.tight_layout()

    # remove the frame
    plt.box(False)

    plt.show()

    # save the figure to FIGURES_PATH
    fig.savefig(f"{FIGURES_PATH}/tvl_decomposition.pdf")


if __name__ == "__main__":
    # load the TVL data
    plot_sankey_tvl_decompose()
