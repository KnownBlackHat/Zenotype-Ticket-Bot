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
                            "title": panel.title,
                            "thumbnail": panel.thumbnail,
                            "image": panel.image,
                            "description": panel.description,
                            "category": panel.category,
                        }
                    )
            return web.json_response(response)

    @helpers.ensure_guild
    async def add(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        data = await request.json()
        ititle = data.get("title")
        idescription = data.get("description")
        ithumbnail = data.get("thumbnail")
        iimage = data.get("image")
        icolor = data.get("color")
        icategory = data.get("category")
        if not all((ititle, idescription, ithumbnail, iimage, icolor, icategory)):
            return web.json_response({"success": False, "error": "missing parameters"})

        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild is None:
                return web.json_response({"success": False})
            guild.panels.append(
                Panel(
                    title=ititle,
                    thumbnail=ithumbnail,
                    image=iimage,
                    description=idescription,
                    color=icolor,
                    category=icategory,
                )
            )
            await session.commit()
        return web.json_response({"success": True})
