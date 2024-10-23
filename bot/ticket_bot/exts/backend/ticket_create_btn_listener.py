import disnake
import logging
from disnake.ext import commands
import sqlalchemy

from ticket_bot.bot import TicketBot
from ticket_bot.constants import ButtonsIds
from ticket_bot.database.config import TicketConfig

logger = logging.getLogger(__name__)


class TicketButtonCreater(commands.Cog, slash_command_attrs={"dm_permissions": False}):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def handler_ticket_creation(self, inter: disnake.MessageInteraction) -> None:
        """This will handle the ticket creation button click event"""
        # Prefix Check
        if (
            not inter.guild
            or not (config_id := inter.component.custom_id)
            or not config_id.startswith(ButtonsIds.tckt_create)
        ):
            return

        # Cleanup
        forum, config_id = config_id.removeprefix(ButtonsIds.tckt_create).split(":")

        async with self.bot.db.begin() as session:
            sql_query = sqlalchemy.select(TicketConfig).where(
                TicketConfig.config == config_id,
                TicketConfig.guild_id == inter.guild_id,
            )
            config = await session.scalars(sql_query)
            config = config.one_or_none()
        if not config:
            logger.warning(f"Config not found for {inter.guild}")
            return
        category = inter.guild.get_channel(config.category)
        if not category:
            logger.warning(f"category not found for {inter.guild}")
            return
        user_or_role = inter.guild.get_role(config.role)
        if not user_or_role:
            user_or_role = inter.guild.get_member(config.role)

        # TODO: forum channel creation
        logger.debug(f"Thread creation proccess started {int(forum)}")
        forum = inter.guild.get_channel(int(forum))
        if not forum or not isinstance(forum, disnake.ForumChannel):
            return
        embed = disnake.Embed(
            title=config.title, description=config.description, color=config.color
        )
        embed.set_image(config.img_url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon)
        channel = await forum.create_thread(
            name=config.title,
            content=config.description,
            embed=embed,
            components=[
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    custom_id=f"{ButtonsIds.tckt_close}{inter.author.id}",
                    label="Close",
                ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    custom_id=f"{ButtonsIds.tckt_close_with_reason}{inter.author.id}",
                    label="Close with reason",
                ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    custom_id=f"{ButtonsIds.tckt_claim}{inter.author.id}",
                    label="Close Ticket",
                ),
            ],
        )

        # Channel is created
        # logger.debug("channel is creation proc started")
        # channel = await inter.guild.create_text_channel(
        #     inter.author.name,
        #     category=category,  # type: ignore[reportArgumentType]
        #     overwrites={  # type: ignore[reportArgumentType]
        #         inter.guild.default_role: disnake.PermissionOverwrite(
        #             read_messages=False
        #         ),
        #         inter.user: disnake.PermissionOverwrite(
        #             read_messages=True,
        #             send_messages=True,
        #             attach_files=True,
        #         ),
        #         user_or_role: disnake.PermissionOverwrite(
        #             read_messages=True,
        #             send_messages=True,
        #             attach_files=True,
        #         ),
        #         inter.guild.me: disnake.PermissionOverwrite(
        #             read_messages=True,
        #             send_messages=True,
        #             attach_files=True,
        #         ),
        #     },
        # )

        # embed = disnake.Embed(
        #     title=config.title,
        #     description=config.description,
        #     color=disnake.Color(config.color),
        # )
        # embed.set_image(config.img_url)
        # embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon)
        # await channel.send(
        #     embed=embed,
        #     components=[
        #         disnake.ui.Button(
        #             style=disnake.ButtonStyle.red,
        #             custom_id=f"{ButtonsIds.tckt_close}{inter.author.id}",
        #             label="Close",
        #         ),
        #         disnake.ui.Button(
        #             style=disnake.ButtonStyle.red,
        #             custom_id=f"{ButtonsIds.tckt_close_with_reason}{inter.author.id}",
        #             label="Close with reason",
        #         ),
        #         disnake.ui.Button(
        #             style=disnake.ButtonStyle.green,
        #             custom_id=f"{ButtonsIds.tckt_claim}{inter.author.id}",
        #             label="Close Ticket",
        #         ),
        #     ],
        # )

        await inter.send(
            "Ticket Created",
            ephemeral=True,
            components=[
                disnake.ui.Button(
                    style=disnake.ButtonStyle.url,
                    label="Go to your ticket",
                    url=channel.thread.jump_url,
                )
            ],
        )


def setup(client: TicketBot):
    client.add_cog(TicketButtonCreater(client))
