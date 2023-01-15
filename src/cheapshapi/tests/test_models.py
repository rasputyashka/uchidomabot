from aiohttp import ClientSession
from cheapshapi.models.deal import ConcreteDeal, Deals
from cheapshapi.models.store import Stores
from cheapshapi.models.game import ConcreteGame, ConcreteGames, ListGames
from cheapshapi.client import CheapShark


async def test_solo_deal():
    deal_ids = [
        "X8sebHhbc1Ga0dTkgg59WgyM506af9oNZZJLU9uSrX8%3D",
        "EX0oH20b7A1H2YiVjvVx5A0HH%2F4etw3x%2F6YMGVPpKbA%3D",
        "z4El8C19yCEHrk1%2ByEedebThQVbblI7H0Z%2BAmxgZiS8%3D",
        "TlzUCY9p3Sq1bY%2Br4aGWO5Cs2UxE1lYnuQD05gxNwIM%3D",
    ]
    for deal_id in deal_ids:
        async with ClientSession() as session:
            async with session.request(
                "GET",
                url=f"https://www.cheapshark.com/api/1.0/deals?id={deal_id}",
            ) as response:
                exp_json = await response.json()
                expected = ConcreteDeal(**exp_json)
            client = CheapShark(session)
            result = await client.get_deal(deal_id)

            assert expected == result


async def test_listing_deals():
    async with ClientSession() as session:
        async with session.request(
            "GET",
            url="https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15",
        ) as response:
            exp_json = await response.json()
            expected = Deals(exp_json)
        client = CheapShark(session)
        result = await client.list_deals(store_id=1, upper_price=15)
        assert expected == result


async def test_stores():
    async with ClientSession() as session:
        async with session.request(
            "GET", url="https://www.cheapshark.com/api/1.0/stores"
        ) as response:
            resp_json = await response.json()
            expected = Stores(resp_json)
        client = CheapShark(session)
        result = await client.get_stores()

        assert result == expected


async def test_solo_game():
    game_ids = [248711, 252015, 249250]
    for game_id in game_ids:
        async with ClientSession() as session:
            async with session.request(
                "GET",
                url=f"https://www.cheapshark.com/api/1.0/games?id={game_id}",
            ) as response:
                exp_json = await response.json()
                expected = ConcreteGame.parse_obj(exp_json)
            client = CheapSharp(session)
            result = await client.get_game(game_id)

            assert expected == result


async def test_several_games():
    game_ids = [248711, 252015, 249250]
    async with ClientSession() as session:
        ids = ",".join([str(game_id) for game_id in game_ids])
        async with session.request(
            "GET",
            url=f"https://www.cheapshark.com/api/1.0/games?ids={ids}",
        ) as response:
            exp_json = await response.json()
            expected = ConcreteGames.parse_obj(exp_json)
        client = CheapShark(session)
        result = await client.get_games(*game_ids)

        assert expected == result


async def test_listing_games():
    async with ClientSession() as session:
        async with session.request(
            "GET",
            url="https://www.cheapshark.com/api/1.0/games?title=spider%20man",
        ) as response:
            exp_json = await response.json()
            expected = ListGames(exp_json)
        client = CheapShark(session)
        result = await client.list_games(title="spider man")
        assert expected == result
