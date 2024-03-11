from aiogram import Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, RESTRICTED, ADMINISTRATOR, CREATOR
from aiogram.types import ChatMemberUpdated

from helpers.helpers import bot_in

chat = Router()


@chat.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (KICKED | LEFT | -RESTRICTED)
        >>
        (ADMINISTRATOR | CREATOR)
    )
)
async def chat_member(event: ChatMemberUpdated):
    bot_in.add(event.chat.full_name)


@chat.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (ADMINISTRATOR | CREATOR)
        >>
        (KICKED | LEFT | -RESTRICTED)
    )
)
async def chat_member(event: ChatMemberUpdated):
    if event.chat.full_name in bot_in:
        bot_in.remove(event.chat.full_name)
