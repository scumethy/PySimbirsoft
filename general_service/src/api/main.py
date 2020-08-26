from fastapi import FastAPI

from src.api import db
from .views import init_app


def get_app():
    app = FastAPI(title="General service app")
    db.init_app(app)
    init_app(app)
    return app