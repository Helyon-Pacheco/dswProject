from domain.core.models.customer import Customer
from infrastructure.infra.repositories.repository import Repository


class CustomerRepository(Repository[Customer]):
    def __init__(self, session, notifier):
        super().__init__(session, notifier, Customer)
