from typing import Optional

import disnake

from ticket_bot.constants import ButtonsIds


class DeleteButton(disnake.ui.Button):
    """Delete Button Component"""

    def __init__(
        self,
        user: int | disnake.User | disnake.Member,
        *,
        allow_manage: bool = True,
        initial_msg: Optional[disnake.Message | int] = None,
        style: Optional[disnake.ButtonStyle] = None,
        emoji: Optional[str | disnake.Emoji | disnake.PartialEmoji] = None,
    ):
        # we will customize the main lib button only. CRAZY

        if isinstance(user, int):
            user_id = user
        else:
            user_id = user.id

        super().__init__()
        self.custom_id = ButtonsIds.delete_btn
        permissions = disnake.Permissions()
        if allow_manage:
            permissions.manage_messages = True
        self.custom_id += f"{permissions.value}:{user_id}"

        if initial_msg:
            if isinstance(initial_msg, disnake.Message):
                initial_msg = initial_msg.id
            self.custom_id += f"{initial_msg}"

        if not style:
            if initial_msg:
                self.style = disnake.ButtonStyle.danger
            else:
                self.style = disnake.ButtonStyle.secondary
        else:
            self.style = style

        if not emoji:
            if self.style == disnake.ButtonStyle.danger:
                self.emoji = "💣"
            else:
                self.emoji = "🗑️"

        else:
            self.emoji = emoji
