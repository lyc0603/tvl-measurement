"""
Script to fetch the gas price and eth price
"""

import os

from config.constants import DATA_PATH
from environ.data_fetching.fetch_etherscan import get_csv_from_etherscan

# chcek if the market folder exists
if not os.path.exists(f"{DATA_PATH}/market"):
    os.mkdir(f"{DATA_PATH}/market")

# fetch the gas price
get_csv_from_etherscan(series="gasprice")

# fetch the eth price
get_csv_from_etherscan(series="etherprice")
