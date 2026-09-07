from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="Добавить в избранное")
builder.button(text="Назад")


recipe_menu_kb =builder.as_markup()
recipe_menu_kb.resize_keyboard = True

__all__ = ["recipe_menu_kb"]