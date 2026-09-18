from aiogram.fsm.state import StatesGroup, State


class Saves(StatesGroup):
    SavesList = State() # Список избранного
    Recipe = State() # Просмотр конкретного рецепта