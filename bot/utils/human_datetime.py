
from datetime import datetime as dt

import pytz

from data.config import HUMAN_MONTHS_TWO


# async def get_datetime(timestamp: int) -> dt:
#     datetime = dt.utcfromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M')
#     print(datetime)
#     return datetime

def get_datetime(timestamp: int) -> dt:
    datetime = dt.utcfromtimestamp(timestamp)
    datetime = datetime.replace(tzinfo=pytz.utc)
    datetime = datetime.astimezone(pytz.timezone('Europe/Moscow'))
    return datetime


# def get_datetime2(timestamp: int) -> dt:
#     datetime = dt.utcfromtimestamp(timestamp)
#     datetime = datetime.replace(tzinfo=pytz.utc)
#     datetime = datetime.astimezone(pytz.timezone('Europe/Moscow'))
#     return datetime


def humanize_datetime(datetime: dt) -> str:
    """timestamp (1700931600) to 26 Ноября в 20:00"""
    day = datetime.day
    month = datetime.month
    year = datetime.year

    hour = datetime.hour
    minute = str(datetime.minute)
    made_time = ''
    if datetime.now().year != year:
        made_time += f'__{year}__'
    made_time += f' {day} {HUMAN_MONTHS_TWO[month]} в {hour}:'
    made_time += '0'+minute if int(minute) < 10 else minute
    return made_time
    # return f'{str(year)+cringe if datetime.now().year != year else ""}{day} {HUMAN_MONTHS_TWO[month]} в {hour}:{minute if minute != 0 else "00"}'


# humanize_datetime(get_datetime(1667464436))
# print(get_datetime(1700931600))
# humanize_datetime(
#     get_datetime2(1700931600)
# )
