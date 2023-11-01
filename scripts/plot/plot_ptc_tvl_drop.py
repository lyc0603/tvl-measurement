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
    "LTV": "$\\alpha$",
    "collat": "$Q^{M}$",
}

COLOR_LIST = ["red", "darkblue", "lightgreen"]


for test_var, test_var_dict in risk_plot_dict.items():
    # set the figure size
    plt.figure(figsize=(4, 4))
    for color_idx, (test_var_value, df_plot) in enumerate(test_var_dict.items()):
        PLOT_DICT = {
            "tvl": {
                "x": df_plot["eth_price"],
                "y": df_plot["tvl"],
                "label": str(test_var_value)
                + str(VAR_NAMING_MAPPING[test_var])
                + ", TVL"
                if test_var_value != 1
                else str(VAR_NAMING_MAPPING[test_var]) + ", TVL",
            },
            "tvr": {
                "x": df_plot["eth_price"],
                "y": df_plot["tvr"],
                "label": str(test_var_value)
                + str(VAR_NAMING_MAPPING[test_var])
                + ", TVR"
                if test_var_value != 1
                else str(VAR_NAMING_MAPPING[test_var]) + ", TVR",
            },
        }

        # plot the results
        for var, var_info in PLOT_DICT.items():
            plt.plot(
                var_info["x"],
                var_info["y"],
                label=var_info["label"],
                ls="dashed" if var == "tvr" else "-",
                color=COLOR_LIST[color_idx],
            )

    # show the legend with two columns and no box
    plt.legend(ncol=2, frameon=False)

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # x and y labels
    plt.xlabel("ETH Price Decline in Percentage")

    # set the y label
    plt.ylabel("Change in TVL and TVR (USD)")

    # tight layout
    plt.tight_layout()

    plt.savefig(f"{FIGURES_PATH}/sensitivity_{test_var}.pdf", dpi=300)
    plt.show()
