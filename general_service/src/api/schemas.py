from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemModel(BaseModel):
    title: str
    description: str
    city: str
    price: int
    photo: Optional[str]
    tag: Optional[str]
