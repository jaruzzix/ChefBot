from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

buttons = ['Изменить настройки', "Новый подбор", "Закрыть"]


for text in buttons:
    builder.button(text=text)
builder.adjust(2, 1)

rl_menu_kb =builder.as_markup()
rl_menu_kb.resize_keyboard = True

__all__ = ["rl_menu_kb"]