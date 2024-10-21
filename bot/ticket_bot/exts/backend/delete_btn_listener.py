import logging
import disnake
from disnake.ext import commands

from ticket_bot.bot import TicketBot
from ticket_bot.constants import ButtonsIds

logger = logging.getLogger(__name__)


class Delete_btn_listener(commands.Cog, slash_command_attrs={"dm_permissions": False}):
    def __init__(self, bot: TicketBot) -> None:
        self.bot = bot

    # SCHEMA
    # PREFIX:PERMS:USER_ID:MESSAGE_ID
    @commands.Cog.listener("on_button_click")
    async def handle_delete_button(self, inter: disnake.MessageInteraction) -> None:
        """This will handle the delete button click event"""
        # Prefix check
        if not (custom_id := inter.component.custom_id) or not custom_id.startswith(
            ButtonsIds.delete_btn
        ):
            return

        # Cleanup
        custom_id = custom_id.removeprefix(ButtonsIds.delete_btn)

        perms, user_id, *msg_id = custom_id.split(":")
        delete_msg = None

        if msg_id:
            if msg_id[0]:
                delete_msg = int(msg_id[0])

        perms, user_id = int(perms), int(user_id)

        # Perms check
        if not (is_original_author := inter.author.id == user_id):
            permissions = disnake.Permissions(perms)
            user_permission = inter.permissions
            if not permissions.value & user_permission.value:
                await inter.send(
                    "You don't have enough perms to remove this message",
                    ephemeral=True,
                    delete_after=5,
                )
                return

        if isinstance(
            inter.channel,
            (disnake.TextChannel, disnake.Thread, disnake.VoiceChannel),
        ) and isinstance(inter.me, disnake.Member):
            if (
                not hasattr(inter.channel, "guild")
                or not (
                    myperms := inter.channel.permissions_for(inter.me)
                ).read_messages
            ):
                await inter.response.defer()
                await inter.delete_original_response()
                return

            # main msg got deleted here
            await inter.message.delete()

            if (
                not delete_msg
                or not myperms.manage_permissions
                or not is_original_author
            ):
                return
            if msg := inter.bot.get_message(delete_msg):
                if msg.edited_at:
                    return
            else:
                msg = inter.channel.get_partial_message(delete_msg)

            try:
                await msg.delete()
            except disnake.NotFound:
                ...
            except disnake.Forbidden:
                logger.warning("Cache is unreliable or something is weird")
        else:
            logger.debug("Interaction's channel doesn't have required type.")


def setup(client: TicketBot):
    client.add_cog(Delete_btn_listener(client))
