# from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
#     ReplyKeyboardRemove, ContentType
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram import Bot, Dispatcher, types, F
# from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.context import FSMContext
# from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
# import logging
# import asyncio
# import StatesAuthor
# from StatesAuthor import arr1
# from StatesAuthor import GlobalStates
#
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token="6733664975:AAFvr0jrCGHjhSlg0LM1zCmmHSevjsB96E8")
# dp = Dispatcher()
#
# @dp.message(F.text, Command("editOrRegistrCommunity"))
# async def cmd_start(message: types.Message):
#     # choosing the status of a person
#     one_time_keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="New community"), KeyboardButton(text="Existed community")],
#         ],
#         one_time_keyboard=True,
#         resize_keyboard=True,
#     )
#
#     await message.answer("1. Do you want to registr new community?\n"
#                          "2. Do you want to edit communtity INFO?", reply_markup=one_time_keyboard)
#
# @dp.message(F.text.lower() == "new community")
# async def NewCom(message: types.Message):
#     await message.reply("!")
#
# @dp.message(F.text.lower() == "existed community")
# async def ExistCom(message: types.Message):
#     await message.reply("!")
#
# @dp.message(CommandStart(), StateFilter(None))
# async def command_start_handler(message: Message, state: FSMContext) -> None:
#     await message.answer(f"Hello, {message.from_user.full_name}!\n\nChoose the field for editing:",
#                          reply_markup=StatesAuthor.make_row_keyboard(arr1))
#     await state.set_state(GlobalStates.waiting_for_actions)
#
#
# # databases for saving INFO bout owners and chat id's
# async def register_chat(chat_id, user_id):
#     return
#     # here we need to save INFO about chatID and owner ID
#
#
# async def is_bot_administrator(chat_id):
#     # Проверка, является ли бот администратором чата
#     try:
#         bot_member = await bot.get_chat_member(chat_id, bot.id)
#         return bot_member.status in ['administrator', 'member']
#     except Exception as e:
#         logging.exception(e)
#         return False
#
#
# @dp.message(Command('register_chat'))
# async def register_chat_command(message: types.Message):
#     try:
#         chat_id = message.chat.id
#         user_id = message.from_user.id
#         # сheck if the bot admin
#         if await is_bot_administrator(chat_id):
#             await register_chat(chat_id, user_id)
#             await message.reply("Chat successfully registered!")
#         else:
#             await message.reply("Bot needs to be an administrator to register the chat.")
#     except Exception as e:
#         logging.exception(e)
#         await message.reply("An error occurred while processing your request.")
# async def on_startup(dp):
#     logging.warning(
#         'Bot has been started.'
#     )
# async def main():
#     await dp.start_polling(bot, on_startup=on_startup, skip_updates=True)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
