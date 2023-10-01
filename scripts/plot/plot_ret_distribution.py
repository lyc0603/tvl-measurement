"""
Script to plot the distribution of ETH, TVL, and TVR return
"""


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# if the processed data is not available, run the script to process the data
from scripts.process.process_distribution import plot_dict


# set the figure size
plt.figure(figsize=(5, 5))

pd.DataFrame(plot_dict).to_csv("test/plot_dict.csv")

FORMAT_DICT = {
    "eth_ret": {
        "label": "ETH / TVR return",
        "color": "blue",
    },
    "tvl_ret": {"label": "TVL return", "color": "red"},
    "tvr_ret": {"label": "TVR return", "color": "green"},
}

# plot the histogram of ETH return and TVL return

for var, var_fmt in FORMAT_DICT.items():
    sns.histplot(
        x=plot_dict[var],
        stat="probability",
        label=var_fmt["label"],
        color=var_fmt["color"],
        alpha=0.5,
        kde=True,
        bins=10,
    )

plt.legend()

plt.show()
