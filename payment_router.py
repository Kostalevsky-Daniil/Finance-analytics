import asyncio
import logging
import sys

from aiogram.fsm.context import FSMContext

import config
import helpers
from helpers import arr1, all_states
from states import GlobalStates

from aiogram.methods.send_invoice import SendInvoice
from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ContentType
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

payment = Router()


@payment.message(StateFilter(GlobalStates.waiting_for_action), Command("pay"))
async def pay_subscription(message: Message, bot: Bot, state: FSMContext, command: CommandObject) -> None:
    if command.args is not None and len(command.args) > 0:
        comunity_name = command.args[0]
        await state.set_data({"user_data": [message.from_user.id, comunity_name]})
        await state.set_state(GlobalStates.waiting_for_payment)
        await bot(SendInvoice(chat_id=message.chat.id,
                              title="Payment",
                              description="monthly payment",
                              payload="Payment for",
                              provider_token=config.STRIPE_TOKEN,
                              currency="USD",
                              prices=[LabeledPrice(label="Monthly Payment", amount=1 * 100)],
                              ))
    else:
        await message.answer("use /pay \"community_name\"")





@payment.pre_checkout_query()
async def pre_checkout(pre_checkoutquery: PreCheckoutQuery, bot: Bot, state: FSMContext) -> None:
    await bot.answer_pre_checkout_query(pre_checkoutquery.id, ok=True)
    st = await state.get_state()
    print(f"{st}")


@payment.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT,
                 StateFilter(GlobalStates.waiting_for_payment))
async def success(message: Message, state: FSMContext) -> None:
    await state.set_state(GlobalStates.waiting_for_action)
    await message.answer("Payment successful", reply_markup=helpers.make_row_keyboard(arr1))
    # await message.answer(f"{community_name}" + get_invite() + "\n")
