
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import escape_md
from data.config import CONTACT, FACULTY_MASS
from keyboards.default.cancel import cancel
from keyboards.default.register_kb import register_kb
from loader import dp
from states.states import UpdateState
from utils.mongo.user_class import User

from .print_account import print_account


@dp.message_handler(Text(equals='Отменить редактирование', ignore_case=True), state='*')
async def cancel_update_handler(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    """Отменяем ввод данных для мероприятия"""
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply('Пасхалка 2/3\!', reply=False, reply_markup=keyboard)
    await state.finish()
    await message.answer('ОК', reply_markup=keyboard)


@dp.message_handler(state=UpdateState.update_full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.split()
    if len(full_name) != 3:
        return await message.answer('Мне кажется ты ввёл не полное ФИО\!\nПопробуй снова', reply_markup=cancel(update=True))
    async with state.proxy() as data:
        data['full_name'] = [el.title() for el in full_name]
    await message.answer(f'Введите ваш факультет:\n' + "\n".join(FACULTY_MASS), reply_markup=cancel(update=True))
    await UpdateState.update_faculty.set()


@dp.message_handler(state=UpdateState.update_faculty)
async def get_faculty(message: Message, state: FSMContext):
    faculty = message.text.upper()
    if faculty not in [fac.upper() for fac in FACULTY_MASS]:
        return await message.answer('Вы ввели не существующий факультет\!\nПопробуйте снова', reply_markup=cancel(update=True))
    async with state.proxy() as data:
        data['faculty'] = faculty
    await message.answer('Введите вашу группу', reply_markup=cancel(update=True))
    await UpdateState.update_group.set()


@dp.message_handler(state=UpdateState.update_group)
async def get_group(message: Message, state: FSMContext):
    group = message.text.upper()
    async with state.proxy() as data:
        data['group'] = group
    await message.answer('Если вы хотите, то можете оставить свой телефон для связи\!', reply_markup=cancel(phone=True, update=True))
    await UpdateState.update_phone_number.set()


@dp.message_handler(content_types='contact', state=UpdateState.update_phone_number)
async def get_phone_number_on_tg_contact(message: Message, state: FSMContext):
    '''Получаем отправленный через contact тел.'''
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    data = await state.get_data()
    await message.answer(print_account(user=data))
    await message.answer('Всё правильно?', reply_markup=cancel(with_ok=True))
    await UpdateState.update_check.set()


@dp.message_handler(content_types='text', state=UpdateState.update_phone_number)
async def get_phone_number_on_write(message: Message, state: FSMContext):
    '''Получаем введённый тел.'''
    phone_number = message.text
    data = await state.get_data()
    if phone_number == 'Пропустить':
        await message.answer(print_account(user=data))
        await message.answer('Всё правильно?', reply_markup=cancel(with_ok=True, update=True))
        return await UpdateState.update_check.set()


@dp.message_handler(state=UpdateState.update_check)
async def check(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    if 'да' in message.text.lower():
        user = await state.get_data()
        zap = await User(message.from_user.id).update_user(user=user)
        if zap:
            await message.answer('Всё\! Добро пожаловать', reply_markup=keyboard)
        else:
            await message.answer(f'Ошибка\! Пожалуйста обратитесь к {escape_md(CONTACT)}', reply_markup=keyboard)
    else:
        await message.answer('Данные сброшены', reply_markup=register_kb)
    await state.finish()
