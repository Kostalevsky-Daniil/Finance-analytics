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

confirm = Router()


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text != "yes", F.text != "no")
async def confirm_action(message: Message, state: FSMContext):
    comm = await state.get_data()
    await state.set_data({"data": message.text})
    print(await state.get_data())
    comm = comm["user_communities"]
    print(message.text)
    if message.text in comm:
        await message.answer("Are you sure?", reply_markup=helpers.make_row_keyboard(["yes", "no"]))


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text == "yes")
async def confirm_action(message: Message, state: FSMContext):
    my_community = await state.get_data()
    my_community = my_community["data"]
    # SQL запрос удаляющий пользователя из базы данных
    # Создание таска на кик пользователя из чата или моментальный кик
    await message.answer("confirmed", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GlobalStates.unsubscribing_from_community)


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text == "no")
async def confirm_action(message: Message, state: FSMContext):
    await message.answer("Canceling...\n\nSending you back to the main menu", reply_markup=helpers.make_row_keyboard(arr1))
    await state.set_state(GlobalStates.waiting_for_action)
