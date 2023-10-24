"""
Scripte to aggregate the protocol to be removed
"""

import json

from config.constants import DATA_PATH

with open(
    f"{DATA_PATH}/defillama/protocol_lst.json", "r", encoding="utf-8"
) as target_file:
    data_json = json.load(target_file)

remove_ptc = [
    _["slug"] for _ in data_json if _["category"] == "CEX" or _["category"] == "Chain"
]
