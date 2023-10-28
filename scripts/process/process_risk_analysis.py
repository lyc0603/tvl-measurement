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
    SAMPLE_SYSTEM_TOKEN,
)
from environ.data_processing.preprocess_tvl_tvr_pct_change import get_tvl_tvr_pct_change
from scripts.process.preprocess_tvl_tvr_makerdao_lido_aave import (
    total_pool_ether,
    df_aave_v3_bal,
)
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

df_plot = {
    "eth_price": [],
    "tvl": [],
    "tvr": [],
}

# iterate from ilk price to highest liq price
for eth_price in np.linspace(0, eth_price_max, 100):
    df_res = {"pool_tvl_drop": [], "pool": []}

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

        df_res["pool_tvl_drop"].append(ilk_total_tvl - withdrawable_value)
        df_res["pool"].append(ilk)

    df_res = pd.DataFrame(df_res)

    makerdao_tvl_change = -df_res["pool_tvl_drop"].sum()

    makerdao_tvr_change = -df_res.loc[
        (df_res["pool"].isin(SAMPLE_SYSTEM_TVR_TOKEN)),
        "pool_tvl_drop",
    ].sum()

    lido_tvr_change = lido_tvl_change = total_pool_ether * (
        eth_price - eth_price_current
    )

    aave_tvl_change = (
        df_aave_v3_bal.loc[
            (df_aave_v3_bal["token_symbols"].isin(SAMPLE_SYSTEM_TOKEN))
            & (df_aave_v3_bal["entries"] == "Reserve Token"),
            "dollar_amount",
        ].sum()
        / eth_price_current
        * (eth_price - eth_price_current)
    )

    aave_tvr_change = (
        df_aave_v3_bal.loc[
            df_aave_v3_bal["token_symbols"].isin(SAMPLE_SYSTEM_TVR_TOKEN)
            & (df_aave_v3_bal["entries"] == "Reserve Token"),
            "dollar_amount",
        ].sum()
        / eth_price_current
        * (eth_price - eth_price_current)
    )

    df_plot["eth_price"].append(eth_price / eth_price_current)
    df_plot["tvl"].append(makerdao_tvl_change + lido_tvl_change + aave_tvl_change)
    df_plot["tvr"].append(makerdao_tvr_change + lido_tvr_change + aave_tvr_change)

df_plot = pd.DataFrame(df_plot)
