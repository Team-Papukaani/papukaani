from datetime import datetime

def current_time_as_lajistore_timestamp():
    return datetime_to_timestamp(datetime.now())

def datetime_to_timestamp(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

def timestamp_to_datetime(timestamp):
    timestamp = timestamp[:-3] + timestamp[-2:]
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")

def timestamp_timeranges_overlap(range_a, range_b):
    return timeranges_overlap(
            (timestamp_to_datetime(range_a[0]), timestamp_to_datetime(range_a[1])),
            (timestamp_to_datetime(range_b[0]), timestamp_to_datetime(range_b[1])))

def timeranges_overlap(range_a, range_b):
    assert(range_a[0] <= range_a[1])
    assert(range_b[0] <= range_b[1])
    if range_a[0] < range_b[0]:
        startsEarlier = range_a
        startsLater = range_b
    else:
        startsEarlier = range_b
        startsLater = range_a
    return startsLater[0] < startsEarlier[1]
