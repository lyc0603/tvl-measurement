"""
fetch gas and ether price from etherscan
"""

import requests

from config.constants import DATA_PATH, USER_AGENT


def get_csv_from_etherscan(
    series: str = "gasprice",
    user_agent: str = USER_AGENT,
) -> bytes:
    """
    download data from etherscan to csv file in GLOBAL_DATA_PATH
    """
    url = f"https://etherscan.io/chart/{series}?output=csv"
    r_data = requests.get(url, headers={"User-Agent": user_agent}, timeout=60)
    # save the data to a csv file
    content = r_data.content
    with open(f"{DATA_PATH}/market/{series}.csv", "wb") as f_data:
        f_data.write(r_data.content)
    return content
