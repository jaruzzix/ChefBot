from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="Закрыть")


close_kb =builder.as_markup()
close_kb.resize_keyboard = True

__all__ = ["close_kb"]