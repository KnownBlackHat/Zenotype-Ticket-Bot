import asyncio

from aiohttp import web
from sqlalchemy import event
from sqlalchemy.engine import Engine

from api.routes import Guilds, Panels, Root, Teams

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
        web.post("/panels/add", Panels().add),
        web.get("/teams", Teams().get),
        web.post("/teams/add", Teams().add),
    ]
)

web.run_app(app)
