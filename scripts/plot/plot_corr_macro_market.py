"""
Script to plot the correlation between the macro and market data
"""

import seaborn as sns
from matplotlib import pyplot as plt

from config.constants import FIGURES_PATH
from scripts.process.process_corr import df_corr

# set the figure size
plt.rcParams["figure.figsize"] = (6, 5)

# plot the correlation heatmap
sns.heatmap(df_corr.corr(), annot=True, cmap="coolwarm")

# rotate the xticklabels
plt.xticks(rotation=90)

# rotate the yticklabels
plt.yticks(rotation=0)

# enlarge the font size
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# tight layout
plt.tight_layout()

# save the plot
plt.savefig(f"{FIGURES_PATH}/corr_market_macro.pdf", dpi=300)
