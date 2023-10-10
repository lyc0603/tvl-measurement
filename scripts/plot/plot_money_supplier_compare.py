"""
Script to plot the comparison of money supply between the trafi and defi
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from scripts.process.process_money_multiplier import money_multiplier_dict
from scripts.process.process_leverage_ratio import leverage_ratio_dict
from config.constants import FIGURES_PATH

# set the figure size
plt.figure(figsize=(5, 2))

df_money_supplier = pd.DataFrame(money_multiplier_dict)
df_money_supplier.rename(
    columns={"value": "money_multiplier"},
    inplace=True,
)
df_leverage_ratio = pd.DataFrame(leverage_ratio_dict)
df_leverage_ratio.rename(
    columns={"value": "leverage_ratio"},
    inplace=True,
)

df_agg = df_leverage_ratio.merge(
    df_money_supplier,
    how="left",
    on="date",
)

PLOT_DICT = {
    "money_multiplier": {
        "label": "Money Multiplier",
        "color": "blue",
        "marker": "o",
        "markersize": 2,
        "linewidth": 1,
    },
    "leverage_ratio": {
        "label": "Leverage Ratio",
        "color": "red",
        "marker": "o",
        "markersize": 2,
        "linewidth": 1,
    },
}

for var, var_plot_info in PLOT_DICT.items():
    plt.plot(
        df_agg["date"],
        df_agg[var],
        label=var_plot_info["label"],
        color=var_plot_info["color"],
        marker=var_plot_info["marker"],
        markersize=var_plot_info["markersize"],
        linewidth=var_plot_info["linewidth"],
    )


# show the legend on the upper right corner
plt.legend(loc="upper right")

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# set the x limit to 2019-06-01
plt.xlim(
    [
        pd.to_datetime("2019-06-01"),
        df_leverage_ratio[df_leverage_ratio["leverage_ratio"].notnull()]["date"].max(),
    ]
)

# set the unit of the x axis
# plt.gca().xaxis.set_major_formatter(
#     mdates.DateFormatter("%Y-%m"),
# )
plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=2),
)

# label the y axis
plt.ylabel("Ratio")

# rotate the xticks
plt.xticks(rotation=90)

# tight layout
plt.tight_layout()

# save the figure
plt.savefig(f"{FIGURES_PATH}/money_supply_compare.pdf", dpi=300)

plt.show()
