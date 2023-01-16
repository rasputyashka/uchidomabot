from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from cheapshapi.models.store import Store
from uchidomabot.handlers.callbacks import (
    game_criteria_callback,
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
            callback_data=store_callback.new(store_id),
        )
        markup.insert(button)
    return markup


def create_store_keyboard(store_id, page):
    markup = InlineKeyboardMarkup(row_width=2)

    concrete_criterias = (
        ("AAA игры: ", "AAA"),
        ("Скидки: ", "onSale"),
        ("Сортировать по выгоде", "Savings"),
        ("Сортировать по цене", "Price"),
        ("Сортировать по оценке metacritic", "Metacritic"),
        ("Сортировать по дате", "Release"),
        ("Сортировать по отзывам", "Reviews"),
    )

    for criteria in concrete_criterias:
        concrete_button = InlineKeyboardButton(
            text=criteria[0],
            callback_data=game_criteria_callback.new(criteria[1], store_id, page),
        )
        markup.insert(concrete_button)

    exit_button = InlineKeyboardButton(
        "вернуться", callback_data=stores_list_callback.new()
    )
    markup.add(exit_button)
    return markup


def create_back_next_page_keyboard(sort_type: str, store_id, page):
    markup = InlineKeyboardMarkup(2)
    next_button = InlineKeyboardButton(
        text="Дальше",
        callback_data=back_next_game_page_callback.new(
            sort_type, "next", store_id, page + 1
        ),
    )
    prev_button = InlineKeyboardButton(
        text="Назад",
        callback_data=back_next_game_page_callback.new(
            sort_type, "back", store_id, page - 1
        ),
    )
    markup.row(prev_button, next_button)

    exit_button = InlineKeyboardButton(
        "Вернуться", callback_data=store_callback.new(store_id)
    )
    markup.add(exit_button)
    return markup


def create_settings_keyboard():
    markup = InlineKeyboardMarkup(1)
    change_button = InlineKeyboardButton(
        "Поменять порядок сортировки",
        callback_data="invert_sort_order",
    )
    markup.insert(change_button)
    return markup


def create_store_link_keyboard(url):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Перейти", url=url)
    return markup.insert(button)
