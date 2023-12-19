"""
Json encoder
"""

from json import JSONEncoder

from web3.datastructures import AttributeDict
from web3.types import HexBytes


class EthJSONEncoder(JSONEncoder):
    """
    Class for encoding EthJSON
    """

    def default(self, o):
        """
        Method to encode EthJSON
        """
        if isinstance(o, HexBytes):
            return o.hex()
        if isinstance(o, AttributeDict):
            return dict(o)
        if isinstance(o, bytes):
            return o.hex()
        return super().default(o)
