from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseGame(StatesGroup):
    GAMEID = State()
