import asyncio
import logging
import sys

import config

from aiogram import Router
from aiogram.filters import CommandObject

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from psycopg2 import *
from main_router import main_r
from payment_router import payment
from confirm_router import confirm

create = Router()
sub = Router()
view = Router()
edit = Router()


async def main():
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(main_r)
    dp.include_router(payment)
    dp.include_router(confirm)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
