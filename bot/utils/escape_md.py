from aiogram.utils.markdown import escape_md


def escape(user: dict):
    '''Проходимся по списку или массиву и изменяем \ на \\'''
    for key, value in user.items():
        if isinstance(user[key], list):
            for num, v in enumerate(user[key]):
                user[key][num] = escape_md(v)
        else:
            if user[key]:
                user[key] = escape_md(value)
    return user
