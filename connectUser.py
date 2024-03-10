import random
from aiogram.filters import StateFilter
from aiogram import F, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import logging
import asyncio
from StatesAuthor import GlobalStates, changingStates

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="6733664975:AAFvr0jrCGHjhSlg0LM1zCmmHSevjsB96E8")
dp = Dispatcher()
# Dictionary to store unique links for chats
unique_links = {}


# Function to generate a unique chat link
async def generate_unique_link(chat_id):
    link = await bot.create_chat_invite_link(chat_id, member_limit=1)
    unique_links[chat_id] = link
    return link


# Function to check if a user has a paid subscription
async def is_subscription_paid(user_id):
    # Implement logic for checking subscription payment for a specific user
    return True


routerForOwner = Router()


@dp.message(F.text, Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}! I am a chat owner's helper bot.")

    # Keyboard for choosing the user's status
    one_time_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Owner"), KeyboardButton(text="Member")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Choose the status"
    )

    await message.answer("1. Are you the owner?\n"
                         "2. Do you want to join the chat?", reply_markup=one_time_keyboard)


@dp.message(F.text.lower() == "owner")
async def author(message: types.Message):
    # Keyboard for choosing the action for the owner
    one_time_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="New community"), KeyboardButton(text="Existing community")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    await message.answer("1. Do you want to register a new community?\n"
                         "2. Do you want to edit community INFO?", reply_markup=one_time_keyboard)


# -----------------------------------------------------------#new community#--------------------------------------------------------------------

@dp.message(F.text.lower() == "new community")
async def start_new_community(message: types.Message, state: FSMContext):
    one_time_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Cancel")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    await message.reply("To register a new community, please follow these steps:\n"
                        "1. Add me to your group as an administrator.\n"
                        "2. Grant me the rights to invite new members.\n"
                        "3. Send the name of your community.", reply_markup=one_time_keyboard)
    await state.set_state(GlobalStates.chat_name)


@dp.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.chat_name))
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Community registration canceled.")


@dp.message(StateFilter(GlobalStates.chat_name))
async def confirm_add_bot(message: types.Message, state: FSMContext):
    community_name = message.text.lower()
    # check if the bot is administrator
    # chat_member = await bot.get_chat_member(message.chat.id, bot.id)
    chat_member = "administrator"
    if chat_member == "administrator":  # chat_member.status
        await message.reply(f"Great! Community name set to {community_name}. Now, set the limit of users.")
        await state.set_state(GlobalStates.limit_of_users)
    else:
        await message.reply("Please add the bot as an administrator to proceed.")


@dp.message(F.text, StateFilter(GlobalStates.limit_of_users))
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


@dp.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_limit_of_users))
async def confirm_limit_of_users(message: types.Message, state: FSMContext):
    data = await state.get_data()
    limit_of_users = data.get("limit_of_users")
    await message.reply(f"Limit of users set to {limit_of_users}. Now, set the price per month.")
    await state.set_state(GlobalStates.price_per_month)


@dp.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.confirmation_limit_of_users))
async def cancel_limit_of_users(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Community registration canceled.")


@dp.message(F.text, StateFilter(GlobalStates.price_per_month))
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

        await message.reply(f"Price per month: {price}. Confirm or cancel?", reply_markup=confirmation_keyboard)
        await state.update_data(price=int(price))
        await state.set_state(GlobalStates.confirmation_price)
    else:
        await message.reply("Invalid input. Please enter a positive integer for the price per month.")


@dp.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_price))
async def confirm_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    price = data.get("price")
    await message.reply(f"Price per month set to {price}. Now, set the channel description.")
    await state.set_state(GlobalStates.description)


@dp.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.confirmation_price))
async def cancel_price(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Community registration canceled.")


@dp.message(F.text, StateFilter(GlobalStates.description))
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


@dp.message(F.text.lower() == 'confirm', StateFilter(GlobalStates.confirmation_description))
async def confirm_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    description = data.get("description")
    await message.reply(f"Description set. Community registration is complete.")
    await state.clear()


@dp.message(F.text.lower() == 'cancel', StateFilter(GlobalStates.confirmation_description))
async def cancel_description(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Community registration canceled.")


# -----------------------------------------------------------#Existed#--------------------------------------------------------------------

@dp.message(F.text.lower() == "existing community")
async def existed_com(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Dummy logic for checking if the person is the owner
    is_owner = True
    if is_owner:
        await message.reply("Which community data do you want to edit? (enter the name)\n")
        await state.set_state(changingStates.choosing_existing_community)
        # Get the user's information
    else:
        await message.reply("You are not the owner of any community.")


@dp.message(StateFilter(changingStates.choosing_existing_community), F.text)
async def handle_community_name(message: types.Message, state: FSMContext):
    community_name = message.text
    user_id = message.from_user.id

    # Dummy logic for checking if the community exists and if the person is really the owner
    is_owner = True

    if is_owner:
        await message.answer(f"You are the owner of the community '{community_name}'. ")
        await message.answer("Enter new description.")
        await state.set_state(changingStates.writing_new_description)
    else:
        await message.answer(f"You are not the owner of the community '{community_name}'.")


@dp.message(StateFilter(changingStates.writing_new_description), F.text)
async def set_new_community_description(message: types.Message, state: FSMContext):
    await state.update_data(new_description=message.text.lower())
    await state.set_state(changingStates.setting_new_limitOfUsers)
    await message.answer(text="Brilliant, description had been changed. Now set new limit of people.")


@dp.message(StateFilter(changingStates.setting_new_limitOfUsers), F.text)
async def set_new_community_count_of_people(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(count_of_people=message.text.lower())
        await state.set_state(changingStates.setting_new_price_per_month)
        await message.answer(text="Nice, count of people had been changed. Now set new prices per month.")
    else:
        await message.answer(text="You entered not integer value. Try again!")


@dp.message(StateFilter(changingStates.setting_new_price_per_month), F.text)
async def set_new_community_price_per_month(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_month=message.text.lower())
        await state.set_state(changingStates.setting_new_price_per_month)
        await message.answer(text="Price per month had been changed.")
        await state.clear()
    else:
        await message.answer(text="You entered not integer value. Try again!")


@dp.message(F.text.lower() == "member")
async def member(message: types.Message):
    await message.reply("!")


# Bot functions
@dp.message(Command("help"))
async def help_user(message: types.Message):
    await message.answer("1. /start - Start interacting with the bot.\n"
                         "2. /join_chat - Join a private chat by providing the chat ID.\n"
                         "3. /help - Display this help message.")


@dp.message(Command("join_chat"))
async def join_chat(message: types.Message):
    # Ask the user for the chat ID
    await message.answer("Please provide the chat ID you want to join. (Enter any digits, will be changed)")


async def process_chat_id(message: types.Message):
    # Assume the user provided the chat ID
    chat_id_to_join = message.text
    user_id = message.from_user.id

    # Check if the subscription is paid
    if await is_subscription_paid(user_id):
        # Check if the provided chat ID is valid
        if is_valid_chat_id(chat_id_to_join):
            link = await generate_unique_link(-4165995754)
            await message.answer(
                f'{message.from_user.full_name}! Here is your personal link to join the chat: {link.invite_link}')
        else:
            await message.answer(
                f'{message.from_user.full_name}! To gain access to a private chat, pay a monthly subscription.')
    else:
        await message.answer('To gain access to a private chat, pay a monthly subscription.')


@dp.message(F.text.isdigit())
async def process_chat_id_wrapper(message: types.Message):
    await process_chat_id(message)


# Random responses for unrecognized commands or messages
random_responses = [
    "Unfortunately, I don't have the capability to fulfill this request. Can I assist you with something else?",
    "I'm sorry, my abilities are limited, and I cannot process this request. Is there something else you need?",
    "It seems that this is beyond my current capabilities. Can I help you with something different?",
    "Unfortunately, but I'm not designed to handle such tasks. If you have other questions, feel free to ask.",
    "I apologize, but I'm just a bot and don't have that functionality. Can I help with something else?",
]


# Handler for random messages
@dp.message(F.text)
async def process_message(message: types.Message):
    response = random.choice(random_responses)
    await message.reply(response)
    await message.answer("Enter /help; I can show you my abilities.")


# Function to check if the chat ID is valid (you can add your own validation logic here)
def is_valid_chat_id(chat_id):
    return True


# Start the bot
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
