import logging
import httpx
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from disnake.ext import commands

from ticket_bot.constants import Database
from ticket_bot.utils import extensions
from ticket_bot.database import Base

logger = logging.getLogger(__name__)


class TicketBot(commands.Bot):
    """TicketBot inherited form commands.Bot"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        logger.info("Ticket Bot got initialized!")
        self.http_session = httpx.AsyncClient()
        self.db_engine = create_async_engine(Database.uri)
        self.db_session = async_sessionmaker(
            self.db_engine, expire_on_commit=False, class_=AsyncSession
        )
        logger.info("Ticket Bot is Ready!")

    def load_bot_extensions(self) -> None:
        """Load bot extensions released by walk_extensions()"""
        for ext in extensions.walk_extensions():
            logger.info(f"{ext} extension loaded!")
            self.load_extension(ext)
        logger.info("Extension loading process completed")

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        """Alias of bot.db_session"""
        return self.db_session

    async def init_db(self) -> None:
        """Init Db"""
        async with self.db_engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Close all sessions"""
        await super().close()
        if self.http_session:
            await self.http_session.aclose()
        if self.db_engine:
            await self.db_engine.dispose()
