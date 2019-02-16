import pytest
from main import process
import pytest


def test_given_scenario():
    raw_events = [
        '10|1|SELL|toaster_1|10.00|20',
        '12|8|BID|toaster_1|7.50',
        '13|5|BID|toaster_1|12.50',
        '15|8|SELL|tv_1|250.00|20',
        '16',
        '17|8|BID|toaster_1|20.00',
        '18|1|BID|tv_1|150.00',
        '19|3|BID|tv_1|200.00',
        '20',
        '21|3|BID|tv_1|300.00'
    ]

    results = process(raw_events)

    assert list(results) == [
        '20|toaster_1|8|SOLD|12.50|3|20.00|7.50',
        '20|tv_1||UNSOLD|0.00|2|200.00|150.00'
    ]


def test_no_bids():
    raw_events = [
        '10|1|SELL|toaster_1|10.00|20',
        '15|8|SELL|tv_1|250.00|20',
        '16'
    ]

    results = process(raw_events)

    assert list(results) == [
        '20|toaster_1||UNSOLD|0.00|0|0.00|0.00',
        '20|tv_1||UNSOLD|0.00|0|0.00|0.00'
    ]


def test_earlier_bid_wins():
    raw_events = [
        '10|1|SELL|toaster_1|10.00|20',
        '13|5|BID|toaster_1|12.50',
        '14|6|BID|toaster_1|12.50',
        '16'
    ]

    results = process(raw_events)

    assert list(results) == [
        '20|toaster_1|5|SOLD|10.00|1|12.50|12.50',
    ]


def test_heartbeat():
    raw_events = [
        '16'
    ]

    results = process(raw_events)

    assert not any(results)
