import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import disnake
from disnake.ext import commands
import sqlalchemy

from ticket_bot.bot import TicketBot
from ticket_bot.constants import ButtonsIds
from ticket_bot.database import TicketConfig, Tickets

logger = logging.getLogger(__name__)

def transcript_embed(inter: disnake.ModalInteraction | disnake.MessageInteraction, config: Tickets) -> disnake.Embed:
    if not inter.guild:
        return disnake.Embed()
    openedBy = inter.guild.get_member(config.openedBy)
    closedBy = inter.guild.get_member(config.closedBy)
    claimedBy = inter.guild.get_member(config.claimedBy)
    embed = disnake.Embed(color=disnake.Colour.green())
    embed.title = "Ticket Closed"
    embed.add_field(name="Ticket Id", value=config.id)
    embed.add_field(name="Opened By", value=openedBy.mention if openedBy else None)
    embed.add_field(name="Closed By", value=closedBy.mention if closedBy else None)
    embed.add_field(name="Claimed By",value=claimedBy.mention if claimedBy else None)
    embed.add_field(name="Open Time", value=disnake.utils.format_dt(config.opentime))
    embed.add_field(name="Reason", value=config.reason or None)

    return embed

class CloseWtihReasonModal(disnake.ui.Modal):
    def __init__(self, custom_id: str, db: async_sessionmaker[AsyncSession]) -> None:
        components = [
            disnake.ui.TextInput(
                label="Reason", placeholder="Enter Reason Here", custom_id="Reason"
            )
        ]
        super().__init__(
            title="Ticket Setup", custom_id="ticket_setup", components=components
        )
        self.custom_id = custom_id
        self.db = db

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="Ticket Got Closed", description=f"Reason: {inter.text_values["Reason"]}")
        await inter.channel.send(embed=embed)
        await close_ticket(inter, self.custom_id, self.db,inter.text_values["Reason"]) 
        return await super().callback(inter)


async def close_ticket(inter: disnake.MessageInteraction| disnake.ModalInteraction, custom_id: str, db: async_sessionmaker[AsyncSession], reason: Optional[str] = None):
    # Assumption (75% true):
    # DB Fetch here but there may be inefficient fetch, some kind of state unsync can happen 
    # if this is api used concurrently. 
    # custom_id = custom_id.removeprefix(ButtonsIds.tckt_close)
    logger.debug(f"Custom Id: {custom_id}")
    _, _, tid = custom_id.split(":")
    if not isinstance(inter.channel, disnake.PartialMessageable) and isinstance(
        inter.channel, disnake.Thread
    ):
        async with db.begin() as session:
            sql_query = sqlalchemy.select(Tickets).where(Tickets.id == tid)
            configmeta = await session.scalars(sql_query)
            configmeta = configmeta.one_or_none()
            if not configmeta:
                logger.warning(f"Config Meta entry didn't existed {tid=}")
                return
            sql_query = sqlalchemy.select(TicketConfig).where(TicketConfig.id == configmeta.configid)
            config = await session.scalars(sql_query)
            config = config.one_or_none()
            if not config:
                logger.warning(f"Config entry didn't existed {configmeta.configid=}")
                return
            configmeta.closedBy = inter.author.id
            configmeta.reason = reason or ""
            await session.commit()

        await inter.send("Ticket Got Closed Successfully!", ephemeral=True)
        
        await inter.channel.edit(locked=True, archived=True)

        if not inter.guild:
            logger.warning("Guild not found")
            return
        channel = inter.guild.get_channel(config.transcript)
        if not isinstance(channel, disnake.TextChannel):
            logger.warning(f"{channel} isn't text channel")
            return
        await channel.send(embed=transcript_embed(inter, configmeta), components=[disnake.ui.Button(style=disnake.ButtonStyle.url, url=inter.channel.jump_url, label="Archived Ticket")])
    else:
        if not inter.guild:
            return
        logger.warning(f"Failed to delete {inter.channel} in {inter.guild.name}")



class TicketButtonCreater(commands.Cog, slash_command_attrs={"dm_permissions": False}):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def handler_ticket_creation(self, inter: disnake.MessageInteraction) -> None:
        """This will handle the ticket creation button click event"""

        # TODO: Refactor needed
        if not (custom_id := inter.component.custom_id) or not inter.guild:
            return
        elif custom_id.startswith(ButtonsIds.tckt_close):
            # Ticket Close 
            await close_ticket(inter, custom_id, self.bot.db)
        elif inter.component.custom_id.startswith(ButtonsIds.tckt_close_with_reason):
            # Ticket Close  with reason
            await inter.response.send_modal(CloseWtihReasonModal(db=self.bot.db, custom_id=custom_id))
        elif inter.component.custom_id.startswith(ButtonsIds.tckt_claim):
            # Ticket Claim
            logger.debug("claiming ticket")
            async with self.bot.db.begin() as session:
                _, _, tid = custom_id.split(":")
                sql_query = sqlalchemy.select(Tickets).where(Tickets.id == tid)
                result = await session.scalars(sql_query)
                result = result.one_or_none()
                if result is None:
                    logger.warning(f"Failed to fetch Tickets of id {tid}")
                    return
                result.claimedBy = inter.author.id
                await session.commit()
                
            embed = disnake.Embed(color=disnake.Color.green(), title="Claimed",
                                  description=f"This ticket is claimed by {inter.author.mention}")
            await inter.send(embed=embed)

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
        # category = inter.guild.get_channel(config.category)
        # if not category:
        #     logger.warning(f"category not found for {inter.guild}")
        #     return
        # user_or_role = inter.guild.get_role(config.role)
        # if not user_or_role:
        #     user_or_role = inter.guild.get_member(config.role)

        # Forum Channel Creation
        logger.debug(f"Thread creation proccess started {int(forum)}")
        async with self.bot.db.begin() as session:
            sql_query = Tickets(
                openedBy=inter.author.id,
                closedBy=None,
                claimedBy=None,
                opentime=datetime.now(),
                configid=config_id,
                reason=None,
            )
            session.add(sql_query)
            await session.commit()
        forum = inter.guild.get_channel(int(forum))
        if not forum or not isinstance(forum, disnake.ForumChannel):
            return
        embed = disnake.Embed(title=config.title, description=config.description, color=config.color)
        embed.set_image(config.img_url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon)
        channel = await forum.create_thread(
            name=config.title,
            embed=embed,
            components=[
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    custom_id=f"{ButtonsIds.tckt_close}{inter.author.id}:{sql_query.id}",
                    label="Close",
                ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    custom_id=f"{ButtonsIds.tckt_close_with_reason}{inter.author.id}:{sql_query.id}",
                    label="Close with reason",
                ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    custom_id=f"{ButtonsIds.tckt_claim}{inter.author.id}:{sql_query.id}",
                    label="Claim",
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
