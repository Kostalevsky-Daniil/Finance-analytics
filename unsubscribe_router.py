import asyncio
import logging
import sys

from aiogram.fsm.context import FSMContext

import config
import helpers
from helpers import arr1, all_states
from states import GlobalStates

from aiogram import F, Router
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ContentType
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from confirm_router import confirm_action


unsub = Router()
comm = ["Community 1", "Community 2", "Community 3"]


@unsub.message(StateFilter(GlobalStates.unsubscribing_from_community), F.text == any(comm))
async def unsubscribe(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.confirming_action)
    # if await confirm_action():
    #     await message.answer(f"You've been unsubscribed from {message.text}")

