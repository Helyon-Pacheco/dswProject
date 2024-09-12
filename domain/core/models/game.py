from pydantic import Field
from .entity_base import EntityBase
from typing import Optional

class Game(EntityBase):
    title: str = Field(..., alias="Title")
    description: Optional[str] = Field(None, alias="Description")
    price: float = Field(..., alias="Price")
    stock: int = Field(..., alias="Stock")
