import asyncio
from utils.set_bot_commands import set_default_commands
from schedule.schedule import scheduler


async def startup(dp):
    # import filters
    import middlewares
    # filters.setup(dp)
    middlewares.setup(dp)

    # from utils.notify_admins import on_startup_notify
    # await on_startup_notify(dp)
    await set_default_commands(dp)

    asyncio.create_task(scheduler())


async def shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp,
                           on_startup=startup,
                           on_shutdown=shutdown)
