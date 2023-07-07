"""
Functions to fetch the tvl data of DeFiLlama
"""

import json
import os
import time

import requests

from config.constants import (
    DATA_PATH,
    DEFI_LLAMA_PROTOCOL_URL,
    DEFI_LLAMA_TVL_URL,
    DEFI_LLAMA_TREASURY_URL,
    DEFI_LLAMA_ETH_TVL_URL,
)


def fetch_llama_total_tvl(chain: str = "Ethereum") -> dict:
    """
    Function to fetch the total or chain tvl from DeFiLlama
    """

    return requests.get(
        url=f"https://api.llama.fi/v2/historicalChainTvl/{chain}"
        if chain != "Total"
        else "https://api.llama.fi/v2/historicalChainTvl",
        timeout=120,
    ).json()


def fetch_llama_total_tvl_eth() -> None:
    """
    Function to fetch the total tvl from DeFiLlama
    """

    # check whether the path exists
    if not os.path.exists(f"{DATA_PATH}/defillama"):
        os.makedirs(f"{DATA_PATH}/defillama")

    data_json = requests.get(url=DEFI_LLAMA_ETH_TVL_URL, timeout=120).json()
    with open(
        f"{DATA_PATH}/defillama/total_tvl_eth_without_double_counting.json",
        "w",
        encoding="utf-8",
    ) as target_file:
        json.dump(data_json, target_file, indent=4)


def fetch_llama_protocol_lst(save_path: str) -> None:
    """
    Function to fetch the protocol list from DeFiLlama
    """

    # check whether the path exists
    if not os.path.exists(f"{DATA_PATH}/defillama"):
        os.makedirs(f"{DATA_PATH}/defillama")

    data_json = requests.get(url=DEFI_LLAMA_PROTOCOL_URL, timeout=120).json()
    with open(save_path, "w", encoding="utf-8") as target_file:
        json.dump(data_json, target_file, indent=4)


def fetch_llama_tvl(ptc_slug: str = "aave_v2") -> None:
    """
    Function to fetch the tvl data from DeFiLlama
    """

    time.sleep(1)

    # check whether the path exists
    if not os.path.exists(f"{DATA_PATH}/defillama/tvl"):
        os.makedirs(f"{DATA_PATH}/defillama/tvl")

    data_json = requests.get(url=f"{DEFI_LLAMA_TVL_URL}/{ptc_slug}", timeout=120).json()

    # check whether the data is empty
    if len(data_json["chainTvls"]) == 0:
        raise ValueError(f"The data for {ptc_slug} is empty.")

    with open(
        f"{DATA_PATH}/defillama/tvl/{ptc_slug}.json", "w", encoding="utf-8"
    ) as target_file:
        json.dump(data_json, target_file, indent=4)


def fetch_llama_treasury(ptc_slug: str = "aave_v2") -> None:
    """
    Function to fetch the treasury data from DeFiLlama
    """

    time.sleep(5)

    # check whether the path exists
    if not os.path.exists(f"{DATA_PATH}/defillama/treasury"):
        os.makedirs(f"{DATA_PATH}/defillama/treasury")

    data_json = requests.get(
        url=f"{DEFI_LLAMA_TREASURY_URL}/{ptc_slug}", timeout=120
    ).json()

    with open(
        f"{DATA_PATH}/defillama/treasury/{ptc_slug}.json", "w", encoding="utf-8"
    ) as target_file:
        json.dump(data_json, target_file, indent=4)


if __name__ == "__main__":
    # fetch_llama_protocol_lst(save_path=f"{DATA_PATH}/defillama/protocol_lst.json")
    # fetch_llama_tvl(ptc_slug="aave_v2")
    # fetch_llama_treasury(ptc_slug="yearn-finance")
    fetch_llama_total_tvl_eth()
