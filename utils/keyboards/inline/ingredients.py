from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import List

def ingredients_ikb(ingredients: List[str]):
    builder = InlineKeyboardBuilder()
    ingredient_id = 0
    for ingredient in ingredients:
        builder.button(text=ingredient, callback_data=str(ingredient_id))
        ingredient_id += 1

    builder.adjust(1)
    return builder.as_markup()

__all__ = ["ingredients_ikb"]