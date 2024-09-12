from typing import List
from pydantic import Field
from datetime import datetime
from .entity_base import EntityBase

class OrderItem(EntityBase):
    game_id: str = Field(..., alias="GameId")
    quantity: int = Field(..., alias="Quantity")

class Order(EntityBase):
    customer_id: str = Field(..., alias="CustomerId")
    items: List[OrderItem] = Field(..., alias="Items")
    total: float = Field(..., alias="Total")
    order_date: datetime = Field(default_factory=datetime.utcnow, alias="OrderDate")
