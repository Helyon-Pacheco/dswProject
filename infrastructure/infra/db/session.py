from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from infrastructure.infra.db.config import async_session


@asynccontextmanager
async def get_db() -> AsyncSession:
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
