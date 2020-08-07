from aiohttp import web
from aiohttp_swagger import *

from api.redis import setup_redis, close_redis
from api.routes import setup_routes
from api.db import init_db, close_pg
from api.middlewares import error_middleware


async def init_app():
    app = web.Application(middlewares=[error_middleware])

    setup_routes(app)
    await init_db(app)
    await setup_redis(app)

    setup_swagger(
        app,
        swagger_from_file="user_service/api/swagger.yaml",
        swagger_url="/auth/doc",
        ui_version=3,
    )

    app.on_cleanup.append(close_pg)
    app.on_cleanup.append(close_redis)

    return app


app = init_app()
web.run_app(app)
