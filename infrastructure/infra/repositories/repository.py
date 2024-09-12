from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, List, Any, Generic, TypeVar, Sequence
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.future import select
from uuid import UUID
from domain.core.enums.notification_type import NotificationType
from domain.core.models.entity_base import EntityBase
from domain.core.notifications.notifier import INotifier


TEntity = TypeVar('TEntity', bound=EntityBase)

class Repository(Generic[TEntity]):
    def __init__(self, session: AsyncSession, notifier: INotifier, entity: Type[TEntity]):
        self._session = session
        self._entity = entity
        self._notifier = notifier

    async def get_by_id(self, entity_id: UUID) -> TEntity:
        try:
            self._notifier.handle(f"Getting {self._entity.__name__} by ID {entity_id}.")
            result = await self._session.execute(select(self._entity).filter_by(id=str(entity_id)))
            entity = result.scalars().first()
            if not entity:
                raise NoResultFound(f"{self._entity.__name__} with ID {entity_id} not found.")
            return entity
        except SQLAlchemyError as ex:
            self._notifier.handle(f"Error getting {self._entity.__name__} by ID {entity_id}: {ex}", NotificationType.ERROR)
            raise

    async def get_all(self) -> Sequence[Row[Any] | RowMapping | Any]:
        try:
            self._notifier.handle(f"Getting all {self._entity.__name__}.")
            result = await self._session.execute(select(self._entity))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            self._notifier.handle(f"Error getting all {self._entity.__name__}: {ex}", NotificationType.ERROR)
            raise

    async def add(self, entity: TEntity) -> None:
        try:
            self._notifier.handle(f"Adding {self._entity.__name__}.")
            self._session.add(entity)
            await self._session.commit()
        except SQLAlchemyError as ex:
            await self._session.rollback()
            self._notifier.handle(f"Error adding {self._entity.__name__}: {ex}", NotificationType.ERROR)
            raise

    async def update(self, entity: TEntity) -> None:
        try:
            self._notifier.handle(f"Updating {self._entity.__name__}.")
            await self._session.commit()
        except SQLAlchemyError as ex:
            await self._session.rollback()
            self._notifier.handle(f"Error updating {self._entity.__name__}: {ex}", NotificationType.ERROR)
            raise

    async def delete(self, entity: TEntity) -> None:
        try:
            self._notifier.handle(f"Deleting {self._entity.__name__}.")
            await self._session.delete(entity)
            await self._session.commit()
        except SQLAlchemyError as ex:
            await self._session.rollback()
            self._notifier.handle(f"Error deleting {self._entity.__name__}: {ex}", NotificationType.ERROR)
            raise

    async def find(self, **kwargs: Any) -> Sequence[Row[Any] | RowMapping | Any]:
        try:
            self._notifier.handle(f"Finding {self._entity.__name__}.")
            result = await self._session.execute(select(self._entity).filter_by(**kwargs))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            self._notifier.handle(f"Error finding {self._entity.__name__}: {ex}", NotificationType.ERROR)
            raise
