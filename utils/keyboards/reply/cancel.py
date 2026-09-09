from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="Отмена")


cancel_kb =builder.as_markup()
cancel_kb.resize_keyboard = True

__all__ = ["cancel_kb"]