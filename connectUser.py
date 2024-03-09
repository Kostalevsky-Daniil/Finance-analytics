import asyncio
import random
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6733664975:AAFvr0jrCGHjhSlg0LM1zCmmHSevjsB96E8")
dp = Dispatcher()
unique_links = {}
async def generate_unique_link(chat_id):
    link = await bot.create_chat_invite_link(-4165995754, member_limit=1)
    unique_links[-4165995754] = link
    return link
async def is_subscription_paid(user_id):
    # Implement logic for checking subscription payment for a specific user
    return True
@dp.message(F.text, Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}! I'am chat author's helper bot.")
    # choosing the status of a person
    kb = [
        [
            types.KeyboardButton(text="Author"),
            types.KeyboardButton(text="Member")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose the status"
    )
    await message.answer("1. Are you the author?\n"
                         "2. Do you want to join the chat?", reply_markup=keyboard)
@dp.message(F.text.lower() == "author")
async def author(message: types.Message):
    await message.reply("!")

@dp.message(F.text.lower() == "member")
async def member(message: types.Message):
    await message.reply("!")
# bot functions
@dp.message(Command("help"))
async def helpUser(message: types.Message):
    await message.answer("1. /start - Start interacting with the bot.\n"
                         "2. /join_chat - Join a private chat by providing the chat ID.\n"
                         "3. /help - Display this help message.")


@dp.message(Command("join_chat"))
async def join_chat(message: types.Message):
    # Ask the user for the chat ID
    await message.answer("Please provide the chat ID you want to join.")

    @dp.message(F.text.isdigit())
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


random_responses = [
    "Unfortunately, I don't have the capability to fulfill this request. Can I assist you with something else?",
    "I'm sorry, my abilities are limited, and I cannot process this request. Is there something else you need?",
    "It seems that this is beyond my current capabilities. Can I help you with something different?",
    "Unfortunately, but I'm not designed to handle such tasks. If you have other questions, feel free to ask.",
    "I apologize, but I'm just a bot and don't have that functionality. Can I help with something else?",
]
@dp.message(F.text)
async def process_message(message: types.Message):
    response = random.choice(random_responses)
    await message.reply(response)
    await message.answer("Enter /help, i can show you my abilities.")


def is_valid_chat_id(chat_id):
    # try:
    #     int(chat_id)
    #     return True
    # except ValueError:
    #     return False
    return True


# Start the bot
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())