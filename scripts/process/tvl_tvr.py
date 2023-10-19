"""
Script to process the TVL and TVR data
"""

from config.constants import TVL_RELATED_NAMING_DICT
from environ.data_processing.preprocess_tvl import preprocess_ptc_tvl

tvl_tvr_agg_total_df = preprocess_ptc_tvl(
    chain="Total",
).rename(
    columns=TVL_RELATED_NAMING_DICT,
)
