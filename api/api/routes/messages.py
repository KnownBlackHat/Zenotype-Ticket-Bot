import sqlalchemy
from aiohttp import web

from api.models import Guild, Message
from api.utils import helpers

from .root import Root


class Messages(Root):
    @helpers.ensure_guild
    async def get(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        response = []
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            response = []
            if guild:
                for messages in guild.messages:
                    response.append(
                        {
                            "userId": messages.userId,
                            "userName": messages.userName,
                            "channel": messages.channel,
                            "message": messages.message,
                            "createdAt": messages.createdAt,
                            "updatedAt": messages.updatedAt,
                        }
                    )
        return web.json_response(response)

    @helpers.ensure_guild
    async def add(self, request: web.Request) -> web.Response:
        guild_id = int(request.query.get("guild", 1))
        iuserId = request.query.get("userId")
        iuserName = request.query.get("userName")
        ichannel = request.query.get("channel")
        imessage = request.query.get("message")
        ipanel = request.query.get("panel")
        if not all((iuserId, iuserName, ichannel, imessage, ipanel)):
            return web.json_response({"success": False, "error": "missing parameters"})
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Guild).where(Guild.guild == guild_id)
            guild = await session.scalars(sql_query)
            guild = guild.one_or_none()
            if guild is None:
                return web.json_response({"success": False})
            guild.messages.append(
                Message(
                    userId=iuserId,
                    userName=iuserName,
                    channel=ichannel,
                    message=imessage,
                )
            )
        return web.json_response({"success": True})
