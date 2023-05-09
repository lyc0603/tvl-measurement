"""
Classes to abstract the collateral
"""


class Collateral:
    """
    Class to record the name, symbol, and address of a collateral
    """

    def __init__(self, name, symbol, address):
        self.name = name
        self.symbol = symbol
        self.address = address


class CollateralInfo:
    """
    Class to record the info of a collateral
    """

    def __init__(self, name, symbol, class_, dec, gem, pip, join):
        self.name = name
        self.symbol = symbol
        self.class_ = class_
        self.dec = dec
        self.gem = gem
        self.pip = pip
        self.join = join


class CollateralData:
    """
    Class to record the data of a collateral
    """

    def __init__(self, Art, rate, spot, line, dust):
        self.Art = Art
        self.rate = rate
        self.spot = spot
        self.line = line
        self.dust = dust
