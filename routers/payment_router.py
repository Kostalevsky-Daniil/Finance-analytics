from aiogram.fsm.context import FSMContext

from helpers import config
from helpers.helpers import arr1, make_row_keyboard
from helpers.states import GlobalStates

from aiogram.methods.send_invoice import SendInvoice
from aiogram import F, Router
from aiogram.filters import Command, CommandObject, StateFilter

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ContentType
from aiogram import Bot

payment = Router()
comm = ["Community1", "Community2", "Community3"]


@payment.message(StateFilter(GlobalStates.waiting_for_action), Command("pay"))
async def pay_subscription(message: Message, bot: Bot, state: FSMContext, command: CommandObject) -> None:
    if command.args is not None and len(command.args) > 0 and command.args in comm:
        community_name = command.args
        await state.set_state(GlobalStates.waiting_for_payment)
        await state.set_data({"user_data": [message.from_user.id, community_name]})
        await bot(SendInvoice(chat_id=message.chat.id,
                              title="Payment for {}".format(community_name),
                              description="Monthly payment for {}".format(community_name),
                              payload="Payment",
                              provider_token=config.STRIPE_TOKEN,
                              currency="USD",
                              prices=[LabeledPrice(label="Monthly Payment", amount=1 * 100)],
                              ))
    else:
        await message.answer(f"use /pay"+' *' + 'existing community name' + '*')


@payment.pre_checkout_query()
async def pre_checkout(pre_checkoutquery: PreCheckoutQuery, bot: Bot, state: FSMContext) -> None:
    await bot.answer_pre_checkout_query(pre_checkoutquery.id, ok=True)
    st = await state.get_data()
    print(f"{st}")


@payment.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT,
                 StateFilter(GlobalStates.waiting_for_payment))
async def success(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    uid, c_name = data["user_data"]
    await message.answer("Payment successful", reply_markup=make_row_keyboard(arr1))
    await message.answer(f"Here is your invite to {c_name}: " + "invite link")
    await state.set_data(dict())
    await state.set_state(GlobalStates.waiting_for_action)
