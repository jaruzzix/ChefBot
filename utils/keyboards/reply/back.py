from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="Назад")


back_kb =builder.as_markup()
back_kb.resize_keyboard = True

__all__ = ["back_kb"]