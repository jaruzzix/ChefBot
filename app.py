from aiogram.types import Update

from data.config import webhook_url
from loader import *
from handlers import *

from fastapi import FastAPI, Request, Response
import json

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
dp.include_routers(start_bot, compilation_recipes)

is_Initialised = False

@app.on_event('startup')
async def on_startup():
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

        is_Initialised = True
        logger.info("бот запущен")
    except Exception as err_:
        logger.error(f"Ошибка инициализации: {err_}")


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
