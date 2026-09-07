from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from data.config import bot_token as token
from aiogram.client.session.aiohttp import AiohttpSession
from data.db.chef_bot_db import PoolConnection
from aiogram.enums import ParseMode



session = AiohttpSession()

bot = Bot(token=token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
db = PoolConnection()

__all__ = ["bot", "dp", "db"]