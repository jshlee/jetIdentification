import datetime

def get_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M')[2:]

