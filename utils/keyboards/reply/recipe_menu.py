from aiogram.utils.keyboard import ReplyKeyboardBuilder


def recipe_menu_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Добавить в избранное")
    builder.button(text="Назад")


    reply_kb =builder.as_markup()
    reply_kb.resize_keyboard = True

    return reply_kb


def rm_with_del_save_kb():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Удалить из избранного")
    builder.button(text="Назад")

    reply_kb = builder.as_markup()
    reply_kb.resize_keyboard = True

    return reply_kb



__all__ = ["recipe_menu_kb", "rm_with_del_save_kb"]