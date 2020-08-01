from aiohttp import web
from aiohttp_swagger import *

from api.db import init_db, users
from api.redis import setup_redis
from api.routes import setup_routes


async def init_app():
    app = web.Application()

    setup_routes(app)
    await init_db(app)
    await setup_redis(app)

    setup_swagger(
        app,
        swagger_from_file="user_service/api/swagger.yaml",
        swagger_url="/auth/doc",
        ui_version=3,
    )

    return app


app = init_app()
web.run_app(app)
