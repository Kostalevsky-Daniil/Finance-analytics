from aiogram import F, Router
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from helpers.helpers import bot_in, make_row_keyboard, arr1
from helpers.states import GlobalStates

create = Router()


@create.message(StateFilter(GlobalStates.creating_community))
async def confirm_add_bot(message: types.Message, state: FSMContext):
    community_name = message.text
    if message.text in bot_in:
        await message.reply(f"Great! Community name set to {community_name}. Now, set the limit of users.")
        await state.set_state(GlobalStates.limit_of_users)
    else:
        await message.reply("Please add the bot as an administrator to proceed and restart this action",
                            reply_markup=make_row_keyboard(arr1))
        await state.set_state(GlobalStates.waiting_for_action)


@create.message(F.text, StateFilter(GlobalStates.limit_of_users))
async def get_limit(message: types.Message, state: FSMContext):
    limit_of_users = message.text

    # Check if limit_of_users is a positive integer
    if limit_of_users.isdigit() and int(limit_of_users) > 0:
        # Ask for confirmation
        confirmation_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Confirm"), KeyboardButton(text="Cancel")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        )

        await message.reply(f"Limit of users: {limit_of_users}. Confirm or cancel?", reply_markup=confirmation_keyboard)
        await state.update_data(limit_of_users=int(limit_of_users))
        await state.set_state(GlobalStates.confirmation_limit_of_users)
    else:
        await message.reply("Invalid input. Please enter a positive integer for the limit of users.")


@create.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_limit_of_users))
async def confirm_limit_of_users(message: types.Message, state: FSMContext):
    data = await state.get_data()
    limit_of_users = data.get("limit_of_users")
    await message.reply(f"Limit of users set to {limit_of_users}. Now, set the price per month in USD.")
    await state.set_state(GlobalStates.price_per_month)


@create.message(F.text, StateFilter(GlobalStates.price_per_month))
async def get_price(message: types.Message, state: FSMContext):
    price = message.text

    # Check if price is a positive integer
    if price.isdigit() and int(price) > 0:
        # Ask for confirmation
        confirmation_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Confirm"), KeyboardButton(text="Cancel")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        )

        await message.reply(f"Price per month: {price} USD. Confirm or cancel?", reply_markup=confirmation_keyboard)
        await state.update_data(price=int(price))
        await state.set_state(GlobalStates.confirmation_price)
    else:
        await message.reply("Invalid input. Please enter a positive integer for the price per month.")


@create.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_price))
async def confirm_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    price = data.get("price")
    await message.reply(f"Price per month set to {price} USD. Now, set the channel description.")
    await state.set_state(GlobalStates.description)


@create.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.confirmation_price))
async def cancel_price(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Community registration canceled.")


@create.message(F.text, StateFilter(GlobalStates.description))
async def get_description(message: types.Message, state: FSMContext):
    description = message.text

    # Ask for confirmation
    confirmation_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Confirm"), KeyboardButton(text="Cancel")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    await message.reply(f"Description: {description}. Confirm or cancel?", reply_markup=confirmation_keyboard)
    await state.update_data(description=description)
    await state.set_state(GlobalStates.confirmation_description)


@create.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_description))
async def confirm_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    description = data.get("description")
    await message.reply(f"Description set. Community registration is complete.")
    await state.clear()


@create.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.confirmation_description))
async def cancel_description(message: types.Message, state: FSMContext):
    await state.set_state(GlobalStates.waiting_for_action)
    await message.reply("Community registration canceled.", reply_markup=make_row_keyboard(arr1))
