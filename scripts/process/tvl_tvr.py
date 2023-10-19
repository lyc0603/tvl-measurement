"""
Script to process the TVL and TVR data
"""

from environ.data_processing.preprocess_tvl import preprocess_ptc_tvl

TVL_RELATED_NAMING_DICT = {
    "tvl": "$TVL^{Adj}_t$",
    "totalLiquidityUSD": "$TVL_t$",
    "tvr": "$TVR_t$",
}

tvl_tvr_agg_total_df = preprocess_ptc_tvl(
    chain="Total",
).rename(
    columns=TVL_RELATED_NAMING_DICT,
)
