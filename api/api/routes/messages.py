import sqlalchemy
from aiohttp import web

from api.models import Message, Panel

from .root import Root


class Messages(Root):
    async def get(self, request: web.Request) -> web.Response:
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
        response = []
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Panel).where(Panel.id == panel_id)
            panel = await session.scalars(sql_query)
            panel = panel.one_or_none()
            if panel is None:
                return web.json_response({"success": False, "error": "Panel not found"})
            for messages in panel.messages:
                response.append(
                    {
                        "userId": messages.userId,
                        "userName": messages.userName,
                        "channel": messages.channel,
                        "message": messages.message,
                        "createdAt": messages.createdAt.timestamp(),
                        "updatedAt": (
                            messages.updatedAt.timestamp()
                            if messages.updatedAt
                            else None
                        ),
                    }
                )
        return web.json_response(response)

    async def add(self, request: web.Request) -> web.Response:
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
        data = await request.json()
        iuserId = data.get("userId")
        iuserName = data.get("userName")
        ichannel = data.get("channel")
        imessage = data.get("message")
        if not all((iuserId, iuserName, ichannel, imessage)):
            return web.json_response({"success": False, "error": "missing parameters"})
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Panel).where(Panel.id == panel_id)
            panel = await session.scalars(sql_query)
            panel = panel.one_or_none()
            if panel is None:
                return web.json_response({"success": False, "error": "Panel not found"})
            panel.messages.append(
                Message(
                    userId=iuserId,
                    userName=iuserName,
                    channel=ichannel,
                    message=imessage,
                )
            )
        return web.json_response({"success": True})
