from collections.abc import Sequence
from typing import Literal, Optional

from cheapshapi.base import SharkBase
from cheapshapi.exceptions import SharkException
from cheapshapi.models.deal import ConcreteDeal, Deals
from cheapshapi.models.game import ConcreteGame, ConcreteGames, ListGames
from cheapshapi.models.store import Stores


class CheapShark(SharkBase):
    async def list_deals(
        self,
        *,
        store_id: Optional[str] = None,
        page_number: int = 0,
        page_size: int = 60,
        sort_by: str = "Deal Rating",
        desc: bool = False,
        lower_price: int = 0,
        # according to api reference, 50 acts like there's no limit
        upper_price: Optional[int] = 50,
        metacritic: Optional[int] = None,
        steam_rating: Optional[int] = None,
        steam_app_id: Optional[str] = None,
        title: Optional[str] = None,
        excact: bool = False,
        aaa: bool = False,
        steamworks: bool = False,
        on_sale: bool = False,
        output: Optional[str] = None,
    ) -> Deals:
        """Implement `List of Deal` section."""
        path = "deals"
        params = {
            "pageNumber": page_number,
            "pageSize": page_size,
            "sortBy": sort_by,
            "desc": int(desc),  # api requires bool to be numbers
            "lowerPrice": lower_price,
            "upperPrice": upper_price,
            "excact": int(excact),
            "AAA": int(aaa),
            "steamworks": int(steamworks),
            "onSale": int(on_sale),
        }

        if store_id is not None:
            params["storeID"] = store_id
        if metacritic is not None:
            params["metacritic"] = metacritic
        if steam_rating is not None:
            params["steamRating"] = steam_rating
        if steam_app_id is not None:
            params["steamAppID"] = steam_app_id
        if title is not None:
            params["title"] = title
        if output is not None:
            params["output"] = output

        headers = {"x_rapidapi_user": "rasputyashka@gmail.com"}
        return await self._request(
            path,
            fabric=Deals,
            method="GET",
            params=params,
            headers=headers,
        )

    async def get_deal(self, deal_id: str) -> ConcreteDeal:
        """Implement of `Deal Loopup` section.

        aiohttp does not support encoded params, so url is created manually.
        """
        path = "deals"
        return await self._request(
            f"{path}?id={deal_id}", fabric=ConcreteDeal, method="GET"
        )

    async def list_games(
        self,
        *,
        title: str,
        steam_app_id: Optional[int] = None,
        limit: int = 60,
        excact: bool = False,
    ) -> ListGames:
        """Implment `List of Games` section."""
        path = "games"
        params = {
            "title": title,
            "limit": limit,
            "excact": int(excact),
        }
        if steam_app_id is not None:
            params["steamAppID"] = steam_app_id

        return await self._request(path, fabric=ListGames, method="GET", params=params)

    async def get_game(self, game_id: int) -> ConcreteGame:
        """Implement `Game Lookup` section.

        aiohttp does not support encoded params, so url is created manually.
        """
        path = "games"
        return await self._request(
            f"{path}?id={game_id}", fabric=ConcreteGame, method="GET"
        )

    async def get_games(self, *game_ids: Sequence[int]) -> ConcreteGames:
        """Implement `Multiple Game Lookup` section.

        aiohttp does not support encoded params, so url is created manually.
        """
        path = "games"
        # conversion to str allows user to pass id in more convinient way
        game_ids = ",".join([str(game_id) for game_id in game_ids])
        if not game_ids:
            raise SharkException("Not enough game ids")
        return await self._request(
            f"{path}?ids={game_ids}",
            fabric=ConcreteGames,
            method="GET",
        )

    async def get_stores(self) -> Stores:
        """Implement `Stores Info` section."""
        path = "stores"
        return await self._request(path, fabric=Stores, method="GET")

    async def edit_alert(
        self,
        *,
        action: Literal["set", "delete"],
        email: str,
        game_id: int,
        price: Optional[float] = None,
    ) -> bool:
        """Implement `Edit Alert` section.

        Since the api does not give correct prices, I don't use this method.
        """
        path = "alerts"
        if action == "set" and price is None:
            msg = "Price is required if action parameter is 'set'"
            raise SharkException(msg)
        params = {
            "action": action,
            "email": email,
            "gameID": game_id,
            "price": price,
        }
        return await self._request(path, method="GET", params=params)

    async def manage_alert(self, action: Literal["set", "delete"], email: str) -> bool:
        """Implement `Edit Alert` section.

        Since the api does not give correct prices, I don't use this method.
        """
        path = "alerts"
        params = {"action": action, "email": email}
        return await self._request(path, method="GET", parms=params)
