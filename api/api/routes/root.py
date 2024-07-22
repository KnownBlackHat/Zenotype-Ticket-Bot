from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.constants import Database
from api.models import Base


class Root:
    def __init__(self) -> None:
        self.db_engine = create_async_engine(Database.uri)
        self.db_session = async_sessionmaker(
            self.db_engine, expire_on_commit=True, class_=AsyncSession
        )

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        """Alias of db_session"""
        return self.db_session

    async def init_db(self) -> None:
        """Initializes the database"""
        async with self.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Closes session when shutting down"""
        if self.db_engine:
            await self.db_engine.dispose()
