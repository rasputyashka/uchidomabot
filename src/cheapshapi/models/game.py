# It is possible to make some base classes with common fields
# but i've noticed it too late, so I won't do anythting about it so far

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from collections.abc import Sequence


class Info(BaseModel):
    title: str
    steam_app_id: Optional[str] = Field(alias="steamAppID")
    thumb: str


class CheapestPriceEver(BaseModel):
    price: str
    date: datetime


class Deals(BaseModel):
    store_id: str = Field(alias="storeID")
    deal_id: str = Field(alias="dealID")
    price: float
    retail_price: str = Field(alias="retailPrice")
    savings: str


class ConcreteGame(BaseModel):
    info: Info
    cheapest_price_ever: CheapestPriceEver = Field(alias="cheapestPriceEver")
    deals: list[Deals]


class ConcreteGames(BaseModel):
    __root__: dict[str, ConcreteGame]


class _Game(BaseModel):
    game_id: str = Field(alias="gameID")
    steam_app_id: Optional[str] = Field(alias="steamAppID")
    cheapest: str
    cheapest_deal_id: str = Field(alias="cheapestDealID")
    external: str
    thumb: str


class ListGames(BaseModel):

    # since pydantic does not allow using positonal arguments, i've rewritten init
    def __init__(self, games):
        print(games)
        super().__init__(games=games)

    games: list[_Game]
