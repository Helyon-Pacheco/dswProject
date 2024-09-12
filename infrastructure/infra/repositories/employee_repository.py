from domain.core.models.employee import Employee
from infrastructure.infra.repositories.repository import Repository


class EmployeeRepository(Repository[Employee]):
    def __init__(self, session, notifier):
        super().__init__(session, notifier, Employee)
