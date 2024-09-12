from typing import Optional, List
from uuid import UUID
from domain.core.models.employee import Employee
from infrastructure.infra.db.models.employee_db_model import EmployeeDBModel
from infrastructure.infra.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self._employee_repository = employee_repository

    async def get_employee_by_id(self, employee_id: UUID) -> Optional[Employee]:
        employee_db = await self._employee_repository.get_by_id(employee_id)
        if employee_db:
            return Employee.from_orm(employee_db)
        return None

    async def get_all_employees(self) -> List[Employee]:
        employees_db = await self._employee_repository.get_all()
        return [Employee.from_orm(employee) for employee in employees_db]

    async def create_employee(self, employee_data: Employee) -> Employee:
        employee_db = EmployeeDBModel(**employee_data.dict())
        await self._employee_repository.add(employee_db)
        return Employee.from_orm(employee_db)

    async def update_employee(self, employee_id: UUID, employee_data: Employee) -> Optional[Employee]:
        employee_db = await self._employee_repository.get_by_id(employee_id)
        if employee_db:
            for key, value in employee_data.dict(exclude_unset=True).items():
                setattr(employee_db, key, value)
            await self._employee_repository.update(employee_db)
            return Employee.from_orm(employee_db)
        return None

    async def delete_employee(self, employee_id: UUID) -> bool:
        employee_db = await self._employee_repository.get_by_id(employee_id)
        if employee_db:
            await self._employee_repository.delete(employee_db)
            return True
        return False
