from aiogram.fsm.state import StatesGroup, State

class Set_Mood(StatesGroup):
    waiting_number = State()

class Register(StatesGroup):
    waiting_name = State()