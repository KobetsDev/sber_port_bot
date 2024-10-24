
import time
from aiogram.utils.markdown import escape_md
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.exceptions import FileIsTooBig
from data.config import CONTACT
from data.config import EVENT_FORM
from keyboards.default.cancel import cancel
from keyboards.inline.jazz import jazz_keyboard
from keyboards.inline.dialog_calendar import DialogCalendar
from loader import dp
from states.states import EventState
from utils.human_datetime import get_datetime, humanize_datetime
from utils.mongo.events_class import Events

# import os


@dp.message_handler(Text(equals='Отменить создание', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    """Отменяем ввод данных для мероприятия"""
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply('Пасхалка 1/3\!', reply=False, reply_markup=keyboard)
    await state.finish()
    await message.reply('ОК', reply=False, reply_markup=keyboard)


# @dp.message_handler(state=EventState.title)
# async def event_title(message: Message, state: FSMContext):
#     """Title мероприятия"""
#     async with state.proxy() as data:
#         data['title'] = message.text
#     # await message.reply('Отправьте одно фото или видео', reply=False, reply_markup=cancel(add=True))
#     await message.reply('Введи текст мероприятия\!', reply=False, reply_markup=cancel(add=True))
#     await EventState.next()


# @dp.message_handler(content_types=['photo', 'video'], state=EventState.photo)
# async def event_media(message: Message, state: FSMContext):
#     """Медиа мероприятия"""
#     # print(message)
#     async with state.proxy() as data:
#         if message.photo:
#             data['media_type'] = 'photo'
#             media_id = message.photo[0].file_id
#         elif message.video:
#             data['media_type'] = 'video'
#             media_id = message.video.file_id
#         try:
#             file_info = await message.bot.get_file(media_id)
#             data['media'] = file_info.file_id
#             await message.reply('Введи текст мероприятия\!', reply=False, reply_markup=cancel(add=True))
#             await EventState.next()
#         except FileIsTooBig as e:
#             logging.error(e)
#             await message.reply('Файл слишком большой! (лимит 20мб)', reply=False, reply_markup=cancel(add=True))


@dp.message_handler(state=EventState.text)
async def event_text(message: Message, state: FSMContext):
    """Текст мероприятия"""
    async with state.proxy() as data:
        data['text'] = message.text
    # await message.reply(f'Выберите дату мероприятия',
    #                     reply=False, reply_markup=await DialogCalendar().start_calendar())
    await message.reply(f'Введи ссылку на jazz',
                        reply=False, reply_markup=cancel(add=True))
    await EventState.next()


@dp.message_handler(state=EventState.jazz)
async def event_jazz(message: Message, state: FSMContext, keyboard):
    """Текст мероприятия"""
    async with state.proxy() as data:
        data['jazz'] = message.text
    await message.reply(f'Всё правильно?', reply=False,
                        reply_markup=cancel(add=True, with_ok=True))
    await EventState.next()
    await message.answer(data.get('text'),  reply_markup=jazz_keyboard(data.get('jazz')))

# @dp.message_handler(state=EventState.places)
# async def event_places(message: Message, state: FSMContext):
#     """Кол-во мест мероприятия"""
#     async with state.proxy() as data:
#         data['places'] = message.text
#     data = await state.get_data()
#     caption = EVENT_FORM.format(
#         escape_md(data.get('title')),
#         escape_md(data.get('text')),
#         humanize_datetime(
#             get_datetime(
#                 data.get('timestamp')
#             )
#         ),
#     ) + f'\(Мест {data.get("places")}\)'
#     # если несколько файлов
#     # if len(data.get('media')) == 1:
#     if data.get('media_type') == 'photo':
#         await message.bot.send_photo(message.from_user.id,
#                                      photo=data.get('media'),
#                                      caption=caption)
#     else:
#         await message.bot.send_video(message.from_user.id,
#                                      video=data.get('media'),
#                                      caption=caption)
#     await message.reply('Всё правильно?', reply=False, reply_markup=cancel(with_ok=True, add=True))
#     await EventState.next()


@dp.message_handler(state=EventState.check)
async def event_check(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    """Проверка мероприятия перед выпуском"""
    if 'да' == (message.text).lower():
        event = await state.get_data()
        event['author'] = message.from_user.id
        event['timestamp'] = int(time.time())
        if not await Events().add_event(event=event):
            await message.answer(f'Произошла ошибка Обратитесь за помощью к {escape_md(CONTACT)}', reply_markup=keyboard)
        else:
            await message.answer('Готово', reply_markup=keyboard)
    else:
        await message.answer('Данные сброшены', reply_markup=keyboard)
    await state.finish()
