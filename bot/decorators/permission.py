from aiogram.types import CallbackQuery


def check_permission(func):
    '''Декоратор проверка прав пользователя'''
    async def _wrapper(query: CallbackQuery, user: dict):
        if not user.get('is_admin'):
            return await query.answer('У вас недостаточно прав!')
        await func(query, user)
    return _wrapper
