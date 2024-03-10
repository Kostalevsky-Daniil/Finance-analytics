import asyncio
import logging
import sys

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, Router

import helpers.helpers
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
    dp.include_routers(main_r, payment, confirm)
    bot_cmd = []
    for cmd in helpers.helpers.bot_command:
        bot_cmd.append(BotCommand(command=cmd[0], description=cmd[1]))

    await bot.set_my_commands(bot_cmd)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
