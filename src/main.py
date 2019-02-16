import sys
from typing import List, Generator
from events import HeartBeat, Bid, Listing, Event
from auction import Auction
import argparse
import os


def process(raw_events: List) -> Generator:
    auctions = {}
    errors = []

    for raw_event in raw_events:

        event = Event.decode(raw_event)

        if event is None:
            errors.append({'error': raw_event})

        if isinstance(event, Listing):
            auction = Auction(
                item=event.item,
                end_time=event.end_time,
                reserve_price=event.reserve_price,
                bids=[]
            )
            auctions[event.item] = auction
            continue

        # Route bid to correct auction
        if isinstance(event, Bid):
            if event.item in auctions:
                auctions[event.item].bid(event)
                continue

        # Broadcast HeartBeat to all auctions
        if isinstance(event, HeartBeat):
            for _, auction in auctions.items():
                auction.update(event)
                continue

    for auction in auctions.values():
        yield str(auction)

    if any(errors):
        yield errors


def main(path):
    if not os.path.exists(path):
        print(f'{path} does not exist', file=sys.stderr)
        return

    with open(path) as file:
        raw_events = [r.rstrip('\n') for r in file.readlines()]

    results = process(raw_events)
    for r in results:
        print(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--file', help="event file name e.g. 'tests/output.txt'", required=True)
    args = parser.parse_args()
    main(args.file)
