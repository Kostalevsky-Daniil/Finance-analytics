from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
class GlobalStates(StatesGroup):
    chat_name = State()
    confirmation_chat_name = State()
    limit_of_users = State()
    confirmation_limit_of_users = State()
    price_per_month = State()
    confirmation_price = State()
    description = State()
    confirmation_description = State()
    waiting_for_actions = State()


class changingStates(StatesGroup):
    choosing_existing_community = State()
    writing_new_description = State()
    setting_new_limitOfUsers = State()
    setting_new_price_per_month = State()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

arr1 = ["Description", "Count of people", "Price per month"]