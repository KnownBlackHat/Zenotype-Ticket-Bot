import logging

import disnake
from disnake.ext import commands

from ticket_bot.bot import TicketBot

logger = logging.getLogger(__name__)


class Commands(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        data = None
        success = False
        for guild in self.bot.guilds:
            data = {
                "id": str(guild.id),
                "name": guild.name,
                "icon": guild.icon.url if guild.icon else "",
                "description": guild.description,
                "owner": str(guild.owner_id),
            }
            res = await self.bot.request("/guilds/add", "POST", data=data)
            success = False
            if res.get("success"):
                success = True

        if success:
            logger.info("Db synced with guild")
        else:
            logger.error(f"Db update failed")

    @commands.slash_command(name="add_role")
    async def role_add(
        self, inter: disnake.GuildCommandInteraction, role: disnake.Role
    ) -> None:
        data = {"id": str(role.id)}
        res = await self.bot.request(
            f"/role/add?guild={inter.guild_id}", "POST", data=data
        )
        if not res.get("success"):
            raise commands.CommandError(f"IPC Error in role/add {res}")
        await inter.send(f"{role.mention} is now new role for dashboard access")


def setup(bot: TicketBot):
    bot.add_cog(Commands(bot))
