import datetime


def get_now_time_minutes():
    now = datetime.datetime.now()
    return int(now.strftime('%M')) + (int(now.strftime('%H'))*60)