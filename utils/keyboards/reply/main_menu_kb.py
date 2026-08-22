from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

buttons = ["Подобрать рецепты", "Избранное"]

for text in buttons:
    builder.button(text=text)
builder.adjust(2)

main_kb =builder.as_markup()
main_kb.resize_keyboard = True

__all__ = ["main_kb"]
