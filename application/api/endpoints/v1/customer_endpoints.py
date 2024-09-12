from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from infrastructure.infra.db.session import get_db
from service.management.services.customer_service import CustomerService
from infrastructure.infra.repositories.customer_repository import CustomerRepository
from domain.core.models.customer import Customer


router = APIRouter()

@router.get("/", response_model=List[Customer])
async def get_customers(db=Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    customers = await customer_service.get_all_customers()
    return customers

@router.get("/{customer_id}", response_model=Customer)
async def get_customer_by_id(customer_id: UUID, db=Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    customer = await customer_service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: Customer, db=Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    new_customer = await customer_service.create_customer(customer)
    return new_customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer_details(customer_id: UUID, customer: Customer, db=Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    updated_customer = await customer_service.update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_customer(customer_id: UUID, db=Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    success = await customer_service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
