from typing import Optional

from pydantic import BaseModel, Field


class CheapestPrice(BaseModel):
    price: str
    date: int


class CheaperStore(BaseModel):
    deal_id: str = Field(alias="dealID")
    store_id: str = Field(alias="storeID")
    sale_price: str = Field(alias="salePrice")
    retail_price: str = Field(alias="retailPrice")


class GameInfo(BaseModel):
    store_id: str = Field(alias="storeID")
    game_id: str = Field(alias="gameID")
    name: str
    steam_app_id: Optional[str] = Field(alias="steamAppID")
    sale_price: str = Field(alias="salePrice")
    retail_price: str = Field(alias="retailPrice")
    steam_rating_text: Optional[str] = Field(alias="steamRatingText")
    steam_rating_percent: str = Field(alias="steamRatingPercent")
    steam_rating_count: str = Field(alias="steamRatingCount")
    metacritic_score: str = Field(alias="metacriticScore")
    metacritic_link: Optional[str] = Field(alias="metacriticLink")
    release_date: int = Field(alias="releaseDate")
    publisher: str
    steamworks: str
    thumb: str


class ConcreteDeal(BaseModel):
    game_info: GameInfo = Field(alias="gameInfo")
    cheaper_stores: list[CheaperStore] = Field(alias="cheaperStores")
    cheapest_price: CheapestPrice = Field(alias="cheapestPrice")


# that api has different deals (for deal lookup and list of deals)


class Store(BaseModel):
    store_id: int = Field(alias="storeID")
    store_name: str = Field(alias="storeName")
    is_active: bool = Field(alias="isActive")


class Deal(BaseModel):
    internal_name: str = Field(alias="internalName")
    title: str
    metacritic_link: Optional[str] = Field(alias="metacriticLink")
    deal_id: str = Field(alias="dealID")
    store_id: str = Field(alias="storeID")
    game_id: str = Field(alias="gameID")
    sale_price: str = Field(alias="salePrice")
    normal_price: str = Field(alias="normalPrice")
    is_on_sale: str = Field(alias="isOnSale")
    savings: str
    metacritic_score: str = Field(alias="metacriticScore")
    steam_rating_text: Optional[str] = Field(alias="steamRatingText")
    steam_rating_percent: str = Field(alias="steamRatingPercent")
    steam_rating_count: str = Field(alias="steamRatingCount")
    steam_app_id: Optional[str] = Field(alias="steamAppID")
    release_date: int = Field(alias="releaseDate")
    last_change: int = Field(alias="lastChange")
    deal_rating: str = Field(alias="dealRating")
    thumb: str


class Deals(BaseModel):

    # since pydantic does not allow using positonal arguments, i've rewritten init

    __root__: list[Deal]
