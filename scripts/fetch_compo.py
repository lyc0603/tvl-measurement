"""
Script to fetch the receipt tokens and their composition eight different protocols
"""

import json

from config import constants
from environ.data_fetching import (
    aave_v2_data_fetching,
    balancer_data_fetching,
    compound_v2_data_fetching,
    curve_v1_data_fetching,
    makerdao_data_fetching,
    uniswap_v2_data_fetching,
    yearn_data_fetching,
)

FETCH_DICT = {
    "Aave V2": aave_v2_data_fetching.get_receipt_tokens_and_composition(),
    "Balancer": balancer_data_fetching.get_receipt_tokens_and_composition(),
    "Compound V2": compound_v2_data_fetching.get_receipt_tokens_and_composition(),
    "Curve V1": curve_v1_data_fetching.get_receipt_tokens_and_composition(),
    "MakerDAO": makerdao_data_fetching.get_receipt_tokens_and_composition(),
    "Uniswap V2": uniswap_v2_data_fetching.get_receipt_tokens_and_composition(),
    "Yearn": yearn_data_fetching.get_receipt_tokens_and_composition(),
}


# save the json to data path
with open(
    f"{constants.DATA_PATH}/composition/defi_compo.json", "w", encoding="utf-8"
) as f:
    json.dump(FETCH_DICT, f, indent=4)
