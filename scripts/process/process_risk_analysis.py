"""
Script to generate the balance sheets of sample protocols to implement the risk analysis
"""

import numpy as np
import pandas as pd

from config.constants import (
    MAKERDAO_ETH_RELATED_TOKEN,
    PROCESSED_DATA_PATH,
    SAMPLE_SYSTEM_TVR_TOKEN,
)
from environ.data_processing.preprocess_tvl_tvr_pct_change import get_tvl_tvr_pct_change
from scripts.process.preprocess_tvl_tvr_makerdao_lido_aave import total_pool_ether

df_makerdao = pd.read_csv(f"{PROCESSED_DATA_PATH}/defiexplore/defiexplore.csv")
eth_price_current = 1703.91

TEST_PARAMS = {
    "TVL_Lido": [1, 0.75, 0.5],
    "liqRatio": [1, 4, 0.25],
    "LTV": [1, 0.5, 1.5],
    "collat": [0.8, 1, 1.2],
}

risk_plot_dict = {}

for test_var, test_var_list in TEST_PARAMS.items():
    risk_plot_dict[test_var] = {}
    for test_var_value in test_var_list:
        df_plot = {
            "eth_price": [],
            "tvl": [],
            "tvr": [],
        }
        RUN_PARAMS = {}
        RUN_PARAMS[test_var] = test_var_value
        for default_var, default_vat_list in TEST_PARAMS.items():
            if default_var != test_var:
                RUN_PARAMS[default_var] = default_vat_list[0]

        # iterate from ilk price to highest liq price
        for eth_price in np.linspace(0, eth_price_current, 100):
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
                    liq_ratio_multiplier=RUN_PARAMS["liqRatio"],
                    ltv_multiplier=RUN_PARAMS["LTV"],
                    collat_multiplier=RUN_PARAMS["collat"],
                )

                df_res["pool_tvl_drop"].append(ilk_total_tvl - withdrawable_value)
                df_res["pool"].append(ilk)

            df_res = pd.DataFrame(df_res)

            makerdao_tvl_change = -df_res["pool_tvl_drop"].sum()

            makerdao_tvr_change = -df_res.loc[
                (df_res["pool"].isin(SAMPLE_SYSTEM_TVR_TOKEN)),
                "pool_tvl_drop",
            ].sum()
            lido_tvr_change = lido_tvl_change = (
                total_pool_ether
                * RUN_PARAMS["TVL_Lido"]
                * (eth_price - eth_price_current)
            )

            df_plot["eth_price"].append(1 - eth_price / eth_price_current)
            df_plot["tvl"].append(makerdao_tvl_change + lido_tvl_change)
            df_plot["tvr"].append(makerdao_tvr_change + lido_tvr_change)

        df_plot = pd.DataFrame(df_plot)
        risk_plot_dict[test_var][test_var_value] = df_plot
