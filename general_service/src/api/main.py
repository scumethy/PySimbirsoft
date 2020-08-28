from fastapi import FastAPI

from src.api import db
from src.api.initializator import put_routers


def get_app():
    app = FastAPI(title="General service app")

    db.init_app(app)

    put_routers(app)

    return app
