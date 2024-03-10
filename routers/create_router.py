import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, \
    ReplyKeyboardRemove, ContentType
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
import logging
import asyncio

create = Router()


@create.message()
async def new_com(message: types.Message):
    await message.reply("Введите chatId")
    global flag
    flag = 1
