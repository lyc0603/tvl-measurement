"""
Script to plot the flow amount of the different protocols
"""

import json

import pandas as pd

from config import constants
from environ.data_visualization.plot_sankey import plot_sankey

# load the flow data
with open(
    f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow.json", "r", encoding="utf-8"
) as f_json:
    flow_dict = json.load(f_json)

# convert the flow data to the DataFrame
flow_df = pd.DataFrame(flow_dict)

# plot the flow amount of the different protocols
plot_sankey(
    flow_df,
)


# load the flow usd data
flow_usd_df = pd.read_csv(
    f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv",
)
