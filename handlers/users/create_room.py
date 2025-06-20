from aiogram import types, Router
from states.states import CreateRoomState
from aiogram.fsm.context import FSMContext
from utils.db_api.user_query import get_user_language
from utils.db_api.room_queries import create_room

router = Router()

@router.message(lambda message:message.text in ['➕Xona yaratish','➕Создать комнату','➕Create Room'])
async def create_room_start(message:types.Message, state:FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    msg = {
        'uz': "Xona nomini kiriting.",
        'ru': "Введите название комнаты.",
        'en': "Enter the room name."
    }
    await message.reply(text=msg.get(lang, msg['uz']))
    await state.set_state(CreateRoomState.room_name)


@router.message(CreateRoomState.room_name)
async def create_room_db(message:types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    room_name = message.text
    room_info = create_room(room_name=room_name, user_id=user_id)
    room_id, invitation_link = room_info[0], room_info[3]

    

    msg = {
        'uz': (
            "🎉 <b>Xona yaratildi!</b>\n"
            f"<b>ID:</b> <code>{room_id}</code>\n"
            f"<b>Xona nomi:</b> <i>{room_name}</i>\n\n"
            f"🔗 <a href='{invitation_link}'>Do‘stlarni taklif qilish havolasi</a>\n\n"
            "⤴️ Yuqoridagi havolani do‘stlaringizga ulashing yoki quyidagi tugmani bosib ulashing. "
            "Ularni xonaga qo‘shiling!"
        ),
        'ru': (
            "🎉 <b>Комната успешно создана!</b>\n"
            f"<b>ID:</b> <code>{room_id}</code>\n"
            f"<b>Название комнаты:</b> <i>{room_name}</i>\n\n"
            f"🔗 <a href='{invitation_link}'>Ссылка для приглашения друзей</a>\n\n"
            "⤴️ Поделитесь ссылкой с друзьями или нажмите кнопку ниже, чтобы пригласить их в комнату."
        ),
        'en': (
            "🎉 <b>Room created successfully!</b>\n"
            f"<b>ID:</b> <code>{room_id}</code>\n"
            f"<b>Room Name:</b> <i>{room_name}</i>\n\n"
            f"🔗 <a href='{invitation_link}'>Invitation link to share with friends</a>\n\n"
            "⤴️ Share the link above with your friends or click the button below to invite them to the room."
        )
    }

    text_inline = {
         'uz': "🤝 Do‘stlar bilan ulashing",
         'ru': "🤝 Поделиться с друзьями",
         'en': "🤝 Share with friends"   
    }
    await state.clear()

    text_switch_inline = {
        'uz': f"📎 {room_name} xonasiga qo‘shiling: {invitation_link} 🎁 Secret Friend o‘yinida ishtirok eting!",
        'ru': f"📎 Присоединяйтесь к комнате {room_name}: {invitation_link} 🎁 Играйте в Secret Friend!",
        'en': f"📎 Join the room {room_name}: {invitation_link} 🎁 Play Secret Friend!"
    }


    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=text_inline.get(lang, text_inline['uz']), switch_inline_query=text_switch_inline.get(lang, text_switch_inline['uz']))]
        ]
    )
    await message.answer(text=msg.get(lang, msg['uz']),reply_markup=kb)