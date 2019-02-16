from dataclasses import dataclass


def isfloat(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


@dataclass
class HeartBeat:
    timestamp: int

    @classmethod
    def _can_parse(cls, tokens):
        if len(tokens) != 1:
            return False
        criteria = [
            tokens[0].isdigit()
        ]
        return all(criteria)

    @classmethod
    def parse(cls, tokens):
        if cls._can_parse(tokens):
            return cls(timestamp=tokens[0])


@dataclass
class Bid:
    timestamp: int
    user_id: str
    item: str
    bid_amount: float

    @classmethod
    def _can_parse(cls, tokens):
        if len(tokens) != 5:
            return False
        timestamp, user_id, action, item, bid_amount = 0, 1, 2, 3, 4
        criteria = [
            tokens[timestamp].isdigit(),
            tokens[user_id].isdigit(),
            tokens[action] == 'BID',
            tokens[item].isidentifier(),
            isfloat(tokens[bid_amount])
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
class Listing:
    timestamp: int
    user_id: str
    item: str
    reserve_price: float
    end_time: int

    @classmethod
    def _can_parse(cls, tokens):
        if len(tokens) != 6:
            return False
        timestamp, user_id, action, item, reserve_price, end_time = 0, 1, 2, 3, 4, 5
        criteria = [
            tokens[timestamp].isdigit(),
            tokens[user_id].isdigit(),
            tokens[action] == 'SELL',
            tokens[item].isidentifier(),
            isfloat(tokens[reserve_price]),
            tokens[end_time].isdigit()
        ]
        return all(criteria)

    @classmethod
    def parse(cls, tokens):
        if cls._can_parse(tokens):
            timestamp, user_id, action, item, reserve_price, end_time = 0, 1, 2, 3, 4, 5
            return cls(
                timestamp=int(tokens[timestamp]),
                user_id=tokens[user_id],
                item=tokens[item],
                reserve_price=float(tokens[reserve_price]),
                end_time=int(tokens[end_time])
            )


def infer_event(tokens):
    heartbeat = HeartBeat.parse(tokens)
    if heartbeat is not None:
        return HeartBeat(timestamp=int(tokens[0]))

    listing = Listing.parse(tokens)
    if listing is not None:
        return listing

    bid = Bid.parse(tokens)
    if bid is not None:
        return bid

    heartbeat = HeartBeat.parse(tokens)
    if heartbeat is not None:
        return heartbeat

    raise ValueError(f'Unknown event {tokens}')
