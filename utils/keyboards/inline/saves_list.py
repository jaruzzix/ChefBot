from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from typing import Dict, Any


def saves_list_ikb(items: Dict[str, Any], page_max_length: int | None = None, page: int = 0):
    builder = InlineKeyboardBuilder()
    max_page = 0

    if len(items) == 0:
        return None

    keys = list(items.keys())

    if not page_max_length:
        items_keys = keys
    else:
        max_page = -(-len(keys) // page_max_length) - 1
        if page > max_page:
            page = max_page

        start_index = page * max_page
        end_index = start_index + page_max_length
        items_keys = keys[start_index: end_index]

    for key in items_keys:
        builder.row(InlineKeyboardButton(text=items[key]["title"], callback_data=key))

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


__all__ = ["saves_list_ikb"]