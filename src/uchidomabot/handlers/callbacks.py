from aiogram.utils.callback_data import CallbackData


store_callback = CallbackData("get_store", "store_id")
stores_list_callback = CallbackData("list_stores")
game_criteria_callback = CallbackData("sort_type", "type", "store_id", "page")
back_next_game_page_callback = CallbackData(
    "swap_page", "type", "direction", "store_id", "page"
)
