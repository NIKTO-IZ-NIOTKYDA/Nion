from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

import utils
import requests.lessons as rq_lessons
from handlers.core import log, GetRouter
from keyboards.other import __BACK_IN_MAIN_MENU__
from handlers.states.update_lesson import FormUpdate
from keyboards.admins import GenUpdateMenu, __UPDATE_HOMEWORK__, __UPDATE_URL__


router = GetRouter()


@router.message(F.text)
async def update_select_category(message: Message, state: FSMContext) -> None:
    if (
        not (await utils.GetPermissions(message.chat.id)).lessons.edit.homework and
        not (await utils.GetPermissions(message.chat.id)).lessons.edit.url
        ):
        try: await utils.RQReporter(m=message)
        except utils.AccessDeniedError: return

    await message.answer('Где нужно поставить этот текст ?', reply_markup=await GenUpdateMenu(message.chat.id))
    
    await state.set_state(FormUpdate.select_category)
    await state.set_data({'text': message.text})


@router.callback_query(F.data, FormUpdate.select_category)
async def update_select_lesson(callback: CallbackQuery, state: FSMContext) -> None:
    
    if callback.data == 'update:homework':
        if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return

        await callback.message.edit_text('👇 Выберете предмет по которому хотите заменить Д/З', reply_markup=__UPDATE_HOMEWORK__)
    elif callback.data == 'update:url':
        if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.url: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return

        await callback.message.edit_text('👇 Выберете предмет по которому хотите заменить ГДЗ', reply_markup=__UPDATE_URL__)

    await state.set_state(FormUpdate.select_lesson)


@router.callback_query(F.data != 'paragraph', FormUpdate.select_lesson)
async def update(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text('⚙️ Выполняется замена, пожалуйста, подождите . . .')
    lesson_id = callback.data.split(':')[-1]

    if callback.data.startswith('update:homework:'):
        if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return
        
        await rq_lessons.UpdateLesson(
                callback.message.chat.id,
                lesson_id,
                homework=(await state.get_data())['text']
            )

        await callback.message.edit_text('✅ Успешно !')

        await callback.message.edit_text('⚠ Активирована система уведомлений . . .', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        await utils.SendUpdateLesson(callback.message.chat.id, lesson_id, bot=callback.bot)

    elif callback.data.startswith('update:homework_and_photo:'):
        if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return
        elif not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.photo: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return

        await rq_lessons.UpdateLesson(
                callback.message.chat.id,
                lesson_id,
                homework=(await state.get_data())['homework'],
                photo=(await state.get_data())['file']
            )

        await callback.message.edit_text('✅ Успешно !')

        await callback.message.edit_text('⚠ Активирована система уведомлений . . .', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))
        await utils.SendUpdateLesson(callback.message.chat.id, lesson_id, bot=callback.bot)

    elif callback.data.startswith('update:url:'):
        if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.url: 
            try: await utils.RQReporter(c=callback)
            except utils.AccessDeniedError: return

        lesson = await rq_lessons.GetLesson(callback.message.chat.id, lesson_id)

        await rq_lessons.UpdateLesson(
            callback.message.chat.id,
            lesson_id,
            homework=lesson['homework'],
            photo=lesson['photo'],
            url=(await state.get_data())['text']
        )

        await callback.message.edit_text('✅ Успешно !', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]]))


@router.callback_query(F.data == 'paragraph')
async def paragraph(callback: CallbackQuery) -> None:
    
    await callback.message.edit_text('<code>§</code>\n\n#paragraph')
