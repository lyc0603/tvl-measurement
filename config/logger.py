"""
Logger configuration
"""

import logging

from config.constants import LOG_FORMAT


def _create_logger():
    """
    Function to create logger
    """
    logger = logging.Logger("tvl-measurement")  # pylint: disable=redefined-outer-name
    formatter = logging.Formatter(LOG_FORMAT)
    hander = logging.StreamHandler()
    hander.setFormatter(formatter)
    hander.setLevel(logging.INFO)
    logger.addHandler(hander)

    return logger


logger = _create_logger()
