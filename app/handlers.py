from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb
import app.database as db


router = Router()


class Set_Mood(StatesGroup):
    waiting_number = State()


@router.message(CommandStart())
async def cmdstart(message: Message, state: FSMContext):
    await message.answer("Привет!\nЯ бот для оценки настроения.\nНажми кнопку снизу чтобы отметить свое настроение.", reply_markup=kb.main)
    await state.clear()


@router.message(F.text == "Отметить мое настроение")
async def call_dreams(message: Message, state: FSMContext):
    if db.check_mood_today(message.from_user.id):
        await message.answer("Вы уже отмечали сегодня настроение.", reply_markup=kb.mood)
        await state.clear()
    else:
        await message.answer("Введите свой уровень настроения от 0 до 10.")
        await state.set_state(Set_Mood.waiting_number)


@router.message(Set_Mood.waiting_number, F.text)
async def check_number(message: Message, state: FSMContext):
    text = message.text.strip()
    if db.check_mood_today(message.from_user.id):
        await message.answer("Вы уже отмечали сегодня настроение.", reply_markup=kb.mood)
        await state.clear()
    else:
        if not text.isdigit():
            await message.answer("Настроение не должно быть текстом, а должно быть целым числом.")
            return

        number = int(text)
        user_id = message.from_user.id

        if number < 0 or number > 10:
            await message.answer("Число должно быть от 0 до 10.")
            return

        db.save_mood(number, user_id)

        await message.answer(f"Твое настроение сохранено: {number}", reply_markup=kb.mood)
        await state.clear()


@router.callback_query(F.data == 'check_mood')
async def check_mood(callback: CallbackQuery):
    last_mood = db.get_last_mood(callback.from_user.id)
    if not last_mood:
        await callback.message.answer("Вы еще не отмечали своё настроение.")
    else:
        score, date = last_mood
        await callback.message.answer(f"Твое последнее настроение это: {score} за {date}.")
    await callback.answer()

@router.callback_query(F.data == 'check_average')
async def check_average_mood(callback: CallbackQuery):
    average_mood = db.get_average_mood(callback.from_user.id)
    if not average_mood:
        await callback.message.answer("У вас нет данных.")
    else:
        numbers = [row[0] for row in average_mood]
        average = round((sum(numbers) / len(numbers)),1)
        count = len(numbers)

        if count == 1:
            day = f"{count} день"

        elif 2 <= len(numbers) <= 4:
            day = f"{count} дня"

        elif 5 <= len(numbers) <= 7:
            day = f"{count} дней"
        
        await callback.message.answer(f"Твое среднее настроение за {day} это: {average}.")
    await callback.answer()

