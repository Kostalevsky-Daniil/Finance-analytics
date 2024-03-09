from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ChatPermissions
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6733664975:AAFvr0jrCGHjhSlg0LM1zCmmHSevjsB96E8")
dp = Dispatcher()

# databases for saving INFO bout owners and chat id's
async def register_chat(chat_id, user_id):
    return
    # here we need to save INFO about chatID and owner ID

async def is_bot_administrator(chat_id):
    # Проверка, является ли бот администратором чата
    try:
        bot_member = await bot.get_chat_member(chat_id, bot.id)
        return bot_member.status in ['administrator', 'member']
    except Exception as e:
        logging.exception(e)
        return False

@dp.message(Command['register_chat'])
async def register_chat_command(message: types.Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        # сheck if the bot admin
        if await is_bot_administrator(chat_id):
            await register_chat(chat_id, user_id)
            await message.reply("Chat successfully registered!")
        else:
            await message.reply("Bot needs to be an administrator to register the chat.")
    except Exception as e:
        logging.exception(e)
        await message.reply("An error occurred while processing your request.")

async def on_startup(dp):
    logging.warning(
        'Bot has been started.'
    )
async def main():
    await dp.start_polling(bot, on_startup=on_startup, skip_updates=True)
if __name__ == '__main__':
    asyncio.run(main())