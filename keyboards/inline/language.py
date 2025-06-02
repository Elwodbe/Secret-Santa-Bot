from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_button():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data='lang_uz'),
                InlineKeyboardButton(text="🇷🇺 Ruscha", callback_data='lang_ru'),
                InlineKeyboardButton(text="🇺🇸 English", callback_data='lang_en')
            ]
        ]
    )
    return btn
