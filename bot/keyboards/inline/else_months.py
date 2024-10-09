from aiogram.types import KeyboardButton, InlineKeyboardMarkup


def else_months(edit: bool = False) -> InlineKeyboardMarkup:
    '''Клавиатура показа других месяцев'''
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(KeyboardButton('Клац!', callback_data=f'else_{"edit" if edit else ""}'))
    return keyboard
