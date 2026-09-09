from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from typing import List

def items_list_ikb(items: List[str], page_max_length: int | None = None, page: int = 0):
    builder = InlineKeyboardBuilder()
    ingredient_id = 0
    max_page = 0

    if len(items) == 0:
        return None

    if not page_max_length:
        items_lst = items
    else:
        max_page = -(-len(items) // page_max_length) - 1
        start_index = page * max_page
        end_index = start_index + page_max_length
        items_lst = items[start_index: end_index]

    for item in items_lst:
        builder.row(InlineKeyboardButton(text=item, callback_data=str(ingredient_id)))
        ingredient_id += 1

    if page_max_length:
        if page == 0 and page < max_page:
            builder.row(InlineKeyboardButton(text="След. страница", callback_data=f"page_{page + 1}"))
        elif page == max_page and max_page != 0:
            builder.row(InlineKeyboardButton(text="Пред. страница", callback_data=f"page_{page - 1}"))
        else:
            builder.row(
                InlineKeyboardButton(text="Пред. страница", callback_data=f"page_{page - 1}"),
                InlineKeyboardButton(text="След. страница", callback_data=f"page_{page + 1}")
            )


    return builder.as_markup()

def get_page(callback: str):
    page = int(callback.split("_")[1])
    return page

__all__ = ["items_list_ikb", "get_page"]