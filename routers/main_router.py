from aiogram.fsm.context import FSMContext
from helpers.helpers import arr1, all_states, make_row_keyboard, params
from helpers.states import GlobalStates

from aiogram import F, Router, types
from aiogram.filters import CommandStart, StateFilter, Command

from aiogram.types import Message

main_r = Router()


@main_r.message(CommandStart(), StateFilter(None))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    # con = connect(dbname='communities', user='postgres', password='12345678', host='localhost', port='5432')
    # cur = con.cursor()
    # res = cur.execute(f"SELECT * FROM communities WHERE owner = {message.from_user.id}")
    # cur.close()
    # con.close()
    # if len(res) > 0:
    #    arr1.append("Edit community")
    await message.answer(f"Hello, {message.from_user.full_name}!\n\nChoose one of the actions below:",
                         reply_markup=make_row_keyboard(arr1))
    await state.set_state(GlobalStates.waiting_for_action)


@main_r.message(F.text == "Create community", StateFilter(GlobalStates.waiting_for_action))
async def create_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.creating_community)
    await message.answer("Creating...", reply_markup=types.ReplyKeyboardRemove())


@main_r.message(F.text == "Edit community", StateFilter(GlobalStates.waiting_for_action))
async def create_handler(message: Message, state: FSMContext):
    # SQL запрос на проверку есть ли комьюнити с овнером = user_id (берем только названия комьюнити)
    res = ["Community1", "Community2", "Community3"]
    # res = []
    if res:
        await message.answer("Which community do you want to edit?", reply_markup=make_row_keyboard(res))
        await state.set_state(GlobalStates.editing_community)
        await state.update_data({'data': res})
    else:
        await message.answer("You don't have any communities to edit!", reply_markup=make_row_keyboard(arr1))


@main_r.message(F.text == "See my subscriptions", StateFilter(GlobalStates.waiting_for_action))
async def show_handler(message: Message, state: FSMContext):
    comm = ["Community 1", "Community 2", "Community 3"] # Вместо этого парсим данные из бд
    s = "\n".join(comm)
    await message.answer("Your communities are: \n\n" + s)


@main_r.message(F.text == "Unsubscribe", StateFilter(GlobalStates.waiting_for_action))
async def unsubscribe_handler(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.confirming_action)
    # проверка состоит ли пользователь в комьюнити
    comm = ["Community 1", "Community 2", "Community 3"]
    await state.set_data({"user_communities": comm})
    await message.answer("Choose a community that you want to leave", reply_markup=make_row_keyboard(comm))


@main_r.message(StateFilter(*all_states), Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is GlobalStates.waiting_for_action or current_state is None:
        return
    await state.set_state(GlobalStates.waiting_for_action)
    await message.answer(
        "Cancelled.",
        reply_markup=make_row_keyboard(arr1),
    )
