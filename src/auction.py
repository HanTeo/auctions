import heapq
from dataclasses import dataclass
from typing import List
from src.events import Bid, HeartBeat


@dataclass
class Auction:
    item: str
    end_time: int
    reserve_price: float
    bids: List

    winner: str = ''
    outcome: str = 'UNSOLD'
    price_paid: float = 0.0
    best_bid_amount: float = 0.0
    max_bid_amount: float = None
    min_bid_amount: float = None

    def isvalid(self, bid: Bid) -> bool:
        criteria = [
            bid.timestamp <= self.end_time,
            bid.bid_amount > self.best_bid_amount
        ]
        return all(criteria)

    def update_best_bid_amount(self):
        nlargest = heapq.nlargest(1, self.bids, key=lambda b: b.bid_amount)
        if any(nlargest):
            self.best_bid_amount = nlargest[0].bid_amount

    def bid(self, bid: Bid):
        if bid.timestamp > self.end_time:
            pass

        if self.isvalid(bid):
            self.bids.append(bid)
            self.update_best_bid_amount()

        if bid.timestamp <= self.end_time:
            self.max_bid_amount = max(self.max_bid_amount, bid.bid_amount) if self.max_bid_amount else bid.bid_amount
            self.min_bid_amount = min(self.min_bid_amount, bid.bid_amount) if self.min_bid_amount else bid.bid_amount

    def update(self, heartbeat: HeartBeat):
        if heartbeat.timestamp < self.end_time:
            pass

        # SOLD condition
        if self.best_bid_amount >= self.reserve_price:
            nlargest = heapq.nlargest(2, self.bids, key=lambda b: b.bid_amount)
            self.outcome = 'SOLD'
            self.winner = nlargest[0].user_id

            # Price paid is the reserve price if there is only one bid
            # otherwise price paid is the next highest bid price
            self.price_paid = self.reserve_price if len(nlargest) < 2 else nlargest[1].bid_amount

        if not any(self.bids):
            self.min_bid_amount = 0.0
            self.max_bid_amount = 0.0

    def __str__(self):
        return f'{self.end_time}|' \
              f'{self.item}|' \
              f'{self.winner}|' \
              f'{self.outcome}|' \
              f'{self.price_paid:.2f}|' \
              f'{len(self.bids)}|' \
              f'{self.max_bid_amount:.2f}|' \
              f'{self.min_bid_amount:.2f}'
