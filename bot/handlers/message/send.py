from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from keyboards.default.cancel import cancel
from loader import dp, bot
from states.states import MessageState
import asyncio
import logging
from utils.mongo.user_class import User
from aiogram.utils import exceptions
from aiogram.utils.markdown import escape_md
from aiogram.dispatcher import FSMContext
from keyboards.default.cancel import cancel

async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    '''Отравляем сообщения ловля все исключения'''
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False



@dp.message_handler(Text(equals='Отменить отправку', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext, keyboard: ReplyKeyboardMarkup):
    """Отменяем ввод данных для мероприятия"""
    await state.finish()
    await message.reply('ОК', reply=False, reply_markup=keyboard)



@dp.message_handler(Text(equals="Отправить соощение всем пользователям"), state="*")
async def add_events(message: Message):
    await message.answer('Введи текст сообщения', reply_markup=cancel(add=True))
    await MessageState.message.set()



@dp.message_handler(state=MessageState.message)
async def sendMessage(message: Message, state: FSMContext):
    """Текст мероприятия"""
    users = await User(0).get_all()
    for user in users:
        await send_message(user_id=user.get('_id'), text=escape_md(message.text))
    await state.finish()
    await message.answer('Сообщения отправлены')

