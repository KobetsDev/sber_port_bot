from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)


main_kb.row(KeyboardButton(text='🎭Мероприятия'), KeyboardButton(text='📥Моё участие📥'))
main_kb.row(KeyboardButton(text='📑Распоряжения'), KeyboardButton(text='🗿Мои данные🗿'))
