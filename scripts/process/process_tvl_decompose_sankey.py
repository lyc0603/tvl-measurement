"""
Script to process the data of TVL decomposition sankey plot
"""

import pandas as pd

from config.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
from environ.data_processing.process_tvl_decompose_sankey import (
    tvl_decompose_sankey_data,
)
from scripts.process.remove_ptc import remove_ptc

# load the data
tvl_total_df = pd.read_csv(
    f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all_Total.csv"
)
tvr_total_df = pd.read_csv(
    f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all_Total.csv"
)

# remove ptc
tvl_total_df = tvl_total_df[~tvl_total_df["protocol"].isin(remove_ptc)]
tvr_total_df = tvr_total_df[~tvr_total_df["protocol"].isin(remove_ptc)]

# get the max date
tvl_agg_df = tvl_total_df.groupby(["date"])["totalLiquidityUSD"].sum().reset_index()
tvl_max_date = tvl_agg_df.loc[
    tvl_agg_df["totalLiquidityUSD"] == tvl_agg_df["totalLiquidityUSD"].max(), "date"
].values[0]

TVL_DECOMPOSE_SANKEY_DICT = {}

for event, date in SAMPLE_DATA_DICT.items():
    TVL_DECOMPOSE_SANKEY_DICT[event] = tvl_decompose_sankey_data(
        tvl_total_df=tvl_total_df,
        tvr_total_df=tvr_total_df,
        date=date + " 00:00:00",
    )
