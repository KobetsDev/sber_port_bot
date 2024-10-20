
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.event.print_events import print_events
from keyboards.inline.change_account import change_account
from data.config import FACULTY_MASS
from keyboards.default.cancel import cancel
from keyboards.default.main_kb import main_kb
from loader import dp
from states.states import RegisterState
from utils.misc.throttling import rate_limit
from utils.mongo.user_class import User
from utils.mongo.events_class import Events

from .print_account import print_account


@rate_limit(3, 'Регистрация')
@dp.message_handler(Text(equals='Регистрация'), state='*')
async def register(message: Message):
    user = await User(message.from_user.id).get_info()
    if user:
        return await message.answer(f'{user.get("first_name")}, вы уже зарегистрированны\!')
    await message.answer('📇Введи своё ФИО\nНа то имя будт выдат сертификат\!',
                         reply_markup=ReplyKeyboardRemove())
    await RegisterState.register_full_name.set()


@dp.message_handler(Text(equals='Отменить редактирование', ignore_case=True), state='*')
async def cancel_update_handler(message: Message, state: FSMContext, keyboard):
    """Отменяем ввод данных для регистрации"""
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply('Пасхалка 2/3\!', reply=False, reply_markup=keyboard)
    await state.finish()
    await message.answer('ОК', reply_markup=keyboard)


@dp.message_handler(state=RegisterState.register_full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.split()
    if len(full_name) != 3:
        return await message.answer('Вы ввели не полное ФИО\!\nПопробуйте снова')
    async with state.proxy() as data:
        data['full_name'] = [el.title() for el in full_name]
    await message.answer(f'🏢Введи свою почту')
    await RegisterState.register_email.set()


@dp.message_handler(state=RegisterState.register_email)
async def get_faculty(message: Message, state: FSMContext):
    email = message.text#.upper()
    # if faculty not in [fac.upper() for fac in FACULTY_MASS]:
    #     return await message.answer('Вы ввели не существующий факультет\!\nПопробуйте снова')
    async with state.proxy() as data:
        data['email'] = email
    await message.answer('👥Введи свой университет')
    await RegisterState.register_university.set()


@dp.message_handler(state=RegisterState.register_university)
async def get_group(message: Message, state: FSMContext):
    university = message.text.upper()
    async with state.proxy() as data:
        data['university'] = university
    await message.answer('Введи свой факультет\.', reply_markup=cancel())
    await RegisterState.register_faculty.set()

@dp.message_handler(state=RegisterState.register_faculty)
async def get_group(message: Message, state: FSMContext):
    faculty = message.text.upper()
    async with state.proxy() as data:
        data['faculty'] = faculty
    await message.answer('Введи свой курс\.', reply_markup=cancel())
    await RegisterState.register_course.set()
    
@dp.message_handler(state=RegisterState.register_course)
async def get_group(message: Message, state: FSMContext):
    course = message.text.upper()
    async with state.proxy() as data:
        data['course'] = course
    await message.answer('Введи свой телефон\.', reply_markup=cancel(phone=True))
    await RegisterState.register_phone_number.set()


@dp.message_handler(content_types='contact', state=RegisterState.register_phone_number)
async def get_phone_number_on_tg_contact(message: Message, state: FSMContext):
    '''Получаем отправленный через contact тел.'''
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    data = await state.get_data()
    await message.answer(print_account(user=data))
    # await message.reply('🎉Отлично\!\nТеперь поклацай по кнопочкам, что бы посмотреть что я умею\.',
    #                     reply=False, reply_markup=main_kb)
    user = await state.get_data()
    try:
        hasUser  = await User(message.from_user.id).get_info()
        if hasUser:
            await User(message.from_user.id).update_user(user=user)
            await message.answer('Всё\!', reply_markup=main_kb)
        else:
            await User(message.from_user.id).register_user(user=user)
            await message.reply('''Отлично\! Проверь, верно ли указаны данные\?
Это важно, так как сертификат участника TechQuest будет выдан на данные, которые ты указал в анкете\.
Чтобы отредактировать информацию о себе нажми на кнопку "Анкета цчастника"\.''',
                                reply=False, reply_markup=main_kb)
            events = await Events.get_all()
            await print_events(events, useId=message.from_user.id, 
                    #    events, edit=False, is_admin=is_admin
                       )
    except Exception as e:
        logging.error(e)
    await state.finish()


# @dp.message_handler(content_types='text', state=RegisterState.register_phone_number)
# async def get_phone_number_on_write(message: Message, state: FSMContext):
#     '''Получаем введённый тел.'''
#     data = await state.get_data()
#     if message.text == 'Пропустить':
#         await message.answer(print_account(user=data), reply_markup=change_account())
#         user = await state.get_data()
#         try:
#             hasUser  = await User(message.from_user.id).get_info()
#             if hasUser:
#                 await User(message.from_user.id).update_user(user=user)
#                 await message.answer('Всё\! Добро пожаловать', reply_markup=main_kb)
#             else:
#                 await User(message.from_user.id).register_user(user=user)
#                 await message.reply('🎉Отлично\!\nТеперь поклацай по кнопочкам, что бы посмотреть что я умею\.',
#                                     reply=False, reply_markup=main_kb)

#         except Exception as e:
#             logging.error(e)
#         await state.finish()
