"""
Script to process the correlation panel
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from config.constants import CORR_NAMING_DICT, FIGURES_PATH
from scripts.process.process_fred_data import df_fred
from scripts.process.process_leverage_ratio import leverage_ratio_dict
from scripts.process.process_market_data import df_market

# set the figure size
plt.rcParams["figure.figsize"] = (6, 5)

df_leverage = pd.DataFrame(leverage_ratio_dict).rename(columns={"value": "leverage"})

# merge the fred and market data
df_corr = df_fred.merge(df_market, on="date", how="left")

# merge the leverage ratio data
df_corr = df_corr.merge(df_leverage, on="date", how="left")

# only keep the data after 2021 and before the max date of the leverage ratio data
df_corr = df_corr[df_corr["date"] >= "2021-01-01"]
df_corr = df_corr[df_corr["date"] <= df_leverage["date"].max()]

# drop the date column
df_corr = df_corr.drop(columns=["date"])

# rename the columns
df_corr = df_corr.rename(columns=CORR_NAMING_DICT)

# convert the data to float
df_corr = df_corr.astype(float)

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
plt.savefig(f"{FIGURES_PATH}/corr.pdf", dpi=300)
