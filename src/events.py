from dataclasses import dataclass
from typing import List
from abc import abstractmethod, ABC


@dataclass
class Event(ABC):
    timestamp: int

    @staticmethod
    def infer_event(cols):
        heartbeat = HeartBeat.parse(cols)
        if heartbeat is not None:
            return HeartBeat(timestamp=int(cols[0]))

        listing = Listing.parse(cols)
        if listing is not None:
            return listing

        bid = Bid.parse(cols)
        if bid is not None:
            return bid

    @classmethod
    @abstractmethod
    def _can_parse(cls, cols: List) -> bool:
        """class method to determine if a given list can be parsed into an event"""

    @classmethod
    @abstractmethod
    def parse(cls, tokens):
        """class method to parse a list in an event type"""

    @classmethod
    def isfloat(cls, text):
        try:
            float(text)
            return True
        except ValueError:
            return False


@dataclass
class HeartBeat(Event):

    @classmethod
    def _can_parse(cls, cols: List) -> bool:
        if len(cols) != 1:
            return False
        criteria = [
            cols[0].isdigit()
        ]
        return all(criteria)

    @classmethod
    def parse(cls, tokens):
        if cls._can_parse(tokens):
            return cls(timestamp=tokens[0])


@dataclass
class Bid(Event):
    user_id: str
    item: str
    bid_amount: float

    @classmethod
    def _can_parse(cls, cols):
        if len(cols) != 5:
            return False
        timestamp, user_id, action, item, bid_amount = 0, 1, 2, 3, 4
        criteria = [
            cols[timestamp].isdigit(),
            cols[user_id].isdigit(),
            cols[action] == 'BID',
            cols[item].isidentifier(),
            cls.isfloat(cols[bid_amount])
        ]
        return all(criteria)

    @classmethod
    def parse(cls, tokens):
        if cls._can_parse(tokens):
            timestamp, user_id, action, item, bid_amount = 0, 1, 2, 3, 4
            return cls(
                timestamp=int(tokens[timestamp]),
                user_id=tokens[user_id],
                item=tokens[item],
                bid_amount=float(tokens[bid_amount])
            )


@dataclass
class Listing(Event):
    user_id: str
    item: str
    reserve_price: float
    end_time: int

    @classmethod
    def _can_parse(cls, cols):
        if len(cols) != 6:
            return False
        timestamp, user_id, action, item, reserve_price, end_time = 0, 1, 2, 3, 4, 5
        criteria = [
            cols[timestamp].isdigit(),
            cols[user_id].isdigit(),
            cols[action] == 'SELL',
            cols[item].isidentifier(),
            cls.isfloat(cols[reserve_price]),
            cols[end_time].isdigit()
        ]
        return all(criteria)

    @classmethod
    def parse(cls, cols):
        if cls._can_parse(cols):
            timestamp, user_id, action, item, reserve_price, end_time = 0, 1, 2, 3, 4, 5
            return cls(
                timestamp=int(cols[timestamp]),
                user_id=cols[user_id],
                item=cols[item],
                reserve_price=float(cols[reserve_price]),
                end_time=int(cols[end_time])
            )
