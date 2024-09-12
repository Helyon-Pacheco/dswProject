from typing import List, Optional
from uuid import UUID
from domain.core.models.customer import Customer
from infrastructure.infra.db.models.customer_db_model import CustomerDBModel
from infrastructure.infra.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository

    async def get_customer_by_id(self, customer_id: UUID) -> Optional[Customer]:
        customer_db = await self._customer_repository.get_by_id(customer_id)
        if customer_db:
            return Customer.from_orm(customer_db)
        return None

    async def get_all_customers(self) -> List[Customer]:
        customers_db = await self._customer_repository.get_all()
        return [Customer.from_orm(customer) for customer in customers_db]

    async def create_customer(self, customer_data: Customer) -> Customer:
        customer_db = CustomerDBModel(**customer_data.dict())
        await self._customer_repository.add(customer_db)
        return Customer.from_orm(customer_db)

    async def update_customer(self, customer_id: UUID, customer_data: Customer) -> Optional[Customer]:
        customer_db = await self._customer_repository.get_by_id(customer_id)
        if customer_db:
            for key, value in customer_data.dict(exclude_unset=True).items():
                setattr(customer_db, key, value)
            await self._customer_repository.update(customer_db)
            return Customer.from_orm(customer_db)
        return None

    async def delete_customer(self, customer_id: UUID) -> bool:
        customer_db = await self._customer_repository.get_by_id(customer_id)
        if customer_db:
            await self._customer_repository.delete(customer_db)
            return True
        return False
