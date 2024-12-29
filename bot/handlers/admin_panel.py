from re import fullmatch
from platform import system, python_version, release

import psutil
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

import utils
import requests.roles as rq_roles
from handlers.core import log, GetRouter
from handlers.states.newsletter import FormNewsletter
from handlers.states.role_create import FormRoleCreate
from other.PermissionsManager.PermissionsManager import PM
from keyboards.other import GenButtonBack, __BACK_IN_MAIN_MENU__
from keyboards.admins import GenAdminPanel, __NEWSLETTER_WARN__, GenRoleMenu, GenRoleOpen


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


@router.callback_query(F.data == 'admin_panel:role')
async def admin_panel_role(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not (await utils.GetPermissions(callback.message.chat.id)).admin_panel.use.role: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return
    
    await state.clear()
    
    await callback.message.edit_text('👇 Выберите роль', reply_markup=(await GenRoleMenu(callback.message.chat.id)))


@router.callback_query(F.data.startswith('admin_panel:role:open:'))
async def admin_panel_role_open(callback: CallbackQuery):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not (await utils.GetPermissions(callback.message.chat.id)).admin_panel.use.role: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return
    
    role_id: int = int(callback.data.replace('admin_panel:role:open:', ''))
    role = await rq_roles.GetRole(callback.message.chat.id, role_id, 60)
    users = '' if role['users'] != [] else '❌'

    for user in role['users']:
        users += f'\'{user['first_name']}\'' + ' [ @' + str(user['username'])+(' ], ' if user['user_id'] != role['users'][-1]['user_id'] else ' ]')


    def print_permissions(permissions: dict):
        msg = ''
        
        for key, value in permissions.items():
            if isinstance(value, dict):
                if 'description' in value and 'value' in value:
                    msg += f'- {value['description']}: {'✅' if value['value'] else '❌'}\n'
                else:
                    msg += print_permissions(value)

        return msg


    await callback.message.edit_text(f'''ID роли: <code>{role['role_id']}</code>
Название роли: {role['name']}
Пользователи с этой ролью: {users}
Разрешения:\n{print_permissions(role['permissions'])}''', reply_markup=(await GenRoleOpen(role_id)))


@router.callback_query(F.data == 'admin_panel:role:create')
async def admin_panel_role_create(callback: CallbackQuery, state: FSMContext):
    log.info(str(callback.message.chat.id), f'Received \'[{callback.data}]\'')

    if not (await utils.GetPermissions(callback.message.chat.id)).admin_panel.use.role: 
        try: await utils.RQReporter(c=callback)
        except utils.AccessDeniedError: return
    
    await callback.message.edit_text(f'➡️ Введите ID роли которую хотите создать. ID - это уникальный индикатор роли. Занятые ID: {[role['role_id'] for role in (await rq_roles.GetRoles(callback.message.chat.id))]}',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [GenButtonBack('admin_panel:role')],
                [__BACK_IN_MAIN_MENU__]
            ]
        ))

    await state.set_state(FormRoleCreate.input_id)


@router.message(F.text, FormRoleCreate.input_id)
async def admin_panel_role_create_input_id(message: Message, state: FSMContext):
    log.info(str(message.chat.id), f'Received \'{message.text}\'')

    if not (await utils.GetPermissions(message.chat.id)).admin_panel.use.role: 
        try: await utils.RQReporter(m=message)
        except utils.AccessDeniedError: return

    if not fullmatch('^\\d+$', str(message.text)) or len(message.text) > 5:
        await message.answer('‼️ Некорректные входные данные!\n\n➡️ Введите ID')

        await state.set_state(FormRoleCreate.input_id)
        
        return

    await state.set_data({
        'role_id': int(message.text)
    })

    await message.answer('✅ ID роли успешно сохранено!\n\n➡️ Введите название роли которую хотите создать. В названии можно использовать HTML тэги!',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [GenButtonBack('admin_panel:role')],
                [__BACK_IN_MAIN_MENU__]
            ]))

    await state.set_state(FormRoleCreate.input_name)


@router.message(F.text, FormRoleCreate.input_name)
async def admin_panel_role_create_input_name(message: Message, state: FSMContext):
    log.info(str(message.chat.id), f'Received \'{message.text}\'')

    if not (await utils.GetPermissions(message.chat.id)).admin_panel.use.role: 
        try: await utils.RQReporter(m=message)
        except utils.AccessDeniedError: return

    if len(message.text) > 255:
        message.answer('‼️ Некорректные входные данные!\n\n➡️ Введите название')

        state.set_state(FormRoleCreate.input_name)
        
        return

    await rq_roles.SetRole(
        message.chat.id,
        int((await state.get_data())['role_id']),
        [],
        str(message.text),
        PM.DefaultPermissions
    )

    await message.answer('✅ Роль успешно создана!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'Перейти к роли [{(await state.get_data())['role_id']}] ➡️',
                                  callback_data=f'admin_panel:role:open:{(await state.get_data())['role_id']}')],
            [GenButtonBack('admin_panel:role')],
            [__BACK_IN_MAIN_MENU__]
        ]))

    await state.clear()
