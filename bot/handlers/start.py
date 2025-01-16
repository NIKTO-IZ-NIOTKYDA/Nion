from aiogram.types import Message
from aiogram.filters import Command

from other.config import config
import requests.users as rq_users
from requests.users import SetUser
from handlers.core import GetRouter
from keyboards.users import GenStart


router = GetRouter()


@router.message(Command('start'))
async def start(message: Message) -> None:
    try:
        await rq_users.GetUser(message.chat.id)
    except rq_users.httpx.HTTPStatusError:
        await SetUser(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                True,
                False,
                [config.ID_ROLE_DEFAULT]
            )

    await message.answer(f'Добро пожаловать !\n\nVersion: {config.RELEASE}', reply_markup=await GenStart(message.chat.id))
