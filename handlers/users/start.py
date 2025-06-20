from aiogram import types, Router
from aiogram.filters import Command
from utils.db_api.user_query import check_user, add_user, get_user_language
from utils.db_api.room_queries import get_room_info,add_user_room,is_user_in_room
from keyboards.inline.language import language_button
from keyboards.default.default import main_menu
from aiogram.fsm.context import FSMContext
from states.states import RoomJoiningState

router = Router()

@router.message(Command(commands=["start"]))
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    args = message.text.split(" ")[1] if len(message.text.split()) > 1 else None

    if not args:
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
    else:
        lang = get_user_language(user_id) or "uz"
        username = message.from_user.username
        fullname = message.from_user.full_name
        add_user(user_id=user_id, username=username, fullname=fullname, language=lang)
        if is_user_in_room(room_id=args, user_id=user_id):
            msg_info = {
                'uz': "⚠️ <b>Siz allaqachon ushbu xonaga qo‘shilgansiz!</b>\n"
                    "⏳ <i>Iltimos, o‘yin boshlanishini kuting.</i>",

                'ru': "⚠️ <b>Вы уже присоединились к этой комнате!</b>\n"
                    "⏳ <i>Пожалуйста, дождитесь начала игры.</i>",

                'en': "⚠️ <b>You have already joined this room!</b>\n"
                    "⏳ <i>Please wait for the game to start.</i>"
            }
            await message.answer(text=msg_info.get(lang, msg_info["uz"]))
            return



        result = get_room_info(args)
        room_name = result['room_name']
        creator_username = result['creator_username']
        creator_fullname = result['creator_fullname']

        msg = {
            'uz': (
                f"<b>📌 Xona IDsi:</b> <code>{args}</code>\n"
                f"<b>🏷 Xona nomi:</b> <u>{room_name}</u>\n"
                f"<b>👤 Xona admini:</b> <i>{creator_fullname}</i>\n"
                f"<b>🔗 Admin username:</b> @{creator_username}\n\n"
                f"✍️ <b>Iltimos, yuqoridagi xonaga qo‘shilish uchun so‘ralgan ma’lumotlarni to‘ldiring.</b>"
            ),
            'ru': (
                f"<b>📌 ID комнаты:</b> <code>{args}</code>\n"
                f"<b>🏷 Название комнаты:</b> <u>{room_name}</u>\n"
                f"<b>👤 Админ комнаты:</b> <i>{creator_fullname}</i>\n"
                f"<b>🔗 Username админа:</b> @{creator_username}\n\n"
                f"✍️ <b>Пожалуйста, заполните необходимые данные для присоединения к этой комнате.</b>"
            ),
            'en': (
                f"<b>📌 Room ID:</b> <code>{args}</code>\n"
                f"<b>🏷 Room Name:</b> <u>{room_name}</u>\n"
                f"<b>👤 Room Creator:</b> <i>{creator_fullname}</i>\n"
                f"<b>🔗 Creator Username:</b> @{creator_username}\n\n"
                f"✍️ <b>Please fill in the required information to join the room above.</b>"
            )
        }

        msg2 = {
            'uz': (
                "<b>📝 Iltimos, ism va familiyangizni kiriting.</b>\n\n"
                "🎁 <i>Sovg'a yuboruvchi sizni tanib olishi uchun to'liq ism-familiyangizni kiriting!</i>"
            ),
            'ru': (
                "<b>📝 Пожалуйста, введите ваше имя и фамилию.</b>\n\n"
                "🎁 <i>Чтобы человек, который хочет подарить вам подарок, мог вас узнать — введите полное имя!</i>"
            ),
            'en': (
                "<b>📝 Please enter your full name.</b>\n\n"
                "🎁 <i>To help the person giving you a gift recognize you, please enter your full name clearly!</i>"
            )
        }

        await message.reply(text=msg.get(lang, msg["uz"]))
        await message.answer(text=msg2.get(lang, msg2["uz"]))
        await state.update_data(room_id=args)
        await state.set_state(RoomJoiningState.fullname)


@router.message(RoomJoiningState.fullname)
async def get_fullname_tojoin_room(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    msg = {
        'uz': "👇 <b>Quyidagilardan birini tanlang:</b>",
        'ru': "👇 <b>Выберите один из вариантов:</b>",
        'en': "👇 <b>Choose an option:</b>"
    }
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="👨 Erkak", callback_data="room_joining_kb_male"),
                types.InlineKeyboardButton(text="👩 Ayol", callback_data="room_joining_kb_female")
            ]
        ]
    )
    lang = get_user_language(message.from_user.id)
    await message.answer(msg.get(lang, msg['uz']), reply_markup=kb)
    await state.set_state(RoomJoiningState.gender)


@router.callback_query(lambda call: call.data.startswith("room_joining_kb"), RoomJoiningState.gender)
async def get_gender_tojoin_room(callback: types.CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=f"<b>{callback.message.text}</b>")
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    gender = callback.data.split('_')[3]
    await state.update_data(gender = gender)
    msg = {
        'uz': "📝 <b>O'zingiz haqingizda qisqacha yozing:</b>\n"
            "<i>Masalan:</i> 🎯 qiziqishlaringiz, 🎨 hobbylaringiz, 🍫 nimalarni yoqtirishingiz.\n"
            "🎁 Sizga sovg'a olmoqchi bo‘lgan odamga bu ma'lumot yordam beradi!",
        
        'ru': "📝 <b>Напишите немного о себе:</b>\n"
            "<i>Например:</i> 🎯 ваши интересы, 🎨 хобби, 🍫 что вам нравится.\n"
            "🎁 Это поможет человеку выбрать для вас подходящий подарок!",

        'en': "📝 <b>Write a bit about yourself:</b>\n"
            "<i>For example:</i> 🎯 your interests, 🎨 hobbies, 🍫 things you like.\n"
            "🎁 This will help your Secret Santa choose the right gift for you!"
    }

    await callback.message.answer(msg.get(lang, msg["uz"]))
    await state.set_state(RoomJoiningState.about_user)

@router.message(RoomJoiningState.about_user)
async def get_aboutuser_tojoin_room(message: types.Message, state: FSMContext):
    result = await state.get_data()
    lang = get_user_language(message.from_user.id)

    add_user_room(
        room_id=result["room_id"],
        user_id=message.from_user.id,
        gender=result['gender'],
        fullname=result['fullname'],
        username=message.from_user.username,
        about_user= message.text
    )

    msg = {
        'uz': "✅ <b>Siz muvaffaqiyatli xonaga qo‘shildingiz!</b>\n"
            "🎮 O‘yin boshlanganda, bot sizga avtomatik xabar yuboradi!",

        'ru': "✅ <b>Вы успешно присоединились к комнате!</b>\n"
            "🎮 Когда игра начнётся, бот автоматически отправит вам сообщение.",

        'en': "✅ <b>You have successfully joined the room!</b>\n"
            "🎮 When the game starts, the bot will automatically notify you."
    }
    await message.answer(msg.get(lang, msg["uz"]))
    await state.clear()





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