from aiogram.fsm.context import FSMContext
import logging
import helpers
from helpers import arr1, all_states
from States import GlobalStates

from aiogram import F, Router, types
from aiogram.filters import CommandStart,StateFilter, Command

from aiogram.types import Message

main_r = Router()
@main_r.message(CommandStart(), StateFilter(None))
async def command_start_handler(message: Message, state: FSMContext) -> None:
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





@main_r.message(StateFilter(*all_states), Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.set_state(GlobalStates.waiting_for_action)
    await message.answer(
        "Cancelled.",
        reply_markup=helpers.make_row_keyboard(arr1),
    )