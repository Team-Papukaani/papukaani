from datetime import datetime

def current_time_as_lajistore_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+"+00:00"
