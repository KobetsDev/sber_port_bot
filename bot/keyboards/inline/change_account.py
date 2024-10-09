from aiogram.types import InlineKeyboardMarkup, KeyboardButton


def change_account() -> InlineKeyboardMarkup:
    '''Клавиатура показа других месяцев'''
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(KeyboardButton('Редактировать', callback_data='change_account'))
    return keyboard
