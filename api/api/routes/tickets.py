import sqlalchemy
from aiohttp import web

from api.models import Panel, Ticket

from .root import Root


class Tickets(Root):

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
        async with self.db.begin() as session:
            sql_query = sqlalchemy.select(Panel).where(Panel.id == panel_id)
            panel = await session.scalars(sql_query)
            panel = panel.one_or_none()
            if panel is None:
                return web.json_response({"success": False, "error": "Panel not found"})

            response = []
            for ticket in panel.tickets:
                response.append(
                    {
                        "id": ticket.id,
                        "userId": ticket.userId,
                    }
                )
            return web.json_response(response)

    async def add(self, request: web.Request) -> web.Response:
        panel_id = request.query.get("panel")
        data = await request.json()
        userId = data.get("userId")

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

            try:
                panel.tickets.append(Ticket(userId=userId))
                await session.commit()

            except Exception as e:
                return web.json_response({"success": False, "error": f"{e}"})
        return web.json_response({"success": True})
