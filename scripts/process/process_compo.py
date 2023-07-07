"""
Script to process the receipt tokens and their composition eight different protocols
"""

from config.constants import PROCESSED_DATA_PATH
from environ.data_processing.process_compo import _forward_process_compo, _process_compo

# _process_compo()
_forward_process_compo(
    save_path=f"{PROCESSED_DATA_PATH}/non_derivative/non_derivative.json",
)
