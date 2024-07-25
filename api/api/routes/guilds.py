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
                        "id": str(guild.id),
                        "name": guild.name,
                        "icon": guild.icon,
                        "permissions": guild.permissions,
                        "description": guild.description,
                        "owner": guild.owner,
                    }
                )
            return web.json_response(guilds)

    async def add(self, request: web.Request) -> web.Response:
        data = await request.json()
        iguild = data.get("id")
        iname = data.get("name")
        iicon = data.get("icon")
        ipermissions = data.get("permissions")
        idescription = data.get("description")
        iowner = data.get("owner")

        if not all((iguild, iname)):
            return web.json_response({"success": False, "error": "missing arguments"})

        async with self.db.begin() as session:
            sql_query = Guild(
                name=iname,
                guild=iguild,
                icon=iicon,
                description=idescription,
                permissions=ipermissions,
                owner=iowner,
            )
            session.add(sql_query)
            await session.commit()

        return web.json_response({"success": True})
