from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

from config import HELP_TEXT

import app.keyboards as kb
import app.database as db
import app.states as st



router = Router()


@router.message(CommandStart())
async def cmdstart(message: Message, state: FSMContext):
    user_info = db.get_name(message.from_user.id)

    if not user_info:
        await message.answer("Привет!\n"
                                "Я бот для оценки настроения.\n"
                                "Нажми кнопку снизу чтобы начать регистрацию.\n"
                                "Введи команду /help, если тебе необходима помощь в использовании бота.\n",
                                reply_markup=kb.register)
    else:
        name, date = user_info
        await message.answer(f"Привет {name}!\nНажимай кнопку снизу и отмечай свое настроение.", reply_markup=kb.main)
    
    await state.clear()


@router.message(Command('help'))
async def cmdhelp(message: Message):

    await message.answer(HELP_TEXT, parse_mode="HTML")


@router.message(F.text == "🆘Помощь")
async def call_help(message: Message, state: FSMContext):

    await message.answer(HELP_TEXT, parse_mode="HTML")

    await state.clear()


@router.message(F.text == "Начать регистрацию")
async def call_register(message: Message, state: FSMContext):
    user_info = db.get_name(message.from_user.id)

    if user_info:
        name, date = user_info
        await message.answer(f"Вы уже зарегистрированы как: {name}.", reply_markup=kb.main)
        
    else:
        await message.answer("Как могу тебя называть?")
        await state.set_state(st.Register.waiting_name)


@router.message(st.Register.waiting_name)
async def check_name(message: Message, state: FSMContext):
    
    text = message.text.strip()
    await message.answer(f"Твое имя сохранено как: {text}.\nТеперь ты можешь отмечать своё настроение!", reply_markup=kb.main)
    db.register(text, message.from_user.id)

    await state.clear()

    
@router.message(F.text == "✨Отметить мое настроение")
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
        user_info = db.get_name(message.from_user.id)

        if user_info:
            name, date = user_info
            await message.answer(f"{name} твое настроение сохранено: {number} {emoji}", reply_markup=kb.mood)
        else:
            await message.answer(
                f"Твое настроение сохранено: {number} {emoji}.\n\n"
                f"Кстати, ты еще не зарегистрировался! Нажми кнопку снизу, чтобы бот знал твое имя.", 
                reply_markup=kb.register
            )
        await state.clear()


@router.callback_query(F.data == 'check_mood')
async def check_mood(callback: CallbackQuery):

    last_mood = db.get_last_mood(callback.from_user.id)
    user_info = db.get_name(callback.from_user.id)

    if not last_mood or not user_info:
        await callback.message.answer("Вы еще не отмечали своё настроение.😔")

    else:
        name, reg_date = user_info
        score, date = last_mood
        
        
        await callback.message.answer(f"{name} твое последнее настроение это: {score} за {date}.")

    await callback.answer()


@router.callback_query(F.data == 'check_average')
async def check_average_mood(callback: CallbackQuery):
    
    average_mood = db.get_average_mood(callback.from_user.id)
    user_info = db.get_name(callback.from_user.id)
    if not average_mood or not user_info:
        await callback.message.answer("У вас нет данных.")
    else:
        numbers = [row[0] for row in average_mood]
        average = round((sum(numbers) / len(numbers)),1)
        name, date = user_info
        count = len(numbers)

        if count == 1:
            day = f"{count} день"

        elif 2 <= count <= 4:
            day = f"{count} дня"

        elif 5 <= count <= 7:
            day = f"{count} дней"
        
        await callback.message.answer(f"{name} твое среднее настроение за {day} это: {average}.")
    await callback.answer()


@router.callback_query(F.data == 'check_stats')
async def check_stats(callback: CallbackQuery):

    user_info = db.get_name(callback.from_user.id)
    stats = db.get_all_stats(callback.from_user.id)

    if not stats or not user_info:
        await callback.message.answer("У вас недостаточно данных.")
    else:
        numbers = [row[0] for row in stats]
        average = round((sum(numbers) / len(numbers)), 1)
        name, date = user_info

        if average <= 3:
            emoji = '😞'
        elif average <= 5:
            emoji = '😐'
        elif average <= 7:
            emoji = '🙂'
        elif average <= 10:
            emoji = '🤩'

        await callback.message.answer(f"Ты зарегестрировался {date}.\nТы представился как: {name}.\nТвое общее настроение настроение: {average}{emoji}.")

    await callback.answer()