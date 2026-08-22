from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

buttons = ["Подобрать рецепты", "Исключения", "Удалить ингредиент", "Удалить все ингредиенты", "Отмена"]

for text in buttons:
    builder.button(text=text)
builder.adjust(2)

cr_menu_kb =builder.as_markup()
cr_menu_kb.resize_keyboard = True

__all__ = ["cr_menu_kb"]