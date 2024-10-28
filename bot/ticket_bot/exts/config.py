import logging
from typing import Optional

import disnake
from disnake.ext import commands
import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from ticket_bot import TicketBot
from ticket_bot.database import TicketConfig
from ticket_bot.utils.buttons import DeleteButton

from enum import Enum

logger = logging.getLogger(__name__)


class ConfigSlot(Enum):
    Slot1 = 1
    Slot2 = 2
    Slot3 = 3
    Slot4 = 4
    Slot5 = 5
    Slot6 = 6
    Slot7 = 7
    Slot8 = 8
    Slot9 = 9
    Slot10 = 10


class TicketModal(disnake.ui.Modal):
    def __init__(
        self,
        config: ConfigSlot,
        transcript: disnake.TextChannel,
        db: async_sessionmaker[AsyncSession],
        color: Optional[disnake.Color],
    ):
        self.db = db
        self.config = config
        self.color = color
        self.transcript = transcript

        components = [
            disnake.ui.TextInput(
                label="Title",
                placeholder="Enter Title here",
                custom_id="title",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Enter Description here",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Image",
                placeholder="Enter Image URL",
                custom_id="img_url",
                style=disnake.TextInputStyle.short,
                required=False,
            ),
        ]
        super().__init__(
            title="Ticket Setup", custom_id="ticket_setup", components=components
        )

    async def callback(self, inter: disnake.ModalInteraction):
        if not inter.guild:
            return None
        await inter.response.defer()
        title = inter.text_values["title"]
        description = inter.text_values["description"]
        image = inter.text_values["img_url"]

        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(TicketConfig).where(
                TicketConfig.guild_id == inter.guild_id,
                TicketConfig.config == self.config,
            )
            result = await session.scalars(sql_query)
            result = result.one_or_none()

            if not result:
                sql_query = TicketConfig(
                    color=self.color.value if self.color else 0,
                    guild_id=inter.guild_id,
                    title=title,
                    description=description,
                    img_url=image,
                    config=self.config,
                    transcript=self.transcript.id,
                )
                session.add(sql_query)
            else:
                result.guild_id = inter.guild.id
                result.title = title
                result.description = description
                result.img_url = image
                result.config = self.config  # type: ignore
                result.color = self.color.value if self.color else 0
                result.transcript = self.transcript.id

            await session.commit()

            logger.debug(f"Modal Registered for {inter.guild.id}")
            await inter.send(f"`{ConfigSlot(self.config).name}` config created!")

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):  # type: ignore[reportIncompatibleMethodOverride]
        logger.exception(error)
        await inter.response.send_message(
            embed=disnake.Embed(
                color=disnake.Color.red(), title="Oops! Something went wrong :cry:"
            ),
            ephemeral=True,
        )


class TConfig(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.slash_command(name="create")
    async def setup(
        self,
        inter: disnake.GuildCommandInteraction,
        config: ConfigSlot,
        transcript: disnake.TextChannel,
        color: Optional[disnake.Color],
    ) -> None:
        """
        Setup Ticket System

        Parameters
        ----------
        config : Choose a slot to store your config
        """
        await inter.response.send_modal(
            modal=TicketModal(
                db=self.bot.db,
                config=config,
                color=color,
                transcript=transcript,
            )
        )

    @commands.slash_command(name="show_config")
    async def list_config(
        self, inter: disnake.GuildCommandInteraction, slot: ConfigSlot
    ):
        """
        Show config of asked config slot

        Parameters
        ----------
        slot: Slot to save your config
        """
        async with self.bot.db.begin() as session:
            config = await session.scalars(
                sqlalchemy.select(TicketConfig).where(
                    TicketConfig.guild_id == inter.guild_id,
                    TicketConfig.config == slot,
                )
            )
            config = config.one_or_none()
        if not config:
            await inter.send(f"No config found in slot: `{slot}`. Create one first!")
            return

        embed = disnake.Embed(
            title=f"**Slot:** {slot}",
            description=f"""
                **Title:** {config.title}
                **Description:** \n{config.description}\n
                **Color:** {disnake.Color(config.color) if config.color else "None"}
                **Image:** {f"[Click To See]({config.img_url})" if config.img_url else "None"}
                **Transcript:** {inter.guild.get_channel(config.transcript)}
                """,
        )
        embed = embed.set_image(config.img_url)
        embed.color = config.color
        await inter.send(embed=embed, components=[DeleteButton(user=inter.author)])


def setup(client: TicketBot):
    client.add_cog(TConfig(client))
