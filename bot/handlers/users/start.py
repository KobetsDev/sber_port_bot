import random

from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from keyboards.default.admin_kb import admin_kb
from keyboards.default.main_kb import main_kb
from keyboards.default.register_kb import register_kb
from loader import dp
from utils.misc.throttling import rate_limit
from utils.mongo.user_class import User


@rate_limit(3, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    user = await User(message.from_user.id).get_info()
    if user:
        admin = user.get("is_admin")
        if admin:
            await message.answer(f'{user.get("first_name")}, добро пожаловать о великий\!', reply_markup=admin_kb)
        else:
            await message.answer(f'{user.get("first_name")}, добро пожаловать домой\.', reply_markup=main_kb)
    else:
        if random.randint(0, 1) == 1:
            await message.answer(f"👀Ты для меня что то новенькое\.\n📄Тебе нужно рассказать о себе, и тогда наше общение пойдёт дальше\.",
                                 reply_markup=register_kb)
        else:
            await message.answer(f"👀Я не узнал вас, но это не повторится\.\n📄Тебе нужно рассказать о себе, что бы я показал что умею\.", reply_markup=register_kb)
