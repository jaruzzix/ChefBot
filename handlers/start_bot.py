from aiogram import Router, types
from aiogram.filters import CommandStart


router = Router(name=__name__)

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.username}")