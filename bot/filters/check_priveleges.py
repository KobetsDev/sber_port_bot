from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.mongo.user_class import User
from keyboards.default.register_kb import register_kb


class PrivateChatFilter(BoundFilter):
    async def check(self, message: types.Message):
        user = await User(user_id=message.chat.id).get_info()
        if not user:
            return await message.answer(text='Вы не зарегистрированны\!', reply_markup=register_kb)
        if not user.get('is_admin'):
            return await query.answer('У вас недостаточно прав!')
        return len(message.text.replace(".", "")) == 0
