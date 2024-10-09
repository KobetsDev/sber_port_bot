import asyncio
import logging
import time

import aioschedule
from loader import bot
from utils.human_datetime import get_datetime, humanize_datetime
from utils.mongo.events_class import Events
from aiogram.utils import exceptions


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


async def send(event: dict, status: int) -> None:
    '''Проходимся по участникам'''
    event_human_datetime = humanize_datetime(get_datetime(event.get('timestamp')))
    for user in event.get('participants'):
        user_chat_info = await bot.get_chat(user)
        await send_message(user_id=user,
                           text=f'{user_chat_info.first_name}, не забудь про *{event.get("title")}* \nОно пройдёт `{event_human_datetime}`')
    await Events.set_notified(_id=event.get('_id'), status=status)


async def send_notify() -> None:
    events = await Events.get_events_for_next_day(is_admin=False)
    for event in events:
        timestamp = event.get('timestamp')
        time_before_event: int = timestamp - int(time.time())
        notified_status = int(event.get('notified'))  # 1 сутки 2 два часа
        # if notified_status != None:  # Если ещё не было напоминаний and notified_status <= 0 TODO странная проверка
        if (3600*2) <= time_before_event <= 86400 and notified_status < 1:
            await send(event=event, status=1)
        elif 0 <= time_before_event <= (3600*2) and notified_status < 2:
            await send(event=event, status=2)


async def scheduler():
    # aioschedule.every(30).minutes.do(send_notify)
    aioschedule.every(1).seconds.do(send_notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
