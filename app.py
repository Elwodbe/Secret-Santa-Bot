from loader import dp,bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import asyncio
from handlers.users.start import router
from handlers.users.help import router as help_router
from utils.db_api.create import create_table

async def main():
    await set_default_commands(bot)
    await on_startup_notify(bot)
    
    dp.include_router(router)
    dp.include_router(help_router)
    create_table()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())