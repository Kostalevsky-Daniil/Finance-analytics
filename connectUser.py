import random
import logging
import AuthorLog
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# dif

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ReplyKeyboardRemove, ContentType
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
import logging
import asyncio
import StatesAuthor
from StatesAuthor import arr1
from StatesAuthor import GlobalStates

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="YOUR_BOT_TOKEN")
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
            [KeyboardButton(text="New community"), KeyboardButton(text="Existed community")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    await message.answer("1. Do you want to register a new community?\n"
                         "2. Do you want to edit community INFO?", reply_markup=one_time_keyboard)

@dp.message(F.text.lower() == "new community")
async def new_com(message: types.Message):
    await message.reply("!")

@dp.message(F.text.lower() == "existed community")
async def exist_com(message: types.Message):
    user_id = message.from_user.id

    # Dummy logic for checking if the person is the owner
    is_owner = True
    if is_owner:
        await message.reply("Which community data do you want to edit? (enter the name)\n")
        # Get the user's information
    else:
        await message.reply("You are not the owner of any community.")

@dp.message(F.text)
async def handle_community_name(message: types.Message):
    community_name = message.text
    user_id = message.from_user.id

    # Dummy logic for checking if the community exists and if the person is really the owner
    is_owner = True

    if is_owner:
        await message.answer(f"You are the owner of the community '{community_name}'. ")
        # Keyboard for choosing the field to edit
        one_time_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Description"), KeyboardButton(text="Count of people"),
                 KeyboardButton(text="Price per month")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        await message.answer("Choose the field for editing:", reply_markup=one_time_keyboard)
    else:
        await message.answer(f"You are not the owner of the community '{community_name}'.")

@dp.message(F.text.lower() == "description")
async def set_new_community_description(message: types.Message, state: FSMContext):
    await message.answer("Enter the new description:")
    await state.set_state(GlobalStates.writing_new_description)

@dp.message(
    GlobalStates.writing_new_description,
    F.text
)
async def done_set_new_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.lower())
    await message.answer(
        # request to database (set new INFO)
        text="Description had been changed.",
    )
    await state.set_state(GlobalStates.setting_new_limitOfUsers)

@dp.message(F.text.lower() == "count of people")
async def set_new_community_count_of_people(message: types.Message, state: FSMContext):
    await message.answer("Enter the new count of people:")
    await state.set_state(GlobalStates.setting_new_limitOfUsers)

@dp.message(
    GlobalStates.setting_new_limitOfUsers,
    F.text.isdigit()
)
async def done_set_new_count_of_people(message: Message, state: FSMContext):
    await state.update_data(count_of_people=message.text.isdigit())
    # request to database (set new INFO)
    await message.answer(
        text="Count had been changed.",
    )
    await state.set_state(GlobalStates.setting_new_price_per_month)

@dp.message(F.text.lower() == "price per month")
async def set_new_community_price_per_month(message: types.Message, state: FSMContext):
    await message.answer("Enter the new price per month:")
    await state.set_state(GlobalStates.setting_new_price_per_month)

@dp.message(
    GlobalStates.setting_new_price_per_month,
    F.text.isdigit()
)
async def done_set_new_price_per_month(message: Message, state: FSMContext):
    await state.update_data(price_per_month=message.text.isdigit())
    # request to database (set new INFO)
    await message.answer(
        text="Price had been changed.",
    )
    await state.clear()

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
