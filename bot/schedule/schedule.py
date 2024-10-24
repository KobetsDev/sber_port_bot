import asyncio
import logging

import aioschedule
from loader import bot
from utils.mongo.events_class import Events
from utils.mongo.user_class import User
from aiogram.utils import exceptions
from handlers.event.print_events import print_events

async def send(event: dict) -> None:
    '''Проходимся по участникам'''
    users = await User(0).get_all()
    for user in users:
        await print_events(events=[event], useId=user.get('_id'))
    await Events.set_notified(_id=event.get('_id'), status=True)


async def send_notify() -> None:
    events = await Events.get_all()
    for event in events:
        notified_status = int(event.get('notified'))
        if not notified_status:
            await send(event)


async def scheduler():
    # aioschedule.every(30).minutes.do(send_notify)
    aioschedule.every(10).seconds.do(send_notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
