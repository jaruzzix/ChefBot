from aiogram.fsm.state import StatesGroup, State


class CompilationRecipes(StatesGroup):
    Create = State()
    AddIngredient = State()
    AddExceptions = State()
    DeleteIngredient = State()
    DeleteException = State()
    FindRecipe = State()
    FindRecipeWithSelected = State()
    GetRecipe = State()