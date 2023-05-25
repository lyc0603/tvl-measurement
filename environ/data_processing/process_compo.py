"""
Function to process the composition of the receipt tokens
"""

import json
from functools import partial
import multiprocessing as mp

import pandas as pd
from tqdm import tqdm

from config import constants


def _get_token_price() -> dict[str, float]:
    """
    Function to aggregate all the token price
    """

    # a dict to store the token price
    token_price_dict = {}

    # load all token price data
    for protocol in constants.TVL_LIST:
        # load in the csv file
        token_price_df = pd.read_csv(
            f"{constants.DATA_PATH}/tvl/tvl_composition_Origin.{protocol}.csv"
        )

        # iterate through the rows
        for _, row in token_price_df.iterrows():
            # get the token price
            if row["value"] != 0:
                token_price_dict[row["token_contract"]] = float(row["value"])
            elif row["defillama_value"] != 0:
                token_price_dict[row["token_contract"]] = float(row["defillama_value"])
            else:
                continue
    return token_price_dict


def _process_compo_mp(
    compo_dict: dict,
    queue: mp.Queue,
    receipt: str,
    target_protocol: str = "Uniswap V2",
) -> None:
    """
    Multiprocessing function to figure out the flows between different protocols
    """

    for other_protocol, other_info in compo_dict.items():
        for _, other_info in other_info[1].items():
            # iterate through all composition
            for other_compo, compo_amount in other_info.items():
                # if the receipt is in the other composition
                if (receipt in other_compo) & (compo_amount != 0):
                    # add the flow
                    queue.put(
                        {
                            "source": target_protocol,
                            "target": other_protocol,
                            "contract": other_compo,
                            "amount": compo_amount,
                        }
                    )


def _process_compo(
    json_path: str = f"{constants.DATA_PATH}/composition/defi_compo.json",
):
    """
    Function to figure out the flows between different protocols
    """

    # load all receipts and compo
    with open(json_path, "r", encoding="utf-8") as f_json:
        compo_dict = json.load(f_json)

    # a dict to store the source, target and amount
    flow_dict = {"source": [], "target": [], "contract": [], "amount": []}

    manager = mp.Manager()
    queue = manager.Queue()

    # iterate through all keys
    for target_protocol, target_info in compo_dict.items():
        if target_protocol != "Uniswap V2":
            for receipt, _ in tqdm(target_info[1].items()):
                # iterate through other protocols
                for other_protocol, other_info in compo_dict.items():
                    for _, other_info in other_info[1].items():
                        # iterate through all composition
                        for other_compo, compo_amount in other_info.items():
                            # if the receipt is in the other composition
                            if (receipt in other_compo) & (compo_amount != 0):
                                # add the flow
                                queue.put(
                                    {
                                        "source": target_protocol,
                                        "target": other_protocol,
                                        "contract": other_compo,
                                        "amount": compo_amount,
                                    }
                                )
        else:
            with mp.Pool(processes=8) as pool:
                func = partial(_process_compo_mp, compo_dict, queue)
                _ = list(
                    tqdm(
                        pool.imap(func, target_info[1].keys()),
                        total=len(target_info[1]),
                        desc="Processing",
                        leave=False,
                    )
                )

    # iterate through the queue
    while not queue.empty():
        # get the result
        result = queue.get()

        # append the result to the dict
        for key, value in result.items():
            flow_dict[key].append(value)

    # save the flow dict
    with open(
        f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow.json",
        "w",
        encoding="utf-8",
    ) as f_json:
        json.dump(flow_dict, f_json, indent=4)


if __name__ == "__main__":
    _process_compo()
    # print(_get_token_price())
