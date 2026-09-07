from aiogram.fsm.state import StatesGroup, State


class CompilationRecipes(StatesGroup):
    Create = State()
    AddIngredient = State()
    AddExceptions = State()
    DeleteIngredient = State()
    DeleteException = State()
    RecipesListPages = State()
    ShowRecipe = State()