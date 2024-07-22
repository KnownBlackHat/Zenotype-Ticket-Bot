import sqlalchemy
from aiohttp import web

from api.models import Guild

from .root import Root


class Guilds(Root):
    async def get(self, request: web.Request) -> web.Response:
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild)
            result = await session.scalars(sql_query)
            result = result.all()
            guilds = []
            for guild in result:
                guilds.append(
                    {
                        "guild": guild.guild,
                        "name": guild.name,
                    }
                )
            return web.json_response(guilds)

    async def add(self, request: web.Request) -> web.Response:
        data = await request.json()
        iguild = data.get("guild")
        iname = data.get("name")

        if not all((iguild, iname)):
            return web.json_response({"success": False, "error": "missing arguments"})

        async with self.db.begin() as session:
            sql_query = Guild(name=iname, guild=iguild)
            session.add(sql_query)

        return web.json_response({"success": True})
