from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from data.config import bot_token as token, proxy_server as proxy
from aiogram.client.session.aiohttp import AiohttpSession
from data.db.chef_bot_db import PoolConnection

session = AiohttpSession(proxy=proxy)

bot = Bot(token=token, session=session)
dp = Dispatcher(storage=MemoryStorage())
db = PoolConnection()

__all__ = ["bot", "dp", "db"]