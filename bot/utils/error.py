import logging

from aiogram import Dispatcher
from aiogram.types import User
from aiogram.utils.markdown import escape_md
from data.config import CONTACT

from .notify_admins import need_assistance


async def error_msg(dp: Dispatcher, user_data: User):
    try:
        await dp.bot.send_message(user_data.id, f'Произошла какая то ошибка. Напишите {escape_md(CONTACT)}')
        await need_assistance(dp, user_data)
    except Exception as err:
        logging.exception(err)
