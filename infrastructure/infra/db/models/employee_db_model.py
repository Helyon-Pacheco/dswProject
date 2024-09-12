from sqlalchemy import Column, String
from infrastructure.infra.db.models.base_db_model import SQLAlchemyEntityBase


class EmployeeDBModel(SQLAlchemyEntityBase):
    __tablename__ = "employees"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=True)
