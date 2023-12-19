"""
Script to fetch Lido protocol data
"""

import json
import os
import sys
from contextlib import contextmanager
from typing import IO, Iterator

import pandas as pd
from eth_typing.evm import Address
from web3 import Web3

from config.constants import DATA_PATH, STETH_ADDRESS
from environ.data_fetching.contract_caller import ContractCaller
from environ.data_fetching.web3_call import eth_w3
from environ.utils.smart_open import smart_open

LIDO_DATA_PATH = f"{DATA_PATH}/lido/"

if not os.path.exists(LIDO_DATA_PATH):
    os.makedirs(LIDO_DATA_PATH)

df_timestamp_block = pd.read_csv(f"{DATA_PATH}/block/block.csv")
blocks = df_timestamp_block.loc[df_timestamp_block["block"] >= 11473216][
    "block"
].tolist()

with open(f"{DATA_PATH}/abi/{STETH_ADDRESS}.json", encoding="utf-8") as f:
    abi = json.load(f)

address: Address = Web3.toChecksumAddress(STETH_ADDRESS)

contract = eth_w3.eth.contract(address=address, abi=abi)
contract_caller = ContractCaller(contract)


@contextmanager
def smart_open_with_stdout(filename, mode="r", **kwargs) -> Iterator[IO]:
    """
    Function to open file
    """
    if filename is None:
        yield sys.stdout
    else:
        with smart_open(filename, mode, **kwargs) as f:
            yield f


with smart_open_with_stdout(f"{DATA_PATH}/lido/steth.json", "w") as f:
    results = contract_caller.collect_results("getTotalPooledEther", blocks)
    for block, result in results:
        line = {"block": block, "result": result}
        json.dump(line, f)
        print(file=f)
