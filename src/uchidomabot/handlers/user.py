from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.utils.text_decorations import HtmlDecoration

from cheapshapi.client import CheapShark
from cheapshapi.utils import get_image, get_metacritic, redirect
from uchidomabot.handlers.callbacks import (
    back_next_game_page_callback,
    concrete_game_criteria_callback,
    store_callback,
    stores_list_callback,
    sorting_games_callback,
)
from uchidomabot.handlers.utils import get_game_page
from uchidomabot.keyboards.inline import (
    create_back_next_page_keyboard,
    create_store_keyboard,
    create_stores_list_keyboard,
    create_settings_keyboard,
)
from uchidomabot.services.repository import Repo


async def user_start(msg: Message, repo: Repo):
    await repo.add_user(msg.from_id, "descending")
    await msg.reply("Hello, user!")


async def get_store_list(
    msg: Message = None,
    client: CheapShark = None,
):
    stores = await client.get_stores()
    working_stores = [store for store in stores.stores if store.is_active]
    markup = create_stores_list_keyboard(working_stores)
    response_text = (
        "Чтобы получить информацию о магазине, выберите его из списка"
    )
    if isinstance(msg, CallbackQuery):
        msg = msg.message
        await msg.delete()
    await msg.answer(
        response_text,
        reply_markup=markup,
    )


async def display_store_info(
    call: CallbackQuery,
    callback_data: dict,
    client: CheapShark,
    state: FSMContext,
    repo: Repo,
):
    await call.answer()
    stores = await client.get_stores()
    for store in stores.stores:
        if store.store_id == int(callback_data["store_id"]):
            store_thumb = store.images.logo
            store_id = store.store_id
            store_name = store.store_name
            markup = create_store_keyboard()
            async with state.proxy() as state_data:
                state_data["current_store_id"] = store_id
                sorting_setting = (
                    "Возрастание"
                    if await repo.get_user_sort_order(call.from_user.id)
                    == "ascending"
                    else "Убывание"
                )
            await call.message.answer_photo(
                photo=get_image(store_thumb),
                caption=(
                    f"*{store_name}*'s id is `{store_id}`"
                    + "\n\nНажав на кнопку ниже вы"
                    + " получите 5 игр по заданному критерию"
                    + f"\n\nтекущая настройока сортировки: {sorting_setting}"
                    + "\nЧтобы узнать больше о настройках, смотрите /settings"
                ),
                parse_mode="Markdown",
                reply_markup=markup,
            )

            await call.message.delete()
            break


async def get_games(
    call: CallbackQuery,
    callback_data: dict,
    client: CheapShark,
    state: FSMContext,
    repo: Repo,
):
    await call.answer()
    async with state.proxy() as state_data:
        game_page_num = state_data.setdefault("game_page", 0)
        store_id = state_data["current_store_id"]
        direction = callback_data.get("direction")
        if direction is not None:
            if direction == "next":
                state_data["game_page"] += 1
                game_page_num += 1
            else:
                state_data["game_page"] -= 1
                game_page_num -= 1

    sorting_order = await repo.get_user_sort_order(call.from_user.id)
    desc = True if sorting_order == "descending" else False
    if callback_data.get("by") is None:
        if callback_data["type"] == "AAA":
            deals = await client.list_deals(
                store_id=store_id,
                page_number=game_page_num,
                page_size=7,
                aaa=True,
            )
        elif callback_data["type"] == "onSale":
            deals = await client.list_deals(
                store_id=store_id,
                page_number=game_page_num,
                page_size=7,
                on_sale=True,
            )
        else:
            deals = await client.list_deals(
                store_id=store_id,
                page_number=game_page_num,
                page_size=7,
                sort_by=callback_data.get("type"),
                desc=desc,
            )
        markup = create_back_next_page_keyboard(sort_by=callback_data["type"])
    else:
        deals = await client.list_deals(
            store_id=store_id,
            page_number=game_page_num,
            page_size=7,
            sort_by=callback_data.get("by"),
            desc=desc,
        )
        markup = create_back_next_page_keyboard(sort_by=callback_data["by"])

    game_page = get_game_page(deals, game_page_num)

    if callback_data.get("direction") is not None:
        await call.message.edit_text(
            game_page,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=markup,
        )
    else:
        await call.message.answer(
            game_page,
            parse_mode="HTML",
            reply_markup=markup,
            disable_web_page_preview=True,
        )


async def get_settings(msg: Message, repo: Repo):
    user_sort_order = await repo.get_user_sort_order(msg.from_id)

    markup = create_settings_keyboard()
    await msg.answer(
        f"Порядок сортировки: {user_sort_order}", reply_markup=markup
    )


async def invert_user_sorting_order(call: CallbackQuery, repo: Repo):

    order = await repo.get_user_sort_order(call.from_user.id)
    if order == "descending":
        order = "ascending"
    else:
        order = "descending"
    await repo.invert_user_sort_order(call.from_user.id, order)
    await call.answer("Настройка изменена.")
    await call.message.edit_text(
        f"Порядок сортировки: {order}", reply_markup=call.message.reply_markup
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        get_store_list,
        commands=["stores", "store", "магазины", "магазин"],
        state="*",
    )
    dp.register_callback_query_handler(
        display_store_info, store_callback.filter()
    )
    dp.register_callback_query_handler(
        get_store_list, stores_list_callback.filter()
    )

    dp.register_callback_query_handler(
        get_games, concrete_game_criteria_callback.filter()
    )
    dp.register_callback_query_handler(
        get_games, back_next_game_page_callback.filter()
    )

    dp.register_callback_query_handler(
        get_games, sorting_games_callback.filter()
    )

    dp.register_message_handler(get_settings, commands=["settings", "setting"])

    dp.register_callback_query_handler(
        invert_user_sorting_order, text_contains="invert_sort_order"
    )

    dp.register_message_handler(user_start, commands=["start"])
