from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)


admin_kb.row(KeyboardButton(text='🎭Мероприятия'),)
#              KeyboardButton(text='📥Моё участие📥'))
admin_kb.row(KeyboardButton(text='📍Добавить мероприятие'),
            #  KeyboardButton(text='✏️Редактировать мероприятие')
             )
admin_kb.row(
    # KeyboardButton(text='👥Все пользователи'),
             KeyboardButton(text='🗿Мои данные🗿'))
# admin_kb.row(
#     KeyboardButton(text='📑Распоряжения'),
#     KeyboardButton(text='🖌Добавить распоряжение'),
#     KeyboardButton(text='🗑Удалить распоряжение'))
# admin_kb.row(KeyboardButton(text='🖌Добавить распоряжение'), KeyboardButton(text='🗑Удалить распоряжение'))
