from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                    InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отметить мое настроение')]],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите...")

mood = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Посмотреть свое настроение', callback_data='check_mood')]])
