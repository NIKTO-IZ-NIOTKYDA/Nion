from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

import utils
from other.config import config
import requests.users as rq_users
import requests.lessons as rq_lessons
from keyboards.admins import GenDeleteLesson
from handlers.core import GetLessons, GetRouter
from keyboards.users import __HOMEWORK__, GenLesson
from handlers.states.lessons import FormNotificationAdmins
from keyboards.other import __BACK_IN_MAIN_MENU__, GenButtonBack


router = GetRouter()


@router.callback_query(F.data == 'lessons')
async def lessons(callback: CallbackQuery):
    if not (await utils.GetPermissions(callback.message.chat.id)).lessons.use:
        try:
            await utils.RQReporter(c=callback)
        except utils.AccessDeniedError:
            return

    await callback.message.edit_text(text='👇 Выберете урок', reply_markup=__HOMEWORK__)


@router.callback_query(F.data.startswith('lesson:show:'))
async def lesson_show(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    if not (await utils.GetPermissions(callback.message.chat.id)).lessons.use:
        try:
            await utils.RQReporter(c=callback)
        except utils.AccessDeniedError:
            return

    calldata = callback.data.replace('lesson:show:', '')
    lesson = await rq_lessons.GetLesson(callback.message.chat.id, calldata)
    markup = await GenLesson(callback.message.chat.id, calldata, lesson['url'])
    homework = lesson['homework'] if lesson['homework'] is not None else config.NO_FOUND_HOMEWORK_MSG

    # Photo
    if lesson['photo'] is not None:
        photo = BufferedInputFile(file=lesson['photo'], filename='image.png')
        await callback.bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=photo,
                caption=homework,
                reply_markup=markup
            )
    else:
        await callback.message.edit_text(homework, reply_markup=markup)


@router.callback_query(F.data.startswith('lesson:nftadmins:'))
async def lesson_nftadmins_comment(callback: CallbackQuery, state: FSMContext):
    if (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework:
        try:
            await utils.RQReporter(c=callback)
        except utils.AccessDeniedError:
            return

    calldata: str = callback.data.replace('lesson:nftadmins:', '')

    try:
        await callback.message.edit_text('⚠️ Введите комментарий в нём можно указать на ошибку или предложить варианты исправления ошибки',
                                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                            [GenButtonBack('lesson:show:' + calldata)],
                                            [__BACK_IN_MAIN_MENU__]
                                             ]))
    except TelegramBadRequest:
        await callback.message.answer('⚠️ Введите комментарий в нём можно указать на ошибку или предложить варианты исправления ошибки',
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                            [GenButtonBack('lesson:show:' + calldata)],
                                            [__BACK_IN_MAIN_MENU__]
                                        ]))

    await state.set_state(FormNotificationAdmins.comment)
    await state.set_data({'lesson_id': calldata})


@router.message(F.text, FormNotificationAdmins.comment)
async def lesson_nftadmins(message: Message, state: FSMContext):
    if (await utils.GetPermissions(message.chat.id)).lessons.edit.homework:
        try:
            await utils.RQReporter(m=message)
        except utils.AccessDeniedError:
            return

    user = await rq_users.GetUser(message.chat.id)

    await utils.NotificationAdmins(
            f'⚠️ Пользователь: @{user['username']} [{user['user_id']}] уведомил вас в неактуальности данный по уроку \'{await GetLessons().GetName((await state.get_data())['lesson_id'])}\'\n\nКомментарий: {message.text}',
            message.bot,
            InlineKeyboardMarkup(inline_keyboard=[[__BACK_IN_MAIN_MENU__]])
        )

    await message.answer('✅ Отчёт отправлен. Извините за неудобства.',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                         [GenButtonBack('lessons')],
                                         [__BACK_IN_MAIN_MENU__]
                                     ]))

    await state.clear()


@router.callback_query(F.data.startswith('lesson:delete_warn:'))
async def lesson_delete_warn(callback: CallbackQuery):
    if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework:
        try:
            await utils.RQReporter(c=callback)
        except utils.AccessDeniedError:
            return

    lesson_id = callback.data.replace('lesson:delete_warn:', '')
    lesson = await rq_lessons.GetLesson(callback.message.chat.id, lesson_id)

    if lesson['homework']:
        StatusHomework = '✅'
    else:
        StatusHomework = '❌'

    if lesson['photo']:
        StatusPhoto = '✅'
    else:
        StatusPhoto = '❌'

    if lesson['url']:
        StatusURL = '✅'
    else:
        StatusURL = '❌'

    try:
        await callback.message.edit_text(f'⚠️ Вы уверены ?\n\nДомашнее задание: {StatusHomework}\nФото: {StatusPhoto}\nURL: {StatusURL}',
                                         reply_markup=await GenDeleteLesson(lesson_id))
    except TelegramBadRequest:
        await callback.message.answer(f'⚠️ Вы уверены ?\n\nДомашнее задание: {StatusHomework}\nФото: {StatusPhoto}\nURL: {StatusURL}',
                                      reply_markup=await GenDeleteLesson(lesson_id))


@router.callback_query(F.data.startswith('lesson:delete:'))
async def lesson_delete(callback: CallbackQuery):
    if not (await utils.GetPermissions(callback.message.chat.id)).lessons.edit.homework:
        try:
            await utils.RQReporter(c=callback)
        except utils.AccessDeniedError:
            return

    lesson_id = callback.data.replace('lesson:delete:', '')

    await rq_lessons.UpdateLesson(callback.message.chat.id, lesson_id, None, None, None)

    await callback.message.edit_text('✅ Успешно !', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [GenButtonBack(f'lesson:show:{lesson_id}')],
        [__BACK_IN_MAIN_MENU__]
    ]))
