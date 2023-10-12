"""
Script to plot the risk sankey diagram.
"""
import pandas as pd
from environ.process.plot_sankey import plot_sankey

from config.constants import FIGURES_PATH
from scripts.process.process_maker_lido_sankey import SANKEY_PLOT_DICT

# get the df_data
df_data = pd.DataFrame(SANKEY_PLOT_DICT)

plot_sankey(
    df_data=df_data,
    save_path=f"{FIGURES_PATH}/sankey_risk.pdf",
    source_col="source",
    target_col="target",
    amount_col="value",
)
