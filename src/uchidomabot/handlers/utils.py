from aiogram.utils.text_decorations import HtmlDecoration
from cheapshapi.models.deal import Deals
from cheapshapi.utils import redirect, get_metacritic


def get_game_page(deals: Deals, game_page):
    decorator = HtmlDecoration()
    deal_string = ""
    for deal in deals.deals:
        game_link = decorator.link(deal.title.title(), redirect(deal.deal_id))
        sale_price = deal.sale_price
        old_normal_price = deal.normal_price
        normal_price = int(float(deal.normal_price) * 67)
        metacritic_link = get_metacritic(
            decorator.link("metacritic", deal.metacritic_link)
        )
        savings = deal.savings
        deal_string += game_link
        if old_normal_price != sale_price:
            deal_string += (
                f"\n    Цена: "
                f"  {decorator.strikethrough(str(normal_price))}₽   "
                f"  {float(sale_price)*67:.0f}₽"
                f", экономия: {float(savings):.0f}%"
            )
        else:
            deal_string += f"\n    Цена: {normal_price}"
        if metacritic_link:
            deal_string += f"\n    {metacritic_link}"
        deal_string += "\n\n"

    deal_string += f"Страница {game_page + 1}"  # the first api page is 0

    return deal_string
