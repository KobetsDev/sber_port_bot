import asyncio

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    # async def on_pre_process_callback_query(self, message: Message, data: dict):
    #     print('qwe')
    #     handler = current_handler.get()
    #     dispatcher = Dispatcher.get_current()
    #     if handler:
    #         limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
    #         key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
    #     else:
    #         limit = self.rate_limit
    #         key = f"{self.prefix}_message"
    #     try:
    #         await dispatcher.throttle(key, rate=limit)
    #         print('asd1')
    #     except Throttled as t:
    #         print('asd')
    #         await self.message_throttled(message, t)
    #         raise CancelHandler()

    async def message_throttled(self, message: Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.reply('Слишком много запросов\!', reply=False)
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Разблокирован\.', reply=False)
