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

CONTRACT_SYMBOL_MAPPING = {"0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2": "MKR"}


ETH_LIST = ["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "ETH"]

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
    # special case for tokens that cannot be fetched from web3
    if token_contract in CONTRACT_SYMBOL_MAPPING.keys():
        df_bal.loc[
            df_bal["token_contract"] == token_contract, "token_symbol"
        ] = CONTRACT_SYMBOL_MAPPING[token_contract]
    else:
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
                if token_contract not in ETH_LIST
                else "ETH"
            )

    # preprocess the dollar amount
    try:
        df_bal.loc[df_bal["token_contract"] == token_contract, "dollar_amount"] = (
            df_bal.loc[df_bal["token_contract"] == token_contract, "token_quantity"]
            * get_token_price_defillama(token_address=token_contract)
            if token_contract not in ETH_LIST
            else df_bal.loc[
                df_bal["token_contract"] == token_contract, "token_quantity"
            ]
            * get_eth_price()
        )
    except:  # pylint: disable=bare-except
        # df_bal = remove_no_info(
        #     df_bal=df_bal, dict_compo=dict_compo, token_contract=token_contract
        # )
        df_bal.loc[df_bal["token_contract"] == token_contract, "dollar_amount"] = 0.0


# sum up same token symbols
df_bal = (
    df_bal.groupby(["protocol_name", "entry", "token_symbol"])
    .agg({"dollar_amount": "sum"})
    .reset_index()
)

df_bal.sort_values(by=["protocol_name", "dollar_amount"], ascending=False, inplace=True)

# save the balance sheet
df_bal.to_csv(f"{DATA_PATH}/tvl/bal_all.csv", index=False)
