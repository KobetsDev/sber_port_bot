from aiogram.types import InlineKeyboardMarkup, KeyboardButton


def jazz_keyboard(link: str) -> InlineKeyboardMarkup:
    '''Клавиатура удаления'''
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.row(KeyboardButton(f'Ссылка', url=link))
    return keyboard
