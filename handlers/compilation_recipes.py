from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.filters import  StateFilter

from utils.keyboards.reply.main_menu_kb import main_kb
from utils.keyboards.reply.compilation_recipes_menu import cr_menu_kb
from utils.keyboards.reply.exceptions_menu import exceptions_menu_kb
from utils.keyboards.reply.back import back_kb

from utils.keyboards.inline.ingredients import ingredients_ikb

from utils.states.compilation_recipes_fsm import CompilationRecipes

from loader import bot

router = Router()

@router.message(StateFilter(None), F.text.lower() == "подобрать рецепты")
async def start_recipe_compilation(message: Message, state: FSMContext):
    await state.update_data(ingredients=[], exceptions=[])
    await state.set_state(CompilationRecipes.AddIngredient)
    await message.answer("Запишите имеющиеся у вас ингредиенты по одному, "
                         "по ним я подберу подходящие рецепты блюд", reply_markup=cr_menu_kb)


@router.message(StateFilter(CompilationRecipes.AddIngredient, CompilationRecipes.AddExceptions),
                F.text.lower() == "отмена")
async def rc_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Подборка отменена", reply_markup=main_kb)


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


@router.message(CompilationRecipes.AddIngredient, F.text.lower() == "удалить ингредиент")
async def deleting_ingredient_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data["ingredients"]

    if ingredients:
        await message.answer("Удаление добавленных ингредиентов", reply_markup=back_kb)
        msg = await message.answer("Выбери ингредиент из списка",
                             reply_markup=ingredients_ikb(ingredients))
        await state.update_data(message_id=msg.message_id)
        await state.set_state(CompilationRecipes.DeleteIngredient)
    else:
        await message.answer("У вас нет добавленных ингредиентов\n\n"
                             "Напишите в чат, чтобы добавить новый ингредиент")


@router.message(CompilationRecipes.DeleteIngredient, F.text.lower() == "назад")
async def stop_deleting_ingredients(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["message_id"]
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

    await start_add_ingredients(message, state)


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
                             reply_markup=ingredients_ikb(ingredients))
        await state.update_data(message_id=msg.message_id)
    else:
        await call.message.answer("У вас не осталось добавленных ингредиентов\n\n"
                             "Вернитесь назад, чтобы добавить ингредиенты")


@router.message(CompilationRecipes.AddIngredient)
async def add_ingredient(message: Message, state: FSMContext):
    data = await state.get_data()
    ingredients = data['ingredients']
    ingredients.append(message.text)
    await state.update_data(ingredients=ingredients)
    await message.answer(f"Добавлены ингредиенты:\n"
                         f"{"\n".join(ingredients)}\n"
                         f"Можете добавить еще ингредиенты")


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


@router.callback_query(CompilationRecipes.DeleteIngredient)
async def delete_ingredient(call: CallbackQuery, state: FSMContext):
    ingredient_id = int(call.data)
    data = await state.get_data()
    ingredients = data["ingredients"]
    ingredient = ingredients[ingredient_id]
    ingredients.remove(ingredient)

    if ingredients:
        await call.message.answer("Выбери ингредиент из списка",
                                  reply_markup=ingredients_ikb(ingredients))
        await state.set_state(CompilationRecipes.DeleteIngredient)
    else:
        await call.message.answer("У вас не осталось добавленных ингредиентов\n\n"
                                  "Вернитесь назад, чтобы добавить ингредиенты")


# Хендлеры для исключений

@router.message(CompilationRecipes.AddExceptions, F.text.lower() == "удалить исключение")
async def deleting_ingredient_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    exceptions = data["exceptions"]

    if exceptions:
        await message.answer("Удаление добавленных исключений", reply_markup=back_kb)
        await message.answer("Выбери ингредиент из списка",
                             reply_markup=ingredients_ikb(exceptions))
        await state.set_state(CompilationRecipes.DeleteException)
    else:
        await message.answer("У вас нет добавленных исключений\n\n"
                             "Напишите в чат, чтобы добавить исключение")


@router.message(CompilationRecipes.DeleteException, F.text.lower() == "назад")
async def stop_deleting_exceptions(message: Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    await start_add_exceptions(message, state)


@router.callback_query(CompilationRecipes.DeleteException)
async def delete_exception(call: CallbackQuery, state: FSMContext):
    exception_id = int(call.data)
    data = await state.get_data()
    exceptions = data["exceptions"]
    exception = exceptions[exception_id]
    exceptions.remove(exception)

    if exceptions:
        msg = await call.message.answer("Выбери ингредиент из списка",
                                  reply_markup=ingredients_ikb(exceptions))
        await state.update_data(message_id=msg.message_id)
    else:
        await call.message.answer("У вас не осталось добавленных ингредиентов\n\n"
                                  "Вернитесь назад, чтобы добавить ингредиенты")


@router.message(CompilationRecipes.AddExceptions)
async def add_exception(message: Message, state: FSMContext):
    data = await state.get_data()
    exceptions = data['exceptions']
    exceptions.append(message.text)
    await state.update_data(exceptions=exceptions)
    await message.answer(f"Добавлены исключения:\n"
                         f"{"\n".join(exceptions)}\n"
                         f"Можете добавить еще")