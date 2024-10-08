import disnake
from disnake.ext import commands
import sqlalchemy

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from ticket_bot import TicketBot
from ticket_bot.database import Config as TicketConfig

from enum import Enum


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


class Config(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot.db

    class TicketModal(disnake.ui.Modal):
        def __init__(
            self,
            category: disnake.CategoryChannel,
            config: ConfigSlot,
            user_or_role: disnake.Role | disnake.Member,
            db: async_sessionmaker[AsyncSession],
        ):
            self.db = db

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
                sql_query = sqlalchemy.select(Config)

    @commands.slash_command(name="config")
    async def tckt_config(self, inter: disnake.GuildCommandInteraction) -> None:
        # use modals here
        await inter.response.defer()
        await inter.send("config here")


def setup(client: TicketBot):
    client.add_cog(Config(client))
