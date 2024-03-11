import datetime

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from helpers.helpers import arr1, make_row_keyboard
from helpers.states import GlobalStates

confirm = Router()


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text != "yes", F.text != "no")
async def confirm_action(message: Message, state: FSMContext):
    comm = await state.get_data()
    await state.set_data({"data": message.text})
    comm = comm["user_communities"]
    if message.text in comm:
        await message.answer("Are you sure?", reply_markup=make_row_keyboard(["yes", "no"]))


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text == "yes")
async def confirm_action(message: Message, state: FSMContext):
    my_community = await state.get_data()
    my_community = my_community["data"]
    # SQL запрос удаляющий пользователя из базы данных
    # Создание таска на кик пользователя из чата или моментальный кик
    # con = connect(dbname='subscriptions', user='postgres', password='12345678', host='localhost', port='5432')
    # cur = con.cursor()
    # end_date = cur.execute(f"SELECT end_date FROM subscriptions WHERE user_id={uid} AND community_id={cid} ")
    # cur.execute(f'DELETE FROM subscriptions WHERE user_id = {uid} AND community_id = {cid}')
    # cur.close()
    # con.close()
    kick_date = datetime.date(2024, 4, 12)
    await state.set_state(GlobalStates.waiting_for_action)
    await message.answer("Succesfully unsubscribed", reply_markup=make_row_keyboard(arr1))
    await message.answer(f"You'll be kicked at {kick_date}", reply_markup=make_row_keyboard(arr1))


@confirm.message(StateFilter(GlobalStates.confirming_action), F.text == "no")
async def confirm_action(message: Message, state: FSMContext):
    await message.answer("Canceling...\n\nSending you back to the main menu",
                         reply_markup=make_row_keyboard(arr1))
    await state.set_state(GlobalStates.waiting_for_action)
