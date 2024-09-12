from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from domain.core.models.entity_base import EntityBase


@as_declarative()
class SQLAlchemyBase:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class SQLAlchemyEntityBase(SQLAlchemyBase, EntityBase):
    pass
