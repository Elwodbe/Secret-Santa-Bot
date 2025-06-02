import logging
from aiogram import Bot
from data.config import ADMINS
from aiogram.exceptions import TelegramBadRequest

async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            admin = int(admin)
            await bot.send_message(admin, "Bot ishga tushdi")
        except TelegramBadRequest as e:
            print(f"[ERROR] Could not send message to {admin}: {e}")