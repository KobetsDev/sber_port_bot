import logging

from aiogram import Dispatcher
from aiogram.utils.markdown import escape_md
from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")

        except Exception as err:
            logging.exception(err)


async def need_assistance(dp: Dispatcher, user_data):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, f"Пользователю {user_data.first_name} @{escape_md(user_data.username)} нужна помощь")

        except Exception as err:
            logging.exception(err)
