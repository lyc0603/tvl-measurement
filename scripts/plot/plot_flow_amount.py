"""
Script to plot the flow amount of the different protocols
"""

import json

import pandas as pd

from config import constants
from environ.data_visualization.plot_sankey import plot_sankey, process_flow_usd_data

# # load the flow data
# with open(
#     f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow.json", "r", encoding="utf-8"
# ) as f_json:
#     flow_dict = json.load(f_json)

# # convert the flow data to the DataFrame
# flow_df = pd.DataFrame(flow_dict)

# # plot the flow amount of the different protocols
# plot_sankey(
#     flow_df,
# )


# load the flow usd data
flow_usd_df = pd.read_csv(
    f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow_usd.csv",
)

# preprocess the flow usd data
flow_usd_df = process_flow_usd_data(flow_usd_df)

# plot the flow amount of the different protocols
plot_sankey(
    flow_usd_df,
    save_path=f"{constants.FIGURES_PATH}/sankey_usd.pdf",
    amount_col="flow_usd",
)
