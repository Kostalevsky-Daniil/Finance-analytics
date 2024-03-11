from aiogram import Router
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from helpers.helpers import make_row_keyboard, params, arr1
from helpers.states import GlobalStates

edit = Router()


@edit.message(StateFilter(GlobalStates.editing_community))
async def edit_community(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text in data["data"]:
        await message.answer("Which parameter do you want to edit?", reply_markup=make_row_keyboard(params))
        await state.set_state(GlobalStates.choosing_param)
        await state.set_data({"community": message.text})
    else:
        await message.answer("Choose one of the existing communities")


@edit.message(StateFilter(GlobalStates.choosing_param))
async def choosing_param(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text in params and message.text == "Limit of people":
        data["param"] = message.text
        print(data)
        await message.answer("Enter new value", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(GlobalStates.entering_limit)
        await state.set_data(data)
    elif message.text in params and (message.text == "Name" or message.text == "Description"):
        data["param"] = message.text
        await message.answer("Enter new value", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(GlobalStates.entering_string)
        await state.set_data(data)
    else:
        await message.answer("There is no such parameter")


@edit.message(StateFilter(GlobalStates.entering_limit))
async def entering_limit(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 200000 >= int(message.text) >= 1:
        await message.answer("Successfully changed value")
        await message.answer("New Limit of People = {}".format(message.text), reply_markup=make_row_keyboard(arr1))
        await state.set_state(GlobalStates.waiting_for_action)
    else:
        await message.answer("Enter valid number")


@edit.message(StateFilter(GlobalStates.entering_string))
async def entering_string(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Successfully changed value")
    await message.answer(f"New {data["param"]} = {message.text}", reply_markup=make_row_keyboard(arr1))
    await state.set_state(GlobalStates.waiting_for_action)
