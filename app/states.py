from aiogram.fsm.state import StatesGroup, State

class Set_Mood(StatesGroup):
    waiting_number = State()