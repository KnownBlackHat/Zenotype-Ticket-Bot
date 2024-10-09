import logging
from disnake.ext import commands
import sqlalchemy

from ticket_bot.bot import TicketBot
from ticket_bot.database import Guild


logger = logging.getLogger()


class Register(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.begin() as session:

            # Register Guild in db
            for guild in self.bot.guilds:
                await session.merge(Guild(id=guild.id, name=guild.name))
                logger.info("Merged guild: %s", guild)

            # Db cleanup
            bot_guilds_ids = {guild.id for guild in self.bot.guilds}
            stale_guilds = await session.scalars(
                sqlalchemy.select(Guild).where(Guild.id.not_in(bot_guilds_ids))
            )

            for stguild in stale_guilds:
                logger.info(f"Removed Guild: {stguild}")
                await session.delete(stguild)

            await session.commit()


def setup(client: TicketBot):
    client.add_cog(Register(client))
