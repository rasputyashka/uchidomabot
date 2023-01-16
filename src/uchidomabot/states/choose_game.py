from aiogram.dispatcher.filters.state import StatesGroup, State


class ChooseGame(StatesGroup):
    GAMEID = State()
