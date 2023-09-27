"""
Script to plot the comparison of money supply between the trafi and defi
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scripts.process.process_money_multiplier import money_multiplier_dict
from scripts.process.process_leverage_ratio import leverage_ratio_dict
from config.constants import FIGURES_PATH

# set the figure size
plt.figure(figsize=(5, 2))


# plot the money multiplier
plt.plot(
    money_multiplier_dict["date"],
    money_multiplier_dict["value"],
    label="Money Multiplier",
    color="blue",
    marker="o",
    markersize=2,
    linewidth=1,
)

# plot the leverage ratio
plt.plot(
    leverage_ratio_dict["date"],
    leverage_ratio_dict["value"],
    label="Leverage Ratio",
    color="red",
    marker="o",
    markersize=2,
    linewidth=1,
)


# show the legend on the upper right corner
plt.legend(loc="upper right")

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# set the unit of the x axis
# plt.gca().xaxis.set_major_formatter(
#     mdates.DateFormatter("%Y-%m"),
# )
plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=1),
)

# label the y axis
plt.ylabel("Ratio")

# rotate the xticks
plt.xticks(rotation=90)

# tight layout
plt.tight_layout()

# save the figure
plt.savefig(f"{FIGURES_PATH}/money_supply_compare.pdf", dpi=300)
