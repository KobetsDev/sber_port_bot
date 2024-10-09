
from itertools import groupby
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from data.config import HUMAN_MONTHS
from loader import dp
from utils.misc.throttling import rate_limit
from utils.mongo.orders_class import Orders


@rate_limit(3, '📑Распоряжения')
@dp.message_handler(Text(equals="📑Распоряжения"), state='*')
async def delete_event(message: Message, keyboard: ReplyKeyboardMarkup):
    orders: list = await Orders.get_all_orders()
    if not orders:
        return await message.answer(f'{message.from_user.full_name}, ещё нет добавленных распоряжений\!')
    # Группируем по годам
    orders_by_year = groupby(orders, key=lambda event: event.get('year'))
    for year, orders in orders_by_year:
        await message.answer(f'🗄Распоряжения за *{year}*', reply_markup=keyboard)
        for order in orders:
            await message.answer(f'[{HUMAN_MONTHS[order.get("month")]}]({order.get("link")})', disable_web_page_preview=True)
