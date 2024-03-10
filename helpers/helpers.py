from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from helpers.states import GlobalStates


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


arr1 = ["Create community", "See my subscriptions", "Unsubscribe", "Edit community"]
all_states = [GlobalStates.waiting_for_action,
              GlobalStates.waiting_for_payment,
              GlobalStates.viewing_communities,
              GlobalStates.creating_community,
              GlobalStates.unsubscribing_from_community,
              GlobalStates.confirming_action,
              GlobalStates.editing_community]

bot_command = [
    ("start", "Starting the bot"),
    ("pay", "Subscription payment. To use write /pay <Community name>"),
    ("cancel", "Cancel any action")
]
