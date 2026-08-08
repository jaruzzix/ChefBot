from aiogram import Bot, Dispatcher
from data.config import bot_token as token, proxy_server as proxy
from aiogram.client.session.aiohttp import AiohttpSession


session = AiohttpSession(proxy=proxy)

bot = Bot(token=token, session=session)
dp = Dispatcher()

__all__ = ["bot", "dp"]