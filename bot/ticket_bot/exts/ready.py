import disnake
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

            # Retrieve Guild
            existing_guilds = await session.scalars(sqlalchemy.select(Guild))
            existing_guilds = existing_guilds.all()
            logger.info(f"Retrieving Guild: {existing_guilds=}")

            await session.commit()

            # Db cleanup
            bot_guild_ids = {guild_id.id for guild_id in self.bot.guilds}
            async with self.bot.db.begin() as session:
                for guild in existing_guilds:
                    if guild.id not in bot_guild_ids:
                        logger.info(
                            f"{bot_guild_ids} Removed {Guild(id=guild.id, name=guild.name)}"
                        )
                        sql_query = sqlalchemy.delete(Guild).where(Guild.id == guild.id)
                        await session.execute(sql_query)
                        await session.commit()


def setup(client: TicketBot):
    client.add_cog(Register(client))
