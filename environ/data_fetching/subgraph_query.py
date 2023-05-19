"""
Functions related to fetching data from the graph
"""

import json
import time
from typing import Union

import requests

from config.constants import THE_GRAPH_URL


def query_the_graph(query: str, endpoint: str) -> dict:
    """
    Function to fetch data from the graph
    """

    response = requests.post(
        THE_GRAPH_URL + endpoint, json={"query": query}, timeout=120
    )

    if response.status_code == 200:
        return json.loads(response.content)
    raise Exception(f"Query failed. return code is {response.status_code}.{query}")


def run_query_var(
    http: str, query_scripts: str, var: dict[str, Union[int, str]]
) -> dict[str, Union[int, str]]:
    """
    execute query with variable parameters
    """
    while True:
        try:
            # endpoint where you are making the request
            request = requests.post(
                http, "", json={"query": query_scripts, "variables": var}, timeout=120
            )
            if request.status_code == 200:
                return request.json()
        except:  # pylint disable=bare-except
            time.sleep(10)


if __name__ == "__main__":
    # Example of how to use this function
    from config.constants import UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID

    json_response = query_the_graph(UNISWAP_POOLS_QUERY, UNISWAP_V3_SUBGRAPH_ID)
    print(json_response)
    print(len(json_response["data"]["liquidityPools"]))
