import sqlalchemy
from aiohttp import web

from api.models import Guild, Team
from api.utils import helpers

from .root import Root


class Teams(Root):

    @helpers.ensure_guild
    async def get(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            response = []
            if guild:
                for team in guild.teams:
                    response.append({"user": team.user, "name": team.name})

            return web.json_response(response)

    @helpers.ensure_guild
    async def add(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        data = await request.json()
        iuser = data.get("user")
        iname = data.get("name")
        if not all((iuser, iname)):
            return web.json_response({"success": False, "error": "missing parameters"})

        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild is None:
                return web.json_response({"success": False})
            guild.teams.append(Team(user=iuser, name=iname))
            await session.commit()
        return web.json_response({"success": True})
