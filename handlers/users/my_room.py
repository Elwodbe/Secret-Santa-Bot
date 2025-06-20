from aiogram import types, Router
from utils.db_api.user_query import get_user_language
from utils.db_api.room_queries import get_user_rooms_with_details

router = Router()

@router.message(lambda message: message.text in ["🕹Mening o'yinlarim","🕹Мои игры","🕹My Games"])
async def my_game_function(message:types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    detailed_info = get_user_rooms_with_details(user_id)

    if detailed_info ==[]:
            msg1 = {
                'uz': "🎮 Sizda hozircha aktiv o'yinlar mavjud emas!\n➕ Yangi o'yin yaratish uchun menyudan foydalaning.",
                'ru': "🎮 У вас пока нет активных игр!\n➕ Используйте меню, чтобы создать новую игру.",
                'en': "🎮 You don't have any active games yet!\n➕ Use the menu to create a new game."
            }
            
            await message.answer(text=msg1.get(lang, msg1["uz"]))
            return

    for room_info in detailed_info:
        room_id = room_info["room_id"]
        is_game_started = room_info["is_game_started"]
        roomname = room_info["roomname"]
        gender = room_info["gender"]
        fullname = room_info["fullname"] 
        about_user = room_info["about_user"]
        msg2 = {
                'uz': (
                    f"🏠 <b>Xona nomi:</b> <i>{roomname}</i>\n"
                    f"🚻 <b>Jinsi:</b> <i>{gender}</i>\n"
                    f"🧑‍💼 <b>Ismingiz:</b> <i>{fullname}</i>\n"
                    f"ℹ️ <b>Ma'lumot:</b> <i>{about_user}</i>\n"
                ),
                'ru': (
                    f"🏠 <b>Название комнаты:</b> <i>{roomname}</i>\n"
                    f"🚻 <b>Пол:</b> <i>{gender}</i>\n"
                    f"🧑‍💼 <b>Ваше имя:</b> <i>{fullname}</i>\n"
                    f"ℹ️ <b>Информация:</b> <i>{about_user}</i>\n"
                ),
                'en': (
                    f"🏠 <b>Room name:</b> <i>{roomname}</i>\n"
                    f"🚻 <b>Gender:</b> <i>{gender}</i>\n"
                    f"🧑‍💼 <b>Your name:</b> <i>{fullname}</i>\n"
                    f"ℹ️ <b>Info:</b> <i>{about_user}</i>\n"

                )
            }
        if is_game_started:
            await message.answer(text=msg2.get(lang))
        else:
            kb_text = {
                'uz': "🚪 O'yindan chiqish",
                'ru': "🚪 Выйти из игры",
                'en': "🚪 Leave the game"
            }
            kb = types.InlineKeyboardMarkup(
                 inline_keyboard=[
                      [types.InlineKeyboardButton(text=kb_text.get(lang, kb_text["uz"]), callback_data=f"remove_game_{user_id}_{room_id}")]
                 ]
            )
            await message.answer(text=msg2.get(lang, msg2["uz"]), reply_markup=kb)      
             
