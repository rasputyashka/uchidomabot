from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class ChooseGame(StatesGroup):
    GAMEID = State()
