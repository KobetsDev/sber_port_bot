
import os

from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.markdown import escape_md
from data.config import CONTACT
from loader import dp
from utils.create_xlsx import create_table
from utils.misc.throttling import rate_limit
from utils.mongo.user_class import User


@rate_limit(3, '👥Все пользователи')
@dp.message_handler(Text(equals='👥Все пользователи'), state='*')
async def all_users(message: Message):
    '''Вывод всех пользователей'''
    users = await User(0).get_all()
    file_path = os.path.join('file', 'all_users.xlsx')
    if await create_table(file_path=file_path, participants=users):
        await message.answer_document(document=open(file_path, 'rb'), caption=f'Всего: {len(users)}')
        os.remove(file_path)
    else:
        message.answer(f'Произошла ошибка! Обратитесь за помощью к {escape_md(CONTACT)}')
