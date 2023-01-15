from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from cheapshapi.models.store import Store
from uchidomabot.handlers.callbacks import (
    concrete_game_criteria_callback,
    sorting_games_callback,
    store_callback,
    stores_list_callback,
    back_next_game_page_callback,
)


def create_stores_list_keyboard(stores: list[Store]):
    markup = InlineKeyboardMarkup(row_width=4)
    for store in stores:
        store_name = store.store_name
        store_id = store.store_id
        button = InlineKeyboardButton(
            text=store_name,
            callback_data=store_callback.new(store_id=store_id),
        )
        markup.insert(button)
    return markup


def create_store_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    concrete_criterias = (("AAA игры: ", "AAA"), ("Скидки: ", "onSale"))

    for criteria in concrete_criterias:
        concrete_button = InlineKeyboardButton(
            text=criteria[0],
            callback_data=concrete_game_criteria_callback.new(criteria[1]),
        )
        markup.insert(concrete_button)

    sort_criteria = (
        ("Сортировать по выгоде", "Savings"),
        ("Сортировать по цене", "Price"),
        ("Сортировать по оценке metacritic", "Metacritic"),
        ("Сортировать по дате", "Release"),
        ("Сортировать по отзывам", "Reviews"),
    )

    for sort_info in sort_criteria:
        sort_button = InlineKeyboardButton(
            text=sort_info[0],
            callback_data=sorting_games_callback.new(*sort_info[1:]),
        )
        markup.insert(sort_button)

    exit_button = InlineKeyboardButton(
        "назад", callback_data=stores_list_callback.new()
    )
    markup.add(exit_button)
    return markup


def create_back_next_page_keyboard(game_type: str = None, sort_by: str = None):
    markup = InlineKeyboardMarkup(2)
    if sort_by is None:
        param = game_type
    else:
        param = sort_by
    next_button = InlineKeyboardButton(
        text="Дальше",
        callback_data=back_next_game_page_callback.new(param, "next"),
    )
    prev_button = InlineKeyboardButton(
        text="Назад",
        callback_data=back_next_game_page_callback.new(param, "back"),
    )
    markup.row(prev_button, next_button)
    return markup


def create_settings_keyboard():
    markup = InlineKeyboardMarkup(1)
    change_button = InlineKeyboardButton(
        "Поменять порядок сортировки",
        callback_data="invert_sort_order",
    )
    markup.insert(change_button)
    return markup
