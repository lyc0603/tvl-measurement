"""
Script to plot the sensitivity test results
"""


import matplotlib.pyplot as plt
import pandas as pd
from config.constants import FIGURES_PATH, SAMPLE_SYSTEM_TOKEN

from scripts.process.process_risk_analysis import results

# set the figure size
plt.figure(figsize=(5, 2))

df_sensitivity_test = pd.DataFrame(results)

for pool in SAMPLE_SYSTEM_TOKEN:
    df_pool = df_sensitivity_test.loc[df_sensitivity_test["pool"] == pool].copy()

    protocol = df_pool["protocol"].values[0]

    # plot the results
    plt.plot(
        df_pool["price_pct"],
        df_pool["tvl_pct"],
        label=f"{pool} in {protocol}",
    )

# x and y labels
plt.xlabel("Percentage of price drop of ETH")

# set the y label
plt.ylabel("Percentage of TVL")

# show the legend on the upper left corner
plt.legend(loc="upper left")

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# set the font of legend
plt.legend(prop={"size": 6})

# tight layout
plt.tight_layout()

# save the plot
plt.savefig(f"{FIGURES_PATH}/pool_tvl_drop.pdf", dpi=300)
