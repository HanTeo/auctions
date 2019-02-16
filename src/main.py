from typing import List
from src.events import HeartBeat, Bid, Listing, infer_event
from src.auction import Auction


def process(raw_events: List):

    auctions = {}
    errors = []

    for r in raw_events:
        tokenize = r.split('|')
        event = infer_event(tokenize)

        if event is None:
            errors.append({'error': r})

        if isinstance(event, Listing):
            auction = Auction(
                item=event.item,
                end_time=event.end_time,
                reserve_price=event.reserve_price,
                bids=[]
            )
            auctions[event.item] = auction
            continue

        if isinstance(event, Bid):
            if event.item in auctions:
                auctions[event.item].bid(event)
                continue

        if isinstance(event, HeartBeat):
            for _, auction in auctions.items():
                auction.update(event)
                continue

    for auction in auctions.values():
        yield str(auction)

    if any(errors):
        yield errors
