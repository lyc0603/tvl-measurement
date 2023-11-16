"""
Script to detect and store the liquidation spiral
"""

import json
from dataclasses import dataclass
from typing import List

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/tvl-measurement")
db = client.get_database()

DEFAULT_ASSET = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"

MIN_BLOCK = int(
    db.events.find_one(sort=[("blockNumber", pymongo.ASCENDING)])["blockNumber"]
)

MAX_BLOCK = int(
    db.events.find_one(sort=[("blockNumber", pymongo.DESCENDING)])["blockNumber"]
)


@dataclass
class SpiralEvent:
    """
    Class to represent a spiral event
    """

    address: str
    event: str
    log_index: int


@dataclass
class SpiralMintEvent(SpiralEvent):
    """
    Class to represent a mint event
    """

    mint_amount: int


@dataclass
class SpiralBorrowEvent(SpiralEvent):
    """
    Class to represent a borrow event
    """

    borrow_amount: int


@dataclass
class Spiral:
    """
    Class to represent a spiral
    """

    collateral_asset: str
    block_number: int
    transaction_index: int
    transaction_hash: str
    events: List[SpiralEvent]


def store_leverage_spirals(
    market: str,
    file: str,
    start_block: int = MIN_BLOCK,
    end_block: int = MAX_BLOCK,
):
    """
    Function to store the leverage spirals
    """
    spiral_events = []
    cursor = db.events.find(
        {
            "blockNumber": {
                "$gte": start_block,
                "$lte": end_block,
            }
        }
    ).sort(
        [
            ("blockNumber", pymongo.ASCENDING),
            ("transactionIndex", pymongo.ASCENDING),
            ("logIndex", pymongo.ASCENDING),
        ]
    )
    event = cursor.next()
    assert event["blockNumber"] >= start_block
    candidate_spiral = Spiral(
        collateral_asset=market,
        block_number=event["blockNumber"],
        transaction_index=event["transactionIndex"],
        transaction_hash=event["transactionHash"],
        events=[],
    )
    last_block_number = event["blockNumber"]
    last_tx_index = event["transactionIndex"]

    for event in cursor:
        if "event" not in event.keys():
            candidate_spiral = Spiral(
                collateral_asset=market,
                block_number=event["blockNumber"],
                transaction_index=event["transactionIndex"],
                transaction_hash=event["transactionHash"],
                events=[],
            )
            continue
        if (event["blockNumber"] != last_block_number) or (
            (event["transactionIndex"] != last_tx_index)
            and (event["blockNumber"] == last_block_number)
        ):
            if is_spiral(candidate_spiral):
                print("Spiral:", candidate_spiral)
                spiral_events.append(candidate_spiral)
            last_block_number = event["blockNumber"]
            last_tx_index = event["transactionIndex"]
            candidate_spiral = Spiral(
                collateral_asset=market,
                block_number=event["blockNumber"],
                transaction_index=event["transactionIndex"],
                transaction_hash=event["transactionHash"],
                events=[],
            )
        if (event["event"] == "Mint") and (event["address"].lower() == market.lower()):
            spiral_event = process_mint_event(event)
            candidate_spiral.events.append(spiral_event)
        elif event["event"] == "Borrow":
            spiral_event = process_borrow_event(event)
            candidate_spiral.events.append(spiral_event)

    with open(file, "w", encoding="utf-8") as f:
        json.dump(spiral_events, f)


def process_mint_event(event: dict) -> SpiralEvent:
    """
    Function to process a mint event
    """
    return SpiralMintEvent(
        event=event["event"],
        log_index=event["logIndex"],
        address=event["address"],
        mint_amount=int(event["args"]["mintAmount"]) / 1e18,
    )


def process_borrow_event(event: dict) -> SpiralEvent:
    """
    Function to process a borrow event
    """

    return SpiralBorrowEvent(
        event=event["event"],
        log_index=event["logIndex"],
        address=event["address"],
        borrow_amount=int(event["args"]["borrowAmount"]) / 1e18,
    )


def is_spiral(candidate: Spiral) -> bool:
    """
    Check whether the candidate spiral is a valid spiral
    """

    borrow_events = (1 for k in candidate.events if k.event == "Borrow")
    if sum(borrow_events) <= 1:
        return False

    mint_events = (1 for k in candidate.events if k.event == "Mint")
    if sum(mint_events) <= 1:
        return False

    return True


def main():
    """
    Main function
    """
    store_leverage_spirals(
        market=DEFAULT_ASSET,
        file="spiral",
        start_block=MIN_BLOCK,
        end_block=MAX_BLOCK,
    )


if __name__ == "__main__":
    main()
