"""
Function to fetch the current TVL of a given protocol
"""

import time

from tqdm import tqdm

from config.constants import LLAMA_SLUG_LIST, DATA_PATH
from environ.data_fetching.fetch_llama_tvl import fetch_llama_tvl

for ptc_slug in tqdm(LLAMA_SLUG_LIST):
    try:
        # fetch the tvl data
        fetch_llama_tvl(
            ptc_slug=ptc_slug, save_path=f"{DATA_PATH}/defillama/tvl_current"
        )
    except:  # pylint: disable=bare-except
        time.sleep(10)
        print(f"Failed to fetch {ptc_slug}.")
