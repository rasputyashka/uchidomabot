from pydantic import BaseModel
from pydantic import Field


class _Images(BaseModel):
    banner: str
    logo: str
    icon: str


class Store(BaseModel):
    store_id: int = Field(alias="storeID")
    store_name: str = Field(alias="storeName")
    is_active: bool = Field(alias="isActive")
    images: _Images


class Stores(BaseModel):
    # since pydantic does not allow using positonal arguments, i've rewritten init

    __root__: list[Store]
