from aiogram.types import Update

from contextlib import asynccontextmanager
import aiohttp

from data.config import webhook_url
from loader import *
from handlers import *

from fastapi import FastAPI, Request, Response
import json

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp.include_routers(start_bot, compilation_recipes)

is_Initialised = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global is_Initialised
    is_Initialised = False
    logger.info("Запуск инициализации бота ...")

    try:
        webhook_info = await bot.get_webhook_info()
        current_webhook_url = webhook_info.url
        updates_count = webhook_info.pending_update_count
        logger.info("Проверка вебхука ...")
        if current_webhook_url != webhook_url:
            logger.info("Установка вебхука ...")
            await bot.set_webhook(webhook_url, drop_pending_updates=True)
        elif updates_count > 0:
            logger.info("Обновление вебхука ...")
            await bot.delete_webhook()
            await bot.set_webhook(webhook_url, drop_pending_updates=True)
        else:
            logger.info("Обновления не требуются")

        # Создание сессии
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        app.state.http_session = aiohttp.ClientSession(connector=connector)

        dp.workflow_data["session"] = app.state.http_session
        logger.info("Создана новая сессия")
        yield
        # Закрытие сессии
        await app.state.http_session.close()
        logger.info("Сессия закрыта")


        is_Initialised = True
        logger.info("бот запущен")
    except Exception as err_:
        logger.error(f"Ошибка инициализации: {err_}")


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Читаем JSON из запроса
        body = await request.body()
        data = json.loads(body)

        # Создаем объект Update
        update = Update(**data)

        # Передаем в диспетчер
        await dp.feed_update(bot, update)

        return {"status": "ok"}
    except Exception as e:
        logger.info(f"Error: {e}")
        return Response(status_code=200, content="OK")


@app.get("/")
async def root_request():
    data = {}
    if is_Initialised:
        data['bot_status'] = 'alive'
    else:
        data['bot_status'] = 'not initialized'
    data['message'] = 'Server is running'
    return data
