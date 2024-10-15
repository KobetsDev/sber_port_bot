import asyncio
import logging

import aioschedule
from loader import bot
from utils.mongo.events_class import Events
from utils.mongo.user_class import User
from aiogram.utils import exceptions
from handlers.event.print_events import print_events

async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    '''Отравляем сообщения ловля все исключения'''
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


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
