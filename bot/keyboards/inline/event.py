from aiogram.types import InlineKeyboardMarkup, KeyboardButton


def subscribe_keyboard(participants: int,
                       places: int, _id: str,
                       closed: bool, iam_participating: bool,
                       is_admin: bool = False) -> InlineKeyboardMarkup:
    '''Клавиатура записи на мероприятие'''
    keyboard = InlineKeyboardMarkup()
    if closed:
        one_butt = KeyboardButton(text=f'❌Места закончились {participants}/{places}❌', callback_data=_id)
    else:
        if iam_participating:
            one_butt = KeyboardButton(text=f'✅Я участвую {participants}/{places}✅', callback_data=_id)
        else:
            one_butt = KeyboardButton(text=f'Участвовать {participants}/{places}', callback_data=_id)
    keyboard.add(one_butt)
    if participants and is_admin:
        keyboard.row()
        keyboard.insert(KeyboardButton('Участники', callback_data=f'view_participants_{_id}'))
    return keyboard
