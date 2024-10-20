from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def cancel(with_ok: bool = False, phone: bool = False, update: bool = False, add: bool = False):
    '''Клавиатура сброса вводимых данных

    with_ok: для согласия
    phone: возможность пропустить ввод телефона
    update: специальная "Отмена!" для формы редактирования пользовательских данных
    add: специальная "Отмена!" для формы добавления мероприятия
    '''
    buttons: list[KeyboardButton] = []
    if add:
        buttons.append(
            KeyboardButton(text="Отменить создание")
        )
    elif update:
        buttons.append(
            KeyboardButton(text="Отменить редактирование")
        )

    if with_ok:
        buttons.append(
            KeyboardButton(text="Да")
        )

    if phone:
        # buttons.append(
        #     KeyboardButton(text="Пропустить")
        # )
        buttons.append(
            KeyboardButton(text="Отправить", request_contact=True)
        )
    return ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )
