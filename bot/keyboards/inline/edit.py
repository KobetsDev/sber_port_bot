from aiogram.types import InlineKeyboardMarkup, KeyboardButton


def edit_keyboard(_id: str, status: int) -> InlineKeyboardMarkup:
    '''Клавиатура удаления'''
    keyboard = InlineKeyboardMarkup(row_width=3)
    one_butt = KeyboardButton(f'Удалить', callback_data=f'delete_{_id}')
    two_butt = KeyboardButton(f'Спрятать', callback_data=f'hide_{_id}') if status else KeyboardButton(
        'Показать', callback_data=f'show_{_id}')
    keyboard.row(one_butt, two_butt)
    return keyboard
