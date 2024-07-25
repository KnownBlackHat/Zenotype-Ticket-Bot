import logging
from typing import Dict, Literal, Optional

import httpx
from disnake.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ticket_bot.constants import Client, Database
from ticket_bot.database import Base
from ticket_bot.utils import extensions

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
        self.http_session = httpx.AsyncClient()

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
        if self.http_session:
            await self.http_session.aclose()

    def load_bot_extensions(self) -> None:
        """Load bot extensions released by walk_extensions()"""
        for ext in extensions.walk_extensions():
            logger.info(f"{ext} extension loaded!")
            self.load_extension(ext)
        logger.info("Extension loading process completed")

    async def request(
        self,
        route: str,
        method: Literal["GET", "POST"] = "GET",
        data: Optional[Dict] = None,
    ) -> httpx.Response:
        """
        Make a request to the IPC server

        ----------------
        Parameters:
        - route (str): The route to make the request to
        - method (str): The method to use for the request
        - data (dict): The data to send with the request
        """

        if not route.startswith("/"):
            logger.warning("route should start with /")
            raise httpx.InvalidURL("route should start with /")
        if method == "GET":
            resp = await self.http_session.get(Client.ipc_url + route)
        else:
            resp = await self.http_session.post(Client.ipc_url + route, data=data)
        return resp
