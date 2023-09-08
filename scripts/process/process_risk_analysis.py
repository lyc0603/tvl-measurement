"""
Script to generate the balance sheets of sample protocols to implement the risk analysis
"""

import numpy as np
import pandas as pd

from config.constants import PROCESSED_DATA_PATH
from environ.data_fetching.lido_data_fetching import get_total_pooled_ether_lido
from environ.data_fetching.token_price import get_eth_price

eth_price = get_eth_price()

df_makerdao = pd.read_csv(f"{PROCESSED_DATA_PATH}/defiexplore/defiexplore.csv")

# a dict to store the results
results = {
    "protocol": [],
    "pool": [],
    "price_pct": [],
    "tvl_drop": [],
    "tvl_pct": [],
}

for ilk in df_makerdao["ilk"].unique():
    df_ilk = df_makerdao[
        (df_makerdao["ilk"] == ilk) & (df_makerdao["collateral"] != 0)
    ].copy()

    # calculate the price that the collateral is not incentivized to liquidate
    df_ilk["ilk_non_liq_prc"] = df_ilk["debt"] / df_ilk["collateral"]

    # get the total collateral of the collateral
    total_collat = df_ilk["collateral"].sum()
    ilk_total_tvl = total_collat * eth_price

    # iterate from ilk price to highest liq price
    for price_drop in np.linspace(0, 1, 100):
        ilk_price = eth_price * (1 - price_drop)

        # get the colalteral in different states
        df_ilk_safe = df_ilk[df_ilk["liqPrice"] <= ilk_price].copy()
        df_ilk_liquidated = df_ilk[
            (df_ilk["liqPrice"] > ilk_price) & (ilk_price >= df_ilk["ilk_non_liq_prc"])
        ].copy()

        # calculate the withdrawable value
        withdrawable_value = (
            df_ilk_safe["collateral"].sum() * ilk_price
            + df_ilk_liquidated["debt"].sum()
        )

        # calculate the tvl percentage
        ilk_tvl_pct = (withdrawable_value) / ilk_total_tvl

        # append the results to the dict
        results["protocol"].append("MakerDAO")
        results["pool"].append(ilk)
        results["price_pct"].append(price_drop)
        results["tvl_pct"].append(ilk_tvl_pct)
        results["tvl_drop"].append(ilk_total_tvl - withdrawable_value)

# get the total ether of Lido
total_pool_ether = get_total_pooled_ether_lido()

# calculate the total tvl
total_tvl = total_pool_ether * eth_price

# iterate from ilk price to highest liq price
for price_drop in np.linspace(0, 1, 100):
    eth_price_drop = eth_price * (1 - price_drop)

    # calculate the withdrawable value
    withdrawable_value = total_pool_ether * eth_price_drop

    # calculate the tvl percentage
    steth_tvl_pct = (withdrawable_value) / total_tvl

    # append the results to the dict
    results["protocol"].append("Lido")
    results["pool"].append("ETH")
    results["price_pct"].append(price_drop)
    results["tvl_pct"].append(steth_tvl_pct)
    results["tvl_drop"].append(total_tvl - withdrawable_value)
