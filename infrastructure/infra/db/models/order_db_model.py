from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.infra.db.models.base_db_model import SQLAlchemyEntityBase
from infrastructure.infra.db.models.customer_db_model import CustomerDBModel


class OrderDBModel(SQLAlchemyEntityBase):
    __tablename__ = "orders"

    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    total = Column(Float, nullable=False)

    customer = relationship("CustomerDBModel", back_populates="orders")

CustomerDBModel.orders = relationship("OrderDBModel", back_populates="customer")
