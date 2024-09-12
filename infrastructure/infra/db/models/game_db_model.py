from sqlalchemy import Column, String, Float, Integer
from infrastructure.infra.db.models.base_db_model import SQLAlchemyEntityBase


class GameDBModel(SQLAlchemyEntityBase):
    __tablename__ = "games"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
