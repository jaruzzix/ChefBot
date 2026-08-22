from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

buttons = ["Подобрать рецепты", "Ингредиенты", "Удалить исключение", "Удалить все исключения", "Отмена"]

for text in buttons:
    builder.button(text=text)
builder.adjust(2)

exceptions_menu_kb =builder.as_markup()
exceptions_menu_kb.resize_keyboard = True

__all__ = ["exceptions_menu_kb"]