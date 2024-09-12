from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from infrastructure.infra.db.session import get_db
from service.management.services.order_service import OrderService
from infrastructure.infra.repositories.order_repository import OrderRepository
from domain.core.models.order import Order


router = APIRouter()

@router.get("/", response_model=List[Order])
async def get_orders(db=Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    orders = await order_service.get_all_orders()
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order_by_id(order_id: UUID, db=Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    order = await order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_new_order(order: Order, db=Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    new_order = await order_service.create_order(order)
    return new_order

@router.put("/{order_id}", response_model=Order)
async def update_order_details(order_id: UUID, order: Order, db=Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    updated_order = await order_service.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_order(order_id: UUID, db=Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    success = await order_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
