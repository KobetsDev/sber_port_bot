
from keyboards.default.register_kb import register_kb
from utils.mongo.user_class import User


def check_user(func):
    '''Декоратор проверки пользователя'''
    async def _wrapper(query):
        user = await User(user_id=query.message.chat.id).get_info()
        if not user:
            return await query.message.answer(text='Вы не зарегистрированны\!', reply_markup=register_kb)
        await func(query, user)
    return _wrapper
