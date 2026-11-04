from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from collections import defaultdict
from datetime import datetime

import app.keyboards as kb


moods: dict[int, list[tuple[datetime, int]]] = defaultdict(list)


router = Router()


class Set_Mood(StatesGroup):
    waiting_number = State()


@router.message(CommandStart())
async def cmdstart(message: Message, state: FSMContext):
    await message.answer("Привет!\nЯ бот для оценки настроения.\nНажми кнопку снизу чтобы отметить свое настроение.", reply_markup=kb.main)
    await state.clear()


@router.message(F.text == "Отметить мое настроение")
async def call_dreams(message: Message, state: FSMContext):
    await message.answer("Введите свой уровень настроения от 0 до 10.")
    await state.set_state(Set_Mood.waiting_number)


@router.message(Set_Mood.waiting_number, F.text)
async def check_number(message: Message, state: FSMContext):
    text = message.text.strip()

    if not text.isdigit():
        await message.answer("Настроение не должно быть текстом, а должно быть целым числом.")
        return

    number = int(text)

    if number < 0 or number > 10:
        await message.answer("Число должно быть от 0 до 10.")
        return

    moods[message.from_user.id].append((datetime.now(), number))

    await message.answer(f"Твое настроение сохранено: {number}", reply_markup=kb.mood)
    await state.clear()


@router.callback_query(F.data == 'check_mood')
async def check_mood(callback: CallbackQuery):
    items = moods.get(callback.from_user.id)
    if not items:
        await callback.answer('Вы еще не отмечали настроение.')
    else:
        await callback.message.answer(f'Ваше последнее настроение: {items[-1][1]}')
    await callback.answer()
    