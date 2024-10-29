from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from keyboards.default.cancel import cancel
from loader import dp, bot
from states.states import BlocksState
import asyncio
import logging
from utils.mongo.user_class import User
from aiogram.utils import exceptions
from aiogram.utils.markdown import escape_md
from aiogram.dispatcher import FSMContext
from keyboards.default.cancel import cancel

# @dp.message_handler(Text(equals='Отменить отправку', ignore_case=True), state='*')
# async def cancel_handler(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
#     """Отменяем ввод данных для мероприятия"""
#     await state.finish()
#     await message.reply('ОК', reply=False, reply_markup=keyboard)
text = '''
В каждом блоке лекций в трансляции выступления спикера зашито кодовое слово.
Вы увидите его на одном из слайдов презентации. Дополнительно спикер сделает акцент на этом слове и напомнит правила задания.
Вы точно не пропустите кодовое слово, если будете смотреть лекцию.

Для того, чтобы получить сертификат участника TechQuest, нужно собрать минимум 3 кодовых слова из 4.
Собирай кодовые слова и вноси их в бот. Список слов можно отредактировать до 23:00 21 декабря.'''

@dp.message_handler(Text(equals="Задание TechQuest"), state="*")
async def add_events(message: Message):
    await message.answer("*Как получить сертификат участника?*" + escape_md(text),
reply_markup=cancel(add=True)
)
    await message.reply(escape_md('Введи кодовое слово 1 блока. Если ты его не знаешь, введи "-"'), reply=False,
                        reply_markup=cancel(add=True))
    await BlocksState.block1.set()



@dp.message_handler(state=BlocksState.block1)
async def block1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['block1'] = message.text
    await message.reply(escape_md('Введи кодовое слово 2 блока. Если ты его не знаешь, введи "-"'), reply=False,
                        reply_markup=cancel(add=True))
    await BlocksState.next()

@dp.message_handler(state=BlocksState.block2)
async def block2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['block2'] = message.text
    await message.reply(escape_md('Введи кодовое слово 3 блока. Если ты его не знаешь, введи "-"'), reply=False,
                        reply_markup=cancel(add=True))
    await BlocksState.next()

@dp.message_handler(state=BlocksState.block3)
async def block3(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['block3'] = message.text
    await message.reply(escape_md('Введи кодовое слово 4 блока. Если ты его не знаешь, введи "-"'), reply=False,
                        reply_markup=cancel(add=True))
    await BlocksState.next()

@dp.message_handler(state=BlocksState.block4)
async def block4(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    async with state.proxy() as data:
        data['block4'] = message.text
    await message.reply(escape_md('Записал!'), reply=False,
                        reply_markup=keyboard)
    event = await state.get_data()
    # print(event)
    await User(message.from_user.id).update_blocks_user(event)
    await state.finish()
