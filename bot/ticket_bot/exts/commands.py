import disnake
from disnake.ext import commands

from ticket_bot.bot import TicketBot


class Commands(commands.Cog):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

def setup(bot: TicketBot):
    bot.add_cog(Commands(bot))
