import sqlalchemy
from aiohttp import web

from api.models import Guild, Role
from api.utils import helpers

from .root import Root


class Roles(Root):
    @helpers.ensure_guild
    async def get(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild:
                return web.json_response({"role": str(guild.role.role)})
            else:
                return web.json_response({"role": None})

    @helpers.ensure_guild
    async def add(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        data = await request.json()
        irole = data.get("id")

        if not irole:
            return web.json_response({"success": False, "error": "missing parameters"})

        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild is None:
                return web.json_response({"success": False})

            guild.role = Role(role=irole)
            await session.commit()
            return web.json_response({"success": True})
