import sqlalchemy
from aiohttp import web

from api.models import Message, Ticket

from .root import Root


class Messages(Root):
    async def get(self, request: web.Request) -> web.Response:
        ticket_id = request.query.get("ticket")
        if ticket_id is None:
            return web.json_response(
                {"success": False, "error": "missing ticket query"}
            )
        try:
            ticket_id = int(ticket_id)
        except TypeError:
            return web.json_response(
                {
                    "success": False,
                    "error": "ticket query invalid data type, expected int",
                }
            )
        response = []
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Ticket).where(Ticket.id == ticket_id)
            ticket = await session.scalars(sql_query)
            ticket = ticket.one_or_none()
            if ticket is None:
                return web.json_response(
                    {"success": False, "error": "Ticket not found"}
                )
            for messages in ticket.messages:
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
        ticket_id = request.query.get("ticket")
        if ticket_id is None:
            return web.json_response(
                {"success": False, "error": "missing ticket query"}
            )
        try:
            ticket_id = int(ticket_id)
        except TypeError:
            return web.json_response(
                {
                    "success": False,
                    "error": "Ticket query invalid data type, expected int",
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
            sql_query = sqlalchemy.select(Ticket).where(Ticket.id == ticket_id)
            ticket = await session.scalars(sql_query)
            ticket = ticket.one_or_none()
            if ticket is None:
                return web.json_response(
                    {"success": False, "error": "Ticket not found"}
                )
            ticket.messages.append(
                Message(
                    userId=iuserId,
                    userName=iuserName,
                    channel=ichannel,
                    message=imessage,
                )
            )
        return web.json_response({"success": True})
