import asyncio

from aiohttp import web
from sqlalchemy import event
from sqlalchemy.engine import Engine

from api.routes import Guilds, Messages, Panels, Roles, Root, Teams, Tickets

app = web.Application()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


root = Root()
asyncio.run(root.init_db())

app.add_routes(
    [
        web.get("/guilds", Guilds().get),
        web.post("/guilds/add", Guilds().add),
        web.get("/panels", Panels().get),
        web.get("/panels/find", Panels().find),
        web.post("/panels/add", Panels().add),
        web.get("/teams", Teams().get),
        web.post("/teams/add", Teams().add),
        web.get("/messages", Messages().get),
        web.post("/messages/add", Messages().add),
        web.get("/role", Roles().get),
        web.post("/role/add", Roles().add),
        web.get("/tickets", Tickets().get),
        web.post("/tickets/add", Tickets().add),
    ]
)

web.run_app(app)
