from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils
import other.log.colors as colors
import other.log.logging as logging
from handlers.core import GetLessons
from keyboards.other import GenLesson, __BACK_IN_MAIN_MENU__

log = logging.logging(Name='INIT', Color=colors.purple)


async def GenDeleteLesson(lesson_id: str):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text='✅ Да ✅', callback_data=f'lesson:delete:{lesson_id}')],
        [InlineKeyboardButton(text='❌ Нет ❌', callback_data=f'lesson:show:{lesson_id}')]
    ])


__PARAGRAPH__ = InlineKeyboardButton(text='§', callback_data='paragraph')
log.init('__PARAGRAPH__' + ': OK')

__UPDATE_HOMEWORK__ = GenLesson(append_text=' (r)', appstart_callback_data='update:homework:', lessons=GetLessons())
__UPDATE_HOMEWORK__.inline_keyboard.append([__PARAGRAPH__])
log.init('__UPDATE_HOMEWORK__' + ': OK')

__UPDATE_HOMEWORK_AND_PHOTO__ = GenLesson(append_text=' (rp)', appstart_callback_data='update:homework_and_photo:', lessons=GetLessons())
__UPDATE_HOMEWORK_AND_PHOTO__.inline_keyboard.append([__PARAGRAPH__])
log.init('__UPDATE_HOMEWORK_P__' + ': OK')

__UPDATE_URL__ = GenLesson(append_text=' (u)', appstart_callback_data='update:url:', lessons=GetLessons())
log.init('__UPDATE_URL__' + ': OK')


__DELETE_SCHEDULE_WARN__ = InlineKeyboardButton(text='❌ Удалить ❌', callback_data='schedule:delete_warn')
log.init('__DELETE_SCHEDULE_WARN__' + ': OK')

__DELETE_SCHEDULE__ = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да ✅', callback_data='schedule:delete')],
    [InlineKeyboardButton(text='❌ Нет ❌', callback_data='schedule')]
])
log.init('__DELETE_SCHEDULE__' + ': OK')


async def GenUpdateMenu(user_id: int) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = [[]]

    if (await utils.GetPermissions(user_id)).lessons.edit.homework:
        buttons[0].append(InlineKeyboardButton(text='Д/З', callback_data='update:homework'))
    
    if (await utils.GetPermissions(user_id)).lessons.edit.url:
        buttons[0].append(InlineKeyboardButton(text='ГДЗ', callback_data='update:url'))
    
    buttons.append([__BACK_IN_MAIN_MENU__])

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)


async def GenAdminPanel(user_id: int) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []

    if (await utils.GetPermissions(user_id)).admin_panel.use.newsletter:
        buttons.append([InlineKeyboardButton(text='Рассылка✉️', callback_data='admin_panel:newsletter_input')])
    
    if (await utils.GetPermissions(user_id)).admin_panel.use.server_status:
        buttons.append([InlineKeyboardButton(text='Статус сервера 🛠️', callback_data='admin_panel:status_server')])
    
    buttons.append([__BACK_IN_MAIN_MENU__])

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)


__NEWSLETTER_WARN__ = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='✅ YES ✅', callback_data='admin_panel:newsletter'),
        InlineKeyboardButton(text='❌ NO ❌', callback_data='admin_panel')
    ]
])
log.init('__NEWSLETTER_WARN__' + ': OK')
