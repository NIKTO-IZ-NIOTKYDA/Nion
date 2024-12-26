from platform import system, python_version, release

import psutil
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

import utils
from handlers.core import log, GetRouter
from handlers.states.newsletter import FormNewsletter
from keyboards.other import GenButtonBack, __BACK_IN_MAIN_MENU__
from keyboards.admins import GenAdminPanel, __NEWSLETTER_WARN__


router = GetRouter()


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    log.warn(callback.message.chat.id, 'Admin logged into the panel . . .')

    await callback.message.edit_text('🛠Вы в админ-панели!\nБудьте осторожны‼️', reply_markup=await GenAdminPanel(callback.message.chat.id))

    await state.clear()


@router.callback_query(F.data == 'admin_panel:newsletter_input')
async def admin_panel_newsletter_input(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not (await utils.GetPermissions(callback.message.chat.id)).admin_panel.use.newsletter: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return

    await callback.message.edit_text('Введите текст рассылки')
    await state.set_state(FormNewsletter.input_text)


@router.message(F.text, FormNewsletter.input_text)
async def admin_panel_form_newsletter_input_text(message: Message, state: FSMContext):
    log.info(str(message.chat.id), f'Received \'{message.text}\'')

    if not (await utils.GetPermissions(message.chat.id)).admin_panel.use.newsletter: 
        try: await utils.RQReporter(m=message)
        except utils.AccessDeniedError: return

    await message.answer(f'<b>‼️ВЫ ТОЧНО ХОТИТЕ ОТПРАВИТЬ СООБЩЕНИЕ ВСЕМ ПОЛЬЗОВАТЕЛЯМ⁉️</b>\nТЕКСТ СООБЩЕНИЯ:\n{message.text}', 
                            reply_markup=__NEWSLETTER_WARN__)

    await state.set_state(FormNewsletter.warn)
    await state.set_data({'text': message.text})


@router.callback_query(F.data == 'admin_panel:newsletter', FormNewsletter.warn)
async def admin_panel_newsletter(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')
    
    if not (await utils.GetPermissions(callback.message.chat.id)).admin: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return
    await callback.message.edit_text('✅ Рассылка началась!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [GenButtonBack('admin_panel')],
        [__BACK_IN_MAIN_MENU__]
    ]))

    await utils.newsletter(callback.message.chat.id, str((await state.get_data())['text']), False, callback.message.bot)


@router.callback_query(F.data == 'admin_panel:status_server')
async def admin_panel_status_server(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not (await utils.GetPermissions(callback.message.chat.id)).admin_panel.use.server_status: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return

    log.info(callback.message.chat.id, 'Admin requested a server status report, generation . . .')  

    log.debug(callback.message.chat.id, 'Generating information about: SystemName')
    SystemName = str(system())

    log.debug(callback.message.chat.id, 'Generating information about: SystemRelease')
    SystemRelease = str(release())

    log.debug(callback.message.chat.id, 'Generating information about: PythonVersion')
    PythonVersion = str(python_version())

    # Загруженость
    # CPU
    log.debug(callback.message.chat.id, 'Generating information about: CPU')
    CPU = psutil.cpu_percent(interval=1)

    # Memory
    log.debug(callback.message.chat.id, 'Generating information about: Memory, Memory_Swap')
    Memory = psutil.virtual_memory()
    Memory_Swap = psutil.swap_memory()

    # Disks
    log.debug(callback.message.chat.id, 'Generating information about: Disks')
    Disks = psutil.disk_usage('/')

    # Network
    log.debug(callback.message.chat.id, 'Generating information about: Network')
    all_interf = psutil.net_if_addrs()
    Network: str = '\n'

    for interf in all_interf:
        Network = f'{Network}- {interf}: {all_interf[interf][0][1]}\n'

    log.info(callback.message.chat.id, 'Generating a report based on the data received . . .')
    
    report = f'OS: {SystemName} {SystemRelease}\nPython: {PythonVersion}\n\nЗагруженость:\n\nCPU: {CPU}%\nMemory: {Memory.percent}%\nMemory Swap: {Memory_Swap.percent}%\nDisks: {Disks.percent}%\nNetwork: {Network}'
    
    log.info(callback.message.chat.id, 'Successfully !')

    await callback.message.edit_text(report, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[GenButtonBack('admin_panel')], [__BACK_IN_MAIN_MENU__]]))

    log.info(callback.message.chat.id, 'Report Sent !')
