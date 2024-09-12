from typing import Optional, List
from uuid import UUID
from domain.core.models.order import Order
from infrastructure.infra.db.models.order_db_model import OrderDBModel
from infrastructure.infra.repositories.order_repository import OrderRepository


class OrderItemDBModel:
    pass


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self._order_repository = order_repository

    async def get_order_by_id(self, order_id: UUID) -> Optional[Order]:
        order_db = await self._order_repository.get_by_id(order_id)
        if order_db:
            return Order.from_orm(order_db)
        return None

    async def get_all_orders(self) -> List[Order]:
        orders_db = await self._order_repository.get_all()
        return [Order.from_orm(order) for order in orders_db]

    async def create_order(self, order_data: Order) -> Order:
        order_items = [OrderItemDBModel(**item.dict()) for item in order_data.items]
        order_db = OrderDBModel(
            customer_id=order_data.customer_id,
            total=order_data.total,
            items=order_items
        )
        await self._order_repository.add(order_db)
        return Order.from_orm(order_db)

    async def update_order(self, order_id: UUID, order_data: Order) -> Optional[Order]:
        order_db = await self._order_repository.get_by_id(order_id)
        if order_db:
            for key, value in order_data.dict(exclude_unset=True).items():
                setattr(order_db, key, value)
            await self._order_repository.update(order_db)
            return Order.from_orm(order_db)
        return None

    async def delete_order(self, order_id: UUID) -> bool:
        order_db = await self._order_repository.get_by_id(order_id)
        if order_db:
            await self._order_repository.delete(order_db)
            return True
        return False
