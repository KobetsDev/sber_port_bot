
import logging
import os
import time
from datetime import datetime
from itertools import groupby

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import escape_md
from data.config import HIDE_TITLE
from decorators import check_permission, check_user
from keyboards.default.cancel import cancel
from keyboards.inline.dialog_calendar import DialogCalendar, calendar_callback
from keyboards.inline.edit import edit_keyboard
from keyboards.inline.event import subscribe_keyboard
from loader import dp
from states.states import EventState
from utils.create_xlsx import create_table
from utils.escape_md import escape
from utils.misc.throttling import rate_limit
from utils.mongo.events_class import Events

from .events import print_events


@rate_limit(3)
@dp.callback_query_handler(text_startswith='delete_')
@check_user
@check_permission
async def delete_callback_handler(query: CallbackQuery, user: dict):
    '''Если нажата кнопка удаления'''
    _id: str = query.data.split('_')[1]
    event: bool | dict = await Events.get_one(_id)
    delete: bool = await Events.delete(_id=_id)
    if event and delete:
        await query.answer('Мероприятие удалено!')
        await query.message.delete()
    else:
        return await query.answer('Ошибка!')


@rate_limit(3)
@dp.callback_query_handler(text_startswith='view_participants')
@check_user
@check_permission
async def view_participants_handler(query: CallbackQuery, user: dict):
    '''Участники мероприятия'''
    _id: str = query.data.split('_')[2]

    event: bool | dict = await Events.get_one(_id)
    if not event:
        return await query.answer('Ошибка!')
    if not event.get('participants'):
        return await query.answer('Ещё нет участников!')
    file_name = f"{datetime.utcfromtimestamp(event.get('timestamp')).strftime('%Y-%m-%d')}_{event.get('title').replace(' ', '_')}"
    file_path = os.path.join('file', f'{file_name}.xlsx')  # f'file\\{file_name}.xlsx'
    await create_table(file_path=file_path, participants=event.get('participants'))
    await query.message.answer_document(open(file_path, 'rb'))
    os.remove(file_path)
    await query.answer('')


@rate_limit(3)
@dp.callback_query_handler(text_startswith='hide_')
@check_user
@check_permission
async def hide_callback_handler(query: CallbackQuery, user: dict):
    '''Спрятать мероприятие'''
    _id = query.data.split('_')[1]
    event: bool | dict = await Events.get_one(_id)
    hide: bool = await Events.hide_or_show(_id=_id, type=0)
    if event and hide:
        await query.answer('Мероприятие спрятано!')
        await query.message.edit_caption(caption=HIDE_TITLE+escape_md(query.message.caption))
        return await query.message.edit_reply_markup(reply_markup=edit_keyboard(_id=_id, status=0))
    return await query.answer('Ошибка!')


@rate_limit(3)
@dp.callback_query_handler(text_startswith='show_')
@check_user
@check_permission
async def show_callback_handler(query: CallbackQuery, user: dict):
    '''Показать мероприятие'''
    _id = query.data.split('_')[1]
    event: bool | dict = await Events.get_one(_id)
    show: bool = await Events.hide_or_show(_id=_id, type=1)
    if event and show:
        await query.answer('Мероприятие доступно для всех!')
        await query.message.edit_caption(caption=escape_md(query.message.caption.replace(HIDE_TITLE, '')))
        return await query.message.edit_reply_markup(reply_markup=edit_keyboard(_id=_id, status=1))
    return await query.answer('Ошибка!')


@rate_limit(3)
@dp.callback_query_handler(text_startswith='event_')
@check_user
async def event_callback_handler(query: CallbackQuery, user: dict):
    '''Показать мероприятие по id'''
    query_data = query.data.split('_')
    _id = query_data[1]
    event = await Events.get_one(_id)
    if not event:
        return await query.answer('Ошибка!')
    await query.answer(' ')
    await print_events(
        message=query,
        events=[event],
        edit=True if query_data[-1] == 'edit' else False,
        is_admin=user.get('is_admin')
    )


# @rate_limit(3)
# @dp.callback_query_handler(text_startswith='my_')
# @check_user
# async def my_callback_handler(query: CallbackQuery, user):
#     '''Вывести месяца в которых были мероприятия'''
#     print('user')
#     all_my_events = await Events.get_all_my(
#         user_id=query.message.chat.id,
#         is_admin=user.get('is_admin')
#     )
#     if not all_my_events:
#         return await query.message.answer('Вы пока не участвовали в мероприятиях\!')
#     # Добавляем дату в формате для сравнивания
#     for event in all_my_events:
#         event['datetime'] = datetime.utcfromtimestamp(event.get('timestamp'))
#     # Группируем по дате
#     events_by_year = groupby(all_my_events, key=lambda event: event['datetime'].year)
#     await query.answer(' ')
#     for year, events in events_by_year:
#         keyboard = InlineKeyboardMarkup()
#         for event in events:
#             event = escape(event)
#             keyboard.row(KeyboardButton(event.get('title'), callback_data=f'event_{event.get("_id")}'))
#         await query.message.answer(f'*{year}*', reply_markup=keyboard)

#     # all_my_events_dict = {}
#     # # Сортируем по годам
#     # for event in all_my_events:
#     #     event_datetime = datetime.utcfromtimestamp(event.get('timestamp'))
#     #     year = event_datetime.year
#     #     try:
#     #         all_my_events_dict[year].append(event)
#     #     except:
#     #         all_my_events_dict[year] = [event]
#     # await query.answer(' ')
#     # for event_year, events in all_my_events_dict.items():
#     #     keyboard = InlineKeyboardMarkup()
#     #     for event in events:
#     #         keyboard.row(KeyboardButton(event.get('title'), callback_data=f'event_{event.get("_id")}'))
#     #     await query.message.answer(f'*{event_year}*', reply_markup=keyboard)


@rate_limit(3)
@dp.callback_query_handler(text_startswith='else_')
@check_user
async def else_callback_handler(query: CallbackQuery, user: dict):
    '''Вывести года и мероприятия в них'''
    all_events = await Events.get_all(is_admin=user.get('is_admin'))
    if not all_events:
        return await query.message.answer('До этого мероприятий не было\!')
    # Добавляем дату в формате для сравнивания
    for event in all_events:
        event['datetime'] = datetime.utcfromtimestamp(event.get('timestamp'))
    # Группируем по дате
    events_by_year = groupby(all_events, key=lambda event: event['datetime'].year)
    await query.answer(' ')
    for year, events in events_by_year:
        keyboard = InlineKeyboardMarkup()
        for event in events:
            event = escape(event)
            keyboard.row(KeyboardButton(event.get('title'),
                                        callback_data=f'event_{event.get("_id")}{"_edit" if query.data.split("_")[-1] == "edit" else ""}'))
        await query.message.answer(f'*{year}*', reply_markup=keyboard)


@rate_limit(3)
@dp.callback_query_handler(lambda call: len(call.data) == 24)  # Подходит только id мероприятия
@check_user
async def id_callback_handler(query: CallbackQuery, user: dict):
    answer_data = query.data
    event = await Events.get_one(answer_data)
    if not event:
        return await query.answer('Такого мероприятие уже нет или оно не доступно!')
    ################################

    # Если мероприятие уже прошло
    if event.get('timestamp') < int(time.time()):
        return await query.answer('Мероприятие уже прошло!')
    # Отписываемся
    if query.message.chat.id in event.get('participants'):
        await Events.delete_participant(user_id=query.message.chat.id, event_id=event.get('_id'))
        await query.answer('Вы больше не участник!')
        my_updated_event = await Events.get_one(event.get('_id'))
        return await query.message.edit_reply_markup(reply_markup=subscribe_keyboard(
            participants=len(my_updated_event.get('participants')),
            places=my_updated_event.get('places'),
            _id=str(my_updated_event.get('_id')),
            closed=True if len(my_updated_event.get('participants')) == my_updated_event.get('places') else False,
            iam_participating=True if not query.from_user.id in event.get('participants') else False,
            is_admin=user.get('is_admin')
        ))
    ################################
    # Проверяем свободные места
    if len(event.get('participants')) >= event.get('places'):
        return await query.answer('Места закончились!')
    # Подписываемся
    try:
        await Events.add_participant(user_id=query.message.chat.id, event_id=answer_data)
        await query.answer('Вы успешно зарегистрировались!')
        event = await Events.get_one(answer_data)
        return await query.message.edit_reply_markup(reply_markup=subscribe_keyboard(
            participants=len(event.get('participants')),
            places=event.get('places'),
            _id=str(event.get('_id')),
            closed=True if len(event.get('participants')) == event.get('places') else False,
            iam_participating=True if query.from_user.id in event.get('participants') else False,
            is_admin=user.get('is_admin')
        ))
    except Exception as e:
        logging.error(e)
        await query.answer('Что то пошло не так!')


@rate_limit(3)
@dp.callback_query_handler(calendar_callback.filter(), state='*')
async def dialog_calendar(query: CallbackQuery, callback_data: dict, state: FSMContext):
    """Календарь"""
    selected, date = await DialogCalendar().process_selection(query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['timestamp'] = int(date.timestamp())
        await query.message.answer(
            'Введи кол\-во участников мероприятия', reply_markup=cancel()
        )
        await EventState.next()
