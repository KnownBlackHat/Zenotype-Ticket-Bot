import logging
import traceback
from typing import Optional

import disnake
from disnake.ext import commands

from ticket_bot import TicketBot


logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """Handles all error across the bot"""

    def __init__(self, client: TicketBot):
        self.bot = client

    @staticmethod
    def error_embed(title: str, description: str) -> disnake.Embed:
        embed = disnake.Embed()
        embed.title = title
        embed.description = description
        embed.color = disnake.Color.red()
        return embed

    def handle_color_error(self) -> disnake.Embed:
        """Handles for disnake color conversion error"""
        return self.error_embed("Invalid color", "Provide correct color")

    @commands.Cog.listener(name="on_slash_command_error")
    async def main_error_handler(
        self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError
    ) -> None:
        """Mega Handler"""

        embed: Optional[disnake.Embed] = None

        if isinstance(error, commands.BadColorArgument):
            embed = self.handle_color_error()

        elif isinstance(error, (commands.CommandInvokeError, commands.ConversionError)):

            # This should in else
            embed = disnake.Embed(
                title="Internal Error",
                description="".join(
                    traceback.format_exception(
                        type(error.original),
                        value=error.original,
                        tb=error.original.__traceback__,
                        limit=-3,
                    )
                ),
            )

        if embed is None:
            embed = self.error_embed("", str(error))

        await inter.send(embed=embed)


def setup(client: TicketBot):
    client.add_cog(ErrorHandler(client))
