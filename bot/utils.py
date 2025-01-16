import re
from copy import copy
from time import sleep

import aiogram
import aiogram.utils
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery

from other.config import config
import requests.users as rq_users
import other.log.colors as colors
import other.log.logging as logging
from handlers.core import GetLessons
from keyboards.other import __BACK_IN_MAIN_MENU__
from other.PermissionsManager.models import Permissions
from other.PermissionsManager.PermissionsManager import PM


log = logging.logging(Name='UTILS', Color=colors.blue)
auth_users: list[int] = []


class AccessDeniedError(Exception):
    pass


async def GetTimeToLesson(lessons: list[dict[str, str]], current_time: str) -> tuple[int, float] | tuple[int, None]:
    current_hour, current_minute = map(float, str(current_time).split('.'))
    current_time_in_minutes = current_hour * 60 + current_minute

    for i, lesson in enumerate(lessons):
        start_time = sum(float(x) * 60**i for i, x in enumerate(reversed(str(lesson['start_time']).split('.'))))
        end_time = sum(float(x) * 60**i for i, x in enumerate(reversed(str(lesson['end_time']).split('.'))))

        if start_time <= current_time_in_minutes <= end_time:
            return 0, end_time - current_time_in_minutes

        if i < len(lessons) - 1:
            next_start_time = sum(float(x) * 60**i for i, x in enumerate(reversed(lessons[i + 1]['start_time'].split('.'))))
            if end_time < current_time_in_minutes < next_start_time:
                return 1, next_start_time - current_time_in_minutes

    return -1, None


async def newsletter(user_id: int, text: str, auto: bool, bot: aiogram.Bot) -> None:
    log.warn(user_id, 'Start of the mailing')

    users = (await rq_users.GetUsers(user_id))
    timer: int = 0

    for user in users:
        if timer == 29:
            timer = 0
            sleep(1.15)

        try:
            if ((user['send_notifications'] and auto) or not auto) and not user['blocked_bot']:
                await bot.send_message(chat_id=user['user_id'], text=text,
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
                log.info(str(user['user_id']), f'Sent: {user['user_id']}')

        except (TelegramForbiddenError, TelegramBadRequest):
            log.warn(str(user['user_id']), f'User {user['user_id']} has blocked the bot!')
            await rq_users.SetUser(
                user['user_id'],
                user['username'],
                user['first_name'],
                user['last_name'],
                user['send_notifications'],
                True,
                user['role_ids']
            )

        timer += 1

    log.info(user_id, 'Mailing is over')
    await bot.send_message(user_id, '✅ Рассылка закончена!',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
    return


async def SendUpdateLesson(user_id: int, lesson_id: str, bot: aiogram.Bot) -> None:
    await newsletter(user_id=user_id, text=f'⚠ Обновлено Д/З [{await GetLessons().GetName(lesson_id)}]', auto=True, bot=bot)
    return


async def CheckAuthUser(message: Message, bot: aiogram.Bot) -> bool:
    for user_id in auth_users:
        if user_id == message.chat.id:
            return True

    try:
        await rq_users.GetUser(message.chat.id)
    except rq_users.httpx.HTTPStatusError:
        log.info(str(message.chat.id), 'User unauthenticated !')

        await rq_users.SetUser(
            message.chat.id,
            message.chat.username,
            message.chat.first_name,
            message.chat.last_name,
            True,
            [config.ID_ROLE_DEFAULT]
        )
        await bot.send_message(message.chat.id, f'❌ Ошибка аутентификации !\n\n ✅ Данные добавлены !\n\nVersion: {config.RELEASE}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        return False
    else:
        auth_users.append(message.chat.id)
        return True


async def NotificationAdmins(text: str, bot: aiogram.Bot, reply_markup: aiogram.types.InlineKeyboardMarkup | None = None) -> None:
    log.info(None, 'Sending notifications to admins')
    admins = await rq_users.GetAdmins(config.TG_ID_OWNER)

    for admin in admins['admins']:
        try:
            await bot.send_message(chat_id=admin['user_id'], text=text, reply_markup=reply_markup)
            log.info(None, f'Send {admin['user_id']}')
        except (TelegramForbiddenError, TelegramBadRequest):
            log.warn(str(admin['user_id']), f'Admin {admin['user_id']} blocked or didn\'t start the bot!')


async def GetPermissions(user_id: int) -> Permissions | Exception:
    log.info(user_id, f'Getting permissions {user_id}')

    try:
        log.debug(user_id, 'Copying DefaultPermissions')
        permission = copy(PM.DefaultPermissions)

        user = await rq_users.GetUser(user_id)

        for role in user['roles']:
            log.debug(user_id, f'Combining {role['name']} [{role['role_id']}]')
            permission = PM.Combine(user_id, permission, PM.JSONToClass(user_id, role))

        return permission
    except Exception as Error:
        log.error(user_id, f'{Error}')


async def RQReporter(c: CallbackQuery = None, m: Message = None) -> AccessDeniedError:
    if c is not None:
        await c.answer(f'❌ Запрос не удался!\n\nLOG:\ncallback.data: \'{c.data}\'', show_alert=True)
        raise AccessDeniedError

    if m is not None:
        await m.answer('❌ Запрос не удался!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        raise AccessDeniedError


def RemoveHTMLTags(text: str) -> str:
    return re.sub(r'<.*?>', '', text)


def get_permissions(permissions: dict) -> str:
    msg = ''

    for key, value in permissions.items():
        if isinstance(value, dict):
            if 'description' in value and 'value' in value:
                msg += f'- {value['description']}: {'✅' if value['value'] else '❌'}\n'
            else:
                msg += get_permissions(value)

    return msg
