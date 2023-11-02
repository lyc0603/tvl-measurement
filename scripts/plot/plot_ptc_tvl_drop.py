"""
Script to plot the sensitivity test results of protocol
"""

import matplotlib.pyplot as plt

from config.constants import FIGURES_PATH
from scripts.process.process_risk_analysis import risk_plot_dict

VAR_NAMING_MAPPING = {
    "TVL_Lido": "$q^{L}$",
    "liqRatio": "$\\beta$",
    "LTV": "$L$",
    "collat": "$q^{M}$",
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
    plt.xlabel(r"ETH Price Decline in Percentage, $d$", loc="left")

    # set the y label
    plt.ylabel(r"Change in TVL and TVR (USD), $\Delta_{TVL}$, $\Delta_{TVR}$")

    # increase label and tick size
    axes.xaxis.label.set_size(16)
    axes.yaxis.label.set_size(18)

    # set the x axis range
    axes.xaxis.set_label_coords(-0.5, -0.08)

    # increase the font size
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=18)

    # tight layout
    plt.tight_layout()

    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.1f}B".format(x / 1e9))
    )

    plt.savefig(f"{FIGURES_PATH}/sensitivity_{test_var}.pdf", dpi=2000)
    plt.show()
