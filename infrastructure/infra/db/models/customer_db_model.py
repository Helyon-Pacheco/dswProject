from sqlalchemy import Column, String
from infrastructure.infra.db.models.base_db_model import SQLAlchemyEntityBase


class CustomerDBModel(SQLAlchemyEntityBase):
    __tablename__ = "customers"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
