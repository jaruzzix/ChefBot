from aiogram import Router, types
from utils.keyboards.reply.main_menu_kb import main_kb
from aiogram.filters import CommandStart, StateFilter

from data.db.chef_bot_db import PoolConnection

router = Router()
router.message.filter(StateFilter(None))


@router.message(CommandStart())
async def start(message: types.Message, pool: PoolConnection):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {full_name}, я ChefBot - твой путеводитель "
                         f"в мире кулинарии. Используй меню ниже для работы со мной.",
                         reply_markup=main_kb)

    if not await pool.get_user(user_id):
        await pool.add_user(user_id, username, full_name)
