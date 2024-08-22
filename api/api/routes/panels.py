import sqlalchemy
from aiohttp import web

from api.models import Guild, Panel
from api.utils import helpers

from .root import Root


class Panels(Root):

    @helpers.ensure_guild
    async def get(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guilds = await session.scalars(sql_query)
            guilds = guilds.one_or_none()
            response = []
            if guilds:
                for panel in guilds.panels:
                    response.append(
                        {
                            "id": panel.id,
                            "title": panel.title,
                            "description": panel.description,
                            "color": panel.color,
                            "disable_panel": panel.disable_panel,
                            "button_color": panel.button_color,
                            "button_text": panel.button_text,
                            "button_emoji": panel.button_emoji,
                            "mention_on_open": panel.mention_on_open,
                            "support_team": panel.support_team,
                            "category": panel.category,
                            "naming_scheme": panel.naming_scheme,
                            "large_image": panel.large_image,
                            "small_image": panel.small_image,
                            "wlcm_title": panel.wlcm_title,
                            "wlcm_description": panel.wlcm_description,
                            "wlcm_color": panel.wlcm_color,
                            "author_name": panel.author_name,
                            "author_url": panel.author_url,
                            "roles": panel.roles,
                        }
                    )
            return web.json_response(response)

    async def find(self, request: web.Request) -> web.Response:
        panel_id = request.query.get("panel")
        if panel_id is None:
            return web.json_response({"success": False, "error": "missing panel query"})
        try:
            panel_id = int(panel_id)
        except TypeError:
            return web.json_response(
                {
                    "success": False,
                    "error": "panel query invalid data type, expected int",
                }
            )
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Panel).where(Panel.id == panel_id)
            panel = await session.scalars(sql_query)
            panel = panel.one_or_none()
            if panel is None:
                return web.json_response({"success": False, "error": "Panel not found"})
            return web.json_response(
                {
                    "id": panel.id,
                    "title": panel.title,
                    "description": panel.description,
                    "color": panel.color,
                    "disable_panel": panel.disable_panel,
                    "button_color": panel.button_color,
                    "button_text": panel.button_text,
                    "button_emoji": panel.button_emoji,
                    "mention_on_open": panel.mention_on_open,
                    "support_team": panel.support_team,
                    "category": panel.category,
                    "naming_scheme": panel.naming_scheme,
                    "large_image": panel.large_image,
                    "small_image": panel.small_image,
                    "wlcm_title": panel.wlcm_title,
                    "wlcm_description": panel.wlcm_description,
                    "wlcm_color": panel.wlcm_color,
                    "author_name": panel.author_name,
                    "author_url": panel.author_url,
                    "roles": panel.roles,
                }
            )

    @helpers.ensure_guild
    async def add(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        data = await request.json()

        ititle = data.get("title")
        idescription = data.get("description")
        icolor = data.get("color")
        idisable_panel = data.get("disable_panel")
        ibutton_color = data.get("button_color")
        ibutton_text = data.get("button_text")
        ibutton_emoji = data.get("button_emoji")
        imention_on_open = data.get("mention_on_open")
        isupport_team = data.get("support_team")
        icategory = data.get("category")
        inaming_scheme = data.get("naming_scheme")
        ilarge_image = data.get("large_image")
        ismall_image = data.get("small_image")
        iwlcm_title = data.get("wlcm_title")
        iwlcm_description = data.get("wlcm_description")
        iwlcm_color = data.get("wlcm_color")
        iauthor_name = data.get("author_name")
        iauthor_url = data.get("author_url")
        iroles = data.get("roles")

        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild is None:
                return web.json_response({"success": False})
            try:
                guild.panels.append(
                    Panel(
                        title=ititle,
                        description=idescription,
                        color=icolor,
                        disable_panel=idisable_panel,
                        button_color=ibutton_color,
                        button_text=ibutton_text,
                        button_emoji=ibutton_emoji,
                        mention_on_open=imention_on_open,
                        support_team=isupport_team,
                        category=icategory,
                        naming_scheme=inaming_scheme,
                        large_image=ilarge_image,
                        small_image=ismall_image,
                        wlcm_title=iwlcm_title,
                        wlcm_description=iwlcm_description,
                        wlcm_color=iwlcm_color,
                        author_name=iauthor_name,
                        author_url=iauthor_url,
                        roles=iroles,
                    )
                )
                await session.commit()
            except Exception as e:
                return web.json_response({"success": False, "error": f"{e}"})

        return web.json_response({"success": True})
