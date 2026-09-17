from aiogram.fsm.state import StatesGroup, State


class CompilationRecipes(StatesGroup):
    AddIngredient = State() # Добавление Ингредиентов
    AddExceptions = State() # Добавление Исключений
    DeleteIngredient = State() # Удаление Ингредиентов
    DeleteException = State() # Удаление Исключений
    SearchRecipes = State() # Поиск Рецептов
    RecipesListPages = State() # Выбор Рецепта из списка
    ShowRecipeProcessing = State() # Процесс отображения рецепта
    Recipe = State() # Рецепт