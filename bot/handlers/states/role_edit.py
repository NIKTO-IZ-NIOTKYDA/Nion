from aiogram.filters.state import State, StatesGroup


class FormRoleEdit(StatesGroup):
    input_name = State()
    edit_users = State()
    input_user_id_or_username = State()
