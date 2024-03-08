import asyncio
import logging
import sys

from aiogram import types
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from aiogram.enums import ParseMode
from psycopg2 import *
from aiogram import Bot, Dispatcher

import config

# Разбор системы оплаты и интеграция в код
# Реализация кнопки оплаты подписки + связь с платежной системой
# Реализация отписки от сообщества (легко)
class GlobalStates(StatesGroup):
    creating_community = State()
    viewing_communities = State()
    unsubscribing_from_community = State()
    editing_community = State()

# class CreationStates(StatesGroup):


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [types.KeyboardButton(text="Create community")],
        [types.KeyboardButton(text="See my subscriptions")],
        [types.KeyboardButton(text="Unsubscribe")]
    ]
    # if message.from_user.id in db:
    #     kb += [types.KeyboardButton(text="Edit my communities")]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard)


@dp.message(Command("unsubscribe"))
async def unsubscribe_handler(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer(
            "Error: no arguments provided"
        )
        return
    else:
        community_name = command.args

    # unsubscribe(1223, 23213)
    await message.answer(f"Successfully unsubscribed from {community_name}")


def pay_subscription():
    pass


# Спрашиваем подтверждение
# Удаление из базы данных определенного комьюнити
# Добавление даты когда кикать в бд с отложенными делами
def unsubscribe(uid, cid):
    print("Are you sure you want to unsubscribe? yes/no")
    if input() == "yes":
        print("Unsubscribing...")
        unsubscribe_user(uid, cid)
        print('Unsubscribed user_id: {uid}')
    else:
        print("Exiting...")
    pass


# когда создается комьюнити - настраивается платежка
def set_up_payment():
    pass


def unsubscribe_user(uid, cid):
    con = connect(dbname='subscriptions', user='postgres', password='12345678', host='localhost', port='5432')
    cur = con.cursor()
    cur.execute(f'DELETE FROM subscriptions WHERE user_id = {uid} AND community_id = {cid}')
    cur.close()
    con.close()
    print('Unsubscribed user_id: {uid} ')


async def main() -> None:
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
