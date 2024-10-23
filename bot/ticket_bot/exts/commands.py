import logging
from typing import Union

import disnake
from disnake.ext import commands
import sqlalchemy

from ticket_bot.bot import TicketBot
from ticket_bot.constants import ButtonsIds
from ticket_bot.exts.config import ConfigSlot
from ticket_bot.database import TicketConfig

logger = logging.getLogger(__name__)


class EmbedModal(disnake.ui.Modal):
    def __init__(self, color):
        self.color = color
        components = [
            disnake.ui.TextInput(
                label="Image url",
                placeholder="Enter image here",
                custom_id="image",
                style=disnake.TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Title",
                placeholder="Enter title here",
                custom_id="title",
                style=disnake.TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Suggestion: Use <@User_Id> for mention & <#Channel_Id> for tagging the channel!",
                custom_id="body",
                style=disnake.TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Embed Generator", custom_id="embed_generator", components=components
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        if not interaction.guild:
            return
        await interaction.response.defer()
        title = interaction.text_values["title"]
        content = interaction.text_values["body"]
        image = interaction.text_values["image"]

        embed = disnake.Embed(color=self.color, title=title, description=content)
        embed.set_image(image)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon)
        await interaction.send(
            embed=disnake.Embed(
                title="Embed sent! :white_check_mark:", color=disnake.Colour.green()
            ),
            ephemeral=True,
            delete_after=1,
        )
        await interaction.channel.send(embed=embed)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):  # type: ignore[reportIncompatibleMethodOverride]
        await inter.response.send_message(
            embed=disnake.Embed(
                color=disnake.Color.red(), title="Oops! Something went wrong :cry:"
            ),
            ephemeral=True,
        )


class Commands(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.slash_command(name="embed", dm_permission=False)
    async def slash_embed(
        self,
        interaction: disnake.CommandInteraction,
        color: Union[disnake.Color, None] = None,
    ):
        """
        Creates embed

        Parameters
        ----------
        color: Hex code or name of colour
        """
        await interaction.response.send_modal(modal=EmbedModal(color=color))

    @commands.slash_command(name="set_button")
    async def link(
        self,
        inter: disnake.GuildCommandInteraction,
        msg: disnake.Message,
        config: ConfigSlot,
        archive_forum: disnake.ForumChannel,
    ) -> None:
        """
        Adds a button to msg and link it with config slot

        Parameters
        ----------
        msg: Message link
        config: Choose a config to add button for
        """
        await inter.response.defer(ephemeral=True)
        async with self.bot.db.begin() as session:
            sql_query = sqlalchemy.select(TicketConfig).where(
                TicketConfig.config == config
            )
            result = await session.scalars(sql_query)
            result = result.one_or_none()
        if result is None:
            await inter.send("Given config is empty", ephemeral=True)
            return
        elif self.bot.user.id != msg.author.id:
            await inter.send(
                "Message is not created by me, use `/embed` command to create one",
                ephemeral=True,
            )
            return

        await msg.edit(
            components=[
                disnake.ui.Button(
                    emoji="🎫",
                    style=disnake.ButtonStyle.blurple,
                    custom_id=f"{ButtonsIds.tckt_create}{archive_forum.id}:{config}",
                )
            ]
        )

        await inter.send(
            f"Ticket Button Linked to config slot: {config}", ephemeral=True
        )


def setup(bot: TicketBot):
    bot.add_cog(Commands(bot))
