

from data.config import REGISTER_FORM
from utils.escape_md import escape


def print_account(user: dict, update: bool = False):
    '''Вывод в формате информацию о пользователе'''
    user = escape(user)
    return REGISTER_FORM.format(
        (
            f"{user.get('last_name')} {user.get('first_name')} {user.get('patronymic')}"
            if update else
            f"{user.get('full_name')[0]} {user.get('full_name')[1]} {user.get('full_name')[2]}"
        ),
        user.get('faculty'), user.get('group'),
        user.get('phone_number') if user.get('phone_number') else 'Не указан'
    )
