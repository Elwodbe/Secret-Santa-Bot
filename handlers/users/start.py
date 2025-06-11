from aiogram import types, Router
from aiogram.filters import Command
from utils.db_api.user_query import check_user, add_user, get_user_language
from keyboards.inline.language import language_button
from keyboards.default.default import main_menu

router = Router()

@router.message(Command(commands=["start"]))
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if check_user(user_id=user_id):
        lang = get_user_language(user_id)
        msg = {
            "uz": "Bosh menyu",
            "ru": "Главное меню",
            "en": "Main Menu"
        }
        await message.answer(text=msg.get(lang, msg["uz"]), reply_markup=main_menu(lang))
    else:
        await message.answer(
            "<b>Tilni tanlang\nВыберите язык\nChoose language</b>",
            reply_markup=language_button()
        )

@router.message(lambda message: message.text in ["🌍Til sozlamalari", "🌍Настройки языка", "🌍Language Settings"])
async def language_settings(message: types.Message):
    await message.answer(
        "<b>Tilni tanlang\nВыберите язык\nChoose language</b>",
        reply_markup=language_button()
    )

@router.callback_query(lambda call: call.data.startswith("lang_"))
async def add_user_to_database(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    username = callback.from_user.username
    fullname = callback.from_user.full_name
    user_id = callback.from_user.id

   
    add_user(user_id=user_id, username=username, fullname=fullname, language=lang)

   
    welcome_msg = {
        'uz': f"<b>Assalomu aleykum {fullname}.</b>\n\n<i>Botimizga xush kelibsiz!</i>",
        'ru': f"<b>Здравствуйте, {fullname}.</b>\n\n<i>Добро пожаловать в нашего бота!</i>",
        'en': f"<b>Hello, {fullname}.</b>\n\n<i>Welcome to our bot!</i>"
    }

    
    menu_msg = {
        "uz": "Bosh menyu",
        "ru": "Главное меню",
        "en": "Main Menu"
    }

    await callback.message.delete()
    await callback.message.answer(text=welcome_msg.get(lang, welcome_msg['uz']), parse_mode="HTML")
    await callback.message.answer(text=menu_msg.get(lang, menu_msg["uz"]), reply_markup=main_menu(lang))
