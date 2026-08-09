from aiogram.fsm.state import StatesGroup, State


class CreateRecipe(StatesGroup):
    Create = State()
    AddIngredient = State()
    FindRecipe = State()
    FindRecipeWithSelected = State()
    GetRecipe = State()