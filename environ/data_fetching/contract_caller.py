"""
Class for calling contract functions
"""

import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import time

from retry import retry
from web3.contract import Contract

from config.logger import logger


class ContractCaller:
    """
    Class for calling contract functions
    """

    def __init__(self, contract: Contract):
        self.contract = contract

    def collect_results(
        self,
        func_name: str,
        blocks: list[int],
    ):
        """
        Method to collect results from contract function calls
        """
        max_workers = multiprocessing.cpu_count() * 5

        def run_task(block: int) -> Optional[tuple[int, float]]:
            """
            Function to run task
            """
            try:
                return self.call_func(func_name, block)
            except Exception as ex:  # pylint: disable=broad-except
                print(f"failed to fetch block {block}: {ex}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(run_task, blocks)
            for _, (block, result) in enumerate(zip(blocks, results)):
                if result is not None:
                    yield (block, result)

    @retry(delay=1, backoff=2, tries=3, logger=logger)
    def call_func(self, func_name: str, block: int) -> Optional[tuple[int, float]]:
        """
        Method to call contract function
        """
        func = getattr(self.contract.functions, func_name)
        time.sleep(5)
        return func().call(block_identifier=block)
