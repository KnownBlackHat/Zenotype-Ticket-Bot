import logging

from disnake.ext import commands
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from ticket_bot.constants import Database
from ticket_bot.database import Base

logger = logging.getLogger(__name__)


class TicketBot(commands.Bot):
    """TicketBot inherited form commands.Bot"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.db_engine = create_async_engine(Database.uri)
        self.db_session = async_sessionmaker(
            self.db_engine, expire_on_commit=False, class_=AsyncSession
        )
        logger.info("Ticket Bot got initialized!")

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        """Alias of bot.db_session"""
        return self.db_session

    async def init_db(self) -> None:
        """Init db"""
        async with self.db_engine.begin() as session:
            await session.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Close all sessions"""
        await super().close()
        if self.db_engine:
            await self.db_engine.dispose()
