from aiogram.utils.callback_data import CallbackData

store_callback = CallbackData("get_store", "store_id")
stores_list_callback = CallbackData("list_stores")
concrete_game_criteria_callback = CallbackData("game_type", "type")
sorting_games_callback = CallbackData("sort_game_by", "by")
back_next_game_page_callback = CallbackData("swap_page", "type", "direction")
