"""
Script to generate the balance sheets of sample protocols
"""

import json

import pandas as pd
from tqdm import tqdm

from config.constants import DATA_PATH
from environ.data_fetching.token_price import get_eth_price, get_token_price_defillama
from environ.data_fetching.web3_call import get_token_symbol
from environ.data_processing.process_bal import preprocess_tvl_compo

PTC_PATH_MAPPING = {
    "MakerDAO": f"{DATA_PATH}/tvl/tvl_composition_Origin.MAKER.csv",
    "Aave V2": f"{DATA_PATH}/tvl/tvl_composition_Origin.AAVE_V2.csv",
    "Compound V2": f"{DATA_PATH}/tvl/tvl_composition_Origin.COMPOUND_V2.csv",
    "Balancer": f"{DATA_PATH}/tvl/tvl_composition_Origin.BALANCER.csv",
    "Curve V1": f"{DATA_PATH}/tvl/tvl_composition_Origin.CURVE.csv",
    "Yearn": f"{DATA_PATH}/tvl/tvl_composition_Origin.YEARN.csv",
}

df_bal = []

with open(f"{DATA_PATH}/composition/defi_compo.json", encoding="utf-8") as compo_json:
    dict_compo = json.load(compo_json)

for ptc_name, path in PTC_PATH_MAPPING.items():
    # load the composition dataframe
    df_compo = pd.read_csv(path)

    # preprocess the composition dataframe
    df_bal.append(preprocess_tvl_compo(dict_compo=dict_compo, ptc_dict_name=ptc_name))

df_bal = pd.concat(df_bal).reset_index(drop=True)

# preprocess the token symbol
for token_contract in tqdm(
    df_bal["token_contract"].unique(), desc="Calculating Dollar Amount"
):
    try:
        df_bal.loc[
            df_bal["token_contract"] == token_contract, "token_symbol"
        ] = df_compo.loc[
            df_compo["token_contract"] == token_contract, "token_symbol"
        ].values[
            0
        ]
    except:  # pylint: disable=bare-except
        df_bal.loc[df_bal["token_contract"] == token_contract, "token_symbol"] = (
            get_token_symbol(token_address=token_contract)
            if token_contract
            not in ["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "ETH"]
            else "ETH"
        )

    # preprocess the dollar amount
    try:
        df_bal.loc[df_bal["token_contract"] == token_contract, "dollar_amount"] = (
            df_bal.loc[df_bal["token_contract"] == token_contract, "token_quantity"]
            * get_token_price_defillama(token_address=token_contract)
            if token_contract
            not in ["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "ETH"]
            else df_bal.loc[
                df_bal["token_contract"] == token_contract, "token_quantity"
            ]
            * get_eth_price()
        )
    except Exception as e:  # pylint: disable=bare-except
        print(e)
        df_bal.loc[df_bal["token_contract"] == token_contract, "dollar_amount"] = (
            df_bal.loc[df_bal["token_contract"] == token_contract, "token_quantity"] * 0
        )

df_bal.sort_values(by=["protocol_name", "dollar_amount"], ascending=False, inplace=True)
df_bal.drop(columns=["token_quantity"], inplace=True)

# save the balance sheet
df_bal.to_csv(f"{DATA_PATH}/tvl/bal_all.csv", index=False)
