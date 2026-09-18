from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from utils.keyboards.inline.items_list import get_page
from utils.states.saves_fsm import Saves
from utils.keyboards.inline.saves_list import saves_list_ikb
from utils.keyboards.reply.close import close_kb
from utils.keyboards.reply.recipe_menu import *
from utils.keyboards.reply.main_menu_kb import main_kb

from data.config import saves_max_page_length as max_page_length
import loader

bot = loader.bot
db = loader.db

router = Router()


# Показать список избранного. Вход в машину состояний
@router.message(StateFilter(None), F.text.lower() == 'избранное')
async def show_saved_list(message: Message, state: FSMContext, page: int = 0):
    saves = await db.get_all_saves(message.from_user.id)

    if saves:
        await message.answer("Открываю избранное", close_kb)
        msg = await message.answer("Твои Сохраненные рецепты:",
                                   reply_markup=saves_list_ikb(saves, max_page_length, page))

        await state.update_data(message_id=msg.message_id, page=page, current_save_id = '')
        await state.set_state(Saves.SavesList)
    else:
        await message.answer("Список избранных пуст")

        current_state = state.get_state()
        if current_state:
            await state.clear()


# Закрыть список рецептов
@router.message(Saves.SavesList, F.text.lower() == 'закрыть')
async def close_list(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']

    await bot.delete_message(message.chat.id, message_id)
    await message.answer("Список избранного закрыт", reply_markup=main_kb)
    await state.clear()


# Переход на страницу
@router.callback_query(Saves.SavesList, F.data.contains("page"))
async def close_list(call: CallbackQuery, state: FSMContext):
    saves = await db.get_all_saves(call.from_user.id)
    page = get_page(call.data)

    await call.message.delete()
    msg = await call.message.answer("Твои Сохраненные рецепты:",
                                    reply_markup=saves_list_ikb(saves, max_page_length, page))
    await state.update_data(message_id=msg.message_id, page=page)



# Показ рецепта
@router.callback_query(Saves.SavesList)
async def show_recipe(call: CallbackQuery, state: FSMContext):
    data = await db.get_save(call.from_user.id, call.data)
    recipe_text = data['content']

    await call.message.answer(recipe_text, reply_markup=rm_with_del_save_kb())
    await state.set_state(Saves.Recipe)
    await state.update_data(current_save_id=call.data)


@router.message(Saves.Recipe, F.text.lower() == "назад")
async def back_to_saves_list(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data['page']

    await show_saved_list(message, state, page)

@router.message(Saves.Recipe, F.text.lower() == "удалить из избранного")
async def back_to_saves_list(message: Message, state: FSMContext):
    data = await state.get_data()

    await db.del_save(message.from_user.id, data["current_save_id"])
    await message.answer("Рецепт успешно удален из избранного. Возвращаю к списку")
    await back_to_saves_list(message, state)

