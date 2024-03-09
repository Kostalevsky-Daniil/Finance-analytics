import asyncio
import logging
import sys

from aiogram.fsm.context import FSMContext

import config
import helpers
from helpers import arr1
from States import GlobalStates

from aiogram.methods.send_invoice import SendInvoice
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ReplyKeyboardRemove, ContentType
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from psycopg2 import *

main_r = Router()
create = Router()
unsub = Router()
sub = Router()
view = Router()
edit = Router()
payment = Router()


@main_r.message(CommandStart(), StateFilter(None))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    # con = connect(dbname='communities', user='postgres', password='12345678', host='localhost', port='5432')
    # cur = con.cursor()
    # res = cur.execute(f"SELECT * FROM communities WHERE owner = {message.from_user.id}")
    # cur.close()
    # con.close()
    # if len(res) > 0:
    #    arr1.append("Edit community")
    await message.answer(f"Hello, {message.from_user.full_name}!\n\nChoose one of the actions below:",
                         reply_markup=helpers.make_row_keyboard(arr1))
    await state.set_state(GlobalStates.waiting_for_action)


@main_r.message(F.text == "Create community", StateFilter(GlobalStates.waiting_for_action))
async def create_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.creating_community)
    await message.answer("Creating...", reply_markup=types.ReplyKeyboardRemove())


@main_r.message(F.text == "Edit community", StateFilter(GlobalStates.waiting_for_action))
async def create_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.editing_community)
    await message.answer("Editing...", reply_markup=types.ReplyKeyboardRemove())


@main_r.message(F.text == "See my subscriptions", StateFilter(GlobalStates.waiting_for_action))
async def show_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.viewing_communities)
    await message.answer("Seeing...", reply_markup=types.ReplyKeyboardRemove())


@main_r.message(F.text == "Unsubscribe", StateFilter(GlobalStates.waiting_for_action))
async def unsubscribe_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.unsubscribing_from_community)
    await message.answer("Unsubscribing...", reply_markup=types.ReplyKeyboardRemove())


@main_r.message(F.text == "", StateFilter(GlobalStates.waiting_for_action))
async def create_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.creating_community)
    await message.answer("Creating...", reply_markup=None)


async def unsubscribe_handler(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer(
            "Error: no arguments provided"
        )
        return
    else:
        community_name = command.args
    # запрос в бд для поиска комьюнити и получение его id
    # unsubscribe(1223, 23213)
    await message.answer(f"Successfully unsubscribed from {community_name}")


async def pay_subscription(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.set_state(GlobalStates.waiting_for_payment)
    await bot(SendInvoice(chat_id=message.chat.id, title="Payment", description="monthly payment",
                          payload="Payment for", provider_token=config.STRIPE_TOKEN,
                          currency="USD", prices=[LabeledPrice(label="Monthly Payment", amount=5 * 100)],
                          ))


async def pre_checkout(pre_checkoutquery: PreCheckoutQuery, bot: Bot, state: FSMContext) -> None:
    await bot.answer_pre_checkout_query(pre_checkoutquery.id, ok=True)
    st = await state.get_state()
    print(f"{st}")


@payment.message(lambda x: x.content_type == ContentType.SUCCESSFUL_PAYMENT,
                 StateFilter(GlobalStates.waiting_for_payment))
async def success(message: Message, state: FSMContext) -> None:
    await state.set_state(GlobalStates.waiting_for_action)
    await message.answer("Payment successful", reply_markup=helpers.make_row_keyboard(arr1))


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
def set_up_payment():
    pass


async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


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
    await bot.delete_webhook(drop_pending_updates=True)

    dp.message.register(pay_subscription, GlobalStates.waiting_for_action, Command("pay"))
    dp.pre_checkout_query.register(pre_checkout)
    dp.message(cancel_handler, StateFilter(None), Command('cancel'))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
