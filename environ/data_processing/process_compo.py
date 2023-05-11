"""
Function to process the composition of the receipt tokens
"""

import json

from tqdm import tqdm

from config import constants


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

    # iterate through all keys
    for target_protocol, target_info in tqdm(compo_dict.items()):
        for receipt, _ in target_info[1].items():
            # iterate through other protocols
            for other_protocol, other_info in compo_dict.items():
                for _, other_info in other_info[1].items():
                    # iterate through all composition
                    for other_compo, compo_amount in other_info.items():
                        # if the receipt is in the other composition
                        if (receipt in other_compo) & (compo_amount != 0):
                            # add the flow
                            flow_dict["source"].append(other_protocol)
                            flow_dict["target"].append(target_protocol)
                            flow_dict["contract"].append(other_compo)
                            flow_dict["amount"].append(compo_amount)

    # save the flow dict
    with open(
        f"{constants.PROCESSED_DATA_PATH}/token_flow/defi_flow.json",
        "w",
        encoding="utf-8",
    ) as f_json:
        json.dump(flow_dict, f_json, indent=4)


if __name__ == "__main__":
    _process_compo()
