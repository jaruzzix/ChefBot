from aiogram import Router, types
from loader import db
from utils.keyboards.reply.main_menu_kb import main_kb
from aiogram.filters import CommandStart


router = Router(name=__name__)

@router.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {full_name}, я ChefBot - твой путеводитель "
                         f"в мире кулинарии. Используй меню ниже для работы со мной.",
                         reply_markup=main_kb)

    if not db.get_user(user_id):
        db.add_user(user_id, username, full_name)
