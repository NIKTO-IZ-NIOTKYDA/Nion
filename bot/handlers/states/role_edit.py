from aiogram.filters.state import State, StatesGroup

class FormRoleEdit(StatesGroup):
    input_name = State()
