from events import Event, Bid, Listing, HeartBeat


def test_str_float():
    assert Event.isfloat('0.1')
    assert Event.isfloat('1.0')
    assert Event.isfloat('2.1')
    assert not Event.isfloat('hello')
    assert not Event.isfloat('1sadf')


def test_infer_bids():
    raw_event = '13|5|BID|toaster_1|12.50'
    event = Event.decode(raw_event)
    assert isinstance(event, Bid)
    assert event.timestamp == 13
    assert event.user_id == '5'
    assert event.item == 'toaster_1'
    assert event.bid_amount == 12.50


def test_infer_listing():
    raw_event = '10|1|SELL|toaster_1|10.00|20'
    event = Event.decode(raw_event)
    assert isinstance(event, Listing)
    assert event.timestamp == 10
    assert event.user_id == '1'
    assert event.item == 'toaster_1'
    assert event.reserve_price == 10
    assert event.end_time == 20


def test_infer_heartbeat():
    raw_event = '10'
    event = Event.decode(raw_event)
    assert isinstance(event, HeartBeat)
    assert event.timestamp == 10


def test_garbage_does_not_create_event():
    raw_event = 'adsfasdf'
    event = Event.decode(raw_event)
    assert event is None
