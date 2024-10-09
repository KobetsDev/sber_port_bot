from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import Message
from aiogram.utils.markdown import escape_md
from data.config import CONTACT
from loader import dp
from utils.misc import rate_limit

# from utils.notify_admins import need_assistance


@rate_limit(5, 'help')
@dp.message_handler(Text(equals="Нужна помощь"), state='*')
@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    # await need_assistance(dp, message.from_user)
    await message.answer(f'Пожалуйста обратитесь к {escape_md(CONTACT)}')
