# from aiogram.utils.helper import Helper, HelperMode, ListItem, Item
from aiogram.dispatcher.filters.state import State, StatesGroup


class EventState(StatesGroup):
    # title = State()
    # photo = State()
    text = State()
    jazz = State()
    # date = State()
    # places = State()
    check = State()


class OrderState(StatesGroup):
    date = State()
    link = State()


class UploadState(StatesGroup):
    event = State()
    link = State()


class RegisterState(StatesGroup):
    register_full_name = State()
    register_email = State()
    register_university = State()
    register_phone_number = State()
    register_check = State()


class UpdateState(StatesGroup):
    update_full_name = State()
    update_email = State()
    update_university = State()
    update_phone_number = State()
    update_check = State()
