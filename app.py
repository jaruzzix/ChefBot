import asyncio
import logging
import sys

from loader import *
from handlers import *


async def main():
    dp.include_routers(start_bot, compilation_recipes)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())