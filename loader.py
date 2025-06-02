from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from data import config
import logging

# logging.basicConfig(level=logging.WARNING)  
# logging.getLogger("aiogram.dispatcher.dispatcher").setLevel(logging.WARNING)  


bot = Bot(
    token=config.BOT_TOKEN,  
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)