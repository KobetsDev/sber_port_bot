
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from keyboards.default.cancel import cancel
from loader import dp
from states.states import UpdateState
from utils.misc.throttling import rate_limit


@rate_limit(3)
@dp.callback_query_handler(Text(equals='change_account'))
async def change_account_callback_handler(query: CallbackQuery):
    '''Если нажата кнопка удаления'''
    await query.message.answer('Введи своё ФИО', reply_markup=cancel(update=True))
    await query.answer(' ')
    await UpdateState.update_full_name.set()
