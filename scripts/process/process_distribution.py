"""
Scripts to process the distribution mapping from ETH return to TVL and TVR return
"""

import pandas as pd

from config.constants import PROCESSED_DATA_PATH, SAMPLE_SYSTEM_TOKEN
from environ.data_fetching.lido_data_fetching import get_total_pooled_ether_lido
from environ.data_fetching.token_price import get_eth_price
from environ.data_processing.preprocess_tvl_tvr_pct_change import get_tvl_tvr_pct_change
from scripts.process.process_sp import df_sp
from scripts.process.preprocess_tvl_tvr_makerdao_lido_aave import tvl_tvr_dict

results = {
    "idx": [],
    "protocol": [],
    "pool": [],
    "eth_ret": [],
    "ilk_withdrawable_value": [],
    "ilk_total_tvl": [],
}

eth_price = get_eth_price()
total_pool_ether = get_total_pooled_ether_lido()

df_makerdao = pd.read_csv(f"{PROCESSED_DATA_PATH}/defiexplore/defiexplore.csv")

# keep data from 2022-01-01 to 2023-09-01
df_sp = df_sp[(df_sp["date"] >= "2022-01-01") & (df_sp["date"] <= "2023-09-01")]

# calculate the percentage change
df_sp["s&p"] = df_sp["s&p"].pct_change()

# drop the first row
df_sp = df_sp.iloc[1:, :]

idx = 0

# iterate throught the S&P percentage change
for sp_ret in df_sp["s&p"]:
    idx += 1

    for ilk in SAMPLE_SYSTEM_TOKEN:
        df_ilk = df_makerdao[
            (df_makerdao["ilk"] == ilk) & (df_makerdao["collateral"] != 0)
        ].copy()

        withdrawable_value, ilk_total_tvl = get_tvl_tvr_pct_change(
            df_ilk=df_makerdao,
            eth_price=eth_price,
            eth_ret=sp_ret,
        )

        # append the results to the dict
        results["idx"].append(idx)
        results["protocol"].append("MakerDAO")
        results["pool"].append(ilk)
        results["eth_ret"].append(sp_ret)
        results["ilk_withdrawable_value"].append(withdrawable_value)
        results["ilk_total_tvl"].append(ilk_total_tvl)

    # calculate the total tvl
    total_tvl = total_pool_ether * eth_price

    # iterate from ilk price to highest liq price
    eth_price_drop = eth_price * (1 + eth_ret)

    # calculate the withdrawable value
    withdrawable_value = total_pool_ether * eth_price_drop

    # append the results to the dict
    results["idx"].append(idx)
    results["protocol"].append("Lido")
    results["pool"].append("ETH")
    results["eth_ret"].append(sp_ret)
    results["ilk_withdrawable_value"].append(withdrawable_value)
    results["ilk_total_tvl"].append(total_tvl)

df_res = pd.DataFrame(results)

plot_dict = {
    "eth_ret": [],
    "tvl_ret": [],
    "tvr_ret": [],
}

# iterate through the idx
for idx in df_res["idx"].unique():
    df_idx = df_res[df_res["idx"] == idx].copy()
    total_tvl = df_idx["ilk_total_tvl"].sum()
    tvl_agg_bef = tvl_tvr_dict["tvl"]["MakerDAO"] + tvl_tvr_dict["tvl"]["Lido"]
    tvl_agg_aft = (
        tvl_agg_bef - (df_idx["ilk_withdrawable_value"] - df_idx["ilk_total_tvl"]).sum()
    )
    tvr_agg_bef = tvl_tvr_dict["tvr"]["MakerDAO"] + tvl_tvr_dict["tvr"]["Lido"]
    tvr_agg_aft = tvr_agg_bef - (
        (
            df_idx.loc[
                df_idx["pool"].isin(["ETH", "ETH-A", "ETH-B", "ETH-C"]),
                "ilk_withdrawable_value",
            ]
            - df_idx.loc[
                df_idx["pool"].isin(["ETH", "ETH-A", "ETH-B", "ETH-C"]),
                "ilk_total_tvl",
            ]
        ).sum()
    )

    plot_dict["eth_ret"].append(df_idx["eth_ret"].values[0])
    plot_dict["tvl_ret"].append(tvl_agg_aft / tvl_agg_bef - 1)
    plot_dict["tvr_ret"].append(tvr_agg_aft / tvr_agg_bef - 1)
