# from aiogram.utils.helper import Helper, HelperMode, ListItem, Item
from aiogram.dispatcher.filters.state import State, StatesGroup


class EventState(StatesGroup):
    title = State()
    photo = State()
    text = State()
    date = State()
    places = State()
    check = State()


class OrderState(StatesGroup):
    date = State()
    link = State()


class UploadState(StatesGroup):
    event = State()
    link = State()


class RegisterState(StatesGroup):
    register_full_name = State()
    register_faculty = State()
    register_group = State()
    register_phone_number = State()
    register_check = State()


class UpdateState(StatesGroup):
    # Добавить update_ так как путается с register
    update_full_name = State()
    update_faculty = State()
    update_group = State()
    update_phone_number = State()
    update_check = State()
