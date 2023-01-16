from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand("help", "Памагити, я ничего не понимаю, у меня лапки"),
            BotCommand(
                "settings",
                "Каков мой путь, каковы мои настройки на этом пути?",
            ),
            BotCommand(
                "stores",
                (
                    "Списочек магазинов (хз что с ними,"
                    " но цены они выдают неправильные)"
                ),
            ),
            BotCommand("get_game", "Получить информацию о игре\играх по id."),
        ]
    )
