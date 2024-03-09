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





async def unsubscribe_handler(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer("Error: no arguments provided")
        return
    else:
        community_name = command.args
    # запрос в бд для поиска комьюнити и получение его id
    # unsubscribe(1223, 23213)
    await message.answer(f"Successfully unsubscribed from {community_name}")

# Спрашиваем подтверждение
# Удаление из базы данных определенного комьюнити
# Добавление даты когда кикать в бд с отложенными делами
def unsubscribe(uid, cid, false=None):
    print("Are you sure you want to unsubscribe? yes/no")
    if input() == "yes":
        print("Unsubscribing...")
        unsubscribe_user(uid, cid)
        print('Unsubscribed user_id: {uid}')
        return True
    else:
        print("Exiting...")
        return False
    pass


# когда создается комьюнити - настраивается платежка
async def set_up_payment():
    pass


def unsubscribe_user(uid, cid):
    con = connect(dbname='subscriptions', user='postgres', password='12345678', host='localhost', port='5432')
    cur = con.cursor()
    end_date = cur.execute(f"SELECT end_date FROM subscriptions WHERE user_id={uid} AND community_id={cid} ")
    cur.execute(f'DELETE FROM subscriptions WHERE user_id = {uid} AND community_id = {cid}')
    cur.close()
    con.close()
    print('Unsubscribed user_id: {uid} ')


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
