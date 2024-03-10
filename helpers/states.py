from aiogram.fsm.state import StatesGroup, State


class GlobalStates(StatesGroup):
    waiting_for_payment = State()
    creating_community = State()
    viewing_communities = State()
    unsubscribing_from_community = State()
    editing_community = State()
    confirming_action = State()
    waiting_for_action = State()