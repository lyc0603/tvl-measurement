"""
Script to process the summary statistics
"""

import pandas as pd

from config.constants import PROCESSED_DATA_PATH

TVL_AGG_DICT = {
    "Total": pd.DataFrame(),
    "Ethereum": pd.DataFrame(),
    "Binance": pd.DataFrame(),
    "Tron": pd.DataFrame(),
}

for chain, df_tvl_agg in TVL_AGG_DICT.items():
    TVL_AGG_DICT[chain] = pd.read_csv(
        f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all_{chain}.csv"
    )
