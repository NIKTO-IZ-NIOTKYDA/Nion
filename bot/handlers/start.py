from aiogram.types import Message
from aiogram.filters import Command

from utils import CheckAuthUser
from other.config import config
from requests.users import SetUser
from keyboards.users import GenStart
from handlers.core import log, GetRouter


router = GetRouter()


@router.message(Command('start'))
async def start(message: Message) -> None:
    if not await CheckAuthUser(message, message.bot):
        await SetUser(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                True,
                [config.ID_ROLE_DEFAULT]
            )

    await message.answer(f'Добро пожаловать !\n\nVersion: {config.RELEASE}', reply_markup=await GenStart(message.chat.id))
