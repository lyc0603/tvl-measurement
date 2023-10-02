"""
Script to preprocess the TVL and TVR of MakerDao and Lido and store in cache
"""

import pandas as pd

from config.constants import DATA_PATH
from environ.data_fetching.lido_data_fetching import get_total_pooled_ether_lido
from environ.data_fetching.token_price import get_eth_price
from scripts.process.process_token_lst import df_token_cate

df_makerdao_bal = pd.read_csv(f"{DATA_PATH}/tvl/bal_makerdao.csv")

lido_tvl_tvr = get_total_pooled_ether_lido() * get_eth_price()

tvl_tvr_dict = {
    "tvl": {
        "MakerDAO": df_makerdao_bal.loc[
            df_makerdao_bal["entries"] == "Reserve Token", "dollar_amount"
        ].sum(),
        "Lido": lido_tvl_tvr,
    },
    "tvr": {
        "MakerDAO": df_makerdao_bal.loc[
            df_makerdao_bal["token_symbols"].isin(df_token_cate["symbol"].unique()),
            "dollar_amount",
        ].sum(),
        "Lido": lido_tvl_tvr,
    },
}

dft = df_makerdao_bal.loc[
    df_makerdao_bal["token_symbols"].isin(df_token_cate["symbol"].unique()),
    ["token_symbols", "dollar_amount"],
]
dft.sort_values(by="dollar_amount", ascending=False, inplace=True)
