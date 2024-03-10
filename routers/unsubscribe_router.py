from aiogram.fsm.context import FSMContext

from helpers.states import GlobalStates

from aiogram import F, Router
from aiogram.filters import StateFilter

from aiogram.types import Message

unsub = Router()
comm = ["Community 1", "Community 2", "Community 3"]


@unsub.message(StateFilter(GlobalStates.unsubscribing_from_community), F.text == any(comm))
async def unsubscribe(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.confirming_action)
    # if await confirm_action():
    #     await message.answer(f"You've been unsubscribed from {message.text}")

