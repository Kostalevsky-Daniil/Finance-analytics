import asyncio
import logging
import sys

from aiogram import Router
from aiogram import Bot, Dispatcher

from helpers import config

from routers.main_router import main_r
from routers.payment_router import payment
from routers.confirm_router import confirm

create = Router()
sub = Router()
view = Router()
edit = Router()


async def main():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(main_r)
    dp.include_router(payment)
    dp.include_router(confirm)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
