from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database as db
import app.states as st


router = Router()


@router.message(CommandStart())
async def cmdstart(message: Message, state: FSMContext):
    await message.answer("Привет!\nЯ бот для оценки настроения.\n"
                         "Нажми кнопку снизу чтобы отметить свое настроение.\n"
                         "Введи команду /help, если тебе необходима помощь в использовании бота.\n",
                         reply_markup=kb.main)
    await state.clear()


@router.message(Command('help'))
async def cmdhelp(message: Message):
    await message.answer((
        "🤖 <b>Помощь по боту</b>\n\n"
        "Я умею отслеживать твое настроение.\n"
        "• Нажми <i>Отметить настроение</i>, чтобы записать день.\n"
        "• Нажми <i>Посмотреть настроение</i>, чтобы увидеть последнюю запись.\n"
        "• Нажми <i>Среднее за 7 дней</i>, чтобы увидеть статистику."
    ), parse_mode="HTML")


@router.message(F.text == "Отметить мое настроение")
async def call_dreams(message: Message, state: FSMContext):
    if db.check_mood_today(message.from_user.id):
        await message.answer("Вы уже отмечали сегодня настроение.", reply_markup=kb.mood)
        await state.clear()
    else:
        await message.answer("Введите свой уровень настроения от 0 до 10.")
        await state.set_state(st.Set_Mood.waiting_number)


@router.message(st.Set_Mood.waiting_number, F.text)
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
        emoji = None
        
        user_id = message.from_user.id

        if number < 0 or number > 10:
            await message.answer("Число должно быть от 0 до 10.")
            return

        if number <= 3:
            emoji = '😢'

        elif number <= 7:
            emoji = '😐'

        elif number <= 10:
            emoji = '😊'

        db.save_mood(number, user_id)

        await message.answer(f"Твое настроение сохранено: {number}{emoji}", reply_markup=kb.mood)
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

        elif 2 <= count <= 4:
            day = f"{count} дня"

        elif 5 <= count <= 7:
            day = f"{count} дней"
        
        await callback.message.answer(f"Твое среднее настроение за {day} это: {average}.")
    await callback.answer()

