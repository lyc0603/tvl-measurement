"""
Script to plot the sensitivity test results of protocol
"""

import matplotlib.pyplot as plt
import numpy as np

from config.constants import FIGURES_PATH
from scripts.process.process_risk_analysis import (
    df_plot,
    eth_price_current,
    eth_price_max,
)

# set the figure size
plt.figure(figsize=(5, 2))

PLOT_DICT = {
    "tvl": {
        "x": df_plot["eth_price"],
        "y": df_plot["tvl"],
        "label": "TVL",
    },
    "tvr": {
        "x": df_plot["eth_price"],
        "y": df_plot["tvr"],
        "label": "TVR",
    },
}

# plot the results
for var, var_info in PLOT_DICT.items():
    plt.plot(
        var_info["x"],
        var_info["y"],
        label=var_info["label"],
    )


DASHED_LINE_DICT = {
    "current_eth_price": {
        "x": eth_price_current / eth_price_current,
        "color": "black",
        "linestyle": "dashed",
        "linewidth": 1,
        "alpha": 0.5,
        "label": "Current ETH price",
    },
    "max_eth_price": {
        "x": eth_price_max / eth_price_current,
        "color": "red",
        "linestyle": "dashed",
        "linewidth": 1,
        "alpha": 0.5,
        "label": "Max ETH price",
    },
}

# plot a verticle dashed line at the current ether price
for _, dashed_line_info in DASHED_LINE_DICT.items():
    plt.axvline(
        x=dashed_line_info["x"],
        color=dashed_line_info["color"],
        linestyle=dashed_line_info["linestyle"],
        linewidth=dashed_line_info["linewidth"],
        alpha=dashed_line_info["alpha"],
        label=dashed_line_info["label"],
    )

# lower legend font size
plt.rcParams["legend.fontsize"] = 6

# show the legend on the upper left corner
plt.legend(loc="upper left")

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# x and y labels
plt.xlabel("% of ETH price")

# set the y label
plt.ylabel("% of TVL/TVR")

# tight layout
plt.tight_layout()

plt.savefig(f"{FIGURES_PATH}/protocol_tvl_drop.pdf", dpi=300)

plt.show()
