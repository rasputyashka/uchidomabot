from functools import partial

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.text_decorations import HtmlDecoration

from cheapshapi.client import CheapShark
from cheapshapi.utils import get_image
from uchidomabot.handlers.callbacks import (
    back_next_game_page_callback,
    game_criteria_callback,
    store_callback,
    stores_list_callback,
)
from uchidomabot.handlers.utils import (
    get_games_page,
    get_game_ids,
    get_game_pages,
)
from uchidomabot.keyboards.inline import (
    create_back_next_page_keyboard,
    create_store_keyboard,
    create_stores_list_keyboard,
    create_settings_keyboard,
)
from uchidomabot.services.repository import Repo
from uchidomabot.states.choose_game import ChooseGame


async def user_start(msg: Message, repo: Repo):
    await repo.add_user(msg.from_id, "descending")
    await msg.reply("Дарова, заебал! Чтобы увидеть справку, тыкните /help")


async def get_store_list(
    msg: Message = None,
    client: CheapShark = None,
):
    stores = await client.get_stores()
    working_stores = [store for store in stores.__root__ if store.is_active]
    markup = create_stores_list_keyboard(working_stores)
    response_text = "Чтобы получить информацию о магазине, выберите его из списка"
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
    for store in stores.__root__:
        if store.store_id == int(callback_data["store_id"]):
            store_thumb = store.images.logo
            store_id = store.store_id
            store_name = store.store_name
            markup = create_store_keyboard(store_id, page=0)
            async with state.proxy() as state_data:
                state_data["current_store_id"] = store_id
                sorting_setting = (
                    "Убывание"
                    if await repo.get_user_sort_order(call.from_user.id) == "descending"
                    else "Возрастание"
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
    repo: Repo,
):
    await call.answer()
    store_id = callback_data["store_id"]
    page = int(callback_data["page"])

    sorting_order = await repo.get_user_sort_order(call.from_user.id)
    desc = False if sorting_order == "descending" else True
    base_func = partial(
        client.list_deals,
        store_id=store_id,
        page_number=page,
        page_size=7,
        desc=desc,
    )
    if callback_data["type"] == "AAA":
        deals = await base_func(aaa=True)
    elif callback_data["type"] == "onSale":
        deals = await base_func(on_sale=True)
    else:
        deals = await base_func(
            sort_by=callback_data["type"],
        )
    markup = create_back_next_page_keyboard(callback_data["type"], store_id, page)
    decorator = HtmlDecoration()
    game_page = get_games_page(deals, page, decorator)

    if callback_data.get("direction") is not None:
        await call.message.edit_caption(
            game_page,
            parse_mode="HTML",
            reply_markup=markup,
        )
    else:
        await call.message.edit_caption(
            game_page,
            parse_mode="HTML",
            reply_markup=markup,
        )


async def get_settings(msg: Message, repo: Repo):
    user_sort_order = await repo.get_user_sort_order(msg.from_id)

    # user friendly representation
    user_order = "Убывание" if user_sort_order == "descending" else "Возрастание"

    info_string = (
        "Порядок сортировки*: {0}\n\n*Порядок сортировки используется"
        " в командах типа /store\n\n Режима только два: убывание и возрастание"
    )
    markup = create_settings_keyboard()
    await msg.answer(info_string.format(user_order), reply_markup=markup)


async def invert_user_sorting_order(call: CallbackQuery, repo: Repo):

    order = await repo.get_user_sort_order(call.from_user.id)
    if order == "descending":
        order = "ascending"
    else:
        order = "descending"
        # user friendly representation
    user_order = "Убывание" if order == "descending" else "Возрастание"

    info_string = (
        "Порядок сортировки*: {0}\n\n*Порядок сортировки используется"
        " в командах типа /store\n\n Режима только два: убывание и возрастание"
    )
    await repo.invert_user_sort_order(call.from_user.id, order)
    await call.answer("Настройка изменена.")
    await call.message.edit_text(
        info_string.format(user_order), reply_markup=call.message.reply_markup
    )


async def get_game(msg: Message, client: CheapShark, state: FSMContext):
    user_data = msg.get_full_command()[1]
    if not user_data:
        await msg.answer(
            (
                "Укажите нужные вам id (вы можете взять их"
                " через поиск по сайту в команде /stores)"
            )
        )
        await state.set_state(ChooseGame.GAMEID)
    else:
        decorator = HtmlDecoration()
        game_ids = get_game_ids(user_data)
        if len(game_ids) == 1:
            game = await client.get_game(game_ids[0])
            game_pages = get_game_pages(game, decorator)
        else:
            games = await client.get_games(*game_ids)
            game_pages = get_game_pages(games, decorator)

        for page in game_pages:
            await msg.answer_photo(
                photo=page.thumb,
                caption=page.text,
                parse_mode="HTML",
                reply_markup=page.markup,
            )


async def get_game_with_state(msg: Message, state: FSMContext, client: CheapShark):
    user_data = msg.text
    decorator = HtmlDecoration()
    game_ids = get_game_ids(user_data)
    if not game_ids:
        await msg.answer("Ни одного id не найдено")
    if len(game_ids) == 1:
        game = await client.get_game(game_ids[0])
        game_pages = get_game_pages(game, decorator)
    else:
        games = await client.get_games(*game_ids)
        game_pages = get_game_pages(games, decorator)

    for page in game_pages:
        await msg.answer_photo(
            photo=page.thumb,
            caption=page.text,
            parse_mode="HTML",
            reply_markup=page.markup,
        )
    await state.finish()


async def help_message(msg: Message):
    await msg.answer(
        (
            "Есть два стула: /stores и /get_game"
            " \n\nА ещё есть настройки: /settings, выбирай"
        )
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        get_store_list,
        commands=["stores", "store", "магазины", "магазин"],
        state="*",
    )
    dp.register_message_handler(get_settings, commands=["settings", "setting"])
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(help_message, commands=["help", "помощь"])
    dp.register_message_handler(get_game, commands=["get_game"])

    dp.register_callback_query_handler(display_store_info, store_callback.filter())
    dp.register_callback_query_handler(get_store_list, stores_list_callback.filter())

    dp.register_callback_query_handler(get_games, game_criteria_callback.filter())
    dp.register_callback_query_handler(get_games, back_next_game_page_callback.filter())
    dp.register_callback_query_handler(
        invert_user_sorting_order, text_contains="invert_sort_order"
    )
    dp.register_message_handler(get_game_with_state, state=ChooseGame.GAMEID)
