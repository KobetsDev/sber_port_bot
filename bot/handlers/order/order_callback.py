
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.dialog_calendar_add_order import (
    DialogCalendarAddOrder, calendar_add_order_callback)
from keyboards.inline.dialog_calendar_remove_order import (
    DialogCalendarRemoveOrder, calendar_remove_order_callback)
from loader import dp
from states.states import OrderState
from utils.misc.throttling import rate_limit
from utils.mongo.orders_class import Orders
from data.config import HUMAN_MONTHS


@rate_limit(3)
@dp.callback_query_handler(calendar_add_order_callback.filter(), state='*')
async def dialog_calendar_add(query: CallbackQuery, callback_data: dict, state: FSMContext):
    """Добавляем"""
    selected, date = await DialogCalendarAddOrder().process_selection(query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['date'] = date
        await query.message.answer('Скиньте ссылку на распоряжение')
        await OrderState.link.set()


@rate_limit(3)
@dp.callback_query_handler(calendar_remove_order_callback.filter(), state='*')
async def dialog_calendar_remove(query: CallbackQuery, callback_data: dict):
    """Удаляем"""
    selected, date = await DialogCalendarRemoveOrder().process_selection(query, callback_data)
    if selected:
        year: int = date.year
        month: int = date.month
        if await Orders.delete_order(year, month):
            await query.message.answer(f'Распоряжения для *{year} {HUMAN_MONTHS[month]}* удалено\!')
        else:
            await query.message.answer('Не могу найти распоряжение')
