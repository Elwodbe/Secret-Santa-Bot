from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(lang):
    kb = {
        'uz': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🕹Mening o'yinlarim")],
                [KeyboardButton(text="➕Xona yaratish"), KeyboardButton(text="📋Aktiv xonalarim")],
                [KeyboardButton(text="🌍Til sozlamalari")]
            ],
            resize_keyboard=True
        ),
        'ru': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🕹Мои игры")],
                [KeyboardButton(text="➕Создать комнату"), KeyboardButton(text="📋Активные комнаты")],
                [KeyboardButton(text="🌍Настройки языка")]
            ],
            resize_keyboard=True
        ),
        'en': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🕹My Games")],
                [KeyboardButton(text="➕Create Room"), KeyboardButton(text="📋Active Rooms")],
                [KeyboardButton(text="🌍Language Settings")]
            ],
            resize_keyboard=True
        )
    }

    return kb.get(lang, kb['uz']) 