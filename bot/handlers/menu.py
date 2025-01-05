from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from other.config import config
from utils import CheckAuthUser
from handlers.start import start
from handlers.core import GetRouter
from keyboards.users import GenStart
from requests.users import UpdateUser, GetUser


router = GetRouter()


@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    if await CheckAuthUser(callback.message, callback.message.bot):
        try:
            await callback.message.edit_text(f'Добро пожаловать !\n\nRelease: {config.RELEASE}', reply_markup=await GenStart(callback.message.chat.id))

            user = await GetUser(callback.message.chat.id)
            await UpdateUser(
                callback.message.chat.id,
                callback.message.chat.username,
                callback.message.chat.first_name,
                callback.message.chat.last_name,
                user['send_notifications'],
                [role['role_id'] for role in user['roles']]
            )

        except TelegramBadRequest:
            await start(callback.message)
