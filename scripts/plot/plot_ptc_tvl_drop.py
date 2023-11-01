"""
Script to plot the sensitivity test results of protocol
"""

import matplotlib.pyplot as plt

from config.constants import FIGURES_PATH
from scripts.process.process_risk_analysis import (
    risk_plot_dict,
)

VAR_NAMING_MAPPING = {
    "TVL_Lido": "$N^{L}$",
    "liqRatio": "$\\beta$",
    "LTV": "$L$",
    "collat": "$Q^{M}$",
}

COLOR_LIST = ["red", "darkblue", "green"]


for test_var, test_var_dict in risk_plot_dict.items():
    # set the figure size
    fig, axes = plt.subplots(
        figsize=(4, 6),
    )

    ls_list = []

    for color_idx, (test_var_value, df_plot) in enumerate(test_var_dict.items()):
        PLOT_DICT = {
            "tvl": {
                "x": df_plot["eth_price"],
                "y": df_plot["tvl"],
                "label": str(test_var_value) + str(VAR_NAMING_MAPPING[test_var])
                if test_var_value != 1
                else str(VAR_NAMING_MAPPING[test_var]),
                "ls": "TVL",
            },
            "tvr": {
                "x": df_plot["eth_price"],
                "y": df_plot["tvr"],
                "label": str(test_var_value) + str(VAR_NAMING_MAPPING[test_var])
                if test_var_value != 1
                else str(VAR_NAMING_MAPPING[test_var]),
                "ls": "TVR",
            },
        }

        ls_list.append(PLOT_DICT["tvl"]["label"])

        # plot the results
        for var, var_info in PLOT_DICT.items():
            axes.plot(
                var_info["x"],
                var_info["y"],
                # label=var_info["label"],
                ls="dashed" if var == "tvr" else "-",
                color=COLOR_LIST[color_idx],
            )

    lines = axes.get_lines()
    legend1 = plt.legend(
        [
            lines[i]
            for i in [
                0,
                1,
            ]
        ],
        ["TVL", "TVR"],
        frameon=False,
        loc="upper right",
        prop={"size": 18},
    )
    legend2 = plt.legend(
        [lines[i] for i in [0, 2, 4]],
        ls_list,
        frameon=False,
        loc="lower left",
        prop={"size": 18},
    )
    axes.add_artist(legend1)
    axes.add_artist(legend2)

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # x and y labels
    plt.xlabel("ETH Price Decline in Percentage")

    # set the y label
    plt.ylabel("Change in TVL and TVR (USD)")

    # increase label and tick size
    axes.xaxis.label.set_size(14)
    axes.yaxis.label.set_size(18)

    # increase the font size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=18)

    # tight layout
    plt.tight_layout()

    plt.savefig(f"{FIGURES_PATH}/sensitivity_{test_var}.pdf", dpi=2000)
    plt.show()
