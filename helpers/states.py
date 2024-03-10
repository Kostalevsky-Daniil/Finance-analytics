from aiogram.fsm.state import StatesGroup, State


class GlobalStates(StatesGroup):
    confirmation_price = State()
    description = State()
    confirmation_description = State()
    price_per_month = State()
    limit_of_users = State()
    confirmation_limit_of_users = State()
    chat_name = State()
    waiting_for_payment = State()
    creating_community = State()
    viewing_communities = State()
    unsubscribing_from_community = State()
    editing_community = State()
    confirming_action = State()
    waiting_for_action = State()
    choosing_param = State()
    entering_limit = State()
    entering_string = State()
