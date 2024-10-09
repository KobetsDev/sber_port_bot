from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .check_privileges import CheckPriveleges


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckPriveleges())
