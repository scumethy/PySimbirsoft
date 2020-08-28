from pydantic import BaseModel
from typing import Optional


class ItemModel(BaseModel):
    title: str
    description: str
    city: str
    price: int
    photo: Optional[str]
    tag: Optional[str]
