from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from infrastructure.infra.db.session import get_db
from service.management.services.employee_service import EmployeeService
from infrastructure.infra.repositories.employee_repository import EmployeeRepository
from domain.core.models.employee import Employee


router = APIRouter()

@router.get("/", response_model=List[Employee])
async def get_employees(db=Depends(get_db)):
    employee_service = EmployeeService(EmployeeRepository(db))
    employees = await employee_service.get_all_employees()
    return employees

@router.get("/{employee_id}", response_model=Employee)
async def get_employee_by_id(employee_id: UUID, db=Depends(get_db)):
    employee_service = EmployeeService(EmployeeRepository(db))
    employee = await employee_service.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_new_employee(employee: Employee, db=Depends(get_db)):
    employee_service = EmployeeService(EmployeeRepository(db))
    new_employee = await employee_service.create_employee(employee)
    return new_employee

@router.put("/{employee_id}", response_model=Employee)
async def update_employee_details(employee_id: UUID, employee: Employee, db=Depends(get_db)):
    employee_service = EmployeeService(EmployeeRepository(db))
    updated_employee = await employee_service.update_employee(employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return updated_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_employee(employee_id: UUID, db=Depends(get_db)):
    employee_service = EmployeeService(EmployeeRepository(db))
    success = await employee_service.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
