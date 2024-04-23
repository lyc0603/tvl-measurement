"""
Script to plot the correlation between the macro and market data
"""

import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from config.constants import TABLES_PATH
from scripts.process.process_corr import df_corr
import scipy.stats as stats

colors = [(0.5, 0.5, 1), (1, 1, 1), (1, 0.5, 0.5)]  # Light red, white, light blue
color_map = LinearSegmentedColormap.from_list("custom", colors)

# calculate the log return
df_corr = np.log(df_corr).diff().dropna()


def asterisk(p_value: float) -> str:
    """
    Function to add asterisk to the p value
    """
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""


corr = df_corr.corr()

corr_with_asterisk = corr.copy()

# add asterisk to the correlation
for symbol in df_corr.columns:
    for symbol2 in df_corr.columns:
        corr_with_asterisk.loc[symbol, symbol2] = (
            f"{corr_with_asterisk.loc[symbol, symbol2]:.2f}{asterisk(stats.pearsonr(df_corr[symbol], df_corr[symbol2])[1])}"
        )


corr_with_color = corr.style.background_gradient(
    cmap=color_map, vmin=-1, vmax=1
).format("{:.2f}")


# save corr_with_color to latex and preserve the color
corr_latex = corr_with_color.to_latex(
    convert_css=True, column_format="@{}l*{9}{R{9.8mm}}@{}"
)

# add significance level to the latex
with open(f"{TABLES_PATH}/logcorr.tex", "w", encoding="utf-8") as f:
    f.write(corr_latex)
