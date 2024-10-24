from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)


main_kb.row(KeyboardButton(text='Расписание лекций'),
            # KeyboardButton(text='📥Моё участие📥')
            )
main_kb.row(
    KeyboardButton(text='Задание TechQuest'), 
    KeyboardButton(text='Анкета участника'))
