import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL

from helpers import config, helpers
from helpers.helpers import shut_down_event

from db.engine import create_async_engine, get_session_maker, proceed_schema
from db.base import BaseModel
from routers.main_router import main_r
from routers.payment_router import payment
from routers.confirm_router import confirm
from routers.edit_router import edit
from routers.create_router import create
from routers.chat_router import chat




async def main():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(main_r, payment, confirm, edit, create, chat)

    # Database
    # postgres_url = URL.create("postgresql+asyncpg", username="postgres", password="12345678",
    #                           host="localhost", port=5432, database="postgres")
    # print(postgres_url)
    # postgres_url = "postgresql+asyncpg://postgres:12345678@localhost:5432/postgres"
    # async_engine = create_async_engine(postgres_url)
    # # async with async_engine.begin() as con:
    # #     await con.run_sync(BaseModel.metadata.create_all)
    # # session = get_session_maker(async_engine)
    # await proceed_schema(async_engine, BaseModel.metadata)

    await bot.set_my_commands(helpers.bot_cmd)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
