from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.filters import  StateFilter

from utils.keyboards.reply.main_menu_kb import main_kb
from utils.keyboards.reply.compilation_recipes_menu import cr_menu_kb
from utils.keyboards.reply.exceptions_menu import exceptions_menu_kb
from utils.keyboards.reply.back import back_kb
from utils.keyboards.reply.cancel import cancel_kb
from utils.keyboards.reply.recipe_menu import recipe_menu_kb
from utils.keyboards.reply.recipes_list_menu import rl_menu_kb

from utils.keyboards.inline.items_list import *

from utils.states.compilation_recipes_fsm import CompilationRecipes
from utils.ai_tools import *

from data.config import prompts_dir, max_page_length, max_recipes_count
from loader import bot
import asyncio
import aiohttp


router = Router()

# Начало подбора
@router.message(StateFilter(None), F.text.lower() == "подобрать рецепты")
async def start_recipe_compilation(message: Message, state: FSMContext):
    await state.update_data(ingredients=[], exceptions=[], orig_ingredients=[], orig_exceptions=[],
                            recipes=[], page=0, active_task=None)
    await state.set_state(CompilationRecipes.AddIngredient)
    await message.answer("Запишите имеющиеся у вас ингредиенты по одному, "
                         "по ним я подберу подходящие рецепты блюд", reply_markup=cr_menu_kb)


# Отмена подбора
@router.message(StateFilter(CompilationRecipes.AddIngredient, CompilationRecipes.AddExceptions),
                F.text.lower() == "отмена")
async def rc_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Подборка отменена", reply_markup=main_kb)


# Начало Подбора рецептов
@router.message(StateFilter(CompilationRecipes.AddIngredient, CompilationRecipes.AddExceptions),
                F.text.lower() == "подобрать рецепты")
async def start_compile_recipes(message: Message, state: FSMContext, session: aiohttp.ClientSession):
    data = await state.get_data()
    ingredients = data["ingredients"]
    exceptions = data["exceptions"]
    orig_ingredients = data["orig_ingredients"]
    orig_exceptions = data["orig_exceptions"]
    recipes = data["recipes"]
    page = data["page"]

    if not (ingredients == orig_ingredients) or not (exceptions == orig_exceptions):
        recipes = []

    if not recipes:
        await message.answer("Ищу рецепты ...", reply_markup=cancel_kb)
        await state.set_state(CompilationRecipes.SearchRecipes)

        if not ingredients:
            await message.answer("Подбор рецептов невозможен, пока не добавлен хотя бы один ингредиент\n\n"
                                 "Запишите ингредиенты, из которых собираетесь готовить", reply_markup=cr_menu_kb)
            await state.set_state(CompilationRecipes.AddIngredient)
            return

        with open(f"{prompts_dir}/compile_recipes_prompt.txt", "r", encoding="utf-8") as file:
            prompt = file.read()

        ingredients_str = ", ".join(ingredients)

        if not exceptions:
            exceptions_str = ""
        else:
            exceptions_str = f"Исключить блюда, содержащие следующие ингредиенты: {', '.join(exceptions)}. "

        prompt = prompt.format(ingredients_str, exceptions_str, max_recipes_count)
        task = asyncio.create_task(send_prompt(prompt, session))
        await state.update_data(active_task=task)

        recipes_data = await task

        if task.cancelled():
            return

        if recipes_data:
            recipes = parse_recipes_list(recipes_data)

            if recipes:
                await message.answer("Рецепты подобраны", reply_markup=rl_menu_kb)
                msg = await message.answer("По вашим требованиям подходят следующие рецепты:",
                                     reply_markup=items_list_ikb(recipes, max_page_length))
                await state.update_data(recipes=recipes, orig_ingredients=ingredients.copy(), orig_exceptions=exceptions.copy())
            else:
                msg = await message.answer("Не удалось найти рецепты по вашим требованиям", back_kb)
        else:
            await message.answer("Что-то пошло не так. Попробуйте снова через некоторое время",
                                 reply_markup=cr_menu_kb)
            return
    else:
        await message.answer("Возвращаю к списку рецептов", reply_markup=rl_menu_kb)
        msg = await message.answer("По вашим требованиям подходят следующие рецепты:",
                             reply_markup=items_list_ikb(recipes, max_page_length, page))
    await state.update_data(message_id=msg.message_id)
    await state.set_state(CompilationRecipes.RecipesListPages)


# Отмена поиска
@router.message(CompilationRecipes.SearchRecipes, F.text.lower() == "отмена")
async def cancel_searching(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data['ingredients']
    task = data['active_task']

    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    await message.answer("Подборка отменена")
    await message.answer(f"Добавлены ингредиенты:\n"
                         f"{"\n".join(ingredients)}\n"
                         f"Можете добавить еще ингредиенты", reply_markup=cr_menu_kb)
    await state.set_state(CompilationRecipes.AddIngredient)


# Выбор изменения настроек в меню рецептов
@router.message(CompilationRecipes.RecipesListPages, F.text.lower()  == "изменить настройки")
async def back_to_rc_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data['ingredients']
    message_id = data['message_id']

    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.answer(f"Добавлены ингредиенты:\n"
                         f"{"\n".join(ingredients)}\n"
                         f"Можете добавить еще ингредиенты", reply_markup=cr_menu_kb)
    await state.set_state(CompilationRecipes.AddIngredient)


# Новый подбор в меню рецептов
@router.message(CompilationRecipes.RecipesListPages, F.text.lower()  == "новый подбор")
async def back_to_rc_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']

    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.answer("Начинаю новый подбор")
    await start_recipe_compilation(message, state)


# Закрытие меню рецептов
@router.message(CompilationRecipes.RecipesListPages, F.text.lower()  == "закрыть")
async def back_to_rc_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']

    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.answer("Подбор закрыт")
    await state.clear()


# Отображение страницы рецептов
@router.callback_query(CompilationRecipes.RecipesListPages, F.data.contains("page"))
async def show_page(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    recipes = data["recipes"]
    page = get_page(call.data)

    await call.message.delete()
    msg = await call.message.answer("По вашим требованиям подходят следующие рецепты:",
                         reply_markup=items_list_ikb(recipes, max_page_length, page))
    await state.update_data(page=page, message_id=msg.message_id)


# Показать рецепт
@router.callback_query(CompilationRecipes.RecipesListPages)
async def show_recipe(call: CallbackQuery, state: FSMContext, session: aiohttp.ClientSession):
    data = await state.get_data()
    recipes = data["recipes"]
    exceptions = data["exceptions"]
    recipe_name = recipes[int(call.data)]

    await call.message.delete()
    await call.message.answer("Открываю рецепт ...")

    with open(f"{prompts_dir}/get_recipe_prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()

    if not exceptions:
        exceptions = ""
    else:
        exceptions = f"Ингредиенты, которые должны быть исключены из приготовления: {', '.join(exceptions)}. "

    prompt = prompt.format(recipe_name, exceptions, recipe_name)
    task = asyncio.create_task(send_prompt(prompt, session))

    recipe = await task

    if recipe:
        await call.message.answer(recipe, reply_markup=recipe_menu_kb)
        await state.set_state(CompilationRecipes.ShowRecipe)
    else:
        await call.message.answer("Не удалось показать рецепт. Попробуйте снова через некоторое время")


# Возврат к страницам
@router.message(CompilationRecipes.ShowRecipe, F.text.lower() == "назад")
async def back_to_pages(message: Message, state: FSMContext):
    await start_compile_recipes(message, state)


# Переключение режима на добавление исключений
@router.message(CompilationRecipes.AddIngredient, F.text.lower() == "исключения")
async def start_add_exceptions(message: Message, state: FSMContext):
    await state.set_state(CompilationRecipes.AddExceptions)
    data = await state.get_data()
    exceptions = data["exceptions"]

    if exceptions:
        text = (f"Добавленные исключения:\n"
                f"{"\n".join(exceptions)}\n")
    else:
        text = "На данный момент у вас нет добавленных исключений\n"
    await message.answer(f"Добавьте ингредиенты, которые вам не нравятся или "
                         f"противопоказаны в исключения, "
                         f"чтобы я мог точнее подобрать подходящие блюда\n\n"
                         f"{text}\n"
                         f"Напишите в чат, чтобы добавить исключение", reply_markup=exceptions_menu_kb)


# Переключение на режим удаления ингредиентов
@router.message(CompilationRecipes.AddIngredient, F.text.lower() == "удалить ингредиент")
async def deleting_ingredient_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data["ingredients"]

    if ingredients:
        await message.answer("Удаление добавленных ингредиентов", reply_markup=back_kb)
        msg = await message.answer("Выбери ингредиент из списка",
                             reply_markup=items_list_ikb(ingredients))
        await state.update_data(message_id=msg.message_id)
        await state.set_state(CompilationRecipes.DeleteIngredient)
    else:
        await message.answer("У вас нет добавленных ингредиентов\n\n"
                             "Напишите в чат, чтобы добавить новый ингредиент")


# Отмена удаления добавленных ингредиентов
@router.message(CompilationRecipes.DeleteIngredient, F.text.lower() == "назад")
async def stop_deleting_ingredients(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["message_id"]
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

    await start_add_ingredients(message, state)


# Удаление ингредиента
@router.callback_query(CompilationRecipes.DeleteIngredient)
async def delete_ingredient(call: CallbackQuery, state: FSMContext):
    ingredient_id = int(call.data)
    data = await state.get_data()
    ingredients = data["ingredients"]
    ingredient = ingredients[ingredient_id]
    ingredients.remove(ingredient)

    await call.message.delete()
    if ingredients:
        msg = await call.message.answer("Выбери ингредиент из списка",
                             reply_markup=items_list_ikb(ingredients))
    else:
        msg = await call.message.answer("У вас не осталось добавленных ингредиентов\n\n"
                             "Вернитесь назад, чтобы добавить ингредиенты")

    await state.update_data(message_id=msg.message_id)


# Удаление всех ингредиентов
@router.message(CompilationRecipes.AddIngredient, F.text.lower() == "удалить все ингредиенты")
async def delete_all_ingredients(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data["ingredients"]

    if ingredients:
        await state.update_data(ingredients=[])
        text = ("Все ингредиенты успешно удалены\n\n"
                "Напишите, чтобы добавить ингредиент")
    else:
        text = ("Нет добавленных ингредиентов!\n\n"
                "Напишите, чтобы добавить ингредиент")

    await message.answer(text)


# Добавление ингредиента
@router.message(CompilationRecipes.AddIngredient)
async def add_ingredient(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data['ingredients']
    ingredients.append(message.text)
    await state.update_data(ingredients=ingredients)
    await message.answer(f"Добавлены ингредиенты:\n"
                         f"{"\n".join(ingredients)}\n"
                         f"Можете добавить еще ингредиенты")


# Переключение режима на добавление ингредиентов
@router.message(CompilationRecipes.AddExceptions, F.text.lower() == "ингредиенты")
async def start_add_ingredients(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data['ingredients']

    if ingredients:
        text = (f"Добавлены ингредиенты:\n"
                f"{"\n".join(ingredients)}\n"
                f"Можете добавить еще ингредиенты")
    else:
        text = ("Нет добавленных ингредиентов\n"
                "Напишите в чат, чтобы добавить")

    await state.set_state(CompilationRecipes.AddIngredient)
    await message.answer(text=text, reply_markup=cr_menu_kb)


# Хендлеры для исключений

# Переключение режима на удаление исключений
@router.message(CompilationRecipes.AddExceptions, F.text.lower() == "удалить исключение")
async def deleting_ingredient_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    exceptions = data["exceptions"]

    if exceptions:
        await message.answer("Удаление добавленных исключений", reply_markup=back_kb)
        await message.answer("Выбери ингредиент из списка",
                             reply_markup=items_list_ikb(exceptions))
        await state.set_state(CompilationRecipes.DeleteException)
    else:
        await message.answer("У вас нет добавленных исключений\n\n"
                             "Напишите в чат, чтобы добавить исключение")


# Отмена удаления исключений
@router.message(CompilationRecipes.DeleteException, F.text.lower() == "назад")
async def stop_deleting_exceptions(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["message_id"]
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

    await start_add_exceptions(message, state)


# Удаление исключения
@router.callback_query(CompilationRecipes.DeleteException)
async def delete_exception(call: CallbackQuery, state: FSMContext):
    exception_id = int(call.data)
    data = await state.get_data()
    exceptions = data["exceptions"]
    exception = exceptions[exception_id]
    exceptions.remove(exception)

    await call.message.delete()
    if exceptions:
        msg = await call.message.answer("Выбери ингредиент из списка",
                                  reply_markup=items_list_ikb(exceptions))
    else:
        msg = await call.message.answer("У вас не осталось добавленных ингредиентов\n\n"
                                  "Вернитесь назад, чтобы добавить ингредиенты")

    await state.update_data(message_id=msg.message_id)


# Удаление всех ингредиентов
@router.message(CompilationRecipes.AddExceptions, F.text.lower() == "удалить все исключения")
async def delete_all_ingredients(message: Message, state: FSMContext):
    data = await state.get_data()
    exceptions = data["exceptions"]

    if exceptions:
        await state.update_data(exceptions=[])
        text = ("Все исключения успешно удалены\n\n"
                "Напишите, чтобы добавить исключение")
    else:
        text = ("Нет добавленных исключений! \n\n"
                "Напишите, чтобы добавить исключение")

    await message.answer(text)


# Добавление исключения
@router.message(CompilationRecipes.AddExceptions)
async def add_exception(message: Message, state: FSMContext):
    data = await state.get_data()
    exceptions = data['exceptions']
    exceptions.append(message.text)
    await state.update_data(exceptions=exceptions)
    await message.answer(f"Добавлены исключения:\n"
                         f"{"\n".join(exceptions)}\n"
                         f"Можете добавить еще")