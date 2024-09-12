from domain.core.models.order import Order
from infrastructure.infra.repositories.repository import Repository


class OrderRepository(Repository[Order]):
    def __init__(self, session, notifier):
        super().__init__(session, notifier, Order)
