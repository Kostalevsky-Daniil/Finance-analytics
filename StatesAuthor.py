from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
class GlobalStates(StatesGroup):
    description = State()
    price_per_month = State()
    limitOfUsers = State()
    waiting_for_actions = State()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

arr1 = ["Description", "Count of people", "Price per month"]