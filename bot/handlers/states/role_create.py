from aiogram.filters.state import State, StatesGroup

class FormRoleCreate(StatesGroup):
    input_id = State()
    input_name = State()
