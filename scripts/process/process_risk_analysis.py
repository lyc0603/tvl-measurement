"""
Script to generate the balance sheets of sample protocols to implement the risk analysis
"""

import numpy as np
import pandas as pd

from config.constants import (
    DEFIEXPLORE_SAMPLE_DATE,
    MAKERDAO_ETH_RELATED_TOKEN,
    PROCESSED_DATA_PATH,
    SAMPLE_MIN_DATE,
    SAMPLE_SYSTEM_TVR_TOKEN,
)
from environ.data_fetching.lido_data_fetching import get_total_pooled_ether_lido
from environ.data_processing.preprocess_tvl_tvr_pct_change import get_tvl_tvr_pct_change
from scripts.process.preprocess_tvl_tvr_makerdao_lido import tvl_tvr_dict
from scripts.process.process_market_data import df_market

df_makerdao = pd.read_csv(f"{PROCESSED_DATA_PATH}/defiexplore/defiexplore.csv")
eth_price_current = df_market.loc[
    df_market["date"] == DEFIEXPLORE_SAMPLE_DATE, "etherprice"
].values[0]
eth_price_max = df_market.loc[
    (df_market["date"] >= SAMPLE_MIN_DATE)
    & (df_market["date"] <= DEFIEXPLORE_SAMPLE_DATE),
    "etherprice",
].max()

# get the total ether of Lido
total_pool_ether = get_total_pooled_ether_lido()

# a dict to store the results
results = {"protocol": [], "pool": [], "eth_price": [], "pool_tvl_drop": []}

# iterate from ilk price to highest liq price
for eth_price in np.linspace(0, eth_price_max, 100):
    for ilk in MAKERDAO_ETH_RELATED_TOKEN:
        df_ilk = df_makerdao[
            (df_makerdao["ilk"] == ilk) & (df_makerdao["collateral"] != 0)
        ].copy()

        # calculate the tvl percentage
        withdrawable_value, ilk_total_tvl = get_tvl_tvr_pct_change(
            df_ilk=df_ilk,
            eth_price=eth_price_current,
            eth_ret=((eth_price - eth_price_current) / eth_price_current),
        )

        # append the results to the dict
        results["protocol"].append("MakerDAO")
        results["pool"].append(ilk)
        results["eth_price"].append(eth_price)
        results["pool_tvl_drop"].append(ilk_total_tvl - withdrawable_value)

df_res = pd.DataFrame(results)

df_plot = {
    "eth_price": [],
    "tvl": [],
    "tvr": [],
}
# prepare the data for plotting
for eth_price in df_res["eth_price"].unique():
    df_plot["eth_price"].append(eth_price / eth_price_current)
    df_plot["tvl"].append(
        (
            tvl_tvr_dict["tvl"]["MakerDAO"]
            - df_res.loc[
                df_res["eth_price"] == eth_price,
                "pool_tvl_drop",
            ].sum()
        )
        / tvl_tvr_dict["tvl"]["MakerDAO"]
    )
    df_plot["tvr"].append(
        (
            tvl_tvr_dict["tvr"]["MakerDAO"]
            - df_res.loc[
                (df_res["eth_price"] == eth_price)
                & (df_res["pool"].isin(SAMPLE_SYSTEM_TVR_TOKEN)),
                "pool_tvl_drop",
            ].sum()
        )
        / tvl_tvr_dict["tvr"]["MakerDAO"]
    )

df_plot = pd.DataFrame(df_plot)
