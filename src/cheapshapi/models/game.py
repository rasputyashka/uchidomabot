from pydantic import BaseModel


class Info(BaseModel):
    title: str
    steam_app_id: int
    thumb: str


class CheapestPriceEver:
    price: str
    date: int  # posix time