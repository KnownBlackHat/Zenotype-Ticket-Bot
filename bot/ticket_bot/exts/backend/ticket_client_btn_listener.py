import logging

import disnake
from disnake.ext import commands

from ticket_bot.bot import TicketBot
from ticket_bot.constants import ButtonsIds


logger = logging.getLogger(__name__)

async def close_ticket(inter: disnake.MessageInteraction| disnake.ModalInteraction, custom_id: str):
    custom_id = custom_id.removeprefix(ButtonsIds.tckt_close)
    if not isinstance(inter.channel, disnake.PartialMessageable) and isinstance(
        inter.channel, disnake.Thread
    ):
        await inter.channel.edit(locked=True, archived=True)
        logger.debug("broadcasting on transcript")
        # TODO: Complete transcripting from here
    else:
        if not inter.guild:
            return
        logger.warning(f"Failed to delete {inter.channel} in {inter.guild.name}")


class CloseWtihReasonModal(disnake.ui.Modal):
    def __init__(self, custom_id: str) -> None:
        components = [
            disnake.ui.TextInput(
                label="Reason", placeholder="Enter Reason Here", custom_id="Reason"
            )
        ]
        super().__init__(
            title="Ticket Setup", custom_id="ticket_setup", components=components
        )
        self.custom_id = custom_id

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="Ticket Got Closed", description=f"Reason: {inter.text_values["Reason"]}")
        await inter.channel.send(embed=embed)
        await close_ticket(inter, self.custom_id)
        return await super().callback(inter)


class Ticket_client_listener(
    commands.Cog, slash_command_attrs={"dm_permissions": False}
):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def handle_delete_button(self, inter: disnake.MessageInteraction) -> None:
        """This will handle the client side ticket buttons"""
        # Prefix check
        if not (custom_id := inter.component.custom_id) or not inter.guild:
            return
        elif custom_id.startswith(ButtonsIds.tckt_close):
            await close_ticket(inter, custom_id)

        elif inter.component.custom_id.startswith(ButtonsIds.tckt_close_with_reason):
            await inter.response.send_modal(CloseWtihReasonModal(custom_id=custom_id))
