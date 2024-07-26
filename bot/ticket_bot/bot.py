import logging
from typing import Any, Dict, List, Literal, Optional

import httpx
from disnake.ext import commands

from ticket_bot.constants import Client
from ticket_bot.utils import extensions

logger = logging.getLogger(__name__)


class TicketBot(commands.Bot):
    """TicketBot inherited form commands.Bot"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        logger.info("Ticket Bot got initialized!")
        self.http_session = httpx.AsyncClient()

    async def close(self) -> None:
        """Close all sessions"""
        await super().close()
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
    ) -> Any:
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
            resp = await self.http_session.post(
                Client.ipc_url + route,
                json=data,
            )
            resp.raise_for_status()
        return resp.json()
