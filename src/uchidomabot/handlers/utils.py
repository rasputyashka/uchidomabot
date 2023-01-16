import re

from cheapshapi.models.deal import Deals
from cheapshapi.models.game import ConcreteGames, ConcreteGame
from cheapshapi.utils import redirect, get_metacritic, get_steam_page
from operator import attrgetter
from collections import namedtuple
from uchidomabot.keyboards.inline import create_store_link_keyboard


NUMBER_PATTERN = re.compile("\d+")
PageInfo = namedtuple("PageInfo", "text thumb markup")


def get_game_ids(
    user_input: str,
) -> list[str]:
    return re.findall(NUMBER_PATTERN, user_input)


def get_games_page(deals: Deals, game_page, decorator):
    deal_string = ""
    for deal in deals.__root__:
        game_link = decorator.link(deal.title.title(), redirect(deal.deal_id))
        sale_price = deal.sale_price
        old_normal_price = deal.normal_price
        normal_price = int(float(deal.normal_price) * 67)
        savings = deal.savings
        deal_string += game_link + f" - id {deal.game_id}"
        if old_normal_price != sale_price:
            deal_string += (
                f"\n    Цена:"
                f" {decorator.strikethrough(str(normal_price))}₽"
                f"  {float(sale_price)*67:.0f}₽"
                f", экономия: {float(savings):.0f}%"
            )
        else:
            deal_string += f"\n    Цена: {normal_price}"
        if deal.metacritic_link:
            metacritic_link = decorator.link(
                "Отзыв метакритики", get_metacritic(deal.metacritic_link)
            )
            deal_string += f"\n    {metacritic_link}"
        deal_string += "\n\n"

    deal_string += f"Страница {game_page + 1}"  # the first api page is 0

    return deal_string


def get_game_pages(games: ConcreteGames | ConcreteGame, decorator) -> list[PageInfo]:
    pages = []
    if isinstance(games, ConcreteGame):
        games = [games]
    elif isinstance(games, ConcreteGames):
        games = games.__root__.values()
    for game in games:
        game_string = ""
        game_info = game.info
        title = game_info.title
        thumb = game_info.thumb
        cheapest_price_info = game.cheapest_price_ever
        cheapest_price = int(float(cheapest_price_info.price) * 67)
        cheapest_price = f"{cheapest_price}₽ at {cheapest_price_info.date: %Y-%m-%d}"
        min_deal = min(game.deals, key=attrgetter("price"))
        min_deal_price = int(float(min_deal.price * 67))
        deal_link = redirect(min_deal.deal_id)

        game_string += decorator.link(title, get_steam_page(title))
        game_string += (
            f"\n\nМинимальная цена за всё время: {cheapest_price}"
            f"\n\nТекущая минимальная цена: {min_deal_price}₽"
        )

        markup = create_store_link_keyboard(deal_link)

        pages.append(PageInfo(game_string, thumb, markup))

    return pages
