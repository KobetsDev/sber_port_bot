
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from keyboards.inline.change_account import change_account
from loader import dp
from utils.misc.throttling import rate_limit
from utils.mongo.user_class import User

from .print_account import print_account


@rate_limit(3, '🗿Мои данные🗿')
@dp.message_handler(Text(equals='🗿Мои данные🗿'), state='*')
async def user_account(message: Message):
    '''Аккаунт пользователя'''
    user = await User(message.from_user.id).get_info()
    await message.answer(text=print_account(user=user, update=True), reply_markup=change_account())
