import logging

import disnake
from disnake.ext import commands

from ticket_bot.bot import TicketBot
from ticket_bot.constants import Colours

logger = logging.getLogger(__name__)


class Commands(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     data = None
    #     success = False
    #     for guild in self.bot.guilds:
    #         data = {
    #             "id": str(guild.id),
    #             "name": guild.name,
    #             "icon": guild.icon.url if guild.icon else "",
    #             "description": guild.description,
    #             "owner": str(guild.owner_id),
    #         }
    #         res = await self.bot.request("/guilds/add", "POST", data=data)
    #         success = False
    #         if res.get("success"):
    #             success = True

    #     if success:
    #         logger.info("Db synced with guild")
    #     else:
    #         logger.error(f"Db update failed")

    # @commands.slash_command(name="add_role")
    # async def role_add(
    #     self, inter: disnake.GuildCommandInteraction, role: disnake.Role
    # ) -> None:
    #     """
    #     Sets required role to access dashboard

    #     Parameters:
    #     ----------
    #     role: The role to be set as required role
    #     """

    #     data = {"id": str(role.id)}
    #     res = await self.bot.request(
    #         f"/role/add?guild={inter.guild_id}", "POST", data=data
    #     )
    #     if not res.get("success"):
    #         raise commands.CommandError(f"IPC Error in role/add {res}")
    #     await inter.send(f"{role.mention} is now new role for dashboard access")

    # @commands.slash_command(name="create_panel")
    # async def create_panel(self, inter: disnake.GuildCommandInteraction, panel_id: int):
    #     """
    #     Creates a new panel

    #     Parameters:
    #     ----------
    #     panel_id: The id of the panel
    #     """
    #     res = await self.bot.request(f"/panels/find?panel={panel_id}", "GET")
    #     if res.get("success") == False:
    #         raise commands.CommandError(f"IPC Error in panel/add {res}")
    #     embed = disnake.Embed(
    #         title=res["title"],
    #         description=res["description"],
    #         color=getattr(Colours, res["color"], Colours.blue),
    #     )
    #     embed.set_footer(text=res["author_name"], icon_url=res["author_url"])
    #     embed.set_thumbnail(res["large_image"])
    #     embed.set_image(res["small_image"])
    #     component = disnake.ui.Button(
    #         label=res["button_emoji"] + " " + res["button_text"],
    #         style=getattr(
    #             disnake.ButtonStyle, res["button_color"], disnake.ButtonStyle.primary
    #         ),
    #         # emoji=res["button_emoji"],
    #     )
    #     await inter.send(embed=embed, components=[component])

    # @create_panel.autocomplete("panel_id")
    # async def create_panel_autocomp(self, inter: disnake.GuildCommandInteraction, _):
    #     res = await self.bot.request(f"/panels?guild={inter.guild.id}", "GET")
    #     ids = map(lambda x: x["id"], res)
    #     return ids


def setup(bot: TicketBot):
    bot.add_cog(Commands(bot))
