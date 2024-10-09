from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Нужна помощь'),
            # KeyboardButton(text='Регистрация', request_contact=True),
            KeyboardButton(text='Регистрация')
        ],
    ],
    resize_keyboard=True
)
