"""
Script to plot the sensitivity test results
"""


import matplotlib.pyplot as plt
import pandas as pd
from config.constants import FIGURES_PATH, SAMPLE_SYSTEM_TOKEN

from scripts.process.process_risk_analysis import results

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

# set the legend
plt.legend()

# tight layout
plt.tight_layout()

# save the plot
plt.savefig(f"{FIGURES_PATH}/pool_tvl_drop.pdf", dpi=300)
