from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from keyboards.default.admin_kb import admin_kb
from keyboards.default.main_kb import main_kb
from keyboards.default.register_kb import register_kb
from utils.mongo.user_class import User

true_mass = ['✏️Редактировать мероприятие', '📍Добавить мероприятие',
             '👥Все пользователи', '🎭Мероприятия', '📥Моё участие📥',
             '🗿Мои данные🗿', '📑Распоряжения']
register_command = ['Нужна помощь', 'Регистрация']
admin_command = ['✏️Редактировать мероприятие', '📍Добавить мероприятие',
                 '👥Все пользователи', 
                #  '🖌Добавить распоряжение',
                #  '🗑Удалить распоряжение'
                 ]


class CheckPriveleges(BaseMiddleware):
    """Проверяем привилегию пользователя"""
    async def on_pre_process_message(self, message: Message, data: dict):
        if not message.text \
                or message.text.startswith('/') \
                or message.text in register_command:
            return
        # print('qwe')
        user = await User(message.from_user.id).get_info()
        # Если проходит регистрацию
        if not user and message.text in true_mass:
            await message.reply('Вы не зарегистрированны\!', reply_markup=register_kb)
            raise CancelHandler()
        # print('qwe1')
        # Если отправил команду, которая доступна только для зарегистрированным
        if not user:
            return
        # Обновляем ласт активность
        await User(message.from_user.id).update_last_active()
        # print('qwe3')
        is_admin = user.get("is_admin")
        data['is_admin'] = is_admin
        # Клавиатура
        data['keyboard'] = admin_kb if is_admin else main_kb
        # Проверка на админ права
        # print('qwe')
        if message.text in admin_command:
            if is_admin:
                # print('admin')
                return
            await message.reply('У вас недостаточно прав\!')
            raise CancelHandler()
        # print('end')
        return
