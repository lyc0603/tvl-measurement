"""
Script to process the MakerDAO and Lido sankey plot data
"""

import pandas as pd

from config.constants import DATA_PATH
from environ.data_fetching.lido_data_fetching import (
    get_total_pooled_ether_lido,
    get_wsteth_total_supply_lido,
    get_steth_per_token_lido,
)
from environ.data_fetching.token_price import get_eth_price


SANKEY_PLOT_DICT = {
    "source": [],
    "target": [],
    "value": [],
}

df_maker = pd.read_csv(f"{DATA_PATH}/tvl/bal_makerdao.csv")
df_maker = df_maker.loc[df_maker["entries"] == "Reserve Token"]

# get the total pooled ether
total_pooled_ether = get_total_pooled_ether_lido()
total_supply_wsteth = get_wsteth_total_supply_lido()
steth_per_token = get_steth_per_token_lido()
eth_price = get_eth_price()

steth_value = (total_pooled_ether - total_supply_wsteth * steth_per_token) * eth_price
wsteth_value = total_supply_wsteth * steth_per_token * eth_price

SANKEY_PLOT_DICT["source"].extend(["ETH", "ETH"])
SANKEY_PLOT_DICT["target"].extend(["stETH", "wstETH"])
SANKEY_PLOT_DICT["value"].extend([steth_value, wsteth_value])
