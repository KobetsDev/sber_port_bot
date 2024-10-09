
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from data.config import FACULTY_MASS
from keyboards.default.cancel import cancel
from keyboards.default.main_kb import main_kb
from loader import dp
from states.states import RegisterState
from utils.misc.throttling import rate_limit
from utils.mongo.user_class import User

from .print_account import print_account


@rate_limit(3, 'Регистрация')
@dp.message_handler(Text(equals='Регистрация'), state='*')
async def register(message: Message):
    user = await User(message.from_user.id).get_info()
    if user:
        return await message.answer(f'{user.get("first_name")}, вы уже зарегистрированны\!')
    await message.answer('📇Введи своё ФИО', reply_markup=ReplyKeyboardRemove())
    await RegisterState.register_full_name.set()


# @dp.message_handler(Text(equals='Отменить регистрацию', ignore_case=True), state='*')
# async def cancel_register_handler(message: Message, state: FSMContext):
#     """Отменяем ввод данных для мероприятия"""
#     current_state = await state.get_state()
#     if current_state is None:
#         return await message.reply('Пасхалка 1/3\!', reply=False, reply_markup=register_kb)
#     await state.finish()
#     await message.reply('ОК', reply=False, reply_markup=register_kb)


@dp.message_handler(state=RegisterState.register_full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.split()
    if len(full_name) != 3:
        return await message.answer('Вы ввели не полное ФИО\!\nПопробуйте снова')
    async with state.proxy() as data:
        data['full_name'] = [el.title() for el in full_name]
    await message.answer(f'🏢Введи свой факультет:\n' + "\n".join(FACULTY_MASS))
    await RegisterState.register_faculty.set()


@dp.message_handler(state=RegisterState.register_faculty)
async def get_faculty(message: Message, state: FSMContext):
    faculty = message.text.upper()
    if faculty not in [fac.upper() for fac in FACULTY_MASS]:
        return await message.answer('Вы ввели не существующий факультет\!\nПопробуйте снова')
    async with state.proxy() as data:
        data['faculty'] = faculty
    await message.answer('👥Введи свою группу')
    await RegisterState.register_group.set()


@dp.message_handler(state=RegisterState.register_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    async with state.proxy() as data:
        data['group'] = group
    await message.answer('📱Если хочешь, то можете оставить свой телефон для связи\.', reply_markup=cancel(phone=True))
    await RegisterState.register_phone_number.set()


@dp.message_handler(content_types='contact', state=RegisterState.register_phone_number)
async def get_phone_number_on_tg_contact(message: Message, state: FSMContext):
    '''Получаем отправленный через contact тел.'''
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    data = await state.get_data()
    await message.answer(print_account(user=data))
    await message.reply('🎉Отлично\!\nТеперь поклацай по кнопочкам, что бы посмотреть что я умею\.', reply=False, reply_markup=main_kb)
    user = await state.get_data()
    try:
        await User(message.from_user.id).register_user(user=user)
    except Exception as e:
        logging.error(e)
    await state.finish()


@dp.message_handler(content_types='text', state=RegisterState.register_phone_number)
async def get_phone_number_on_write(message: Message, state: FSMContext):
    '''Получаем введённый тел.'''
    data = await state.get_data()
    if message.text == 'Пропустить':
        await message.answer(print_account(user=data))
        await message.reply('🎉Отлично\!\nТеперь поклацай по кнопочкам, что бы посмотреть что я умею\.', reply=False, reply_markup=main_kb)
        user = await state.get_data()
        try:
            await User(message.from_user.id).register_user(user=user)
        except Exception as e:
            logging.error(e)
        await state.finish()
